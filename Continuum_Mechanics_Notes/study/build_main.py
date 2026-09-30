import io, re, os

D = r'C:\Users\lenovo\Desktop\A'
FILES = ['continuum_ch1', 'continuum_ch2', 'continuum_ch3']


def rd(f):
    return io.open(os.path.join(D, f + '.tex'), encoding='utf-8').read()


def wr(name, txt):
    io.open(os.path.join(D, name), 'w', encoding='utf-8').write(txt)


appendix_txt = ''
for n, f in enumerate(FILES, 1):
    s = rd(f)
    a = s.find(r'\end{titlepage}') + len(r'\end{titlepage}')
    b = s.rfind(r'\end{document}')
    body = s[a:b]

    body = body.replace(r'\tableofcontents', '')
    body = re.sub(r'\\setcounter\{chapter\}\{\d+\}', '', body)

    # ---- make the two colliding labels unique BEFORE splitting -------
    for L in ['sec:problems', 'app:dict']:
        body = body.replace('{%s}' % L, '{%s:c%d}' % (L, n))

    # ---- pull an appendix out, if any -------------------------------
    ai = body.find('\\appendix')
    if ai >= 0:
        app = body[ai:].replace('\\appendix', '', 1)
        # both chapters ship an appendix of the same name; distinguish them
        app = app.replace('\\chapter{Dictionary to the book}',
                          '\\chapter{Dictionary to the book: '
                          'Chapter %d notation}' % n)
        appendix_txt += '\n' + app
        body = body[:ai]

    # ---- ch3 opens with \chapter*{}: make it a real chapter ---------
    if f == 'continuum_ch3':
        body = body.replace('\\chapter*{}\n\\setcounter{section}{0}', '')
        body = body.replace('\\chapter*{}', '')
        body = re.sub(r'\\setcounter\{section\}\{0\}', '', body)
        body = ('\n\\chapter{Further Preliminaries, with Applications to '
                'the Analysis of Deformation}\n' + body)

    # ---- reset the Problem counter in each chapter ------------------
    body = body.replace('\\section{Problems}',
                        '\\setcounter{problemenv}{0}\n\\section{Problems}')

    # ---- ch2 problems are \paragraph*{...}: give them ToC entries ----
    if f == 'continuum_ch2':
        TAG = '\\paragraph*{Problem '
        out, pos = [], 0
        while True:
            i = body.find(TAG, pos)
            if i < 0:
                out.append(body[pos:])
                break
            out.append(body[pos:i])
            # scan for the brace matching the one that opens the title
            j = i + len('\\paragraph*')          # points at '{'
            depth, k = 0, j
            while k < len(body):
                if body[k] == '{':
                    depth += 1
                elif body[k] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            full = body[j + 1:k]                  # the whole title
            num = re.match(r'(Problem [0-9]+(?:\([a-z]\))?)', full)
            short = num.group(1) if num else 'Problem'
            out.append('\\addcontentsline{toc}{subsection}{'
                       '\\texorpdfstring{' + full + '}{' + short + '}}%\n')
            out.append(body[i:k + 1])
            pos = k + 1
        body = ''.join(out)

    wr('body_ch%d.tex' % n, body)
    print('body_ch%d.tex  %7d chars' % (n, len(body)))

wr('body_appendix.tex', appendix_txt)
print('body_appendix.tex %7d chars' % len(appendix_txt))
