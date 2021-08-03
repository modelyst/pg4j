select
	upd.id as "UvisProcessDetailID:ID(UvisProcessDetail)",
	'UvisProcessDetail' as ":LABEL",
    upd.exposure_requested,
    upd.exposure_time,
    upd.flying_scan,
    upd.lamp_gt_1hr,
    upd.light_power_level,
    upd.rcp_version,
    upd.reflectance_ref_pos_x,
    upd.reflectance_ref_pos_y,
    upd.reflectance_ref_pos_z,
    upd.row_spacing,
    upd.sample_half_width,
    upd.tref_mode
from
	development.uvis_process_detail upd;