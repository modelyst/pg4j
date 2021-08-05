neo4j stop
rm -rf /usr/local/var/neo4j/data/databases/jcap
rm -rf /usr/local/var/neo4j/data/transactions/jcap
neo4j-admin import \
    --id-type=STRING \
    --skip-duplicate-nodes \
    --nodes=./nodes/acquired_point.csv\
    --nodes=./nodes/campaign.csv\
    --nodes=./nodes/data_point.csv\
    --relationships=./edges/acquired_point__campaign.csv \
    --relationships=./edges/acquired_point__data_point.csv \
    --database jcap
neo4j start