r"""make.py -- build the figures of one chapter of the notes in house style v3.

    python figures/common/make.py ch10 [ch10a_name ...] [--dpi 600] [--no-check]

The first argument names a folder of figures/ (or is a path to one). For
every <name>_body.tex in that folder, or only for the names given, it runs
the geometry generator <name>_geom.py when there is one, writes the wrapper
<name>.tex (style: ../common/figstyle.tex; R10 page: 10 pt labels, at most
100 mm wide), runs pdflatex, the checks of fscheck.py (label clearance
>= 1.5 pt, label pairs >= 1.5 pt, no bare arrow tips, width), and
pdftocairo for png/<name>.png (preview) and svg/<name>.svg (outlined
glyphs, for the web version of the notes).
The notes include the PDFs at scale 1.728 (17.28 pt body text).
Exit code 1 if a figure does not compile or fails a check.
"""
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
COMMON = os.path.dirname(os.path.abspath(__file__))
FIGURES = os.path.dirname(COMMON)
sys.path.insert(0, COMMON)
WRAP = r"""\documentclass[10pt,tikz,border=1pt]{{standalone}}
\input{{../common/figstyle}}
\begin{{document}}
\input{{{name}_body}}
\end{{document}}
"""


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          errors='ignore')


def build(folder, name, dpi, check):
    tex = name + '.tex'
    with open(os.path.join(folder, tex), 'w') as f:
        f.write(WRAP.format(name=name))
    run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex],
        folder)
    log = open(os.path.join(folder, name + '.log'), errors='ignore').read()
    err = re.findall(r'^!.*$', log, re.M)
    if err:
        print('  %s: ERROR %s' % (tex, err[:3]))
        return False
    ok = True
    if check:
        import fscheck
        ok = fscheck.check(os.path.join(folder, name + '.pdf'), quiet=True,
                           verbose=True)
    png = os.path.join(folder, 'png')
    svg = os.path.join(folder, 'svg')
    os.makedirs(png, exist_ok=True)
    os.makedirs(svg, exist_ok=True)
    run(['pdftocairo', '-png', '-r', str(dpi), '-singlefile', name + '.pdf',
         os.path.join(png, name)], folder)
    run(['pdftocairo', '-svg', name + '.pdf',
         os.path.join(svg, name + '.svg')], folder)
    for ext in ('.aux', '.log'):
        f = os.path.join(folder, name + ext)
        if os.path.exists(f):
            os.remove(f)
    print('  %s -> %s.pdf, png/%s.png, svg/%s.svg%s'
          % (tex, name, name, name, '' if ok else '   CHECK FAILED'))
    return ok


def main(argv):
    dpi = 300
    if '--dpi' in argv:
        i = argv.index('--dpi')
        dpi = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    check = '--no-check' not in argv
    args = [a for a in argv if not a.startswith('--')]
    if not args:
        print(__doc__)
        return 2
    folder = args[0]
    if not os.path.isdir(folder):
        folder = os.path.join(FIGURES, folder)
    folder = os.path.abspath(folder)
    names = args[1:] or sorted(f[:-9] for f in os.listdir(folder)
                               if f.endswith('_body.tex'))
    allok = True
    for n in names:
        gen = os.path.join(folder, n + '_geom.py')
        if os.path.exists(gen):
            r = run([sys.executable, '-B', gen], folder)
            msg = (r.stdout.strip() or r.stderr.strip())
            if msg:
                print(msg)
            if r.returncode:
                print('  %s: geometry generator failed' % n)
                allok = False
                continue
        allok &= build(folder, n, dpi, check)
    return 0 if allok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
