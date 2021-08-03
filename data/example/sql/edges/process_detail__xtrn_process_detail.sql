select
	pd.id ":START_ID(ProcessDetail)",
	xpd.id ":END_ID(XTRNProcessDetail)"
from
	development.process_detail pd
join development.xtrn_process_detail xpd on
	pd.xtrn_process_detail_id = xpd.id;