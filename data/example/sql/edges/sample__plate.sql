select
	s.id ":START_ID(Sample)",
	c.id ":END_ID(Plate)"
from
	development.sample s
join development.collection_sample cs on
	cs.sample_id = s.id
join development.collection c on
	c.id = cs.collection_id;