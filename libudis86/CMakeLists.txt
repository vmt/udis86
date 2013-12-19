project(libudis86)
cmake_minimum_required(VERSION 2.8)

set(FILES
	decode.c
	decode.h
	extern.h
	itab.c
	itab.h
	syn-att.c
	syn-intel.c
	syn.c
	syn.h
	types.h
	udint.h
	udis86.c)

add_library(libudis86 STATIC ${FILES})
