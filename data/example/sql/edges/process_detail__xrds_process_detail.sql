select
	pd.id ":START_ID(ProcessDetail)",
	xpd.id ":END_ID(XRDSProcessDetail)"
from
	development.process_detail pd
join development.xrds_process_detail xpd on
	pd.xrds_process_detail_id = xpd.id;