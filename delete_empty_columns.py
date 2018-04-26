# -*- coding: utf-8 -*-
"""Delete all empty columns in the sim.db, except the default ones.

Usage: python delete_empty_columns.py
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import helpers
import sqlite3

def delete_empty_columns():
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    column_names, column_types = helpers.get_db_column_names_and_types(db_cursor)
    new_table_dict = {}
    for column_name, column_type in zip(column_names, column_types):
        db_cursor.execute("SELECT {} FROM runs;".format(column_name))
        values =  db_cursor.fetchall()
        is_empty = True
        for value in values:
            if value != (None,):
                is_empty = False
                break
        if not is_empty or (column_name in helpers.default_db_columns):
            new_table_dict[column_name] = column_type

    new_columns_and_types = ""
    new_columns = ""
    for column_name in new_table_dict:
        new_columns_and_types += column_name + " " + new_table_dict[column_name] + ", "
        new_columns += column_name + ", "
    new_columns_and_types = new_columns_and_types[:-2]
    new_columns = new_columns[:-2]
    
    assert new_columns_and_types[0:2] == 'id', "Name of first column in database is not 'id'."
    new_columns_and_types = new_columns_and_types[0:10] + " PRIMARY KEY" \
                           +new_columns_and_types[10:] # Correct id type

    db_cursor.execute("CREATE TABLE IF NOT EXISTS new_runs ({});".format(new_columns_and_types))

    db_cursor.execute("INSERT INTO new_runs SELECT {0} FROM runs;".format(new_columns))

    db_cursor.execute("DROP TABLE runs;")
    db_cursor.execute("ALTER TABLE new_runs RENAME TO runs;")

    db.commit()
    db_cursor.close()
    db.close()

if __name__ == '__main__':
    delete_empty_columns()
