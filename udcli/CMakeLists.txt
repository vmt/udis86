cmake_minimum_required (VERSION 2.8)

project (udcli)

set (udcli_srcs
    udcli.c
)

add_executable (udcli ${udcli_srcs} )
target_link_libraries (udcli ${LIBUDIS_LIB})
