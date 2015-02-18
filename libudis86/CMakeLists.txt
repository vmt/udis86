cmake_minimum_required (VERSION 2.8)

project (udis86)

set (ITAB_H "${CMAKE_CURRENT_LIST_DIR}/itab.h")
set (ITAB_C "${CMAKE_CURRENT_LIST_DIR}/itab.c")

if(NOT EXISTS ${ITAB_H} OR NOT EXISTS ${ITAB_C} )
  message(FATAL_ERROR "You must generate files: ${ITAB_H}, ${ITAB_C} before you start.")
endif()

set (udis86_srcs
    decode.c
    itab.c
    syn.c
    syn-att.c
    syn-intel.c
    udis86.c
)

set (udis86_hdrs
    ../udis86.h
    decode.h
    itab.h
    extern.h
    syn.h
    types.h
    udint.h
)

add_library (libudis86 STATIC ${udis86_srcs} ${udis86_hdrs})
