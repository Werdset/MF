#!/bin/bash

PROJECT_DIR=/home/mf/MuscleFeed

cd $PROJECT_DIR
. venv/bin/activate
python manage.py generate_stats
