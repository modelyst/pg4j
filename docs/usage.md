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

# Usage

This page walks through an extended example which can expose new users the basic use of pg4j.

## Overview

The basic use of pg4j is the dump of a postgresql database, done through the `pg4j dump` command. This is followed by the import of the resulting output directories filled with csv's into a neo4j database, done through the `pg4j import` command.

## Dump

The `pg4j dump` postgres database into a set of csv's that are compatible with neo4j's import tooling. This requires mapping entities and relationships in the postgresql database to nodes and edges in the neo4j database. By default this mapping is done automatically by reading the postgresql's schema. This automatic mapping requires Foreign Key relationships in the postgresql database to be explicit using the Foreign Key Constraint. When this is done most Tables become nodes and Foreign Keys become edges. However, due to the limitation relational databases, many tables in postgresql most accurately represent edges in neo4j. This is true if a table is considered a mapping table, i.e. it contains two foreign keys to two other tables and is the target of any foreign keys in the database. When this is true the mapping table is automatically detected and mapped to an edge in neo4j. This automatic mapping-table transformation can be overridden using the mapping input file (!TODO! link to mapping input section).

To run a basic dump, simple set the `PG4J__POSTGRES_DSN`, `PG4J__POSTGRES_SCHEMA` and `PG4J__POSTGRES_PASSWORD` through either environmental variables, setting files, or the cli arguments `--conn` and `--db-password`, respectively. For example, to connect to a database running locally at port 5432 in the database named pg4j in the public schema for user `postgres` and password `password` run the following command:

```Bash
pg4j dump \
--conn 'postgresql://postgres@localhost/pg4j' \
--password password \
--schema public
```

By default this will dump the result of the mapping and subsequent dump to the directory specified by the cli argument `--output` which defaults to a folder in the current working directory named `./output`. This folder will contain two sub-directories for nodes and edges, where each holds the csv's for a given node or edge, respectively.

To customize the names, attributes, labels and the included/excluded of each node/edge in the mapping see the full overview of the dump command (Coming Soon!)

## Import

Once a postgres database has been dumped into a pg4j data directory it can be imported into neo4j through the `pg4j import` command. To import the output directory created by the command above you run the following command:

```Bash
pg4j import \
--neo4j-home "/usr/local/var/neo4j/data/" \
--dbname neo4j \
--data-dir ./output
```

This will import the data stored in the `./output` folder into the neo4j instance whose data is stored at `--neo4j-home`. Just as with dump you can customize the import through a import file and command-line arguments. See the import section for the full overview of the import command.
