#!/bin/sh
#
# Copyright (C) 2018-2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

cd "$(sim_db get $@)"
if [ -r $HOME/.bashrc ]; then
   source $HOME/.bashrc
fi
if [ -r $HOME/.bash_profile ]; then
   source $HOME/.bash_profile
fi
exec bash
