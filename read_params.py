# -*- coding: utf-8 -*-
""" Read the specified parameters from the database.

The parameters is converted to correct type.
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

from add_sim import get_database_name_from_settings
from add_sim import get_column_names_and_types
import sqlite3

def convert_text_to_correct_type(value, check_that_type_is):
    correct_type = False
    value_split = value.split('[')
    if value == "True":
        value = True
        if (check_that_type_is == 'bool' or check_that_type_is == bool):
            correct_type = True
    elif value == "False":
        value = False
        if (check_that_type_is == 'bool' or check_that_type_is == bool):
            correct_type = True
    elif len(value_split) == 1:
        if (check_that_type_is == 'string' or check_that_type_is == str):
            correct_type = True
    else:
        value = []
        if value_split[0].strip() == 'int':
            if (check_that_type_is == 'int array' or check_that_type_is == list):
                correct_type = True
            for element in value_split[1].split(']')[0].split(','):
                value.append(int(element))
        elif value_split[0].strip() == 'float':
            if (check_that_type_is == 'float array' or check_that_type_is == list):
                correct_type = True
            for element in value_split[1].split(']')[0].split(','):
                value.append(float(element))
        elif value_split[0].strip() == 'string':
            if (check_that_type_is == 'string array' or check_that_type_is == list):
                correct_type = True
            for element in value_split[1].split(']')[0].split(','):
                value.append(str(element))
        elif value_split[0].strip() == 'bool':
            if (check_that_type_is == 'bool array' or check_that_type_is == list):
                correct_type = True
            for element in value_split[1].split(']')[0].split(','):
                if element == 'True':
                    element = True
                elif element == 'False':
                    element = False
                else:
                    correct_type = False
                value.append(element)
        else:
            correct_type = False

    return value, correct_type
    
def read_param_from_db(db_id, column, check_that_type_is=''):
    """Read parameter with id 'db_id' and column name 'column' from the database.

    check_that_type_is (string or type): Throws ValueError if type does not 
        match 'check_that_type_is'. The valid types the strings 'int', 'float', 
        'bool', 'string' and 'int/float/bool/string array' or the types int, 
        float, bool, str and list.
    """
        
    database_name = get_database_name_from_settings()
    if database_name:
        db = sqlite3.connect(database_name)
    else:
        print "Could NOT find a path to a database in 'settings.txt'." \
            + "Add path to the database to 'settings.txt'."
   
    db_cursor = db.cursor()

    db_cursor.execute("SELECT {0} FROM runs WHERE id={1}".format(column, db_id))
    value = db_cursor.fetchone()[0]

    column_names, column_types = get_column_names_and_types(db_cursor)
    type_dict = dict(zip(column_names, column_types))
    type_of_value = type_dict[column]

    correct_type = True
    if ((check_that_type_is == 'int' or check_that_type_is == int) 
            and type_of_value != 'INTEGER'):
        correct_type = False
    elif ((check_that_type_is == 'float' or check_that_type_is == float)
            and type_of_value != 'REAL'):
        correct_type = False
    elif (type_of_value == 'TEXT'):
        value, correct_type = convert_text_to_correct_type(value, 
                                                           check_that_type_is)
    else:
        correct_type = False

    if not correct_type and check_that_type_is != '':
        raise ValueError("The type is NOT {}.".format(check_that_type_is))

    db.commit()
    db_cursor.close()
    db.close()
    
    return value
