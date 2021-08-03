select
	sp.id ":START_ID(SampleProcess)",
	pd.id ":END_ID(ProcessData)"
from
	development.sample_process sp
join development.sample_process_process_data sppd on
	sppd.sample_process_id = sp.id
join development.process_data pd on
	pd.id = sppd.process_data_id