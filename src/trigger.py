from node import Node

def catch_error(nodes: list):
        for node in nodes:
            for parameter in node.parameters:
                min_value = parameter.min_value
                max_value = parameter.max_value
                target_value = parameter.targer_value
                now_value = parameter.value

            if isinstance(now_value, int):
                if max_value <= now_value <= min_value or now_value == target_value:
                    return node.name, parameter.oid, parameter.name, parameter.value
            if isinstance(now_value, str):
                if now_value == target_value:
                    return node.name, parameter.oid, parameter.name, parameter.value




