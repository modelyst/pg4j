select
	pd.id ":START_ID(ProcessDetail)",
	epd.id ":END_ID(EcheProcessDetail)"
from
	development.process_detail pd
join development.eche_process_detail epd on
	pd.eche_process_detail_id = epd.id;