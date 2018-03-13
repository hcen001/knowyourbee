#!/bin/bash

message=$1

export APP_CONFIG_FILE=/home/fabian-a/knowyourbee.org/config/development.py
export FLASK_APP=run.py
export FLASK_DEBUG=1
flask db migrate -m "$message"
