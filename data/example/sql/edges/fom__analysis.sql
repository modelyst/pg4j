select
	md5(a.id::text || '-' || out.key) as ":START_ID(FOM)",
	a.id as ":END_ID(Analysis)"
from
	development.analysis a,
	jsonb_each(a.output) as out