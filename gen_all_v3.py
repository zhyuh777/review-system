#!/usr/bin/env python3
"""Generate all 26 figures following the prompt document exactly"""
import os, subprocess

BASE = '/Users/zzzzed/opencodes/electest'
OUT = os.path.join(BASE, 'latex_figures')
FIG = os.path.join(BASE, '电工电子技术', 'figures')
os.makedirs(OUT, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

H = "\\documentclass[border=12pt]{standalone}\n\\usepackage[siunitx, european]{circuitikz}\n\\usepackage{amsmath}\n\\begin{document}\n"
F = "\n\\end{document}"

def fig(name, *bodies):
    tex = H
    for i, b in enumerate(bodies):
        if i > 0: tex += "\n\n\\vspace{0.8cm}\n\n"
        tex += "\\begin{circuitikz}[scale=1.2, transform shape]\n" + b + "\n\\end{circuitikz}"
    tex += F
    tex_path = os.path.join(OUT, name + ".tex")
    with open(tex_path, 'w') as f:
        f.write(tex)
    subprocess.run(['xelatex', '-interaction=nonstopmode', '-output-directory', OUT, tex_path],
                   capture_output=True, timeout=60)
    pdf = os.path.join(OUT, name + ".pdf")
    png = os.path.join(FIG, f"图{name}.png")
    if os.path.exists(pdf):
        subprocess.run(['magick', '-density', '300', pdf, '-quality', '95', png],
                       capture_output=True, timeout=30)
    log = os.path.join(OUT, name + ".log")
    errs = sum(1 for l in open(log) if l.startswith("!")) if os.path.exists(log) else -1
    sz = os.path.getsize(png)//1024 if os.path.exists(png) else 0
    print(f"  [{'OK' if errs==0 else str(errs)+'e'}] 图{name}.png ({sz}KB)")

# ======== Chapter 1 ========
fig("1-22", r"""
\draw (0,0) to[generic, v^=$U_1$] (0,3.5);
\draw (0,3.5) to[generic, v^=$U_2$] (5,3.5);
\draw (5,3.5) to[generic, v^=$U_3$] (5,0);
\draw (0,0) -- (5,0);
\draw[->,thick] (0.8,1.3) -- (0.8,2.5) node[midway,right] {$I_1$};
\draw[->,thick] (1.5,3.8) -- (3.5,3.8) node[midway,above] {$I_2$};
\draw[->,thick] (4.2,2.5) -- (4.2,1.3) node[midway,left] {$I_3$};
""")

fig("1-23",
r"\draw (0,0) rectangle (2,2); \draw (1,1) node {N};"
r"\draw (2,1) to[V, l_=8V] (4,1); \draw (4,1) -- (4.5,1);"
r"\draw (0,1) -- (-0.5,1);"
r"\draw[->,thick] (2.5,1.4) -- (3.5,1.4) node[midway,above] {2A};"
r"\draw (1,2.5) node[font=\small] {(a)};",
r"\draw (0,0) rectangle (2,2); \draw (1,1) node {N};"
r"\draw (2,1) to[V, l_=4V] (4,1); \draw (4,1) -- (4.5,1);"
r"\draw (0,1) -- (-0.5,1);"
r"\draw[->,thick] (3.5,0.6) -- (2.5,0.6) node[midway,below] {3A};"
r"\draw (1,2.5) node[font=\small] {(b)};",
r"\draw (0,0) rectangle (2,2); \draw (1,1) node {N};"
r"\draw (2,1) to[I, l_=1A] (4,1); \draw (4,1) -- (4.5,1);"
r"\draw (0,1) -- (-0.5,1);"
r"\draw[<->] (4.5,1.5) -- (4.5,0.5) node[midway,right] {5V};"
r"\draw (1,2.5) node[font=\small] {(c)};",
r"\draw (0,0) rectangle (2,2); \draw (1,1) node {N};"
r"\draw (2,1) to[I, l_=3A] (4,1); \draw (4,1) -- (4.5,1);"
r"\draw (0,1) -- (-0.5,1);"
r"\draw[<->] (4.5,1.5) -- (4.5,0.5) node[midway,right] {6V};"
r"\draw (1,2.5) node[font=\small] {(d)};"
)

fig("1-24",
r"\draw (0,0) to[V, l_=6V] (0,2.5);"
r"\draw (0,2.5) to[R, l_=2$\Omega$] (3,2.5);"
r"\draw (3,2.5) -- (3,0) -- (0,0);"
r"\draw[->,thick] (1,2.8) -- (2,2.8) node[midway,above] {$I$};"
r"\draw (0,-0.4) node {a} (3,-0.4) node {b};"
r"\draw[<->] (3.5,2.5) -- (3.5,0) node[midway,right] {8V};"
r"\draw (1.5,3.2) node[font=\small] {(a)};",
r"\draw (0,0) to[V, l_=$U_S$] (0,2.5);"
r"\draw (0,2.5) to[R, l_=2$\Omega$] (2.5,2.5);"
r"\draw (2.5,2.5) to[V, l_=5V] (2.5,0);"
r"\draw (2.5,0) -- (5,0) to[V, l_=2V] (5,2.5);"
r"\draw (5,2.5) to[R, l_=5$\Omega$] (7.5,2.5);"
r"\draw (7.5,2.5) -- (7.5,0) -- (0,0);"
r"\draw (1.2,1.2) node[circle,draw,inner sep=1pt,fill=white] {a};"
r"\draw (6.2,1.2) node[circle,draw,inner sep=1pt,fill=white] {b};"
r"\draw[<->] (8,2.5) -- (8,0) node[midway,right] {8V};"
r"\draw (3.5,3.2) node[font=\small] {(b)};",
r"\draw (0,0) to[V, l_=3V] (0,2.5);"
r"\draw (0,2.5) to[R, l_=$R$] (3.5,2.5);"
r"\draw (3.5,2.5) -- (3.5,0) -- (0,0);"
r"\draw[<->] (4,2.5) -- (4,0) node[midway,right] {2V};"
r"\draw (0,-0.4) node {a} (3.5,-0.4) node {b};"
r"\draw (1.5,3.2) node[font=\small] {(c)};",
r"\draw (0,0) to[I, l_=1A] (0,2.5);"
r"\draw (0,2.5) to[V, l_=2V] (2.5,2.5);"
r"\draw (2.5,2.5) to[R, l_=$R$] (5,2.5);"
r"\draw (5,2.5) -- (5,0) -- (0,0);"
r"\draw[<->] (5.5,2.5) -- (5.5,0) node[midway,right] {5V};"
r"\draw (0,-0.4) node {a} (5,-0.4) node {b};"
r"\draw (2.5,3.2) node[font=\small] {(d)};"
)

fig("1-25",
r"\draw (0,0) to[I, l_=1A] (0,2.5);"
r"\draw (0,2.5) -- (2.5,2.5);"
r"\draw (2.5,2.5) to[V, l_=2V] (2.5,0);"
r"\draw (2.5,0) -- (5,0) to[R, l_=2$\Omega$] (5,2.5);"
r"\draw (5,2.5) -- (0,2.5);"
r"\draw[->,thick] (2.5,2) -- (2.5,0.8) node[midway,left] {$I$};"
r"\draw (2.5,3.2) node[font=\small] {(a)};",
r"\draw (0,0) to[V, l_=1V] (0,2.5);"
r"\draw (0,2.5) to[I, l_=2A] (2.5,2.5);"
r"\draw (2.5,2.5) to[R, l_=1$\Omega$] (5,2.5);"
r"\draw (5,2.5) -- (5,0) -- (0,0);"
r"\draw[<->] (5.5,2.5) -- (5.5,0) node[midway,right] {$U$};"
r"\draw (2.5,3.2) node[font=\small] {(b)};"
)

fig("1-26", r"""
\draw (0,0) -- (12,0);
\draw (0,0) to[V, l_=$U_{S1}$] (0,3.5);
\draw (0,3.5) to[R, l_=$R_1$] (3,3.5);
\draw (3,3.5) to[R, l_=$R_2$] (6,3.5);
\draw (6,3.5) to[V, l_=$U_{S2}$, v^=$U_{S2}$] (6,3.5);
\draw (6,3.5) to[R, l_=$R_5$] (9,3.5);
\draw (9,3.5) to[V, l_=$U_{S3}$] (9,0);
\draw (3,3.5) to[R, l_=$R_3$] (3,0);
\draw (6,3.5) to[R, l_=$R_4$] (6,0);
\draw (3,0) to[V, l_=$U_{S4}$] (3,0);
\draw (3,1.8) to[R, l_=$R_6$] (6,1.8);
\draw[->,thick] (0.8,1.5) -- (0.8,2.5) node[midway,right] {$I_1$};
\draw[->,thick] (1.5,3.8) -- (2.5,3.8) node[midway,above] {$I_2$};
\draw[->,thick] (3,2.8) -- (3,1) node[midway,left] {$I_3$};
\draw[->,thick] (6,2.8) -- (6,1) node[midway,right] {$I_4$};
\draw[->,thick] (4.5,2.1) -- (5.5,2.1) node[midway,above] {$I_5$};
\draw[->,thick] (7.5,3.8) -- (8.5,3.8) node[midway,above] {$I_6$};
""")

fig("1-27", r"""
\draw (0,0) to[R, l=3$\Omega$] (0,3.5);
\draw (0,3.5) -- (0,4.5) to[V, l=6V] (2.5,4.5);
\draw (2.5,4.5) to[R, l=6$\Omega$] (2.5,1);
\draw (2.5,1) -- (0,1) -- (0,0);
\draw (5,0) to[I, l=2A] (5,3.5);
\draw (5,3.5) to[R, l=7$\Omega$] (5,0);
\draw (5,0) -- (0,0);
\draw (5,3.5) -- (8,3.5);
\draw (8,3.5) -- (8,1.5) node[ocirc]{};
\draw (0,3.5) -- (-1,3.5) -- (-1,1.5) node[ocirc]{};
\draw[<->] (-1,2.5) -- (8,2.5) node[midway,above] {$U$};
\draw (2.5,0) to[V, l_=5V] (2.5,0);
""")

fig("1-28", r"""
\draw (0,0) to[V, l_=$U_{S1}$] (0,3.5);
\draw (0,3.5) -- (2,3.5) node[circle,draw,inner sep=1pt,fill=white] {} node[above] {c};
\draw (2,3.5) to[R, l_=$R_1$] (4.5,3.5) node[circle,draw,inner sep=1pt,fill=white] {} node[above] {a};
\draw (4.5,3.5) to[R, l_=$R_2$] (7,3.5) node[circle,draw,inner sep=1pt,fill=white] {} node[above] {d};
\draw (7,3.5) to[V, l_=$U_{S2}$] (7,0);
\draw (4.5,3.5) to[R, l_=$R_3$] (4.5,0) node[circle,draw,inner sep=1pt,fill=white] {} node[below] {b};
\draw (0,0) -- (7,0);
\draw[->,thick] (1,3.8) -- (2.5,3.8) node[midway,above] {$I_1$};
\draw[->,thick] (5.5,3.8) -- (6.5,3.8) node[midway,above] {$I_2$};
\draw[->,thick] (4.5,2.8) -- (4.5,1) node[midway,left] {$I_3$};
""")

fig("1-29", r"""
\draw (0,0) to[V, l_=$U_S$] (0,3.5);
\draw (0,3.5) to[R, l_=$R_0$] (3,3.5);
\draw (3,3.5) to[R, l_=$R_2$] (3,0);
\draw (3,3.5) -- (5,3.5);
\draw (5,3.5) to[R, l_=$R_1$] (5,0);
\draw (0,0) -- (5,0);
\draw (3,3.5) -- (4,3.5) -- (4,2.2);
\draw (4,1.2) circle (0.4) node {P};
\draw (4,1.6) -- (4,0);
\draw (3,1.8) -- (5.5,1.8) -- (7,1.8);
\draw (7,1.8) to[V, l_=$U_x$] (7,0);
\draw (7,0) -- (0,0);
\draw (4,2.2) -- (4.5,2.2) -- (4.5,1.8);
""")

print("第1章完成")

# ======== Chapter 2 ========
fig("2-18",
# (a) 菱形桥: 左6Ω 右6Ω 上12Ω 下12Ω, 对角线交叉不连
r"\draw (2,0) to[R, l=6$\Omega$] (4,2.5);"
r"\draw (2,0) to[R, l=12$\Omega$] (2,4.5);"
r"\draw (2,4.5) to[R, l=6$\Omega$] (4,2.5);"
r"\draw (2,0) to[R, l=12$\Omega$] (4,2.5);"
r"\draw (2,0) node[circ]{} (2,4.5) node[circ]{} (4,2.5) node[circ]{};"
r"\draw (0.5,0) node[font=\small] {(a)};",
# (b) 阶梯网络
r"\draw (0,0) -- (0,4.5);"
r"\draw (0,4.5) to[R, l=3$\Omega$] (3,4.5);"
r"\draw (3,4.5) to[R, l=2$\Omega$] (6,4.5);"
r"\draw (0,3.3) to[R, l=8$\Omega$] (3,3.3);"
r"\draw (3,3.3) -- (3,4.5);"
r"\draw (3,3.3) to[R, l=4$\Omega$] (3,2);"
r"\draw (3,2) to[R, l=2$\Omega$] (6,2);"
r"\draw (6,2) to[R, l=6$\Omega$] (6,4.5);"
r"\draw (6,2) -- (6,0);"
r"\draw (0,0) -- (6,0);"
r"\draw (0,0) node[circ]{} (0,4.5) node[circ]{};"
r"\draw (-0.5,0) node[below] {(b)};"
)

fig("2-19", r"""
\draw (0,0) to[V, l=10V] (0,3.5);
\draw (0,3.5) to[R, l=4$\Omega$] (3,3.5);
\draw (3,3.5) to[switch, l=$S$] (6,3.5);
\draw (6,3.5) to[R, l=2$\Omega$] (6,0);
\draw (3,0) to[R, l=2$\Omega$] (3,3.5);
\draw (3,3.5) to[R, l=6$\Omega$] (4.5,1.8);
\draw (4.5,1.8) to[R, l=2$\Omega$] (6,0);
\draw (0,0) -- (6,0);
\draw[->,thick] (1,1.5) -- (1,2.5) node[midway,right] {$I$};
""")

fig("2-20",
r"\draw (0,0) to[I, l=3A] (0,2.5);"
r"\draw (0,2.5) to[R, l=3$\Omega$] (0,0);"
r"\draw (0,2.5) -- (2.5,2.5) to[V, l_=6V] (2.5,0);"
r"\draw (2.5,0) -- (0,0);"
r"\draw (2.5,2.5) -- (4,2.5) node[ocirc]{};"
r"\draw (2.5,0) -- (4,0) node[ocirc]{};"
r"\draw (1,3.2) node[font=\small] {(a)};",
r"\draw (0,0) to[V, l=3V] (0,2.5);"
r"\draw (0,2.5) to[R, l=4$\Omega$] (0,0);"
r"\draw (1.5,2.5) to[I, l_=5A] (1.5,0);"
r"\draw (0,2.5) -- (2.5,2.5) -- (2.5,0) -- (0,0);"
r"\draw (2.5,2.5) -- (4,2.5) node[ocirc]{};"
r"\draw (2.5,0) -- (4,0) node[ocirc]{};"
r"\draw (1,3.2) node[font=\small] {(b)};",
r"\draw (0,0) to[V, l=5V] (0,2.5);"
r"\draw (0,2.5) to[R, l=2$\Omega$] (2,2.5);"
r"\draw (2,2.5) to[I, l_=1A] (2,0);"
r"\draw (2,0) -- (0,0);"
r"\draw (2,2.5) -- (4,2.5) node[ocirc]{};"
r"\draw (2,0) -- (4,0) node[ocirc]{};"
r"\draw (1,3.2) node[font=\small] {(c)};"
)

fig("2-21", r"""
\draw (0,0) -- (9,0);
\draw (0,0) to[R, l=3$\Omega$] (0,3.5);
\draw (2.5,0) to[I, l=4A] (2.5,3.5);
\draw (5,0) to[V, l=2V] (5,3.5);
\draw (5,3.5) to[R, l=2$\Omega$] (5,2);
\draw (5,2) to[R, l=3$\Omega$] (7,2);
\draw (5,3.5) -- (7,3.5);
\draw (7,3.5) to[R, l=3$\Omega$] (7,2);
\draw (7,2) to[I, l_=4A] (7,0);
\draw (9,0) to[R, l=5$\Omega$] (9,3.5);
\draw[<->] (9.5,3.5) -- (9.5,0) node[midway,right] {$U$};
\draw (7,3.5) -- (9,3.5);
""")

fig("2-22", r"""
\draw (0,0) to[V, l=$U$] (0,3.5);
\draw (0,3.5) -- (1.5,3.5) node[circ]{} node[above] {A};
\draw (1.5,3.5) to[R, l=$R_1$] (4.5,1.8) node[circ]{} node[right] {C};
\draw (1.5,3.5) to[R, l=$R_2$] (1.5,0) node[circ]{} node[below] {B};
\draw (4.5,1.8) to[R, l=$R_5$] (4.5,0);
\draw (4.5,1.8) to[R, l=$R_3$] (7.5,3.5) node[circ]{} node[above] {D};
\draw (7.5,3.5) to[R, l=$R_4$] (7.5,0);
\draw (0,0) -- (7.5,0);
\draw (1.5,0) -- (7.5,0);
""")

fig("2-23", r"""
\draw (0,0) to[V, l=13V] (0,3.5);
\draw (0,3.5) to[R, l=3$\Omega$] (0,0);
\draw (2.5,0) to[I, l=4A] (2.5,3.5);
\draw (5,0) to[R, l=2$\Omega$] (5,3.5);
\draw (0,3.5) -- (5,3.5); \draw (0,0) -- (5,0);
\draw[->,thick] (0.8,1.5) -- (0.8,2.5) node[midway,right] {$I_1$};
\draw[->,thick] (4.2,2.5) -- (4.2,1.5) node[midway,left] {$I_2$};
""")

fig("2-24", r"""
\draw (0,0) to[V, l=20V] (0,3.5);
\draw (0,3.5) to[R, l=2$\Omega$] (0,0);
\draw (2.5,0) to[R, l=3$\Omega$] (2.5,3.5);
\draw (5,0) to[I, l=10A] (5,3.5);
\draw (0,3.5) -- (5,3.5); \draw (0,0) -- (5,0);
\draw[<->] (5.5,3.5) -- (5.5,0) node[midway,right] {$U$};
\draw[->,thick] (0.8,1.5) -- (1.8,1.5) node[midway,above] {$I$};
""")

fig("2-25", r"""
\draw (0,0) to[V, l=8V] (0,3.5);
\draw (0,3.5) -- (2.5,3.5);
\draw (2.5,3.5) to[R, l=2$\Omega$] (2.5,2);
\draw (2.5,2) to[R, l=3$\Omega$] (2.5,0);
\draw (2.5,3.5) -- (5,3.5);
\draw (5,3.5) to[R, l=2$\Omega$] (5,2);
\draw (5,2) to[R, l=4$\Omega$] (5,0);
\draw (2.5,2) -- (3.8,2);
\draw (3.8,2) to[I, l_=4A] (5,2);
\draw (0,0) -- (5,0);
\draw[->,thick] (5,2.8) -- (5,2.2) node[midway,right] {$I$};
""")

fig("2-26",
r"\draw (0,0) to[V, l=1V] (0,2.5);"
r"\draw (0,2.5) to[R, l=3$\Omega$] (2.5,2.5);"
r"\draw (2.5,2.5) -- (3.5,2.5);"
r"\draw (3.5,2.5) to[R, l=6$\Omega$] (3.5,0);"
r"\draw (3.5,0) -- (0,0);"
r"\draw (2.5,0) to[V, l_=10V] (2.5,0);"
r"\draw (3.5,2.5) -- (5,2.5) node[ocirc]{};"
r"\draw (3.5,0) -- (5,0) node[ocirc]{};"
r"\draw (1.5,3.2) node[font=\small] {(a)};",
r"\draw (0,0) to[V, l=3V] (0,2.5);"
r"\draw (0,2.5) to[R, l=2$\Omega$] (2.5,2.5);"
r"\draw (2.5,2.5) to[I, l_=1A] (2.5,0);"
r"\draw (2.5,0) -- (0,0);"
r"\draw (2.5,2.5) -- (3.5,2.5) to[R, l=5$\Omega$] (3.5,0);"
r"\draw (3.5,0) -- (2.5,0);"
r"\draw (3.5,2.5) -- (5,2.5) node[ocirc]{};"
r"\draw (3.5,0) -- (5,0) node[ocirc]{};"
r"\draw (1.5,3.2) node[font=\small] {(b)};"
)

fig("2-27", r"""
\draw (0,0) to[R, l=3$\Omega$] (0,3.5);
\draw (0,3.5) to[V, l_=5V] (0,3.5);
\draw (0,3.5) -- (2,3.5) node[circ]{} node[above] {A};
\draw (2,3.5) to[R, l=5$\Omega$] (4.5,3.5) node[circ]{} node[above] {C};
\draw (4.5,3.5) to[R, l=3$\Omega$] (7,3.5) node[circ]{} node[above] {B};
\draw (4.5,3.5) to[I, l_=3A] (4.5,5);
\draw (4.5,5) -- (7,5);
\draw (7,5) to[R, l=2$\Omega$] (7,3.5);
\draw (2.5,0) to[V, l=14V] (2.5,3.5);
\draw (7,0) to[R, l=2$\Omega$] (7,3.5);
\draw[<->] (7.5,3.5) -- (7.5,0) node[midway,right] {$U$};
\draw (0,0) -- (7,0);
""")

fig("2-28", r"""
\draw (0,0) to[V, l=9V] (0,3.5);
\draw (0,3.5) to[R, l=6$\Omega$] (0,0);
\draw (2.5,0) to[R, l=3$\Omega$] (2.5,3.5);
\draw (5,3.5) to[R, l=3$\Omega$] (5,2);
\draw (5,2) to[I, l_=2A] (5,3.5);
\draw (7.5,0) to[R, l=4$\Omega$] (7.5,3.5);
\draw (0,3.5) -- (7.5,3.5); \draw (0,0) -- (7.5,0);
\draw[->,thick] (7.5,2.8) -- (7.5,1) node[midway,right] {$I$};
""")

fig("2-29", r"""
\draw (0,0) to[I, l=2A] (0,3.5);
\draw (0,3.5) -- (2.5,3.5);
\draw (2.5,3.5) to[R, l=3$\Omega$] (2.5,0);
\draw (2.5,0) -- (0,0);
\draw (5,3.5) to[V, l_=8V] (5,2);
\draw (5,2) to[R, l=1$\Omega$] (5,0);
\draw (2.5,3.5) -- (5,3.5);
\draw (7.5,0) to[R, l=$R$] (7.5,3.5);
\draw (5,3.5) -- (7.5,3.5); \draw (0,0) -- (7.5,0);
""")

print("第2章完成")

# ======== Chapter 3 ========
fig("3-52",
r"\draw (0,0) to[sV, l=$u$] (0,3);"
r"\draw (0,3) -- (3,3);"
r"\draw (3,3) to[R, l=$R$] (3,1);"
r"\draw (3,3) to[C, l=$C$] (3,1);"
r"\draw (3,1) -- (3,0); \draw (0,0) -- (5.5,0);"
r"\draw (4.5,3) circle(6pt) (4.5,3) node {$A$};"
r"\draw (1.5,3) circle(6pt) (1.5,3) node {$A$};"
r"\draw (4.5,0) circle(6pt) (4.5,0) node {$A$};"
r"\draw (2.5,3.5) node[font=\small] {(a)};",
r"\draw (0,0) to[sV, l=$u$] (0,3);"
r"\draw (0,3) to[R, l=$R$] (3,3);"
r"\draw (3,3) to[L, l=$L$] (3,0);"
r"\draw (3,0) -- (0,0); \draw (3,3) -- (5.5,3);"
r"\draw (1.5,3) circle(6pt) (1.5,3) node {$V$};"
r"\draw (3,1.5) circle(6pt) (3,1.5) node {$V$};"
r"\draw (5,3) circle(6pt) (5,3) node {$V$};"
r"\draw (2.5,3.5) node[font=\small] {(b)};"
)

fig("3-53", r"""
\draw (0,0) -- (0,3.5);
\draw (0,3.5) to[generic, l=$Z_3$] (4,3.5);
\draw (4,3.5) to[generic, l=$Z_1$] (7.5,3.5);
\draw (7.5,3.5) -- (7.5,1.8);
\draw (7.5,1.8) to[generic, l=$Z_2$] (4,1.8);
\draw (4,1.8) -- (4,0);
\draw (0,0) -- (7.5,0);
\draw[<->] (4.5,1.8) -- (4.5,3.5) node[midway,right] {$U$};
""")

print("第3章完成")

# ======== Chapter 7 ========
fig("7-18",
r"\draw (0,0) to[R, l=$R$] (0,3.5);"
r"\draw (0,3.5) to[D, l=$VD$] (3.5,3.5);"
r"\draw (3.5,3.5) to[V, l=6V] (3.5,0);"
r"\draw (3.5,0) -- (0,0);"
r"\draw (1.5,4.2) node[font=\small] {(a)};",
r"\draw (0,0) to[V, l=10V] (0,3.5);"
r"\draw (0,3.5) to[D, l=$VD$] (3.5,3.5);"
r"\draw (3.5,3.5) to[V, l=6V] (3.5,0);"
r"\draw (3.5,0) to[R, l=$R$] (0,0);"
r"\draw (1.5,4.2) node[font=\small] {(b)};"
)

fig("7-19",
r"\draw (-1,2) to[sV, l=$u_i$] (-1,4.5);"
r"\draw (-1,4.5) to[R, l=$R$] (2.5,4.5);"
r"\draw (2.5,4.5) -- (3.5,4.5);"
r"\draw (3.5,4.5) -- (3.5,3);"
r"\draw (3.5,3) to[D, l=$VD$] (3.5,1);"
r"\draw (3.5,1) to[V, l_=$U_{REF}$] (3.5,-0.5);"
r"\draw (2.5,0) -- (2.5,4.5); \draw (2.5,0) -- (4.5,0);"
r"\draw (-1,2) -- (4.5,2); \draw (4.5,2) -- (5.5,2) node[right] {$u_o$};"
r"\draw (1.5,5.2) node[font=\small] {(a)};",
r"\draw (-1,2) to[sV, l=$u_i$] (-1,4.5);"
r"\draw (-1,4.5) to[R, l=$R$] (2.5,4.5);"
r"\draw (2.5,4.5) -- (3.5,4.5);"
r"\draw (3.5,4.5) -- (3.5,3);"
r"\draw (3.5,3) to[D, l=$VD$] (3.5,5);"
r"\draw (3.5,5) to[V, l_=$U_{REF}$] (3.5,6.5);"
r"\draw (2.5,0) -- (2.5,4.5); \draw (2.5,0) -- (4.5,0);"
r"\draw (-1,2) -- (4.5,2); \draw (4.5,2) -- (5.5,2) node[right] {$u_o$};"
r"\draw (1.5,5.2) node[font=\small] {(b)};"
)

fig("7-20",
r"\draw (0,0) node[npn](Q){};"
r"\draw (Q.B) -- ++(-1,0) node[left] {5V};"
r"\draw (Q.C) -- ++(0.5,0) node[right] {4.4V};"
r"\draw (Q.E) -- ++(0.5,0) node[right] {4.3V};"
r"\draw (0.8,-1.2) node[font=\small] {(a)};",
r"\draw (0,0) node[pnp](Q){};"
r"\draw (Q.B) -- ++(-1,0) node[left] {-2V};"
r"\draw (Q.C) -- ++(0.5,0) node[right] {-7V};"
r"\draw (Q.E) -- ++(0.5,0) node[right] {-1.6V};"
r"\draw (0.8,-1.2) node[font=\small] {(b)};",
r"\draw (0,0) node[npn](Q){};"
r"\draw (Q.B) -- ++(-1,0) node[left] {1.3V};"
r"\draw (Q.C) -- ++(0.5,0) node[right] {4V};"
r"\draw (Q.E) -- ++(0.5,0) node[right] {2V};"
r"\draw (0.8,-1.2) node[font=\small] {(c)};",
r"\draw (0,0) node[npn](Q){};"
r"\draw (Q.B) -- ++(-1,0) node[left] {3V};"
r"\draw (Q.C) -- ++(0.5,0) node[right] {8.3V};"
r"\draw (Q.E) -- ++(0.5,0) node[right] {2.3V};"
r"\draw (0.8,-1.2) node[font=\small] {(d)};"
)

fig("7-21",
r"\draw (0,0) node[pnp](Q){};"
r"\draw (Q.E) -- ++(-1.2,0) node[left] {2.04mA};"
r"\draw[->] ($(Q.E)+(-0.6,0)$) -- ++(-0.6,0);"
r"\draw (Q.B) -- ++(0.6,0) node[right] {0.04mA};"
r"\draw[->] ($(Q.B)+(0.3,0)$) -- ++(0.3,0);"
r"\draw (Q.C) -- ++(0.6,0) node[right] {2mA};"
r"\draw[->] ($(Q.C)+(0.3,0)$) -- ++(0.3,0);"
r"\draw (0.8,-1.2) node[font=\small] {(a)};",
r"\draw (0,0) node[npn](Q){};"
r"\draw (Q.E) -- ++(-1.2,0) node[left] {3.03mA};"
r"\draw[->] ($(Q.E)+(-0.6,0)$) -- ++(-0.6,0);"
r"\draw (Q.B) -- ++(0.6,0) node[right] {0.03mA};"
r"\draw[->] ($(Q.B)+(0.3,0)$) -- ++(0.3,0);"
r"\draw (Q.C) -- ++(0.6,0) node[right] {3mA};"
r"\draw[->] ($(Q.C)+(0.3,0)$) -- ++(0.3,0);"
r"\draw (0.8,-1.2) node[font=\small] {(b)};"
)

print("第7章完成")
print("\n全部完成!")
