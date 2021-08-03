select
	md5(a.id::text || '-' || out.key) as "FomId:ID(FOM)",
	out.key as "Key",
	out.value as "Value",
    'FOM' as ":LABEL"
from
	development.analysis a,
	jsonb_each(a.output) as out