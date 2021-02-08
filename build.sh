#!/usr/bin/env bash
SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd ${SHELL_FOLDER}
source venv/bin/activate
rm ./dist -rf
python setup.py sdist build
ls dist | grep -v "+" | while read filename; do twine upload dist/$filename -r pypi-kd; done
