# Configuration

pg4j has three major methods of configuration.

- Mapping and Import input files
- Command line arguments
- The pg4j Settings file
- Environmental Variables

## Input Files

Input files are the main inputs used with the `pg4j dump` and `pg4j import` commands. These files hold the most frequently changing parameters for database mapping. Parameters like table aliases, column mappings, and exclude/include filters should all be placed in these files. See

## Command Line Arguments

Command line arguments allow for settings to be overwritten at runtime. Command line arguments take precedence over all other setting sources. For example, the `pg4j dump` command offers the command line argument `--db-password` that overwrites the value of the `pg4j__postgres_password` variable in the settings file or environmental.

## Settings File

The pg4j configuration file should hold project-level infrequently changed information. This mainly includes connection information for both the postgresql and neo4j databases as well as output. A configuration file is formatted in the [dotenv](https://pypi.org/project/python-dotenv/) style.

Below is an example setting file:

```ini
# Pg4j Settings
pg4j__postgres_dsn = postgresql://postgres@localhost:5432/pg4j
pg4j__postgres_password = password
pg4j__postgres_schema = public
pg4j__neo4j_dsn = neo4j://neo4j@localhost:7687/neo4j
pg4j__neo4j_password = password
```

The setting file can be set through the Environmental variable `PG4J_SETTINGS` or can be fed directly to commands like dump and import.

## Environmental Variables

Environmental variables are mainly used to store sensitive information related to connections that shouldn't be written into plain text files. All environmental variables overwrite their respective value in the configuration file using the following prefix `PG4J__`. For example, to override the the postgres_password set the `PG4J__POSTGRES_PASSWORD` environmental variable.

> _Note that all environmental and setting file variables are case insensitive_

## pg4j setting

A helpful function to see the current configuration is the `pg4j setting` command. It prints to the screen all the current settings given the environmental variables and `PG4J_SETTINGS` command. Passwords will automatically be hidden unless the `--show-passwords` flag is passed to the command.

## Precedence

The order of precedence for any setting is as follows:

1.  Command Line Argument
2.  Environmental Variable
3.  Settings File
4.  Defaults
