select
    xpd.id as "XTRNProcessDetailID:ID(XTRNProcessDetail)",
    'XTRNProcessDetail' as ":LABEL",
    xpd.scan_step_y as "scan_step_y",
    xpd.calibration_n_points as "calibration_n_points",
    xpd.scan_step_y_num as "scan_step_y_num",
    xpd.calibration_element as "calibration_element",
    xpd.parameters as "parameters",
    xpd.beam_line as "beam_line",
    xpd.scan_step_x_num as "scan_step_x_num",
    xpd.center_cryovert as "center_cryovert",
    xpd.center_cryohor as "center_cryohor",
    xpd.calibration_id as "calibration_id",
    xpd.calibration_end_energy as "calibration_end_energy",
    xpd.rcp_version as "rcp_version",
    xpd.scan_step_x as "scan_step_x",
    xpd.scan_time as "scan_time",
    xpd.calibration_edge as "calibration_edge",
    xpd.calibration_start_energy as "calibration_start_energy"
from
	development.xtrn_process_detail xpd;
