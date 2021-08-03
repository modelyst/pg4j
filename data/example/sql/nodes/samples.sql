select
	s.id as "sampleID:ID(Sample)",
	split_part(s.label, '-', 2) as "jcap_sample_id:int",
	jcap_plate_id as "jcap_plate_id:int",
	jsd.x "x:float",
	jsd.y "y:float",
	jsd.init_comp,
	'Sample' as ":LABEL"
from
	development.sample s
left join development.jcap_sample_details jsd on
	jsd.id = s.jcap_sample_details_id;