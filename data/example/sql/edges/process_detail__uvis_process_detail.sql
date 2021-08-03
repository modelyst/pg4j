select
	pd.id ":START_ID(ProcessDetail)",
	upd.id ":END_ID(UvisProcessDetail)"
from
	development.process_detail pd
join development.uvis_process_detail upd on
	pd.uvis_process_detail_id = upd.id;