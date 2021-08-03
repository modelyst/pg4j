select
	apd.id as "AnnealProcessDetailID:ID(AnnealProcessDetail)",
	'AnnealProcessDetail' as ":LABEL",
    apd.furnace_name,
    apd.gas_string,
    apd.intended_element,
    apd.max_temperature,
    apd.pressure,
    apd.recipe_description,
    apd.recipe_name,
    apd.recipe_type,
    apd.soak_time
from
	development.anneal_process_detail apd;