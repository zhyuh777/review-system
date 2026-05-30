#!/usr/bin/env python3
"""Generate all 26 figures with correct textbook style"""
import os, subprocess

BASE = '/Users/zzzzed/opencodes/electest'
OUT_DIR = os.path.join(BASE, 'latex_figures')
os.makedirs(OUT_DIR, exist_ok=True)

def make(name, *bodies):
    """Generate a single LaTeX file with one or more circuitikz environments"""
    parts = []
    for i, body in enumerate(bodies):
        parts.append(
            "\\begin{circuitikz}[scale=1.2, transform shape]\n"
            + body +
            "\n\\end{circuitikz}"
        )
    tex = (
        "\\documentclass[border=12pt]{standalone}\n"
        "\\usepackage[siunitx, european]{circuitikz}\n"
        "\\usepackage{amsmath}\n"
        "\\begin{document}\n"
        + "\n\n\\vspace{0.8cm}\n\n".join(parts) +
        "\n\\end{document}"
    )
    tex_path = os.path.join(OUT_DIR, f"{name}.tex")
    with open(tex_path, 'w') as f:
        f.write(tex)
    pdf_path = os.path.join(OUT_DIR, f"{name}.pdf")
    subprocess.run(['xelatex', '-interaction=nonstopmode', '-output-directory', OUT_DIR, tex_path],
                   capture_output=True, text=True, timeout=60)
    if not os.path.exists(pdf_path):
        print(f"  [FAIL] {name}")
        return
    # Count errors
    log_path = os.path.join(OUT_DIR, f"{name}.log")
    errs = 0
    if os.path.exists(log_path):
        with open(log_path) as f:
            for l in f:
                if l.startswith("!"):
                    errs += 1
    png = os.path.join(BASE, "电工电子技术", "figures", f"图{name}.png")
    subprocess.run(['magick', '-density', '300', pdf_path, '-quality', '95', png],
                   capture_output=True, timeout=30)
    sz = os.path.getsize(png)//1024 if os.path.exists(png) else 0
    print(f"  [{'OK' if errs==0 else str(errs)+'e'}] 图{name}.png ({sz}KB)")

# ===== Chapter 1 =====
make("1-22", r"""
\draw (0,0) to[generic, l_=$U_1$] (0,3.5);
\draw (0,3.5) to[generic, l_=$U_2$] (5,3.5);
\draw (5,3.5) to[generic, l_=$U_3$] (5,0);
\draw (0,0) -- (5,0);
\draw[->,thick] (0.8,1.3) -- (0.8,2.5) node[midway,right] {$I_1$};
\draw[->,thick] (1.5,3.8) -- (3.5,3.8) node[midway,above] {$I_2$};
\draw[->,thick] (4.2,2.5) -- (4.2,1.3) node[midway,left] {$I_3$};
""")

make("1-23",
r"\draw (0,0) rectangle (2,2); \draw (1,1) node {N};"
r"\draw (2,1) to[battery1,l_=8V] (4,1);"
r"\draw[->,thick] (2.5,1.4) -- (3.5,1.4) node[midway,above] {2A};"
r"\draw (1,2.5) node[font=\small] {(a)};",
r"\draw (0,0) rectangle (2,2); \draw (1,1) node {N};"
r"\draw (2,1) to[battery1,l_=4V] (4,1);"
r"\draw[->,thick] (3.5,0.6) -- (2.5,0.6) node[midway,below] {3A};"
r"\draw (1,2.5) node[font=\small] {(b)};",
r"\draw (0,0) rectangle (2,2); \draw (1,1) node {N};"
r"\draw (2,1) to[I,l_=1A] (4,1);"
r"\draw[<->] (4.5,1.5) -- (4.5,0.5) node[midway,right] {5V};"
r"\draw (1,2.5) node[font=\small] {(c)};",
r"\draw (0,0) rectangle (2,2); \draw (1,1) node {N};"
r"\draw (2,1) to[I,l_=3A] (4,1);"
r"\draw[<->] (4.5,1.5) -- (4.5,0.5) node[midway,right] {6V};"
r"\draw (1,2.5) node[font=\small] {(d)};"
)

