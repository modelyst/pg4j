select
    id as "dataPointID:ID(DataPoint)",
    magpie_features as "features",
    target as "target",
    'DataPoint' as ":LABEL"
from
    data_point