#!/bin/bash

# Install requirements
pip install -r requirements.txt


# Run app
flask --app app --debug run
