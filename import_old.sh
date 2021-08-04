# Stops database
neo4j stop
# Removes Old Database
rm -rf /usr/local/var/neo4j/data/databases/neo4j
rm -rf /usr/local/var/neo4j/data/transactions/neo4j
# Imports new data
neo4j-admin import \
    --id-type=STRING  \
    --skip-duplicate-nodes  \
    --nodes=Sample=./data/nodes/samples.csv \
    --nodes=Plate=./data/nodes/plates.csv \
    --nodes=SampleProcess=./data/nodes/sample_processes.csv \
    --nodes=Process=./data/nodes/processes.csv \
    --nodes=ProcessData=./data/nodes/process_data.csv \
    --nodes=Analysis=./data/nodes/analysis.csv \
    --nodes=FOM=./data/nodes/fom.csv \
    --nodes=ProcessDetail=./data/nodes/process_details.csv \
    --nodes=UvisProcessDetail=./data/nodes/uvis_process_details.csv \
    --nodes=AnnealProcessDetail=./data/nodes/anneal_process_details.csv \
    --nodes=PrintProcessDetail=./data/nodes/print_process_details.csv \
    --nodes=EcheProcessDetail=./data/nodes/eche_process_details.csv \
    --nodes=XRDSProcessDetail=./data/nodes/xrds_process_details.csv \
    --nodes=XTRNProcessDetail=./data/nodes/xtrn_process_details.csv \
    --nodes=XRFSProcessDetail=./data/nodes/xrfs_process_details.csv \
    --relationships=ON=./data/edges/sample__plate.csv  \
    --relationships=UNDERGOES=./data/edges/sample_process__process.csv \
    --relationships=SAMPLE=./data/edges/sample_process__sample.csv \
    --relationships=NEXT=./data/edges/states.csv \
    --relationships=HAS_DATA=./data/edges/sample_process__process_data.csv \
    --relationships=INPUT=./data/edges/process_data__analysis.csv \
    --relationships=ANALYSIS=./data/edges/fom__analysis.csv \
    --relationships=DETAILS=./data/edges/process__process_detail.csv \
    --relationships=DETAILS=./data/edges/process_detail__uvis_process_detail.csv \
    --relationships=DETAILS=./data/edges/process_detail__eche_process_detail.csv \
    --relationships=DETAILS=./data/edges/process_detail__anneal_process_detail.csv \
    --relationships=DETAILS=./data/edges/process_detail__print_process_detail.csv \
    --relationships=DETAILS=./data/edges/process_detail__xrds_process_detail.csv \
    --relationships=DETAILS=./data/edges/process_detail__xtrn_process_detail.csv \
    --relationships=DETAILS=./data/edges/process_detail__xrfs_process_detail.csv \
    --database neo4j 
neo4j start