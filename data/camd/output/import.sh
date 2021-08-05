neo4j stop
rm -rf /usr/local/var/neo4j/data/databases/test
rm -rf /usr/local/var/neo4j/data/transactions/test
neo4j admin import \
    --id-type=STRING \
    --skip-duplicate-nodes \
    --nodes=/Users/brianrohr/Documents/Modelyst/repos/pg4j/data/camd/output/nodes/data_point.csv \
    --nodes=/Users/brianrohr/Documents/Modelyst/repos/pg4j/data/camd/output/nodes/test.csv \
    --nodes=/Users/brianrohr/Documents/Modelyst/repos/pg4j/data/camd/output/nodes/acquired_point.csv \
    --nodes=/Users/brianrohr/Documents/Modelyst/repos/pg4j/data/camd/output/nodes/campaign.csv \
    --relationships=/Users/brianrohr/Documents/Modelyst/repos/pg4j/data/camd/output/edges/acquired_point__data_point.csv \
    --relationships=/Users/brianrohr/Documents/Modelyst/repos/pg4j/data/camd/output/edges/acquired_point__campaign.csv \
    --database test
neo4j start