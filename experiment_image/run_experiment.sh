#!/bin/bash

chaos run $1 --journal-path=/home/svc/experiments/journal.json

python3 upload_journal.py
