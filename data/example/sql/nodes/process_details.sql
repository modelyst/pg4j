select
	pd.id as "processDetailID:ID(ProcessDetail)",
	'ProcessDetail' as ":LABEL",
	pd.type "type",
	pd.technique "technique"
from
	development.process_detail pd;