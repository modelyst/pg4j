select
    id as ":START_ID(AcquiredPoint)",
    data_point_id as ":END_ID(DataPoint)",
    'DataPoint' as ":LABEL"
from
    acquired_point;