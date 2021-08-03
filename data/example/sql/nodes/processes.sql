select
	p.id as "processID:ID(Process)",
	p.machine_name,
	p."timestamp" "timestamp",
	p."ordering" "ordering:int",
	pd.type,
	pd.technique,
	'Process' as ":LABEL"
from
	development.process p
left join development.process_detail pd on
	pd.id = p.process_detail_id