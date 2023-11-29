#!/bin/bash
set -e
# Script to get push ready by migrating, formatting, outputting static files,
# and running tests.

function alert_failure {
  echo "Commit has failed! BOOOOOOOOO!";
  cat rat_ascii_art.txt;
}

function alert_success {
  echo "Commit has succeeded!";
  cat eagle_ascii_art.txt;
}

backend_directory="backend";
frontend_directory="frontend";

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
    exit 1
fi

trap alert_failure ERR
# Backend
black --preview ./$backend_directory
flake8 --config ./$backend_directory/.flake8 ./$backend_directory
mypy --config-file ./$backend_directory/mypy.ini -p $backend_directory
python ./$backend_directory/manage.py makemigrations
python ./$backend_directory/manage.py migrate
python ./$backend_directory/manage.py loaddata backend/core/fixtures/*.json
# Only test certain critical tests that use openAI API. Otherwise its too slow.
python ./$backend_directory/manage.py test core --exclude-tag=slow
pip freeze > ./$backend_directory/requirements.txt

# Frontend
# yapf . --recursive -i
# prettier --debug-check frontend/src/*
# prettier --write frontend/src/*
# eslint frontend/src/**/*.ts --max-warnings 0
# npm test
# python manage.py test -p *_test.py

git add -A
git commit -m "$1"
git push

alert_success