#!/bin/bash
python -B -m pytest --html-report=output/results.html -s -p no:cacheprovider ./tests
python -B ./upload_to_s3.py