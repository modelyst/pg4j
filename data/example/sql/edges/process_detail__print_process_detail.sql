select
	pd.id ":START_ID(ProcessDetail)",
	ppd.id ":END_ID(PrintProcessDetail)"
from
	development.process_detail pd
join development.print_process_detail ppd on
	pd.print_process_detail_id = ppd.id;