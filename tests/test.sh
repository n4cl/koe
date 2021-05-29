#!/usr/bin/bash

set -u

cd /usr/local/tests
pytest --cov -v test.py
