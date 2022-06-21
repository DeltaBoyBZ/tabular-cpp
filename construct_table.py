#!/bin/python3

'''
 Copyright (c) Matthew Smith (DeltaBoyBZ)
 Provided under an MIT license as part of the tabular-cpp project
 found at https://github.com/DeltaBoyBZ/tabular-cpp 
'''

import sys
import os

# scans a header file and picks out table code
def createTableModule(header_filename):
    header = open(header_filename, "r");
    inside_module = False 
    module_filename = f"{header_filename.split('.')[0]}_tables.py"
    module_name = module_filename.split("/")[-1][:-3]
    module = open(module_filename, "w")

    namespace_prefix = ""
    namespace_suffix = ""
    for line in header:
        if(inside_module):
            if("TABCPP_CLOSE" in line): 
                inside_module = False
                continue
            module.write(line)

        elif("TABCPP_OPEN" in line): inside_module = True 

        elif("namespace" in line):
                namespace_prefix = line
                if('{' not in namespace_prefix): namespace_prefix += "{\n"
                namespace_suffix = "}"



    header.close()
    module.close()

    return (module_name, namespace_prefix, namespace_suffix)

# writes a table constructer to a given header file
def createTableHeader(header_filename, tables, namespace_prefix, namespace_suffix): 
    table_header = open(header_filename, "w")
    table_header.write("#pragma once\n#include<tabcpp/tabcpp.hpp>\n")
    table_header.write(namespace_prefix)
    for table_info in tables:
        table_definition = make_table(table_info)
        table_header.write(table_definition)
    table_header.write(namespace_suffix)
    table_header.close()

# adds an appropriate include statement to a header file
def addInclude(header_filename, include_filename):
    # temp file
    temp = open(f"{header_filename}.temp", "w")
    orig = open(header_filename)
    inserting = False
    orig_lines = [line for line in orig]
    orig_index = 0

    while(orig_index < len(orig_lines)):
        if(not inserting): 
            temp.write(orig_lines[orig_index])
            if("#pragma once" in orig_lines[orig_index]): inserting = True
            orig_index += 1
        else:
            temp.write(f"#include\"{include_filename}\"\n")
            inserting = False

    temp.close()
    orig.close()
    # transfer temp to orig
    os.rename(f"{header_filename}.temp", header_filename)


# inserts a table definition at the appropriate point in the header file
def replaceHeaderBlock(table_info, table_definition, header_filename):
    header = open(header_filename, "r") 
    temp = open(header_filename + "." + table_info["name"] + ".temp", "w")

    inside_table = False

    for line in header:
        if(not inside_table): 
            temp.write(line)
            if("//TABLE_BEGIN {}".format(table_info["name"]) in line and table_info['name'] in line):
                temp.write(table_definition)
                inside_table = True

        else:
            if("//TABLE_END {}".format(table_info["name"]) in line and table_info['name'] in line):
                inside_table = False
                temp.write(line)


    
    temp.close()
    header.close()

    os.rename(header_filename + "." + table_info["name"] + ".temp", header_filename)



def make_table(table_info):
    add_args = ""
    table_row_decs = ""
    get_row_assignments = ""
    for field in table_info['fields']:
        add_args += "{} {}, ".format(field['type'], field['name'])
        table_row_decs += f"TABCPP_ROW_FIELD_DEC({field['type']}, {field['name']}) "
        get_row_assignments += f"row.{field['name']} = this->{field['name']}[index];\n"

    add_args = add_args[:-2]

    table_row = f"TABCPP_ROW_STRUCT({table_info['name']}, {table_row_decs})\n"
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

    table_get_row = f"TABCPP_GET_ROW({table_info['name']}, {table_info['key']['datatype']}, {get_row_assignments})"
    table_definition = f"{table_row} TABCPP_TABLE({table_info['name']}, {table_info['key']['datatype']}, {table_constructor}, {table_destructor}, {table_field_declarations}, {table_add_func}, {table_remove_func}, {table_get_row});\n"

    
    # replace a block in a nominated header file with the code which constructs a new table

    return table_definition

def loadTables(header_filename, module_name):
    table_mod = __import__(module_name)

    tables = table_mod.tables


    for table_info in tables:
        table_definition = make_table(table_info)
        replaceHeaderBlock(table_info, table_definition, header_filename)


def createTables(header_dir, header_name):
    header_filename = f"{header_dir}/{header_name}"
    module_name, namespace_prefix, namespace_suffix = createTableModule(header_filename)
    table_header_filename = f"{header_dir}/{module_name}.hpp"
    table_mod = __import__(module_name)
    createTableHeader(table_header_filename, table_mod.tables, namespace_prefix, namespace_suffix)
    # TODO: rewrite this function so include statement is in good position
    # addInclude(header_filename, f"{module_name}.hpp")

def realiseTables(header_dir, header_name):
    header_filename = f"{header_dir}/{header_name}"
    module_name, namespace_prefix, namespace_suffix = createTableModule(header_filename)
    loadTables(header_filename, module_name)


if __name__ == "__main__":
    if("load" in sys.argv[1]):
        loadTables(f"{sys.argv[2]}/{sys.argv[3]}", sys.argv[4])
    elif("create" in sys.argv[1]):
        createTables(sys.argv[2], sys.argv[3])
    elif("realise" in sys.argv[1]):
        realiseTables(sys.argv[2], sys.argv[3])
    else:
        print("Unknown option: {}".format(sys.argv[1]))

        

