select
	p.id ":START_ID(Process)",
	pd.id ":END_ID(ProcessDetail)"
from
	development.process p
join development.process_detail pd on
	pd.id = p.process_detail_id;