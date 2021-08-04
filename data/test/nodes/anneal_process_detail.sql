SELECT development.anneal_process_detail.id AS "annealProcessDetail:ID(AnnealProcessDetail)", 'AnnealProcessDetail' AS ":LABEL", development.anneal_process_detail.deleted AS deleted, development.anneal_process_detail.furnace_name AS furnace_name, development.anneal_process_detail.gas_string AS gas_string, development.anneal_process_detail.intended_element AS intended_element, development.anneal_process_detail.max_temperature AS max_temperature, development.anneal_process_detail.pressure AS pressure, development.anneal_process_detail.recipe_description AS recipe_description, development.anneal_process_detail.recipe_name AS recipe_name, development.anneal_process_detail.recipe_type AS recipe_type, development.anneal_process_detail.soak_time AS soak_time 
FROM development.anneal_process_detail