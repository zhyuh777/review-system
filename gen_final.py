#!/usr/bin/env python3
"""按提示词文档精确重绘26张电路图
约定：电源=Battery(一长一短竖线)，电流源=圆圈箭头，检流计=圆内一横线
"""
import os, subprocess

BASE = '/Users/zzzzed/opencodes/electest'
OUT = os.path.join(BASE, 'latex_figures')
FIG = os.path.join(BASE, '电工电子技术', 'figures')
os.makedirs(OUT, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

def gen(name, tex_body):
    """单图生成"""
    tex = (r"\documentclass[border=12pt]{standalone}"
           r"\usepackage[siunitx, european]{circuitikz}"
           r"\usepackage{amsmath}" + "\n\\begin{document}\n"
           + tex_body + "\n\\end{document}")
    tp = os.path.join(OUT, name+".tex")
    with open(tp, 'w') as f:
        f.write(tex)
    subprocess.run(['xelatex','-interaction=nonstopmode','-output-directory',OUT,tp],
                   capture_output=True,timeout=60)
    pp = os.path.join(OUT, name+".pdf")
    png = os.path.join(FIG, f"图{name}.png")
    if os.path.exists(pp):
        subprocess.run(['magick','-density','300',pp,'-quality','95',png],
                       capture_output=True,timeout=30)
    lp = os.path.join(OUT, name+".log")
    e = sum(1 for l in open(lp) if l.startswith("!")) if os.path.exists(lp) else -1
    s = os.path.getsize(png)//1024 if os.path.exists(png) else 0
    print(f"  [{'OK' if e==0 else str(e)+'e'}] 图{name}.png ({s}KB)")

# 检流计符号: 圆内一横线
GAL = r"\draw (x,y) circle (0.4); \draw (x-0.3,y) -- (x+0.3,y);"

# ============================================================
# 第1章
# ============================================================

gen("1-22", r"""
% 单回路三元件: 左U₁(+上-下) 上U₂(-左+右) 右U₃(+上-下) 底导线
% I₁↓, I₂→, I₃↓
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery, l_=$U_1$] (0,3.5);
  \draw (0,3.5) to[battery, l_=$U_2$] (5,3.5);
  \draw (5,3.5) to[battery, l_=$U_3$] (5,0);
  \draw (0,0) -- (5,0);
  \draw[->,thick] (0.8,1.3) -- (0.8,2.5) node[midway,right] {$I_1$};
  \draw[->,thick] (1.5,3.8) -- (3.5,3.8) node[midway,above] {$I_2$};
  \draw[->,thick] (4.2,2.5) -- (4.2,1.3) node[midway,left] {$I_3$};
\end{circuitikz}
""")

gen("1-23", r"""
% 四组端子+电源
% (a) 8V +上-下, I=2A从左流入(箭头→)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) rectangle (2,2); \draw (1,1) node {N};
  \draw (2,1) to[battery,l_=8V] (4,1);
  \draw (0,1) -- (-0.5,1); \draw (4,1) -- (4.5,1);
  \draw[->,thick] (2.5,1.4) -- (3.5,1.4) node[midway,above] {2A};
  \draw (1,2.5) node[font=\small] {(a)};
\end{circuitikz}
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) rectangle (2,2); \draw (1,1) node {N};
  \draw (2,1) to[battery,l_=4V] (4,1);
  \draw (0,1) -- (-0.5,1); \draw (4,1) -- (4.5,1);
  \draw[->,thick] (3.5,0.6) -- (2.5,0.6) node[midway,below] {3A};
  \draw (1,2.5) node[font=\small] {(b)};
\end{circuitikz}
% (c) 1A电流源↓, U=5V(+上-下)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) rectangle (2,2); \draw (1,1) node {N};
  \draw (2,1) to[I,l_=1A] (4,1);
  \draw (0,1) -- (-0.5,1); \draw (4,1) -- (4.5,1);
  \draw[<->] (4.5,1.5) -- (4.5,0.5) node[midway,right] {5V};
  \draw (1,2.5) node[font=\small] {(c)};
\end{circuitikz}
% (d) 3A电流源↓, U=6V(-上+下)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) rectangle (2,2); \draw (1,1) node {N};
  \draw (2,1) to[I,l_=3A] (4,1);
  \draw (0,1) -- (-0.5,1); \draw (4,1) -- (4.5,1);
  \draw[<->] (4.5,1.5) -- (4.5,0.5) node[midway,right] {6V};
  \draw (1,2.5) node[font=\small] {(d)};
\end{circuitikz}
""")

gen("1-24", r"""
% (a) 6V(+接a侧) 2Ω R, 电流I(c→b), V(8V跨a-b, +接a,-接b)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[battery,l_=6V] (0,2.5);
  \draw (0,2.5) to[R,l_=2$\Omega$] (3,2.5);
  \draw (3,2.5) -- (3,0) -- (0,0);
  \draw[->,thick] (1,2.8) -- (2,2.8) node[midway,above] {$I$};
  \draw (0,-0.4) node {a} (3,-0.4) node {b};
  \draw[<->] (3.5,2.5) -- (3.5,0) node[midway,right] {8V};
  \draw (1.5,3.2) node[font=\small] {(a)};
\end{circuitikz}
% (b) 串链: U_S-2Ω-5V-2V-5Ω-A(1A), V(8V跨a-b)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[battery,l_=$U_S$] (0,2.5);
  \draw (0,2.5) to[R,l_=2$\Omega$] (2.5,2.5);
  \draw (2.5,2.5) to[battery,l_=5V] (2.5,0);
  \draw (2.5,0) -- (5,0) to[battery,l_=2V] (5,2.5);
  \draw (5,2.5) to[R,l_=5$\Omega$] (7.5,2.5);
  \draw (7.5,2.5) -- (7.5,0) -- (0,0);
  \draw (1.2,1.2) node[circle,draw,inner sep=1pt,fill=white] {a};
  \draw (6.2,1.2) node[circle,draw,inner sep=1pt,fill=white] {b};
  \draw[<->] (8,2.5) -- (8,0) node[midway,right] {8V};
  \draw (3.5,3.2) node[font=\small] {(b)};
\end{circuitikz}
% (c) 3V(+接a) 串R, V(2V跨R, -接a,+接b)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[battery,l_=3V] (0,2.5);
  \draw (0,2.5) to[R,l_=$R$] (3.5,2.5);
  \draw (3.5,2.5) -- (3.5,0) -- (0,0);
  \draw[<->] (4,2.5) -- (4,0) node[midway,right] {2V};
  \draw (0,-0.4) node {a} (3.5,-0.4) node {b};
  \draw (1.5,3.2) node[font=\small] {(c)};
\end{circuitikz}
% (d) A(1A) 2V(+在R侧) R, V(5V跨a-b)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[I,l_=1A] (0,2.5);
  \draw (0,2.5) to[battery,l_=2V] (2.5,2.5);
  \draw (2.5,2.5) to[R,l_=$R$] (5,2.5);
  \draw (5,2.5) -- (5,0) -- (0,0);
  \draw[<->] (5.5,2.5) -- (5.5,0) node[midway,right] {5V};
  \draw (0,-0.4) node {a} (5,-0.4) node {b};
  \draw (2.5,3.2) node[font=\small] {(d)};
\end{circuitikz}
""")

gen("1-25", r"""
% (a) 三并支: 左1A↓ 中2V(+上) 右2Ω
% I参考方向向上(经中支路)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[I,l_=1A] (0,2.5);
  \draw (0,2.5) -- (2.5,2.5) to[battery,l_=2V] (2.5,0);
  \draw (2.5,0) -- (5,0) to[R,l_=2$\Omega$] (5,2.5);
  \draw (5,2.5) -- (0,2.5);
  \draw[->,thick] (2.5,2) -- (2.5,0.8) node[midway,left] {$I$};
  \draw (2.5,3.2) node[font=\small] {(a)};
\end{circuitikz}
% (b) 单回路: 左1V(+上)+2A↑+U(+上), 右1Ω
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[battery,l_=1V] (0,2.5);
  \draw (0,2.5) to[I,l_=2A] (2.5,2.5);
  \draw (2.5,2.5) to[R,l_=1$\Omega$] (5,2.5);
  \draw (5,2.5) -- (5,0) -- (0,0);
  \draw[<->] (5.5,2.5) -- (5.5,0) node[midway,right] {$U$};
  \draw (2.5,3.2) node[font=\small] {(b)};
\end{circuitikz}
""")

gen("1-26", r"""
% 六电阻四源: U_S1(左+上) U_S2(顶+左) U_S3(右+上) U_S4(中−上+下)
% R1-R6, I₁↑ I₂← I₃↑ I₄↓ I₅→ I₆→
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) -- (12,0);
  \draw (0,0) to[battery,l_=$U_{S1}$] (0,3.5);
  \draw (0,3.5) to[R,l_=$R_1$] (3,3.5);
  \draw (3,3.5) to[R,l_=$R_2$] (6,3.5);
  \draw (6,3.5) to[battery,l_=$U_{S2}$] (6,3.5);
  \draw (6,3.5) to[R,l_=$R_5$] (9,3.5);
  \draw (9,3.5) to[battery,l_=$U_{S3}$] (9,0);
  \draw (3,3.5) to[R,l_=$R_3$] (3,0);
  \draw (6,3.5) to[R,l_=$R_4$] (6,0);
  \draw (3,0) to[battery,l_=$U_{S4}$] (3,0);
  \draw (3,1.8) to[R,l_=$R_6$] (6,1.8);
  \draw[->,thick] (0.8,1.5) -- (0.8,2.5) node[midway,right] {$I_1$};
  \draw[->,thick] (1.5,3.8) -- (2.5,3.8) node[midway,above] {$I_2$};
  \draw[->,thick] (3,2.8) -- (3,1) node[midway,left] {$I_3$};
  \draw[->,thick] (6,2.8) -- (6,1) node[midway,right] {$I_4$};
  \draw[->,thick] (4.5,2.1) -- (5.5,2.1) node[midway,above] {$I_5$};
  \draw[->,thick] (7.5,3.8) -- (8.5,3.8) node[midway,above] {$I_6$};
\end{circuitikz}
""")

gen("1-27", r"""
% 左: 3Ω∥(6V源-左+右 串6Ω)  右: 2A↑∥7Ω  底5V(+左-右)  顶开断口U(+左-右)
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[R,l=3$\Omega$] (0,3.5);
  \draw (0,3.5) -- (0,4.5) to[battery,l=6V] (2.5,4.5);
  \draw (2.5,4.5) to[R,l=6$\Omega$] (2.5,1);
  \draw (2.5,1) -- (0,1) -- (0,0);
  \draw (5,0) to[I,l=2A] (5,3.5);
  \draw (5,3.5) to[R,l=7$\Omega$] (5,0);
  \draw (5,0) -- (0,0);
  \draw (5,3.5) -- (8,3.5);
  \draw (8,3.5) -- (8,1.5) node[ocirc]{};
  \draw (0,3.5) -- (-1,3.5) -- (-1,1.5) node[ocirc]{};
  \draw[<->] (-1,2.5) -- (8,2.5) node[midway,above] {$U$};
  \draw (2.5,0) to[battery,l_=5V] (2.5,0);
\end{circuitikz}
""")

gen("1-28", r"""
% 节点: c(左上) a(顶中) d(右上) b(底中)
% U_S1: c→b, +上 R₁: c→a(I₁→) R₃: a→b(I₃↓) R₂: d→a(I₂←) U_S2: d→b +上
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery,l_=$U_{S1}$] (0,3.5);
  \draw (0,3.5) -- (2,3.5) node[circ]{} node[above] {c};
  \draw (2,3.5) to[R,l_=$R_1$] (4.5,3.5) node[circ]{} node[above] {a};
  \draw (4.5,3.5) to[R,l_=$R_2$] (7,3.5) node[circ]{} node[above] {d};
  \draw (7,3.5) to[battery,l_=$U_{S2}$] (7,0);
  \draw (4.5,3.5) to[R,l_=$R_3$] (4.5,0) node[circ]{} node[below] {b};
  \draw (0,0) -- (7,0);
  \draw[->,thick] (1,3.8) -- (2.5,3.8) node[midway,above] {$I_1$};
  \draw[->,thick] (5.5,3.8) -- (6.5,3.8) node[midway,above] {$I_2$};
  \draw[->,thick] (4.5,2.8) -- (4.5,1) node[midway,left] {$I_3$};
\end{circuitikz}
""")

gen("1-29", r"""
% 电位计: 左回路U_S+R₀串, 滑动变阻器R₁下/R₂上, 右检流计P+U_x
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery,l_=$U_S$] (0,3.5);
  \draw (0,3.5) to[R,l_=$R_0$] (3,3.5);
  \draw (3,3.5) to[R,l_=$R_2$] (3,0);
  \draw (3,3.5) -- (5,3.5);
  \draw (5,3.5) to[R,l_=$R_1$] (5,0);
  \draw (0,0) -- (5,0);
  \draw (3,3.5) -- (4,3.5) -- (4,2.2);
  % 检流计: 圆内一横线
  \draw (4,1.2) circle (0.4);
  \draw (3.7,1.2) -- (4.3,1.2);
  \node at (4,0.7) {P};
  \draw (4,1.6) -- (4,0);
  \draw (3,1.8) -- (5.5,1.8) -- (7,1.8);
  \draw (7,1.8) to[battery,l_=$U_x$] (7,0);
  \draw (7,0) -- (0,0);
  \draw (4,2.2) -- (4.5,2.2) -- (4.5,1.8);
\end{circuitikz}
""")

# ============================================================
# 第2章
# ============================================================

gen("2-18", r"""
% (a) 菱形桥: 左6Ω 右6Ω 上12Ω 下12Ω 对角线交叉不连
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (2,0) to[R,l=6$\Omega$] (4,2.5);
  \draw (2,0) to[R,l=12$\Omega$] (2,4.5);
  \draw (2,4.5) to[R,l=6$\Omega$] (4,2.5);
  \draw (2,0) to[R,l=12$\Omega$] (4,2.5);
  \draw (2,0) node[circ]{} (2,4.5) node[circ]{} (4,2.5) node[circ]{};
  \draw (0.5,0) node[font=\small] {(a)};
\end{circuitikz}
\begin{circuitikz}[scale=1.0,transform shape]
% (b) 阶梯网络: 竖8Ω 上3Ω 中4Ω+2Ω 下6Ω+2Ω
  \draw (0,0) -- (0,4.5);
  \draw (0,4.5) to[R,l=3$\Omega$] (3,4.5);
  \draw (3,4.5) to[R,l=2$\Omega$] (6,4.5);
  \draw (0,3.3) to[R,l=8$\Omega$] (3,3.3);
  \draw (3,3.3) -- (3,4.5);
  \draw (3,3.3) to[R,l=4$\Omega$] (3,2);
  \draw (3,2) to[R,l=2$\Omega$] (6,2);
  \draw (6,2) to[R,l=6$\Omega$] (6,4.5);
  \draw (6,2) -- (6,0);
  \draw (0,0) -- (6,0);
  \draw (0,0) node[circ]{} (0,4.5) node[circ]{};
  \draw (-0.5,0) node[below] {(b)};
\end{circuitikz}
""")

gen("2-19", r"""
% 10V桥+开关S: 10V(+上) 4Ω(顶横) 2Ω(底横) 6Ω(对角线左上→右下) 2Ω(对角线左下→右上) S(右竖)
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery,l=10V] (0,3.5);
  \draw (0,3.5) to[R,l=4$\Omega$] (3,3.5);
  \draw (3,3.5) to[switch,l=$S$] (6,3.5);
  \draw (6,3.5) to[R,l=2$\Omega$] (6,0);
  \draw (3,0) to[R,l=2$\Omega$] (3,3.5);
  \draw (3,3.5) to[R,l=6$\Omega$] (4.5,1.8);
  \draw (4.5,1.8) to[R,l=2$\Omega$] (6,0);
  \draw (0,0) -- (6,0);
  \draw[->,thick] (1,1.5) -- (1,2.5) node[midway,right] {$I$};
\end{circuitikz}
""")

gen("2-20", r"""
% (a) 3A↑∥3Ω 串6V(−左+右)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[I,l=3A] (0,2.5);
  \draw (0,2.5) to[R,l=3$\Omega$] (0,0);
  \draw (0,2.5) -- (2.5,2.5) to[battery,l_=6V] (2.5,0);
  \draw (2.5,0) -- (0,0);
  \draw (2.5,2.5) -- (4,2.5) node[ocirc]{};
  \draw (2.5,0) -- (4,0) node[ocirc]{};
  \draw (1,3.2) node[font=\small] {(a)};
\end{circuitikz}
% (b) 3V∥4Ω 顶串5A←
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[battery,l=3V] (0,2.5);
  \draw (0,2.5) to[R,l=4$\Omega$] (0,0);
  \draw (1.5,2.5) to[I,l_=5A] (1.5,0);
  \draw (0,2.5) -- (2.5,2.5) -- (2.5,0) -- (0,0);
  \draw (2.5,2.5) -- (4,2.5) node[ocirc]{};
  \draw (2.5,0) -- (4,0) node[ocirc]{};
  \draw (1,3.2) node[font=\small] {(b)};
\end{circuitikz}
% (c) 5V串2Ω∥1A↑
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[battery,l=5V] (0,2.5);
  \draw (0,2.5) to[R,l=2$\Omega$] (2,2.5);
  \draw (2,2.5) to[I,l_=1A] (2,0);
  \draw (2,0) -- (0,0);
  \draw (2,2.5) -- (4,2.5) node[ocirc]{};
  \draw (2,0) -- (4,0) node[ocirc]{};
  \draw (1,3.2) node[font=\small] {(c)};
\end{circuitikz}
""")

gen("2-21", r"""
% 四竖支+底公共线: 3Ω 4A↑ 顶桥2V(+左)+2Ω 4A↓ 5Ω(U,+上)
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) -- (9,0);
  \draw (0,0) to[R,l=3$\Omega$] (0,3.5);
  \draw (2.5,0) to[I,l=4A] (2.5,3.5);
  \draw (5,0) to[battery,l=2V] (5,3.5);
  \draw (5,3.5) to[R,l=2$\Omega$] (5,2);
  \draw (5,2) to[R,l=3$\Omega$] (7,2);
  \draw (5,3.5) -- (7,3.5);
  \draw (7,3.5) to[R,l=3$\Omega$] (7,2);
  \draw (7,2) to[I,l_=4A] (7,0);
  \draw (9,0) to[R,l=5$\Omega$] (9,3.5);
  \draw[<->] (9.5,3.5) -- (9.5,0) node[midway,right] {$U$};
  \draw (7,3.5) -- (9,3.5);
\end{circuitikz}
""")

gen("2-22", r"""
% 惠斯通电桥: U+顶-底 R₁(顶左→左中) R₂(底左→左中) R₄(顶右→右中) R₃(底右→右中) R₅(左中→右中)
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery,l=$U$] (0,3.5);
  \draw (0,3.5) -- (1.5,3.5) node[circ]{} node[above] {A};
  \draw (1.5,3.5) to[R,l=$R_1$] (4.5,1.8) node[circ]{} node[right] {C};
  \draw (1.5,3.5) to[R,l=$R_2$] (1.5,0) node[circ]{} node[below] {B};
  \draw (4.5,1.8) to[R,l=$R_5$] (4.5,0);
  \draw (4.5,1.8) to[R,l=$R_3$] (7.5,3.5) node[circ]{} node[above] {D};
  \draw (7.5,3.5) to[R,l=$R_4$] (7.5,0);
  \draw (0,0) -- (7.5,0);
  \draw (1.5,0) -- (7.5,0);
\end{circuitikz}
""")

gen("2-23", r"""
% 三并支(共顶共底): 左13V串3Ω I₁↑ 中4A↑ 右2Ω I₂↓
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery,l=13V] (0,3.5);
  \draw (0,3.5) to[R,l=3$\Omega$] (0,0);
  \draw (2.5,0) to[I,l=4A] (2.5,3.5);
  \draw (5,0) to[R,l=2$\Omega$] (5,3.5);
  \draw (0,3.5) -- (5,3.5); \draw (0,0) -- (5,0);
  \draw[->,thick] (0.8,1.5) -- (0.8,2.5) node[midway,right] {$I_1$};
  \draw[->,thick] (4.2,2.5) -- (4.2,1.5) node[midway,left] {$I_2$};
\end{circuitikz}
""")

gen("2-24", r"""
% 三并支: 左20V(+上)串2Ω 中3Ω 右10A↑, U(+上), I→顶线左段
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery,l=20V] (0,3.5);
  \draw (0,3.5) to[R,l=2$\Omega$] (0,0);
  \draw (2.5,0) to[R,l=3$\Omega$] (2.5,3.5);
  \draw (5,0) to[I,l=10A] (5,3.5);
  \draw (0,3.5) -- (5,3.5); \draw (0,0) -- (5,0);
  \draw[<->] (5.5,3.5) -- (5.5,0) node[midway,right] {$U$};
  \draw[->,thick] (0.8,1.5) -- (1.8,1.5) node[midway,above] {$I$};
\end{circuitikz}
""")

gen("2-25", r"""
% 三竖支+中桥: 左8V(+上) 中2Ω串3Ω(中点M) 右2Ω串4Ω(中点N,I↓) 桥4A源(N→M,向左)
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery,l=8V] (0,3.5);
  \draw (0,3.5) -- (2.5,3.5);
  \draw (2.5,3.5) to[R,l=2$\Omega$] (2.5,2);
  \draw (2.5,2) to[R,l=3$\Omega$] (2.5,0);
  \draw (2.5,3.5) -- (5,3.5);
  \draw (5,3.5) to[R,l=2$\Omega$] (5,2);
  \draw (5,2) to[R,l=4$\Omega$] (5,0);
  \draw (2.5,2) -- (3.8,2);
  \draw (3.8,2) to[I,l_=4A] (5,2);
  \draw (0,0) -- (5,0);
  \draw[->,thick] (5,2.8) -- (5,2.2) node[midway,right] {$I$};
\end{circuitikz}
""")

gen("2-26", r"""
% (a) 1V∥10V两源各串3Ω、6Ω并联
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[battery,l=1V] (0,2.5);
  \draw (0,2.5) to[R,l=3$\Omega$] (2.5,2.5);
  \draw (2.5,2.5) -- (3.5,2.5);
  \draw (3.5,2.5) to[R,l=6$\Omega$] (3.5,0);
  \draw (3.5,0) -- (0,0);
  \draw (2.5,0) to[battery,l_=10V] (2.5,0);
  \draw (3.5,2.5) -- (5,2.5) node[ocirc]{};
  \draw (3.5,0) -- (5,0) node[ocirc]{};
  \draw (1.5,3.2) node[font=\small] {(a)};
\end{circuitikz}
% (b) 3V串2Ω∥1A↑ 顶再串5Ω
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[battery,l=3V] (0,2.5);
  \draw (0,2.5) to[R,l=2$\Omega$] (2.5,2.5);
  \draw (2.5,2.5) to[I,l_=1A] (2.5,0);
  \draw (2.5,0) -- (0,0);
  \draw (2.5,2.5) -- (3.5,2.5) to[R,l=5$\Omega$] (3.5,0);
  \draw (3.5,0) -- (2.5,0);
  \draw (3.5,2.5) -- (5,2.5) node[ocirc]{};
  \draw (3.5,0) -- (5,0) node[ocirc]{};
  \draw (1.5,3.2) node[font=\small] {(b)};
\end{circuitikz}
""")

gen("2-27", r"""
% 三竖支: 左3Ω串5V(+上) 中14V(+上) 右2Ω(U,+上)
% 顶网络: A—5Ω—C—3Ω—B  3A源(B→A,向左)
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[R,l=3$\Omega$] (0,3.5);
  \draw (0,3.5) to[battery,l_=5V] (0,3.5);
  \draw (0,3.5) -- (2,3.5) node[circ]{} node[above] {A};
  \draw (2,3.5) to[R,l=5$\Omega$] (4.5,3.5) node[circ]{} node[above] {C};
  \draw (4.5,3.5) to[R,l=3$\Omega$] (7,3.5) node[circ]{} node[above] {B};
  \draw (4.5,3.5) to[I,l_=3A] (4.5,5);
  \draw (4.5,5) -- (7,5);
  \draw (7,5) to[R,l=2$\Omega$] (7,3.5);
  \draw (2.5,0) to[battery,l=14V] (2.5,3.5);
  \draw (7,0) to[R,l=2$\Omega$] (7,3.5);
  \draw[<->] (7.5,3.5) -- (7.5,0) node[midway,right] {$U$};
  \draw (0,0) -- (7,0);
\end{circuitikz}
""")

gen("2-28", r"""
% 左9V(+上)串6Ω 中3Ω竖 顶A—B: 2A→∥3Ω 右4Ω,I↓
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery,l=9V] (0,3.5);
  \draw (0,3.5) to[R,l=6$\Omega$] (0,0);
  \draw (2.5,0) to[R,l=3$\Omega$] (2.5,3.5);
  \draw (5,3.5) to[R,l=3$\Omega$] (5,2);
  \draw (5,2) to[I,l_=2A] (5,3.5);
  \draw (7.5,0) to[R,l=4$\Omega$] (7.5,3.5);
  \draw (0,3.5) -- (7.5,3.5); \draw (0,0) -- (7.5,0);
  \draw[->,thick] (7.5,2.8) -- (7.5,1) node[midway,right] {$I$};
\end{circuitikz}
""")

gen("2-29", r"""
% 左2A↓ 中3Ω竖 顶中—顶右: 8V(−左+右)串1Ω 右:可变R(斜箭头)
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[I,l=2A] (0,3.5);
  \draw (0,3.5) -- (2.5,3.5);
  \draw (2.5,3.5) to[R,l=3$\Omega$] (2.5,0);
  \draw (2.5,0) -- (0,0);
  \draw (5,3.5) to[battery,l_=8V] (5,2);
  \draw (5,2) to[R,l=1$\Omega$] (5,0);
  \draw (2.5,3.5) -- (5,3.5);
  \draw (7.5,0) to[R,l=$R$] (7.5,3.5);
  \draw (5,3.5) -- (7.5,3.5); \draw (0,0) -- (7.5,0);
\end{circuitikz}
""")

# ============================================================
# 第3章
# ============================================================

gen("3-52", r"""
% (a) RC并联: u源, A总表, A₁-R并支, A₂-C并支
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[sV,l=$u$] (0,3);
  \draw (0,3) -- (3,3);
  \draw (3,3) to[R,l=$R$] (3,1);
  \draw (3,3) to[C,l=$C$] (3,1);
  \draw (3,1) -- (3,0); \draw (0,0) -- (5.5,0);
  \draw (4.5,3) circle(6pt) (4.5,3) node {$A$};
  \draw (1.5,3) circle(6pt) (1.5,3) node {$A$};
  \draw (4.5,0) circle(6pt) (4.5,0) node {$A$};
  \draw (2.5,3.5) node[font=\small] {(a)};
\end{circuitikz}
% (b) RL串联: u源, V跨源, V₁跨R, V₂跨L
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) to[sV,l=$u$] (0,3);
  \draw (0,3) to[R,l=$R$] (3,3);
  \draw (3,3) to[L,l=$L$] (3,0);
  \draw (3,0) -- (0,0); \draw (3,3) -- (5.5,3);
  \draw (1.5,3) circle(6pt) (1.5,3) node {$V$};
  \draw (3,1.5) circle(6pt) (3,1.5) node {$V$};
  \draw (5,3) circle(6pt) (5,3) node {$V$};
  \draw (2.5,3.5) node[font=\small] {(b)};
\end{circuitikz}
""")

gen("3-53", r"""
% Z₃串(Z₁∥Z₂), 左上下端子为输入
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) -- (0,3.5);
  \draw (0,3.5) to[generic,l=$Z_3$] (4,3.5);
  \draw (4,3.5) to[generic,l=$Z_1$] (7.5,3.5);
  \draw (7.5,3.5) -- (7.5,1.8);
  \draw (7.5,1.8) to[generic,l=$Z_2$] (4,1.8);
  \draw (4,1.8) -- (4,0);
  \draw (0,0) -- (7.5,0);
  \draw[<->] (4.5,1.8) -- (4.5,3.5) node[midway,right] {$U$};
\end{circuitikz}
""")

# ============================================================
# 第7章
# ============================================================

gen("7-18", r"""
% (a) R竖支 VD顶横→右 6V(+上)竖支: VD阴极接6V+ → 反偏
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[R,l=$R$] (0,3.5);
  \draw (0,3.5) to[D,l=$VD$] (3.5,3.5);
  \draw (3.5,3.5) to[battery,l=6V] (3.5,0);
  \draw (3.5,0) -- (0,0);
  \draw (1.5,4.2) node[font=\small] {(a)};
\end{circuitikz}
% (b) 10V(+上)左竖 VD顶横→右 6V(+上)右竖 R底横: VD阳极近10V+ → 正偏
\begin{circuitikz}[scale=1.2,transform shape]
  \draw (0,0) to[battery,l=10V] (0,3.5);
  \draw (0,3.5) to[D,l=$VD$] (3.5,3.5);
  \draw (3.5,3.5) to[battery,l=6V] (3.5,0);
  \draw (3.5,0) to[R,l=$R$] (0,0);
  \draw (1.5,4.2) node[font=\small] {(b)};
\end{circuitikz}
""")

gen("7-19", r"""
% (a) 限幅: u_i(+上)→R串→u_o(+上) 下支VD(↓)串U_REF(+接VD阴极)至地
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (-1,2) to[sV,l=$u_i$] (-1,4.5);
  \draw (-1,4.5) to[R,l=$R$] (2.5,4.5);
  \draw (2.5,4.5) -- (3.5,4.5);
  \draw (3.5,4.5) -- (3.5,3);
  \draw (3.5,3) to[D,l=$VD$] (3.5,1);
  \draw (3.5,1) to[battery,l_=$U_{REF}$] (3.5,-0.5);
  \draw (2.5,0) -- (2.5,4.5); \draw (2.5,0) -- (4.5,0);
  \draw (-1,2) -- (4.5,2); \draw (4.5,2) -- (5.5,2) node[right] {$u_o$};
  \draw (1.5,5.2) node[font=\small] {(a)};
\end{circuitikz}
% (b) U_REF极性反接(−接VD阴极)
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (-1,2) to[sV,l=$u_i$] (-1,4.5);
  \draw (-1,4.5) to[R,l=$R$] (2.5,4.5);
  \draw (2.5,4.5) -- (3.5,4.5);
  \draw (3.5,4.5) -- (3.5,3);
  \draw (3.5,3) to[D,l=$VD$] (3.5,5);
  \draw (3.5,5) to[battery,l_=$U_{REF}$] (3.5,6.5);
  \draw (2.5,0) -- (2.5,4.5); \draw (2.5,0) -- (4.5,0);
  \draw (-1,2) -- (4.5,2); \draw (4.5,2) -- (5.5,2) node[right] {$u_o$};
  \draw (1.5,5.2) node[font=\small] {(b)};
\end{circuitikz}
""")

gen("7-20", r"""
% 四个BJT: 仅标注B、C、E对地电位
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) node[npn](Q){};
  \draw (Q.B) -- ++(-1,0) node[left] {5V};
  \draw (Q.C) -- ++(0.5,0) node[right] {4.4V};
  \draw (Q.E) -- ++(0.5,0) node[right] {4.3V};
  \draw (0.8,-1.2) node[font=\small] {(a)};
\end{circuitikz}
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) node[pnp](Q){};
  \draw (Q.B) -- ++(-1,0) node[left] {-2V};
  \draw (Q.C) -- ++(0.5,0) node[right] {-7V};
  \draw (Q.E) -- ++(0.5,0) node[right] {-1.6V};
  \draw (0.8,-1.2) node[font=\small] {(b)};
\end{circuitikz}
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) node[npn](Q){};
  \draw (Q.B) -- ++(-1,0) node[left] {1.3V};
  \draw (Q.C) -- ++(0.5,0) node[right] {4V};
  \draw (Q.E) -- ++(0.5,0) node[right] {2V};
  \draw (0.8,-1.2) node[font=\small] {(c)};
\end{circuitikz}
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) node[npn](Q){};
  \draw (Q.B) -- ++(-1,0) node[left] {3V};
  \draw (Q.C) -- ++(0.5,0) node[right] {8.3V};
  \draw (Q.E) -- ++(0.5,0) node[right] {2.3V};
  \draw (0.8,-1.2) node[font=\small] {(d)};
\end{circuitikz}
""")

gen("7-21", r"""
% (a) PNP: 左2.04mA流入 中0.04mA流出 右2mA流出
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) node[pnp](Q){};
  \draw (Q.E) -- ++(-1.2,0) node[left] {2.04mA};
  \draw[->] ($(Q.E)+(-0.6,0)$) -- ++(-0.6,0);
  \draw (Q.B) -- ++(0.6,0) node[right] {0.04mA};
  \draw[->] ($(Q.B)+(0.3,0)$) -- ++(0.3,0);
  \draw (Q.C) -- ++(0.6,0) node[right] {2mA};
  \draw[->] ($(Q.C)+(0.3,0)$) -- ++(0.3,0);
  \draw (0.8,-1.2) node[font=\small] {(a)};
\end{circuitikz}
% (b) NPN: 左3.03mA流出 中0.03mA流入 右3mA流入
\begin{circuitikz}[scale=1.0,transform shape]
  \draw (0,0) node[npn](Q){};
  \draw (Q.E) -- ++(-1.2,0) node[left] {3.03mA};
  \draw[->] ($(Q.E)+(-0.6,0)$) -- ++(-0.6,0);
  \draw (Q.B) -- ++(0.6,0) node[right] {0.03mA};
  \draw[->] ($(Q.B)+(0.3,0)$) -- ++(0.3,0);
  \draw (Q.C) -- ++(0.6,0) node[right] {3mA};
  \draw[->] ($(Q.C)+(0.3,0)$) -- ++(0.3,0);
  \draw (0.8,-1.2) node[font=\small] {(b)};
\end{circuitikz}
""")
