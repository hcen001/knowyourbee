#!/bin/bash

export LANG=en_US.utf8
export LC_ALL=en_US.utf8
export APP_CONFIG_FILE=/home/fabian-a/knowyourbee.org/config/development.py
export FLASK_APP=run.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0
