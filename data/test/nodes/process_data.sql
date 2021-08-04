SELECT development.process_data.id AS "processData:ID(ProcessData)", 'ProcessData' AS ":LABEL", development.process_data.deleted AS deleted, development.process_data.path AS path, development.process_data.file_name AS file_name, development.process_data.file_type AS file_type, development.process_data.begin_line AS begin_line, development.process_data.end_line AS end_line, development.process_data.raw_data_json AS raw_data_json, development.process_data.extracted_path AS extracted_path 
FROM development.process_data