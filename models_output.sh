#!/usr/bin/env bash
date=$(date '+%Y_%m_%d')
./manage.py showmodels 2> "$date.dat"
