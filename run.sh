#!/bin/bash

# Install requirements
pip -q install -r requirements.txt


# Run app
flask --app app --debug run
