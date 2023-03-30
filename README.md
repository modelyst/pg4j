<!--
   Copyright 2021 Modelyst LLC

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 -->

# pg4j

<p align="center">
  <a href="https://www.pg4j.modelyst.com"><img src="docs/img/pg4j_logo.png" alt="pg4j"></a>
</p>
---

**Documentation**: <a href="https://pg4j.modelyst.com" target="_blank">https://pg4j.modelyst.com</a>

**Github**: <a href="https://github.com/modelyst/pg4j" target="_blank">https://github.com/modelyst/pg4j</a>

---

pg4j is a package designed to perform etl from a postgres database to a neo4j database.

pg4j was written to expedite the creation of neo4j graph databases from postgresql databases by leveraging the information stored in the postgresql schema. While there does exist a [neo4j-etl](https://neo4j.com/labs/etl-tool/) tool does exist, it is written primarily in java and not open-source. In contrast, pg4j was meant to be a fully open-source python package for interacting with postgresql and neo4j databases.

## pg4j Feautures

The key features of pg4j:

1.  Automatic mapping of a postgresql schema to nodes, edges in neo4j
2.  Simple customization of the mapping between postgresql and neo4j entities
3.  Utilizes the well-tested [sqlalchemy](https://www.sqlalchemy.org/) package to allow for future interactions with all SQL type databases.
4.  The use of custom SQL for creation of entities in neo4j

pg4j was initially developed by [Modelyst](https://www.modelyst.com/).

## Getting pg4j

### Via Pip (Recommended)

```Bash
pip install pg4j
```

### Via Github

For development purposes pg4j can be obtained from [github](https://github.com/modelyst/pg4j). This is best done by using the [poetry](https://python-poetry.org/) package manager. To do this, first clone the repo to a local directory. Then use the command `poetry install` in the directory to install the required dependencies. You will need at least python 3.7 to install the package.

```Bash
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
```

#### Neo4j Versioning
pg4j version >=0.1.0 is compatibable with Neo4j version 5.0

#### Reporting bugs

Please report any bugs and issues at pg4j's [Github Issues
page](https://github.com/modelyst/pg4j/issues).

## License

pg4j is released under the [Apache 2.0 License](license/).
