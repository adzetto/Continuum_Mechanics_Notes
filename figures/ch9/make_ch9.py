r"""make_ch9.py -- the Chapter 9 figures of the notes, in house style v3.

For every ch9*_body.tex in this folder it runs the geometry generator
ch9*_geom.py when there is one, writes the wrapper ch9*.tex (style:
figstyle9.tex, R10 page: 10 pt labels, at most 100 mm wide), runs pdflatex,
the checks of fscheck9.py (label clearance >= 1.5 pt, label pairs >= 1.5 pt,
no bare arrow tips, width), and pdftocairo for png/ch9*.png (preview) and
svg/ch9*.svg (outlined glyphs, for the web version of the notes).
Usage:
    python make_ch9.py [ch9a_frames ...] [--dpi 600] [--no-check]
The notes include the PDFs at scale 1.728 (17.28 pt body text).
Exit code 1 if a figure does not compile or fails a check.
"""
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, 'png')
SVG = os.path.join(HERE, 'svg')
WRAP = r"""\documentclass[10pt,tikz,border=1pt]{{standalone}}
\input{{figstyle9}}
\begin{{document}}
\input{{{name}_body}}
\end{{document}}
"""


def run(cmd):
    return subprocess.run(cmd, cwd=HERE, capture_output=True, text=True,
                          errors='ignore')


def build(name, dpi, check):
    tex = name + '.tex'
    with open(os.path.join(HERE, tex), 'w') as f:
        f.write(WRAP.format(name=name))
    run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex])
    log = open(os.path.join(HERE, name + '.log'), errors='ignore').read()
    err = re.findall(r'^!.*$', log, re.M)
    if err:
        print('  %s: ERROR %s' % (tex, err[:3]))
        return False
    ok = True
    if check:
        import fscheck9
        ok = fscheck9.check(os.path.join(HERE, name + '.pdf'), quiet=True,
                            verbose=True)
    os.makedirs(PNG, exist_ok=True)
    os.makedirs(SVG, exist_ok=True)
    run(['pdftocairo', '-png', '-r', str(dpi), '-singlefile', name + '.pdf',
         os.path.join(PNG, name)])
    run(['pdftocairo', '-svg', name + '.pdf', os.path.join(SVG, name + '.svg')])
    for ext in ('.aux', '.log'):
        f = os.path.join(HERE, name + ext)
        if os.path.exists(f):
            os.remove(f)
    print('  %s -> %s.pdf, png/%s.png, svg/%s.svg%s'
          % (tex, name, name, name, '' if ok else '   CHECK FAILED'))
    return ok


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dpi = 300
    if '--dpi' in sys.argv:
        dpi = int(sys.argv[sys.argv.index('--dpi') + 1])
        args = [a for a in args if a != str(dpi)]
    check = '--no-check' not in sys.argv
    names = args or sorted(f[:-9] for f in os.listdir(HERE)
                           if f.endswith('_body.tex'))
    allok = True
    for n in names:
        gen = os.path.join(HERE, n + '_geom.py')
        if os.path.exists(gen):
            r = run([sys.executable, '-B', gen])
            msg = (r.stdout.strip() or r.stderr.strip())
            if msg:
                print(msg)
            if r.returncode:
                print('  %s: geometry generator failed' % n)
                allok = False
                continue
        allok &= build(n, dpi, check)
    sys.exit(0 if allok else 1)
