select
	sp.id as "SampleProcessID:ID(SampleProcess)",
    pd.type,
    pd.technique
from
	development.sample_process sp
    left join development.process p on p.id = sp.process_id
    left join development.process_detail pd on pd.id = p.process_detail_id