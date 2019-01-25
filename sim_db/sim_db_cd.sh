#!/bin/sh
cd "$(sim_db get $@)"
if [ -r $HOME/.bashrc ]; then
   source $HOME/.bashrc
fi
if [ -r $HOME/.bash_profile ]; then
   source $HOME/.bash_profile
fi
exec bash
