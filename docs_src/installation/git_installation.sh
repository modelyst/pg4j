# Get DBgen
git clone https://github.com/modelyst/pg4j
cd ./pg4j
# Get Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
# Install Poetry
poetry install
poetry shell
# Test pg4j
pg4j version
