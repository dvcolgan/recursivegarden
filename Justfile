set dotenv-load

default:
    @just --list

clean:
    rm -rf .pytest_cache/ htmlcov/ .coverage coverage.xml

format:
    ruff format .
    ruff check . --fix
    djlint . --reformat --quiet

lint:
    ruff check .
    ruff format . --check
    djlint . --check

test:
    pytest

install:
    pip install -r requirements.txt

install_dev:
    pip install -r requirements-dev.txt

reset_dot_env_file:
    cp -i .env_sample .env

reset_db:
    rm -f ./recursivegarden_dev.db
    python manage.py migrate
    python manage.py create_demo_data