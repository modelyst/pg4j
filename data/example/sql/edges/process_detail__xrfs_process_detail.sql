select
	pd.id ":START_ID(ProcessDetail)",
	xpd.id ":END_ID(XRFSProcessDetail)"
from
	development.process_detail pd
join development.xrfs_process_detail xpd on
	pd.xrfs_process_detail_id = xpd.id;