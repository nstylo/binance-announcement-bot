#!/bin/bash


if [ $1 = 'dev' ]; then
    test -f config.yaml || ln -s config_dev.yaml config.yaml
elif [ $1 = 'prod' ]; then
    test -f config.yaml || ln -s config_prod.yaml config.yaml
else
    >&2 echo \'$1\' "is not a valid argument."
    >&2 echo "must be either 'dev' or 'prod'."
    exit 1
fi

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

python src/main.py
