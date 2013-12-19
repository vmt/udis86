project(udcli)
cmake_minimum_required(VERSION 2.8)
add_executable(udcli udcli.c)
target_link_libraries(udcli libudis86)
