import asyncio
from puresnmp import Client, V2C, V1, PyWrapper, ObjectIdentifier as OID
from my_logger import My_logger

logger = My_logger()

async def requestV2(ip, port_number, password_type, oids_str):
    oids = converter_listStringOIDs_to_listOIDs(oids_str)
    client = Client(ip, V2C(password_type), port=port_number)
    coro = client.multiget(oids)

    try:
        result = await asyncio.wait_for(coro, timeout=5.0)
        return result
    except asyncio.TimeoutError:
        logger.add_log("Error request: Превышен лимит ожидания ответа")
        return None
    except Exception as e:
        logger.add_log(f"Error request: {e}")
        return None

async def requestV1(ip, port_number, password_type, oids_str):
    import warnings
    warnings.filterwarnings("ignore")
    client = PyWrapper(Client(ip, V1(password_type), port=port_number))
    coro = client.multiget(oids_str)

    try:
        result = await asyncio.wait_for(coro, timeout=5.0)
        return result
    except asyncio.TimeoutError:
        logger.add_log("Error request: Превышен лимит ожидания ответа")
        return None
    except Exception as e:
        logger.add_log(f"Error request: {e}")
        return None

def converter_listStringOIDs_to_listOIDs(oids_str: list[str]) -> list[OID]:
    return [OID(oid_str) for oid_str in oids_str]