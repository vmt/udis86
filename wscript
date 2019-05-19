# Build instructions
# ------------------
#
# Build your Windows DLL:
#
#   python waf.py configure build
#
# Change arch:
#
#   python waf.py --msvc_targets=x86 configure ..
#
def options(ctx):
    ctx.load('compiler_c')

def configure(ctx):
    ctx.load('compiler_c')

def build(bld):
    bld(rule = 'python ${SRC[0].abspath()} ${SRC[2].abspath()} libudis86',
        source = [
            'scripts/ud_itab.py',
            'scripts/ud_opcode.py',
            'docs/x86/optable.xml'
        ],
        target = ['libudis86/itab.c',  'libudis86/itab.h'])
    win32 = bld.env.DEST_OS == 'win32'
    libname = 'libudis86' if win32 else 'udis86'
    src = ['libudis86/itab.c'] + bld.path.ant_glob('libudis86/*.c')
    bld.shlib(
        target = libname,
        source = src,
        includes = ['libudis86'],
        defines = ['_USRDLL', 'LIBUDIS86_EXPORTS']
    )
    bld.program(
        target = 'udcli/udcli',
        source = 'udcli/udcli.c',
        includes = ['libudis86', '.'],
        use = libname
    )
