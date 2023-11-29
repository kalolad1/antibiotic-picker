release: python ./backend/manage.py migrate; python ./backend/manage.py loaddata backend/core/fixtures/*.json;
web: gunicorn --chdir backend antibiotic_picker_backend.wsgi
