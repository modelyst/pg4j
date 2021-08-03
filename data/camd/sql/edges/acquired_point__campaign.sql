select
    id as ":START_ID(AcquiredPoint)",
    campaign_id as ":END_ID(Campaign)",
    'Campaign' as ":LABEL"
from
    acquired_point;