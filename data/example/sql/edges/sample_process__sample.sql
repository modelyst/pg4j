select
	sp.id ":START_ID(SampleProcess)",
	s.id ":END_ID(Sample)"
from
	development.sample_process sp
join development.sample s on
	s.id = sp.sample_id