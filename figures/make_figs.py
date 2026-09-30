r"""make_figs.py -- standalone PDFs (here) and PNG previews (../png) of the course figures.

For every figNN_body.tex in this folder it writes the wrapper figNN.tex
(style: style/v3/figstyle.tex), then runs pdflatex, the automatic checks of style/v3/fscheck.py (label
clearance >= 1.5 pt, label pairs >= 1.5 pt, no bare arrowheads) and
pdftocairo (-r DPI).  Usage:
    python make_figs.py [fig01 fig05 ...] [--dpi 600] [--no-check]
Geometry generators (fig01_geom.py) are run first when present.
Exit code 1 if a figure does not compile or fails a check.
"""
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True                        # no __pycache__ in style/v3
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = os.path.normpath(os.path.join(HERE, '..', 'style', 'v3'))
PNG = os.path.normpath(os.path.join(HERE, '..', 'png'))
sys.path.insert(0, STYLE)
WRAP = r"""\documentclass[10pt,tikz,border=1pt]{{standalone}}
\def\FigStyleDir{{../style/v3/}}
\def\FigDir{{}}
\input{{\FigStyleDir figstyle}}
\begin{{document}}
\input{{{name}_body}}
\end{{document}}
"""


def run(cmd):
    return subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, errors='ignore')


def build(name, dpi, check):
    tex = '%s.tex' % name
    open(os.path.join(HERE, tex), 'w').write(WRAP.format(name=name))
    run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex])
    log = open(os.path.join(HERE, tex[:-4] + '.log'), errors='ignore').read()
    err = re.findall(r'^!.*$', log, re.M)
    if err:
        print('  %s: ERROR %s' % (tex, err[:3]))
        return False
    ok = True
    if check:
        import fscheck
        ok = fscheck.check(os.path.join(HERE, tex[:-4] + '.pdf'), quiet=True)
    run(['pdftocairo', '-png', '-r', str(dpi), '-singlefile', tex[:-4] + '.pdf', os.path.join(PNG, tex[:-4])])
    for ext in ('.aux', '.log'):                     # keep the folder clean (log only on error)
        f = os.path.join(HERE, tex[:-4] + ext)
        if os.path.exists(f):
            os.remove(f)
    print('  %s -> %s.pdf, ../png/%s.png%s' % (tex, tex[:-4], tex[:-4], '' if ok else '   CHECK FAILED'))
    return ok


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dpi = 300
    if '--dpi' in sys.argv:
        dpi = int(sys.argv[sys.argv.index('--dpi') + 1])
        args = [a for a in args if a != str(dpi)]
    check = '--no-check' not in sys.argv
    names = args or sorted(f[:-9] for f in os.listdir(HERE) if f.endswith('_body.tex'))
    allok = True
    for n in names:
        gen = os.path.join(HERE, n + '_geom.py')
        if os.path.exists(gen):
            r = run([sys.executable, '-B', gen])
            print(r.stdout.strip() or r.stderr.strip())
        allok &= build(n, dpi, check)
    sys.exit(0 if allok else 1)
