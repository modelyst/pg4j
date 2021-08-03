select
	pd.id ":START_ID(ProcessData)",
	a.id ":END_ID(Analysis)"
from
	development.analysis a 
join development.process_data_analysis pda on
	pda.analysis_id  = a.id
join development.process_data pd on
	pd.id = pda.process_data_id;