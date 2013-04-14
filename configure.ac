#
# udis86 autoconf
#
AC_PREREQ(2.60)
AC_INIT([udis86], [1.7.2], [vivek.mt@gmail.com])
AC_CONFIG_HEADERS(config.h)
AC_CONFIG_AUX_DIR(build)
AC_CONFIG_MACRO_DIR([build/m4])

m4_include([m4/ax_compare_version.m4])
m4_include([m4/ax_prog_sphinx_version.m4])
m4_include([m4/ax_prog_yasm_version.m4])
m4_include([m4/ax_with_prog.m4])
m4_include([m4/ax_with_python.m4])

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
AM_INIT_AUTOMAKE([1.11 -Wall -Wno-portability -Wno-extra-portability -Werror foreign])
AM_SILENT_RULES([yes])

#
# In case we have a Windows build, we pass a 
# TARGET_WINDOWS conditional to automake.
#
AM_CONDITIONAL(TARGET_WINDOWS, test "$TARGET_OS" = windows)

AC_PROG_CC
AC_DISABLE_STATIC
AC_PROG_LIBTOOL
AM_PROG_CC_C_O

# If this is a gnu compiler, pass -Wall
if test "$ac_cv_c_compiler_gnu" = "yes"; then
	CFLAGS="$CFLAGS -Wall"
fi

# Look for python
AX_WITH_PYTHON
if test "x$PYTHON" = "x"; then
	AC_MSG_ERROR([Python not found. Use --with-python to specify path to python binary])
fi

# Yasm (>= 1.2.0)  for testing
AX_WITH_PROG(YASM,yasm)
AX_PROG_YASM_VERSION([1.2.0],[ac_have_yasm_version=1],[])
AM_CONDITIONAL(HAVE_YASM, [test -n "$ac_have_yasm_version"])

# Sphinx (>= 1.1.3) for documentation
AX_WITH_PROG(SPHINX_BUILD,sphinx-build)
AX_PROG_SPHINX([1.1.3],[ac_have_sphinx_version=1],[])
AM_CONDITIONAL(HAVE_SPHINX_DOC, [test -n "$ac_have_sphinx_version"])

AC_CHECK_HEADERS([assert.h stdio.h])

AC_CONFIG_FILES([
	Makefile
	scripts/Makefile
	libudis86/Makefile
	udcli/Makefile
	tests/Makefile
	docs/Makefile
	docs/manual/Makefile
	docs/x86/Makefile
	tests/difftest.sh
])

AC_OUTPUT
