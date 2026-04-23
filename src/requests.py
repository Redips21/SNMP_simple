import asyncio
from puresnmp import Client, ObjectIdentifier as OID, V2C, V1, PyWrapper
from puresnmp import varbind as VarBind

# client = Client("127.0.0.1", V2C("public"), port=1024)
# coro = client.multiget(
#      [OID('1.3.6.1.2.1.1.3.0'), OID('1.3.6.1.2.1.1.2.0')]
# )


# oids - это список вида: [OID(..), OID(..), OID(..), ...]
async def requestV2(ip, port_number, password_type, oids_str):

    oids = converter_listStringOIDs_to_listOIDs(oids_str)
    client = Client(ip, V2C(password_type), port=port_number)
    coro = client.multiget(oids)

    try:
        result = await asyncio.wait_for(coro, timeout=5.0)
        return result
    except asyncio.TimeoutError:
        print("Превышен лимит ожидания ответа")
        return None
    except Exception as e:
        print(f"Error request: {e}")
        return None


async def requestV1(ip, port_number, password_type, oids_str):
    import warnings
    warnings.filterwarnings("ignore")
    client = PyWrapper(Client(ip, V1(password_type), port=port_number))
    coro =  client.multiget(oids_str)

    try:
        result = await asyncio.wait_for(coro, timeout=5.0)
        return result
    except asyncio.TimeoutError:
        print("Превышен лимит ожидания ответа")
        return None
    except Exception as e:
        print(f"Error request: {e}")
        return None


def converter_listStringOIDs_to_listOIDs(oids_str: list[str]) -> list[OID]:
    oids = []
    for oid_str in oids_str:
        oid = OID(oid_str)
        oids.append(oid)
    return oids

"""Парсит различные типы данных SNMP"""
def parsing_snmp_response(response) -> list[str]:
    if isinstance(response, list):
        ready_response = []
        for one_values_response in response:
            oid_values_pair = {}
            oid, value = one_values_response.oid, one_values_response.value
            oid_values_pair[oid] = value
            ready_response.append(oid_values_pair)




if __name__ == "__main__":
    # Определяем параметры
    ip = "192.168.1.2"
    port_number = 161
    password_type = "public"  # community string
    oids = ['1.3.6.1.2.1.2.2.1.15.2', '1.3.6.1.2.1.2.2.1.16.1']

    result = asyncio.run(requestV1(ip, port_number, password_type, oids))
    print(result)

    if result:
        print(f"Тип результата: {type(result)}")  # <class 'tuple'>
        print(f"Длина результата: {len(result)}")  # 2

        # Работаем с результатом
        for var_bind in result:
            print(var_bind)

            #print(f"OID: {var_bind.oid}, Значение: {var_bind.value}")
            # Или так:
            #print(f"OID: {var_bind[0]}, Значение: {var_bind[1]}")