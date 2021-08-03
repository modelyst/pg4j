select
	pd.id as "processDataID:ID(ProcessData)",
	pd.path,
	pd.file_name,
	pd.file_type
from
	development.process_data pd