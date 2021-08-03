select
    xpd.id as "XRFSProcessDetailID:ID(XRFSProcessDetail)",
    'XRFSProcessDetail' as ":LABEL",
    xpd.rcp_version as rcp_version,
    xpd.tube_current as tube_current,
    xpd.spot_size as spot_size,
    xpd.no_of_elements as no_of_elements,
    xpd.amp_time as amp_time,
    xpd.channel_range_min as channel_range_min,
    xpd.plate_elements as plate_elements,
    xpd.comment as comment,
    xpd.elements as elements,
    xpd.preset as preset,
    xpd.quant_method as quant_method,
    xpd.prefix as prefix,
    xpd.chamber_atmosphere as chamber_atmosphere,
    xpd.channel_range_max as channel_range_max,
    xpd.tube_voltage as tube_voltage
from
	development.xrfs_process_detail xpd;
