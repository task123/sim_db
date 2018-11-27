#!/bin/sh
cd "$(sim_db get results_dir $@)"
source /Users/hakonaustlidtasken/.bash_profile
exec bash
