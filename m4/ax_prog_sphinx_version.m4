# SYNOPSIS
#
#   AX_PROG_SPHINX_VERSION([VERSION],[ACTION-IF-TRUE],[ACTION-IF-FALSE])
#
# DESCRIPTION
#
#   Makes sure that sphinx-build supports the version indicated. If true 
#   the shell commands in ACTION-IF-TRUE are executed. If not the shell
#   commands in ACTION-IF-FALSE are run. Note if $SPHINX_BUILD is not set
#   (for example by running AX_WITH_PROG) the macro will fail.
#
#   Example:
#
#     AX_WITH_PROG(SPHINX_BUILD,sphinx-build)
#     AX_PROG_SPHINX([1.1.1],[ ... ],[ ... ])
#
# LICENSE
#
#   ax_prog_python_version.m4
#
#   Copyright (c) 2009 Francesco Salvestrini <salvestrini@users.sourceforge.net>
#
#   Copying and distribution of this file, with or without modification, are
#   permitted in any medium without royalty provided the copyright notice
#   and this notice are preserved. This file is offered as-is, without any
#   warranty.
#
#   ax_prog_sphinx_version.m4
#
#   Copyright (c) 2013 Vivek Thampi <vivekthampi@users.sourceforge.net>


AC_DEFUN([AX_PROG_SPHINX],[
    AC_REQUIRE([AC_PROG_SED])
    AC_REQUIRE([AC_PROG_GREP])


    AS_IF([test -n "$SPHINX_BUILD"],[
        ax_sphinx_version="$1"

        AC_MSG_CHECKING([for sphinx version])
        changequote(<<,>>)
        sphinx_version=`$SPHINX_BUILD -h 2>&1 | $GREP "^Sphinx v" | $SED -e 's/^.* v\([0-9]*\.[0-9]*\.[0-9]*\)/\1/'`
        changequote([,])
        AC_MSG_RESULT($sphinx_version)

        AC_SUBST([SPHINX_VERSION],[$sphinx_version])

        AX_COMPARE_VERSION([$ax_sphinx_version],[le],[$sphinx_version],[
        :
            $2
        ],[
        :
            $3
        ])
    ],[
        AC_MSG_WARN([could not find the sphinx documentation tool])
        $3
    ])
])
