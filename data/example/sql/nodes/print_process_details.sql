select
    ppd.id as "PrintProcessDetailID:ID(PrintProcessDetail)",
    'PrintProcessDetail' as ":LABEL",
    ppd.concentration_elements as "concentration_elements",
    ppd.concentration_values as "concentration_values",
    ppd.elements as "elements",
    ppd.map_id as "map_id",
    ppd.method as "method",
    ppd.printer_name as "printer_name",
    ppd.pvd_details as "pvd_details"
from
	development.print_process_detail ppd;