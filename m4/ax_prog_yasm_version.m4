# SYNOPSIS
#
#   AX_PROG_YASM_VERSION([VERSION],[ACTION-IF-TRUE],[ACTION-IF-FALSE])
#
# DESCRIPTION
#
#   Makes sure that yasm supports the version indicated. If true 
#   the shell commands in ACTION-IF-TRUE are executed. If not the shell
#   commands in ACTION-IF-FALSE are run. Note if $YASM is not set
#   (for example by running AX_WITH_PROG) the macro will fail.
#
#   Example:
#
#     AX_WITH_PROG(YASM,yasm)
#     AX_PROG_YASM_VERSION([1.1.1],[ ... ],[ ... ])
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
#   ax_prog_yasm_version.m4
#
#   Copyright (c) 2013 Vivek Thampi <vivekthampi@users.sourceforge.net>


AC_DEFUN([AX_PROG_YASM_VERSION],[
    AC_REQUIRE([AC_PROG_SED])
    AC_REQUIRE([AC_PROG_GREP])


    AS_IF([test -n "$YASM"],[
        ax_yasm_version="$1"

        AC_MSG_CHECKING([for yasm version])
        changequote(<<,>>)
        yasm_version=`$YASM --version 2>&1 | $GREP "^yasm " | $SED -e 's/^.* \([0-9]*\.[0-9]*\.[0-9]*\)/\1/'`
        changequote([,])
        AC_MSG_RESULT($yasm_version)

        AC_SUBST([YASM_VERSION],[$yasm_version])

        AX_COMPARE_VERSION([$ax_yasm_version],[le],[$yasm_version],[
        :
            $2
        ],[
        :
            $3
        ])
    ],[
        AC_MSG_WARN([could not find the yasm])
        $3
    ])
])
