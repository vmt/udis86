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
    bld(rule = 'python ${SRC[0].abspath()} ${SRC[2].abspath()} .',
        source = [
            'scripts/ud_itab.py',
            'scripts/ud_opcode.py',
            'docs/x86/optable.xml'
        ],
        target = ['itab.c',  'itab.h'])
    win32 = bld.env.DEST_OS == 'win32'
    libname = 'libudis86' if win32 else 'udis86'
    bld.shlib(
        target = libname,
        source = ['itab.c'] + bld.path.ant_glob('libudis86/*.c'),
        includes = 'libudis86',
        defines = ['_USRDLL', 'LIBUDIS86_EXPORTS']
    )
    bld.program(
        target = 'udcli',
        source = 'udcli/udcli.c',
        use = libname
    )
