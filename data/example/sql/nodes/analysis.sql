select
	a.id as "analysisId:ID(Analysis)",
	a.analysis_name as "analysis_name",
	ad.details as "details",
	a.output as "output",
	'Analysis' as ":LABEL"
from
	development.analysis a
join development.analysis_detail ad on
	ad.id = a.analysis_detail_id