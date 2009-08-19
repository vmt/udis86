#
# udis86 autoconf
#
AC_PREREQ(2.59)
AC_INIT([udis86], [pre-1.8], [vivek@sig9.com])
AC_CONFIG_HEADERS(config.h)
AC_CONFIG_AUX_DIR(build)
AC_CONFIG_MACRO_DIR([m4])

# Make sure $ACLOCAL_FLAGS are used during a rebuild.
AC_SUBST([ACLOCAL_AMFLAGS], ["-I $ac_macro_dir \${ACLOCAL_FLAGS}"])

#
# Determine the build host; we notify automake of Windows 
# builds, so it can pass proper parameters for building 
# DLLs to the linker.
#
AC_CANONICAL_HOST

case "$host_os" in
	mingw32* )
		TARGET_OS=windows
		AC_LIBTOOL_WIN32_DLL
		;;
esac

# Initialize the automake subsystem.
AM_INIT_AUTOMAKE([-Wall -Werror foreign])

#
# In case we have a Windows build, we pass a 
# TARGET_WINDOWS conditional to automake.
#
AM_CONDITIONAL(TARGET_WINDOWS, test "$TARGET_OS" = windows)

AC_PROG_CC
AC_DISABLE_SHARED
AC_PROG_LIBTOOL
AC_ENABLE_SHARED
AM_PROG_CC_C_O

# If this is a gnu compiler, pass -Wall
if test "$ac_cv_c_compiler_gnu" = "yes"; then
	CFLAGS="$CFLAGS -Wall"
fi

# Look for python
AX_WITH_PYTHON
if test "x$PYTHON" = "x"; then
    AC_MSG_ERROR( [Python not found. Use --with-python to specify path to python binary] )
fi

# Yasm for testing
AX_WITH_PROG(YASM,yasm)

AC_CHECK_HEADERS([assert.h])

AC_CONFIG_FILES([
    Makefile
    scripts/Makefile
    libudis86/Makefile
    udcli/Makefile
    tests/Makefile
    docs/Makefile
    docs/manual/Makefile
    docs/x86/Makefile
])

AC_OUTPUT
