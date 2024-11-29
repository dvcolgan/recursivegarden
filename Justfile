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

reset_db:
    rm -f ./recursivegarden_dev.db
    python manage.py migrate
    python manage.py create_demo_data