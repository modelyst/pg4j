SELECT development.process_data_analysis.analysis_id AS ":START_ID(Analysis)", development.process_data_analysis.process_data_id AS ":END_ID(ProcessData)", 'ProcessData' AS ":TYPE", development.process_data_analysis.deleted AS deleted, development.process_data_analysis.keyword AS keyword 
FROM development.process_data_analysis