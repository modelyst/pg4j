#   Copyright 2021 Modelyst LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import re
from typing import Callable, List

# Text helpers

camel_regex = re.compile(r"(?<!^)(?=[A-Z])")


def snake_to_camel(string: str, first_capital: bool = False) -> str:
    first, *after = string.split("_")
    output = first.capitalize() if first_capital else first
    return output + "".join(map(lambda x: x.capitalize(), after))


def camel_to_snake(string: str) -> str:
    return camel_regex.sub("_", string)


FILTER_FUNC_TYPE = Callable[[str], bool]


def filters_to_filter_func(list_of_filters: List[str]) -> FILTER_FUNC_TYPE:
    # Compile filter func
    filter_func = lambda x: any(map(lambda pattern: re.findall(pattern, x), list_of_filters))
    return filter_func


# def parse_table(
#     table: Table,
#     exclude_filter_func: FILTER_FUNC_TYPE,
#     include_filter_func: FILTER_FUNC_TYPE,
# ) -> dict:
#     primary_keys = [key.name for key in table.primary_key]
#     if len(primary_keys) > 1:
#         raise NotImplementedError("Haven't dealt with composite keys yet")
#     basic_cols = [
#         col
#         for col in table.columns
#         if not col.primary_key
#         and not col.foreign_keys
#         and include_filter_func(col.name)
#         and not exclude_filter_func(col.name)
#     ]
#     foreign_keys = [
#         parse_foreign_key(list(col.foreign_keys)[0])
#         for col in table.columns
#         if col.foreign_keys
#     ]
#     mapping_table = len(foreign_keys) == 2
#     print(f"Table Name: {table.name}")
#     print(f"Foriegn Keys: {foreign_keys}")
#     print(f"Cols: {basic_cols}")
#     print(f"Mapping Table: {mapping_table}")
#     print("######")


# def parse_foreign_key(foreign_key: SAForeignKey) -> ForeignKey:
#     target_column = foreign_key.column
#     target_table = target_column.table
#     source_column = foreign_key.parent
#     source_table = source_column.table
#     fk = ForeignKey(
#         source_table.name, source_column.name, target_table.name, target_column.name
#     )
#     return fk
