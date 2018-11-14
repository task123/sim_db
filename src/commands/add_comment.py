# -*- coding: utf-8 -*-
"""  Add a comment to a simulation the database.

Usage: python add_comment --id ID -c 'comment' 
       or python add_comment --id ID --filename
       or python add_comment --id ID --append 'comment'
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.commands.update_sim as update_sim
import src.commands.helpers as helpers
import argparse


def command_line_arguments_parser(argv):
    # yapf: disable
    parser = argparse.ArgumentParser(description='Add comment to simulation in database.')
    parser.add_argument('--id', '-i', type=int, required=True, help="<Required> ID of the simulation to add the comment.")
    parser.add_argument('--comment', '-c', type=str, default=None, help="Comment to add.")
    parser.add_argument('--filename', '-f', type=str, default=None, help="Filename of a file which content are to be added as a comment. Only the last 3000 characters will be added.")
    parser.add_argument('--append', '-a', action='store_true', help="Append comment or file to the current comment.")
    # yapf: enable

    return parser.parse_args(argv)


def add_comment(argv=None):
    args = command_line_arguments_parser(argv)
    if (args.comment == None and args.filename == None):
        print("ERROR: Either '--comment'/'-c' or '--filename'/'-f' need to be provided."
              )
        exit()
    comment = ""
    if args.append:
        db = helpers.connect_sim_db()
        db_cursor = db.cursor()
        db_cursor.execute("SELECT comment FROM runs")
        fetched = db_cursor.fetchone()
        if len(fetched) > 0:
            comment = fetched[0]
        db.commit()
        db_cursor.close()
        db.close()
    if args.comment != None:
        comment += args.comment
    if args.filename != None:
        with open(args.filename) as comment_file:
            comment_content = comment_file.read()
            if len(comment_content) > 3000:
                warning = "WARNING: Comment limited to the last 3000 characters of the file."
                print(warning)
                comment_content = warning + '\n'
                comment_content += comment_content[(
                        len(comment_content) - 3000):]
            comment += comment_content
    update_sim.update_sim([
            '--id',
            str(args.id), '--columns', 'comment', '--values', comment
    ])


if __name__ == '__main__':
    add_comment()