make("1-24",
r"\draw (0,0) to[battery1,l_=6V] (0,2.5);"
r"\draw (0,2.5) to[R,l_=2$\Omega$] (3,2.5);"
r"\draw (3,2.5) -- (3,0) -- (0,0);"
r"\draw[->,thick] (0.8,2.8) -- (2,2.8) node[midway,above] {$I$};"
r"\draw (0,-0.4) node {a} (3,-0.4) node {b};"
r"\draw[<->] (3.5,2.5) -- (3.5,0) node[midway,right] {8V};"
r"\draw (1,3.2) node[font=\small] {(a)};",
r"\draw (0,0) to[battery1,l_=$U_S$] (0,2.5);"
r"\draw (0,2.5) to[R,l_=2$\Omega$] (2.5,2.5);"
r"\draw (2.5,2.5) to[battery1,l_=5V] (2.5,0);"
r"\draw (2.5,0) -- (5,0);"
r"\draw (5,0) to[battery1,l_=2V] (5,2.5);"
r"\draw (5,2.5) to[R,l_=5$\Omega$] (7.5,2.5);"
r"\draw (7.5,2.5) -- (7.5,0) -- (5,0);"
r"\draw (7.5,0) -- (0,0);"
r"\draw (1.2,1.2) node[circle,draw,inner sep=1pt,fill=white] {a};"
r"\draw (6.2,1.2) node[circle,draw,inner sep=1pt,fill=white] {b};"
r"\draw[<->] (8,2.5) -- (8,0) node[midway,right] {8V};"
r"\draw (3,3.2) node[font=\small] {(b)};",
r"\draw (0,0) to[battery1,l_=3V] (0,2.5);"
r"\draw (0,2.5) to[R,l_=$R$] (3.5,2.5);"
r"\draw (3.5,2.5) -- (3.5,0) -- (0,0);"
r"\draw[<->] (4,2.5) -- (4,0) node[midway,right] {2V};"
r"\draw (0,-0.4) node {a} (3.5,-0.4) node {b};"
r"\draw (1,3.2) node[font=\small] {(c)};",
r"\draw (0,0) to[I,l_=1A] (0,2.5);"
r"\draw (0,2.5) to[battery1,l_=2V] (2.5,2.5);"
r"\draw (2.5,2.5) to[R,l_=$R$] (5,2.5);"
r"\draw (5,2.5) -- (5,0) -- (0,0);"
r"\draw[<->] (5.5,2.5) -- (5.5,0) node[midway,right] {5V};"
r"\draw (0,-0.4) node {a} (5,-0.4) node {b};"
r"\draw (2,3.2) node[font=\small] {(d)};"
)

make("1-25",
r"\draw (0,0) to[I,l_=1A] (0,2.5);"
r"\draw (0,2.5) -- (2.5,2.5);"
r"\draw (2.5,2.5) to[battery1,l_=2V] (2.5,0);"
r"\draw (2.5,0) -- (5,0);"
r"\draw (5,0) to[R,l_=2$\Omega$] (5,2.5);"
r"\draw (5,2.5) -- (0,2.5);"
r"\draw[->,thick] (2.5,2) -- (2.5,0.8) node[midway,left] {$I$};"
r"\draw (2.5,3.2) node[font=\small] {(a)};",
r"\draw (0,0) to[battery1,l_=1V] (0,2.5);"
r"\draw (0,2.5) to[I,l_=2A] (2.5,2.5);"
r"\draw (2.5,2.5) to[R,l_=1$\Omega$] (5,2.5);"
r"\draw (5,2.5) -- (5,0) -- (0,0);"
r"\draw[<->] (5.5,2.5) -- (5.5,0) node[midway,right] {$U$};"
r"\draw (2.5,3.2) node[font=\small] {(b)};"
)

