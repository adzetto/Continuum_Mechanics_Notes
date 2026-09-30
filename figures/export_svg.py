"""export_svg.py -- Inkscape-ready SVG of every figure and every captioned figure.

Formulas keep their exact LaTeX (Computer Modern) shapes: pdftocairo writes every
glyph as a vector outline, so nothing is re-typeset by Inkscape. Output:
  ../export/svg/figNN.svg                  figure only
  ../export/svg/figNN_captioned.svg        figure with caption
Usage: python export_svg.py   (run after make_figs.py and gallery/split.py)
"""
import glob
import os
import subprocess

H = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(H, '..', 'export')
OUT = os.path.join(EXP, 'svg')
os.makedirs(OUT, exist_ok=True)
for pdf in sorted(glob.glob(os.path.join(EXP, 'figures', 'fig*.pdf')) +
                  glob.glob(os.path.join(EXP, 'gallery_figs', 'fig*_captioned.pdf'))):
    svg = os.path.join(OUT, os.path.basename(pdf)[:-4] + '.svg')
    subprocess.run(['pdftocairo', '-svg', pdf, svg], check=True)
    print(os.path.basename(svg))
