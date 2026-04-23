import rich
from rich.console import Console
from rich.table import Table

def make_head_table(table: Table):
    table.title = "Monitor_SNMP"
    table.add_column("№")
    table.add_column("Device", style='green')
    table.add_column("Parameter")
    table.add_column("Value")

def add_info_in_table(table: Table, nodes: list):
    counter = 1
    for node in nodes:
        table.add_row(str(counter), node.name, "", "")

        for parameter in node.parameters:
            table.add_row("", "", str(parameter.name), str(parameter.value))

        counter = counter + 1

def create_table(nodes: list) -> Table:
    table = Table()
    make_head_table(table)
    add_info_in_table(table, nodes)

    return table

#    with Live(table, refresh_per_second=2) as live:  # update 4 times a second to feel fluid
#        couter = 0
#        for node in nodes:
#            table.add_row(node.name,
#                          node.ip + "/" + node.port,
#                          node.parameters.value[counter] + "/" + answer[counter])
#        time.sleep(0.4)


def main():
    from src import main
    from src import node

    data = main.load_hostsMap('../../data/hostsMap.yaml')
    nodes = main.convert_data_to_Nodes(data)

    table = Table()

    make_head_table(table)

    add_info_in_table(table, nodes)

    console = Console()

    console.print(table)


if __name__ == "__main__":
    main()