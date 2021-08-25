# Basic Configuration

pg4j has three major methods of configuration.

- Mapping and Import input files
- The pg4j configuration file
- Environmental Variables

Main

Input files are the main inputs used with the `pg4j dump` and `pg4j import` commands. These files hold the mose frequently changing parameters for a port. Paraeaters like table aliases, column mappings, and exclude/include filters should all be placed in these files.

The pg4j configuration file should hold project-level infrequently changed information. This mainly includes connection information for both the postgresql and neo4j databases as well as output.

Environmental variables are mainly used to store sensitive information related to connections that shouldn't be written into plain text files. All environmental variables overwrite their respective value in the configuration file using the following prefix `PG4J__`. For example, to overwride the