make("1-26", r"""
\draw (0,0) -- (12,0);
\draw (0,0) to[battery1,l=$U_{S1}$] (0,3.5);
\draw (0,3.5) to[R,l=$R_1$] (3,3.5);
\draw (3,3.5) to[R,l=$R_2$] (6,3.5);
\draw (6,3.5) to[battery1,l_=$U_{S2}$] (6,3.5);
\draw (6,3.5) to[R,l=$R_5$] (9,3.5);
\draw (9,3.5) to[battery1,l=$U_{S3}$] (9,0);
\draw (3,3.5) to[R,l=$R_3$] (3,0);
\draw (6,3.5) to[R,l=$R_4$] (6,0);
\draw (3,0) to[battery1,l_=$U_{S4}$] (3,0);
\draw (3,1.8) to[R,l=$R_6$] (6,1.8);
\draw[->,thick] (0.8,1.5) -- (0.8,2.8) node[midway,right] {$I_1$};
\draw[->,thick] (1.5,3.8) -- (2.5,3.8) node[midway,above] {$I_2$};
\draw[->,thick] (3,2.8) -- (3,1) node[midway,left] {$I_3$};
\draw[->,thick] (6,2.8) -- (6,1) node[midway,right] {$I_4$};
\draw[->,thick] (4.5,2.1) -- (5.5,2.1) node[midway,above] {$I_5$};
\draw[->,thick] (7.5,3.8) -- (8.5,3.8) node[midway,above] {$I_6$};
""")

make("1-27", r"""
\draw (0,0) to[R,l=3$\Omega$] (0,3.5);
\draw (0,3.5) -- (0,4.5) to[battery1,l=6V] (3,4.5);
\draw (3,4.5) to[R,l=6$\Omega$] (3,1);
\draw (3,1) -- (0,1) -- (0,0);
\draw (5.5,0) to[I,l=2A] (5.5,3.5);
\draw (5.5,3.5) to[R,l=7$\Omega$] (5.5,0);
\draw (5.5,0) -- (0,0);
\draw (5.5,3.5) -- (8,3.5);
\draw (8,3.5) -- (8,1.5) node[ocirc]{};
\draw (0,3.5) -- (-1,3.5) -- (-1,1.5) node[ocirc]{};
\draw[<->] (-1,2.5) -- (8,2.5) node[midway,above] {$U$};
\draw (2.8,0) to[battery1,l_=5V] (2.8,0);
""")

make("1-28", r"""
\draw (0,0) to[battery1,l=$U_{S1}$] (0,3.5);
\draw (0,3.5) -- (2,3.5) node[circle,draw,inner sep=1pt,fill=white] {} node[above] {c};
\draw (2,3.5) to[R,l=$R_1$] (4.5,3.5) node[circle,draw,inner sep=1pt,fill=white] {} node[above] {a};
\draw (4.5,3.5) to[R,l=$R_2$] (7,3.5) node[circle,draw,inner sep=1pt,fill=white] {} node[above] {d};
\draw (7,3.5) to[battery1,l=$U_{S2}$] (7,0);
\draw (4.5,3.5) to[R,l=$R_3$] (4.5,0) node[circle,draw,inner sep=1pt,fill=white] {} node[below] {b};
\draw (0,0) -- (7,0);
\draw[->,thick] (1,3.8) -- (2.5,3.8) node[midway,above] {$I_1$};
\draw[->,thick] (5.5,3.8) -- (6.5,3.8) node[midway,above] {$I_2$};
\draw[->,thick] (4.5,2.8) -- (4.5,1) node[midway,left] {$I_3$};
""")

make("1-29", r"""
\draw (0,0) to[battery1,l=$U_S$] (0,3.5);
\draw (0,3.5) to[R,l=$R_0$] (3,3.5);
\draw (3,3.5) to[R,l=$R_2$] (3,0);
\draw (3,3.5) -- (5,3.5);
\draw (5,3.5) to[R,l=$R_1$] (5,0);
\draw (0,0) -- (5,0);
\draw (3,3.5) -- (4,3.5) -- (4,2.2);
\draw (4,1.2) circle (0.4) node {P};
\draw (4,1.6) -- (4,0);
\draw (3,1.8) -- (5,1.8) -- (6.5,1.8);
\draw (6.5,1.8) to[battery1,l=$U_x$] (6.5,0);
\draw (6.5,0) -- (0,0);
\draw (4,2.2) -- (4.5,2.2) -- (4.5,1.8);
""")

print("\n章1完成")
