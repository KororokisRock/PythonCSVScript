import csv, argparse, tabulate

parser = argparse.ArgumentParser()

parser.add_argument("--file", dest="file", help="Takes the path to the file")
parser.add_argument("--where", dest="condition", help="Takes the condition for sampling")
parser.add_argument("--order-by", dest="order", help="Outputs the result in ascending or descending order")
parser.add_argument("--aggregate", dest="aggregate", help="Outputs the maximum, minimum, or average values for a sample column")


def isinteger(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def isfloat(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def values_is_integer(values: list[str]) -> bool:
    for el in values:
        if not isinteger(el):
            return False
    return True


def values_is_float(values: list[str]) -> bool:
    for el in values:
        if not isfloat(el):
            return False
    return True


def change_to_integer(data: list[list], column_index: int):
    for i in range(1, len(data)):
        data[i][column_index] = int(data[i][column_index])


def change_to_float(data: list[list], column_index: int):
    for i in range(1, len(data)):
        data[i][column_index] = float(data[i][column_index])


def get_data(filepath: str) -> list | None:
    try:
        with open(filepath, "r", encoding="utf-8", newline='\n') as file:
            reader = csv.reader(file)
            data = list(reader)

        if len(data) >= 2:
            for i in range(len(data[0])):
                values = [data[j][i] for j in range(1, len(data))]
                if values_is_integer(values):
                    change_to_integer(data, i)
                elif values_is_float(values):
                    change_to_float(data, i)

        return data
    
    except FileNotFoundError:
        print("Incorrect input for --file, file not found")
        return None


def get_column_index_by_name(data: list[list], columnname: str) -> int:
    if columnname in data[0]:
        return data[0].index(columnname)
    else:
        return -1


def match_value_column_types(data: list[list], column_index: int, value: str) -> int | float | str | None:
    if isinstance(data[1][column_index], int):
        if not isinteger(value):
            print("Incorrect input for --where, column type and value do not match (column is int)")
            return None
        else:
            return int(value)
    elif isinstance(data[1][column_index], float):
        if not isfloat(value):
            print("Incorrect input for --where, column type and value do not match (column is float)")
            return None
        else:
            return float(value)
    else:
        return value


def get_greater_condition(data: list[list], column: str, value: str) -> list | None:
    column_index = get_column_index_by_name(data, column)
    if column_index != -1 and len(value) > 0:
        value = match_value_column_types(data, column_index, value)
        if value is not None:
            return [data[0]] + [data[i] for i in range(1, len(data)) if data[i][column_index] > value]
        print("Incorrect input for --where, value is invalid, re-enter the pattern condition: column>value")
        return None
    else:
        print("Incorrect input for --where, column not found or value is invalid, re-enter the pattern condition: column>value")
        return None


def get_less_condition(data: list[list], column: str, value: str) -> list | None:
    column_index = get_column_index_by_name(data, column)
    if column_index != -1 and len(value) > 0:
        value = match_value_column_types(data, column_index, value)
        if value is not None:
            return [data[0]] + [data[i] for i in range(1, len(data)) if data[i][column_index] < value]
        print("Incorrect input for --where, value is invalid, re-enter the pattern condition: column<value")
        return None
    else:
        print("Incorrect input for --where, column not found or value is invalid, re-enter the pattern condition: column<value")
        return None


def get_equal_condition(data: list[list], column: str, value: str) -> list | None:
    column_index = get_column_index_by_name(data, column)
    if column_index != -1 and len(value) > 0:
        value = match_value_column_types(data, column_index, value)
        if value is not None:
            return [data[0]] + [data[i] for i in range(1, len(data)) if data[i][column_index] == value]
        print("Incorrect input for --where, value is invalid, re-enter the pattern condition: column=value")
        return None
    else:
        print("Incorrect input for --where, column not found or value is invalid, re-enter the pattern condition: column=value")
        return None


def get_condition_result(data: list[list], condition: str) -> list | None:
    if '>' in condition:
        column, value = condition.split('>', maxsplit=1)
        return get_greater_condition(data, column, value)
    elif '<' in condition:
        column, value = condition.split('<', maxsplit=1)
        return get_less_condition(data, column, value)
    elif '=' in condition:
        column, value = condition.split('=', maxsplit=1)
        return get_equal_condition(data, column, value)
    else:
        print("Incorrect input for --where, re-enter the condition for one of the templates: column=value column>value column<value")
        return None


def get_aggregate_result(data: list[list], aggr: str) -> list | None:
    if '=' in aggr:
        column, func = aggr.split('=', maxsplit=1)
        column_index = get_column_index_by_name(data, column)

        if column_index == -1:
            print("Invalid input for --aggregate, column name is undefined, retry using pattern: column=func")
            return None
        
        if isinstance(data[1][column_index], str):
            print("Invalid input for --aggregate, column values cannot be str, retry using pattern: column=func")
            return None
        
        if func == 'max':
            return [['max'], [ max( data[i][column_index] for i in range(1, len(data)) ) ]]
        elif func == 'min':
            return [['min'], [ min( data[i][column_index] for i in range(1, len(data)) ) ]]
        elif func == 'avg':
           return [['avg'], [ round(sum( data[i][column_index] for i in range(1, len(data)) ) / (len(data) - 1), 2) ]]
        else:
            print("Invalid input for --aggregate, function was not found, retry using pattern: column=func")
            return None
    else:
        print("Invalid input for --aggregate, retry using pattern: column=func")
        return None


def get_order_by_result(data: list[list], order_rule: str) -> list | None:
    if '=' in order_rule:
        column, order = order_rule.split('=', maxsplit=1)
        column_index = get_column_index_by_name(data, column)
        if column_index != -1:
            if order == "asc":
                return [data[0]] + sorted(data[1:], key=lambda row: row[column_index])
            elif order == "desc":
                return [data[0]] + sorted(data[1:], key=lambda row: row[column_index], reverse=True)
            else:
                print("Invalid input for --order-by, order not found, retry using pattern: column=order")
                return None
        else:
            print("Invalid input for --order-by, column is invalid, retry using pattern: column=order")
            return None
    else:
        print("Invalid input for --order-by, retry using pattern: column=order")
        return None


if __name__ == "__main__":
    args = parser.parse_args()

    if args.file is not None:
        data = get_data(args.file)
        
        if args.condition is not None and data is not None and len(data) >= 2:
            data = get_condition_result(data, args.condition)
        
        if args.order is not None and data is not None and len(data) >= 2:
            data = get_order_by_result(data, args.order)

        if args.aggregate is not None and data is not None and len(data) >= 2:
            data = get_aggregate_result(data, args.aggregate)
        
        if data is not None:
            print(tabulate.tabulate(data, tablefmt="grid"))
