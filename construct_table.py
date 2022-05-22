#!/bin/python3

'''
 Copyright (c) Matthew Smith (DeltaBoyBZ)
 Provided under an MIT license as part of the tabular-cpp project
 found at https://github.com/DeltaBoyBZ/tabular-cpp 
'''

import sys

# inserts a table definition at the appropriate point in the header file
def replaceHeaderBlock(table_info, table_definition, header_filename):
    header = open(header_filename, "r") 
    temp = open(header_filename + "." + table_info["name"] + ".temp", "w")

    inside_table = False

    for line in header:
        if(not inside_table): 
            temp.write(line)
            if("//TABLE_BEGIN {}".format(table_info["name"]) in line):
                inside_table = True

        else:
            if("//TABLE_END {}".format(table_info["name"]) in line):
                inside_table = False
                temp.write(line)


    temp.close()
    header.close()

    header = open(header_filename, "w")
    temp = open(header_filename + "." + table_info["name"] + ".temp", "r")

    for line in temp:
        header.write(line)
        if("//TABLE_BEGIN {}".format(table_info["name"]) in line):
            header.write(table_definition)


# creates table info (if necessary) and parses it before pasting it into a header file 
def make_table(table_info, header_name):
    add_args = ""
    for field in table_info['fields']:
        add_args += "{} {}, ".format(field['type'], field['name'])

    add_args = add_args[:-2]

    table_constructor = f"TABCPP_CONSTRUCTOR({table_info['name']}, {table_info['key']['name']}, {table_info['key']['datatype']})\n"
    table_destructor = f"TABCPP_DESTRUCTOR({table_info['name']})\n"

    table_update_add = ""
    table_update_remove = ""
    table_field_declarations = ""
    for field in table_info['fields']:
        table_field_declarations += f"TABCPP_FIELD({table_info['key']['datatype']}, {field['type']}, {field['name']});\n"
        table_update_add += f"TABCPP_APPEND({field['name']}, {field['name']});\n"
        table_update_remove += f"TABCPP_REMOVE({field['name']}, index);\n"

    if(table_info['key']['type'] == "auto"):
        table_update_remove += f"TABCPP_REMOVE({table_info['key']['name']}, index);\n"
        table_field_declarations += f"TABCPP_FIELD({table_info['key']['datatype']}, { table_info['key']['datatype'] }, { table_info['key']['name'] });\n"
        table_add_func = f"TABCPP_ADD_FUNC_AUTO({table_info['key']['datatype']}, TABCPP_ARGS({add_args}), {table_update_add});\n" 

    else:
        table_add_func = f"TABCPP_ADD_FUNC_MAN({table_info['key']['datatype']}, TABCPP_ARGS({add_args}), {table_update_add});\n"

    table_remove_func = f"TABCPP_REMOVE_FUNC({table_info['key']['datatype']}, {table_update_remove});\n"

    table_definition = f"TABCPP_TABLE({table_info['name']}, {table_info['key']['datatype']}, {table_constructor}, {table_destructor}, {table_field_declarations}, {table_add_func}, {table_remove_func});\n"

    
    # replace a block in a nominated header file with the code which constructs a new table

    header_dir = sys.argv[2] + "/"

    header_filename = header_dir + header_name

    replaceHeaderBlock(table_info, table_definition, header_filename)


    


if __name__ == "__main__":
    table_mod = __import__(sys.argv[1])
    header_name = input("Name of the header file: ")
    for table_info in table_mod.tables:
        make_table(table_info, header_name)


