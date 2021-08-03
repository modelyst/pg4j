select
	sp.id ":START_ID(SampleProcess)",
	p.id ":END_ID(Process)"
from
	development.sample_process sp
join development.process p on
	p.id = sp.process_id