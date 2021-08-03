select
	pd.id ":START_ID(ProcessDetail)",
	apd.id ":END_ID(AnnealProcessDetail)"
from
	development.process_detail pd
join development.anneal_process_detail apd on
	pd.anneal_process_detail_id = apd.id;