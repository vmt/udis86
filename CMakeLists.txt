cmake_minimum_required (VERSION 2.8)
project (udis86)

# modules:
set (M_LIBUDIS "libudis86")
set (M_UDCLI "udcli")

# modules paths:
set (LIBUDIS_DIR "${CMAKE_SOURCE_DIR}/${M_LIBUDIS}" CACHE PATH "libudis86 main path")
set (UDCLI_DIR "${CMAKE_SOURCE_DIR}/${M_UDCLI}" CACHE PATH "udcli main path")

# Add sub-directories
#
# libs
add_subdirectory (libudis86)
get_property (libudis86_location TARGET libudis86 PROPERTY LOCATION)
set (LIBUDIS_LIB ${libudis86_location} CACHE FILE "libudis86 library path")

# executables
add_subdirectory(udcli)

# dependencies
add_dependencies(udcli libudis86)
