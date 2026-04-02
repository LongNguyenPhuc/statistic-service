from datetime import datetime
import re

dict_operators = [
    {"operator": "==", "meaning": "Equals"},
    {"operator": "!=", "meaning": "Not equals"},
    {"operator": ">", "meaning": "Greater than"},
    {"operator": "<", "meaning": "Less than"},
    {"operator": ">=", "meaning": "Greater than or equal to"},
    {"operator": "<=", "meaning": "Less than or equal to"},
    {"operator": "@=", "meaning": "Contains"},
    {"operator": "_=", "meaning": "Starts with"},
    {"operator": "!@=", "meaning": "Does not Contains"},
    {"operator": "!_=", "meaning": "Does not Starts with"},
    {"operator": "[]", "meaning": "Only datetime, date between two date"},
]

list_operators = ["==", "!=", ">", "<", ">=", "<=", "!@=", "!_=", "@=", "_=", "[]"]


def generate_condition_extra(params):
    try:
        character = next((el for el in list_operators if el in params), "")

        arr_left_right = params.split(character)
        arr_left_right[0] = arr_left_right[0].strip()
        arr_left_right[1] = arr_left_right[1].strip()
        if not arr_left_right[1]:
            return None

        condition_right = (
            arr_left_right[1].replace("(", "").replace(")", "").split("|")
            if character != "[]"
            else [arr_left_right[1]]
        )

        condition_return = []
        arr = []
        if "|" in arr_left_right[0]:
            str = get_between_condition(arr_left_right[0])
            arr = str.split("|")
        else:
            arr.append(arr_left_right[0])
        for element in arr:
            for right in condition_right:
                arr_append = [element, right.strip()]
                obj = gen_condition(arr_append, character)
                condition_return.append(obj)
        return condition_return
    except Exception as ex:
        raise ex


def get_between_condition(str):
    return str[str.index("(") + 1 : str.rindex(")")].strip()


def generate_condition(params):
    try:
        character = next((el for el in list_operators if el in params), "")
        arr_left_right = params.split(character)
        arr_left_right[0] = arr_left_right[0].strip()
        arr_left_right[1] = arr_left_right[1].strip()
        if not arr_left_right[1]:
            return None
        condition_return = gen_condition(arr_left_right, character)
        return condition_return
    except Exception as ex:
        raise ex


def gen_condition(arr_left_right, character):
    condition_left, condition_right = arr_left_right
    # if "." in condition_left:
    #     condition_left = "$" + condition_left + "$"
    if condition_right == "null":
        condition_right = None

    # Format
    if character == "==":
        return {condition_left: condition_right}
    if character == "!=":
        return {condition_left: {"$ne": condition_right}}
    if character == ">":
        return {condition_left: {"$gt": condition_right}}
    if character == "<":
        return {condition_left: {"$lt": condition_right}}
    if character == ">=":
        return {condition_left: {"$gte": condition_right}}
    if character == "<=":
        return {condition_left: {"$lte": condition_right}}
    if character == "@=":
        return {condition_left: {"$regex": f".*{condition_right}.*"}}
    if character == "_=":
        return {condition_left: {"$regex": f"{condition_right}.*"}}
    if character == "!@=":
        return {condition_left: {"$not": {"$regex": f".*{condition_right}.*"}}}
    if character == "!_=":
        return {condition_left: {"$not": {"$regex": f"{condition_right}.*"}}}
    if character == "[]":
        val_search = get_between_condition(condition_right)
        arr_start_end = val_search.split("&")
        start = datetime.strptime(f"{arr_start_end[0]} 00:00:00", "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(f"{arr_start_end[1]} 23:59:59", "%Y-%m-%d %H:%M:%S")
        return {
            "$and": [{condition_left: {"$gte": start}}, {condition_left: {"$lte": end}}]
        }
    raise Exception("Invalid operator format")


def get_correct_format_time(value):
    arrayFormat = ["YYYY/MM/DD", "YYYY-MM-DD", "DD/MM/YYYY", "DD-MM-YYYY", "YYYY-MM-DD"]
    for element in arrayFormat:
        if datetime.strptime(value, element):
            return element
    return None


def modify_filter_string(filter):
    # LEGACY: commented out part is for identifying if field is of Date type
    index_op = 0

    filter_string = filter
    arr_filters = filter_string.split(",") if filter_string is not None else []
    condition_checked_child = []
    for element in arr_filters:
        if "|" in element:
            obj_condition = generate_condition_extra(element)
            if not obj_condition:
                continue
            condition_not_or = {"$or": obj_condition}
            condition_checked_child.append(condition_not_or)
        else:
            condition_not_or = generate_condition(element)
            if not condition_not_or:
                continue
            condition_checked_child.append(condition_not_or)
        index_op += 1
    condition = (
        {"$and": condition_checked_child}
        if len(condition_checked_child) > 1
        else condition_checked_child[0]
    )

    return condition if condition_checked_child else {}
