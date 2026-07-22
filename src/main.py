import asyncio
import yaml
from pathlib import Path
from node import Node, Parameter_Node, Location_Node
from requests import requestV1
from data_base import DataBase


def load_hostsMap(path: str) -> dict:
  try:
    with open(path, 'r', encoding='UTF-8') as file:
      data = yaml.safe_load(file)

    if not isinstance(data, dict):
      raise TypeError('При загрузке данных из конфига .yaml не был получен тип данных "dict"')
    return data

  except FileNotFoundError:
    print(f"Файл {path} не найден")
    return {}
  except yaml.YAMLError as e:
    print(f"Ошибка разбора YAML: {e}")
    return {}
  except TypeError as e:
    print(str(e))
    return {}


def convert_data_to_Nodes(data: dict) -> list[Node]:
  nodes = []

  for obj in data.values():
    name = obj.get('name')
    ip = obj.get('ip')
    port = obj.get('port')
    community = obj.get('community_string')

    location_data = obj.get('location', {})
    building = location_data.get('building', '')
    cabinet = location_data.get('cabinet', '')
    location = Location_Node(building, cabinet)

    values = obj.get('values', {})
    parameters = []

    for value in values.values():
      nameV = value.get('name')
      oidV = value.get('oid')
      max_valueV = value.get('max_value')
      min_valueV = value.get('min_value')
      target_valueV = value.get('catch_value')

      parameter = Parameter_Node(nameV, oidV, max_valueV, min_valueV, target_valueV)
      parameters.append(parameter)

    node = Node(name, ip, port, community, location, parameters)
    nodes.append(node)

  return nodes


async def process_node(node: Node, db: DataBase):
  oids = node.getOids()
  result = await requestV1(node.ip, node.port, node.community, oids)

  if isinstance(result, list):
    for return_value, parameter in zip(result, node.parameters):
      parameter.value = return_value
      print(f"[{node.name}] {parameter.name} ({parameter.oid}) = {return_value}")

      # Запись измеренного значения в БД (в таблицу history_parameters_SNMP)
      if hasattr(node, 'db_id') and hasattr(parameter, 'db_id'):
        db.insert_history_record(node.db_id, parameter.db_id, str(return_value))


async def main():
  # Настройка путей
  base_dir = Path(__file__).parent.parent
  yaml_path = base_dir / "data" / "hostsMap_1.yaml"
  db_path = base_dir / "data" / "monitor.db"

  # Инициализация БД
  db = DataBase(str(db_path))
  db.create_tables()

  # Загрузка узлов из YAML
  data = load_hostsMap(str(yaml_path))
  nodes = convert_data_to_Nodes(data)

  # Заполнение первоначальных справочников в БД
  db.insert_nodes_in_db(nodes)

  print("Мониторинг запущен. Для остановки нажмите Ctrl+C.")

  while True:
    # Асинхронный опрос всех узлов одновременно
    tasks = [process_node(node, db) for node in nodes]
    await asyncio.gather(*tasks)

    await asyncio.sleep(1.0)


if __name__ == '__main__':
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print("\nМониторинг остановлен.")
