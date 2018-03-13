#!/bin/bash

message=$1

export FLASK_APP=run.py
export FLASK_DEBUG=1
flask db migrate -m "$message"
