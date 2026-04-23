import asyncio
import time

import yaml
import rich
from rich.table import Table
from rich.live import Live
from puresnmp import varbind as VarBind
from puresnmp import ObjectIdentifier as OID

from node import Node, Parameter_Node
from x690.types import PrintableString


#from requests import requestV1


#"../data/hostsMap.yaml"
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

    values = obj.get('values')

    parameters = []
    
    for value in values.values():
      nameV = value.get('name')
      oidV = value.get('oid')
      max_valueV = value.get('max_value')
      min_valueV = value.get('min_value')
      target_valueV = value.get('catch_value')

      parameter = Parameter_Node(nameV,oidV, max_valueV, min_valueV, target_valueV)
      parameters.append(parameter)
    
    node = Node(name, ip, port, community, parameters)
    
    nodes.append(node)
    
  return nodes

#nodes = [] # переделать в кортеж

#path = '../data/hostsMap.yaml'

#data = load_hostsMap(path)
#nodes = convert_data_to_Nodes(data)

#отправка запросов к узлам
#for node in nodes:
#  ip = node.ip
#  port = node.port
#  community = node.community#

 # oids = []
 # for parameter in node.paraters:


  

#answer = asyncio.run(requestV1(ip, port, community, oids))

  
if __name__ == '__main__':
  import sys
  from pathlib import Path
  sys.path.append(str(Path(__file__).parent / 'testInterface'))
  from testInterface import interface
  from requests import requestV1



  data = load_hostsMap('./data/hostsMap.yaml')
  nodes = convert_data_to_Nodes(data)

  with Live(interface.create_table(nodes), refresh_per_second=3) as live:
    check_exit = True

    while (check_exit):

      for node in nodes:
        ip = node.ip
        port_number = node.port
        password_type = node.community
        oids = node.getOids()

        #rich.inspect(node)
        result = asyncio.run(requestV1(ip, port_number, password_type, oids))

        if isinstance(result, list):
           for return_value,parameter in zip(result,node.parameters):
             parameter.value = return_value
          #rich.inspect(node)

        live.update(interface.create_table(nodes))
        time.sleep(0.1)



  



