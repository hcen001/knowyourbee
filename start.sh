#!/bin/bash

export APP_CONFIG_FILE=/home/fabian-a/knowyourbee.org/config/development.py
export FLASK_APP=run.py
flask run --host=0.0.0.0
