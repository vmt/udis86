# ===========================================================================
#         http://www.nongnu.org/autoconf-archive/ax_with_python.html
# ===========================================================================
#
# SYNOPSIS
#
#   AX_WITH_PYTHON([VALUE-IF-NOT-FOUND],[PATH])
#
# DESCRIPTION
#
#   Locates an installed Python binary, placing the result in the precious
#   variable $PYTHON. Accepts a present $PYTHON, then --with-python, and
#   failing that searches for python in the given path (which defaults to
#   the system path). If python is found, $PYTHON is set to the full path of
#   the binary; if it is not found $PYTHON is set to VALUE-IF-NOT-FOUND if
#   provided, unchanged otherwise.
#
#   A typical use could be the following one:
#
#         AX_WITH_PYTHON
#
# LICENSE
#
#   Copyright (c) 2008 Francesco Salvestrini <salvestrini@users.sourceforge.net>
#
#   Copying and distribution of this file, with or without modification, are
#   permitted in any medium without royalty provided the copyright notice
#   and this notice are preserved.

AC_DEFUN([AX_WITH_PYTHON],[
    AX_WITH_PROG(PYTHON,python,$1,$2)
])
