#!/usr/bin/env python3
"""Generate analysis questions with SVG data:image diagrams for all 3 courses."""
import json, os, base64

SVGS = {}

# ==================== 传感器技术 (5 diagrams) ====================

SVGS["strain_gage"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200">
<rect x="10" y="10" width="280" height="180" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="150" y="30" text-anchor="middle" font-size="14" font-weight="bold">电阻应变片结构示意图</text>
<rect x="60" y="50" width="180" height="100" rx="4" fill="#fff" stroke="#333" stroke-width="2"/>
<line x1="80" y1="55" x2="80" y2="145" stroke="#d00" stroke-width="2"/>
<line x1="220" y1="55" x2="220" y2="145" stroke="#d00" stroke-width="2"/>
<!-- 敏感栅 -->
<path d="M90 65 L210 65" stroke="#2563eb" stroke-width="3"/>
<path d="M90 80 L210 80" stroke="#2563eb" stroke-width="3"/>
<path d="M90 95 L210 95" stroke="#2563eb" stroke-width="3"/>
<path d="M90 110 L210 110" stroke="#2563eb" stroke-width="3"/>
<path d="M90 125 L210 125" stroke="#2563eb" stroke-width="3"/>
<path d="M90 140 L210 140" stroke="#2563eb" stroke-width="3"/>
<!-- 引出线 -->
<line x1="80" y1="65" x2="40" y2="40" stroke="#d00" stroke-width="1.5"/>
<line x1="80" y1="140" x2="40" y2="165" stroke="#d00" stroke-width="1.5"/>
<text x="50" y="35" font-size="10" fill="#d00" text-anchor="end">引出线</text>
<text x="50" y="175" font-size="10" fill="#d00" text-anchor="end">引出线</text>
<text x="150" y="160" font-size="10" fill="#2563eb" text-anchor="middle">敏感栅</text>
<text x="40" y="105" font-size="10" fill="#666" text-anchor="end" transform="rotate(-90,40,105)">基底</text>
<line x1="190" y1="45" x2="190" y2="55" stroke="#999" stroke-width="1"/>
<text x="190" y="42" font-size="9" fill="#999">栅长</text>
</svg>"""

SVGS["thermocouple"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 180">
<rect x="10" y="10" width="330" height="160" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="175" y="30" text-anchor="middle" font-size="14" font-weight="bold">热电偶工作原理图</text>
<!-- 热端 -->
<ellipse cx="60" cy="100" rx="20" ry="12" fill="#fee" stroke="#d00" stroke-width="2"/>
<text x="60" y="104" text-anchor="middle" font-size="9" fill="#d00">热端</text>
<!-- 金属A -->
<line x1="80" y1="92" x2="250" y2="50" stroke="#2563eb" stroke-width="3"/>
<text x="165" y="60" font-size="10" fill="#2563eb" text-anchor="middle">金属A</text>
<!-- 金属B -->
<line x1="80" y1="108" x2="250" y2="140" stroke="#d0870a" stroke-width="3"/>
<text x="165" y="160" font-size="10" fill="#d0870a" text-anchor="middle">金属B</text>
<!-- 冷端 -->
<ellipse cx="270" cy="50" rx="12" ry="8" fill="#e8f4fd" stroke="#2563eb" stroke-width="1.5"/>
<text x="270" y="43" font-size="8" fill="#2563eb" text-anchor="middle">冷端</text>
<ellipse cx="270" cy="140" rx="12" ry="8" fill="#fef6e4" stroke="#d0870a" stroke-width="1.5"/>
<text x="270" y="133" font-size="8" fill="#d0870a" text-anchor="middle">冷端</text>
<!-- 仪表 -->
<rect x="280" y="75" width="40" height="40" rx="4" fill="#fff" stroke="#333" stroke-width="2"/>
<text x="300" y="98" text-anchor="middle" font-size="8">仪表</text>
<line x1="270" y1="50" x2="285" y2="85" stroke="#333" stroke-width="1.5"/>
<line x1="270" y1="140" x2="285" y2="105" stroke="#333" stroke-width="1.5"/>
<text x="300" y="125" font-size="9" fill="#d00" text-anchor="middle">U</text>
<text x="60" y="80" font-size="9" fill="#d00" text-anchor="middle">T1</text>
<text x="240" y="35" font-size="9" fill="#2563eb" text-anchor="middle">T2</text>
</svg>"""

SVGS["capacitive_sensor"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180">
<rect x="10" y="10" width="300" height="160" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="160" y="30" text-anchor="middle" font-size="14" font-weight="bold">电容式传感器原理示意图</text>
<!-- 极板1 -->
<rect x="60" y="60" width="30" height="80" rx="2" fill="#bee3f8" stroke="#2563eb" stroke-width="2"/>
<text x="75" y="140" text-anchor="middle" font-size="9" fill="#2563eb">极板1</text>
<!-- 极板2 -->
<rect x="220" y="60" width="30" height="80" rx="2" fill="#bee3f8" stroke="#2563eb" stroke-width="2"/>
<text x="235" y="140" text-anchor="middle" font-size="9" fill="#2563eb">极板2</text>
<!-- 可动极板 -->
<rect x="140" y="45" width="30" height="110" rx="2" fill="#fef6e4" stroke="#d0870a" stroke-width="2" stroke-dasharray="4,2"/>
<text x="155" y="42" text-anchor="middle" font-size="9" fill="#d0870a">可动极板</text>
<!-- 间隙标注 -->
<line x1="90" y1="50" x2="140" y2="50" stroke="#999" stroke-width="1"/>
<line x1="90" y1="53" x2="90" y2="47" stroke="#999" stroke-width="1"/>
<line x1="140" y1="53" x2="140" y2="47" stroke="#999" stroke-width="1"/>
<text x="115" y="48" text-anchor="middle" font-size="9" fill="#999">d</text>
<line x1="190" y1="50" x2="220" y2="50" stroke="#999" stroke-width="1"/>
<line x1="190" y1="53" x2="190" y2="47" stroke="#999" stroke-width="1"/>
<line x1="220" y1="53" x2="220" y2="47" stroke="#999" stroke-width="1"/>
<text x="205" y="48" text-anchor="middle" font-size="9" fill="#999">Δd</text>
<!-- 介质 -->
<rect x="100" y="65" width="110" height="70" rx="2" fill="#e2e8f0" opacity="0.3"/>
<text x="155" y="100" text-anchor="middle" font-size="10" fill="#666">介质 (ε)</text>
<!-- 电容符号 -->
<text x="160" y="172" text-anchor="middle" font-size="11" fill="#d00">C = εS / d</text>
</svg>"""

SVGS["piezoelectric"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 180">
<rect x="10" y="10" width="280" height="160" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="150" y="30" text-anchor="middle" font-size="14" font-weight="bold">压电效应原理图</text>
<!-- 晶体 -->
<rect x="85" y="50" width="130" height="80" rx="4" fill="#fff" stroke="#333" stroke-width="2"/>
<!-- 正电荷 -->
<circle cx="120" cy="70" r="6" fill="#fcc" stroke="#d00" stroke-width="1.5"/>
<text x="120" y="73" text-anchor="middle" font-size="8" fill="#d00">+</text>
<circle cx="180" cy="70" r="6" fill="#fcc" stroke="#d00" stroke-width="1.5"/>
<text x="180" y="73" text-anchor="middle" font-size="8" fill="#d00">+</text>
<!-- 负电荷 -->
<circle cx="120" cy="110" r="6" fill="#cfc" stroke="#080" stroke-width="1.5"/>
<text x="120" y="113" text-anchor="middle" font-size="8" fill="#080">-</text>
<circle cx="180" cy="110" r="6" fill="#cfc" stroke="#080" stroke-width="1.5"/>
<text x="180" y="113" text-anchor="middle" font-size="8" fill="#080">-</text>
<!-- 力箭头 -->
<line x1="95" y1="40" x2="95" y2="30" stroke="#d00" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="200" y1="40" x2="200" y2="30" stroke="#d00" stroke-width="2"/>
<line x1="95" y1="140" x2="95" y2="150" stroke="#d00" stroke-width="2"/>
<line x1="200" y1="140" x2="200" y2="150" stroke="#d00" stroke-width="2"/>
<text x="150" y="25" text-anchor="middle" font-size="10" fill="#d00">F (压力)</text>
<text x="150" y="165" text-anchor="middle" font-size="10" fill="#2563eb">电极</text>
<text x="150" y="92" text-anchor="middle" font-size="11" fill="#666">压电晶体</text>
<!-- 输出 -->
<line x1="85" y1="90" x2="40" y2="50" stroke="#333" stroke-width="1.5"/>
<line x1="215" y1="90" x2="260" y2="50" stroke="#333" stroke-width="1.5"/>
<text x="260" y="45" font-size="9" fill="#d00" text-anchor="end">电荷输出</text>
</svg>"""

SVGS["hall_sensor"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="10" y="10" width="320" height="180" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="170" y="30" text-anchor="middle" font-size="14" font-weight="bold">霍尔传感器原理图</text>
<!-- 霍尔元件 -->
<rect x="120" y="65" width="100" height="70" rx="4" fill="#e8f4fd" stroke="#2563eb" stroke-width="2"/>
<text x="170" y="105" text-anchor="middle" font-size="10" fill="#2563eb">霍尔元件</text>
<!-- 控制电流 -->
<line x1="80" y1="100" x2="120" y2="100" stroke="#d00" stroke-width="2"/>
<text x="50" y="95" font-size="10" fill="#d00">I (控制电流)</text>
<line x1="220" y1="100" x2="260" y2="100" stroke="#d00" stroke-width="2"/>
<line x1="260" y1="95" x2="270" y2="100" stroke="#d00" stroke-width="2"/>
<line x1="260" y1="105" x2="270" y2="100" stroke="#d00" stroke-width="2"/>
<!-- 磁场 -->
<text x="40" y="50" font-size="10" fill="#080">N</text>
<line x1="60" y1="55" x2="60" y2="145" stroke="#080" stroke-width="2" stroke-dasharray="4,3"/>
<line x1="100" y1="55" x2="100" y2="145" stroke="#080" stroke-width="2" stroke-dasharray="4,3"/>
<text x="60" y="165" font-size="10" fill="#080">S</text>
<text x="80" y="30" font-size="10" fill="#080">B (磁场)</text>
<!-- 霍尔电压输出 -->
<line x1="145" y1="65" x2="145" y2="30" stroke="#d0870a" stroke-width="1.5"/>
<line x1="195" y1="65" x2="195" y2="30" stroke="#d0870a" stroke-width="1.5"/>
<text x="170" y="22" text-anchor="middle" font-size="10" fill="#d0870a">VH (霍尔电压)</text>
<!-- 公式 -->
<text x="170" y="190" text-anchor="middle" font-size="11" fill="#d00">VH = k · I · B / d</text>
</svg>"""

# ==================== 单片机技术 (5 diagrams) ====================

SVGS["mcu_min_sys"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 220">
<rect x="10" y="10" width="360" height="200" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="190" y="30" text-anchor="middle" font-size="14" font-weight="bold">51单片机最小系统原理图</text>
<!-- MCU -->
<rect x="140" y="55" width="100" height="110" rx="6" fill="#fff" stroke="#333" stroke-width="2"/>
<text x="190" y="100" text-anchor="middle" font-size="10" font-weight="bold">AT89C51</text>
<text x="190" y="115" text-anchor="middle" font-size="8" fill="#666">单片机</text>
<!-- VCC -->
<line x1="140" y1="70" x2="100" y2="70" stroke="#d00" stroke-width="1.5"/>
<text x="90" y="74" text-anchor="end" font-size="9" fill="#d00">VCC (+5V)</text>
<!-- GND -->
<line x1="240" y1="150" x2="280" y2="150" stroke="#333" stroke-width="1.5"/>
<text x="290" y="154" font-size="9" fill="#333">GND</text>
<!-- 晶振 -->
<rect x="180" y="172" width="20" height="14" rx="3" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="190" y="182" text-anchor="middle" font-size="7">晶振</text>
<line x1="190" y1="165" x2="190" y2="172" stroke="#333" stroke-width="1"/>
<line x1="185" y1="165" x2="195" y2="165" stroke="#333" stroke-width="1"/>
<!-- 电容 -->
<line x1="210" y1="178" x2="230" y2="178" stroke="#333" stroke-width="1"/>
<line x1="220" y1="175" x2="220" y2="185" stroke="#333" stroke-width="1"/>
<text x="240" y="182" font-size="8" fill="#666">C1 C2</text>
<!-- 复位 -->
<line x1="100" y1="130" x2="140" y2="130" stroke="#333" stroke-width="1.5"/>
<circle cx="95" cy="130" r="5" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="80" y="134" text-anchor="end" font-size="9">RST</text>
<text x="190" y="208" text-anchor="middle" font-size="9" fill="#999">注：含晶振电路、复位电路、电源</text>
</svg>"""

SVGS["led_display"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200">
<rect x="10" y="10" width="300" height="180" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="160" y="30" text-anchor="middle" font-size="14" font-weight="bold">LED数码管及驱动电路</text>
<!-- 数码管 -->
<rect x="80" y="50" width="140" height="120" rx="8" fill="#fff" stroke="#333" stroke-width="2"/>
<!-- 段a -->
<rect x="90" y="58" width="120" height="12" rx="2" fill="#fcc" stroke="#d00" stroke-width="1"/>
<text x="85" y="68" text-anchor="end" font-size="8" fill="#d00">a</text>
<!-- 段b -->
<rect x="200" y="70" width="12" height="45" rx="2" fill="#fcc" stroke="#d00" stroke-width="1"/>
<text x="216" y="88" font-size="8" fill="#d00">b</text>
<!-- 段c -->
<rect x="200" y="115" width="12" height="45" rx="2" fill="#fcc" stroke="#d00" stroke-width="1"/>
<text x="216" y="130" font-size="8" fill="#d00">c</text>
<!-- 段d -->
<rect x="90" y="158" width="120" height="12" rx="2" fill="#fcc" stroke="#d00" stroke-width="1"/>
<text x="85" y="170" text-anchor="end" font-size="8" fill="#d00">d</text>
<!-- 段e -->
<rect x="78" y="115" width="12" height="45" rx="2" fill="#fcc" stroke="#d00" stroke-width="1"/>
<text x="72" y="130" text-anchor="end" font-size="8" fill="#d00">e</text>
<!-- 段f -->
<rect x="78" y="70" width="12" height="45" rx="2" fill="#fcc" stroke="#d00" stroke-width="1"/>
<text x="72" y="88" text-anchor="end" font-size="8" fill="#d00">f</text>
<!-- 段g -->
<rect x="90" y="108" width="120" height="12" rx="2" fill="#fcc" stroke="#d00" stroke-width="1"/>
<text x="85" y="118" text-anchor="end" font-size="8" fill="#d00">g</text>
<!-- DP -->
<circle cx="200" cy="158" r="5" fill="#ddd" stroke="#999" stroke-width="1"/>
<text x="216" y="163" font-size="8" fill="#999">DP</text>
<!-- 限流电阻 -->
<rect x="10" y="165" width="30" height="12" rx="2" fill="#fff" stroke="#999" stroke-width="1"/>
<text x="25" y="174" text-anchor="middle" font-size="7" fill="#999">R</text>
<line x1="40" y1="171" x2="70" y2="171" stroke="#999" stroke-width="1"/>
<text x="50" y="195" text-anchor="middle" font-size="9" fill="#999">共阴极 / 共阳极</text>
</svg>"""

SVGS["matrix_keypad"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 220">
<rect x="10" y="10" width="280" height="200" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="150" y="30" text-anchor="middle" font-size="14" font-weight="bold">4×4矩阵键盘原理图</text>
<!-- 行线 -->
<line x1="50" y1="50" x2="250" y2="50" stroke="#2563eb" stroke-width="2"/>
<line x1="50" y1="80" x2="250" y2="80" stroke="#2563eb" stroke-width="2"/>
<line x1="50" y1="110" x2="250" y2="110" stroke="#2563eb" stroke-width="2"/>
<line x1="50" y1="140" x2="250" y2="140" stroke="#2563eb" stroke-width="2"/>
<!-- 行标签 -->
<text x="40" y="54" text-anchor="end" font-size="9" fill="#2563eb">R1</text>
<text x="40" y="84" text-anchor="end" font-size="9" fill="#2563eb">R2</text>
<text x="40" y="114" text-anchor="end" font-size="9" fill="#2563eb">R3</text>
<text x="40" y="144" text-anchor="end" font-size="9" fill="#2563eb">R4</text>
<!-- 列线 -->
<line x1="80" y1="45" x2="80" y2="155" stroke="#d0870a" stroke-width="2"/>
<line x1="130" y1="45" x2="130" y2="155" stroke="#d0870a" stroke-width="2"/>
<line x1="180" y1="45" x2="180" y2="155" stroke="#d0870a" stroke-width="2"/>
<line x1="230" y1="45" x2="230" y2="155" stroke="#d0870a" stroke-width="2"/>
<text x="80" y="168" text-anchor="middle" font-size="9" fill="#d0870a">C1</text>
<text x="130" y="168" text-anchor="middle" font-size="9" fill="#d0870a">C2</text>
<text x="180" y="168" text-anchor="middle" font-size="9" fill="#d0870a">C3</text>
<text x="230" y="168" text-anchor="middle" font-size="9" fill="#d0870a">C4</text>
<!-- 按键交点 -->
<circle cx="80" cy="50" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="80" y="54" text-anchor="middle" font-size="7">K</text>
<circle cx="130" cy="50" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="130" y="54" text-anchor="middle" font-size="7">K</text>
<circle cx="180" cy="50" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="180" y="54" text-anchor="middle" font-size="7">K</text>
<circle cx="230" cy="50" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="230" y="54" text-anchor="middle" font-size="7">K</text>
<circle cx="80" cy="80" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="80" y="84" text-anchor="middle" font-size="7">K</text>
<circle cx="130" cy="80" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="130" y="84" text-anchor="middle" font-size="7">K</text>
<circle cx="180" cy="80" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="180" y="84" text-anchor="middle" font-size="7">K</text>
<circle cx="230" cy="80" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="230" y="84" text-anchor="middle" font-size="7">K</text>
<circle cx="80" cy="110" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="80" y="114" text-anchor="middle" font-size="7">K</text>
<circle cx="130" cy="110" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="130" y="114" text-anchor="middle" font-size="7">K</text>
<circle cx="180" cy="110" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="180" y="114" text-anchor="middle" font-size="7">K</text>
<circle cx="230" cy="110" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="230" y="114" text-anchor="middle" font-size="7">K</text>
<circle cx="80" cy="140" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="80" y="144" text-anchor="middle" font-size="7">K</text>
<circle cx="130" cy="140" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="130" y="144" text-anchor="middle" font-size="7">K</text>
<circle cx="180" cy="140" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="180" y="144" text-anchor="middle" font-size="7">K</text>
<circle cx="230" cy="140" r="8" fill="#fff" stroke="#333" stroke-width="1.5"/>
<text x="230" y="144" text-anchor="middle" font-size="7">K</text>
<text x="150" y="195" text-anchor="middle" font-size="9" fill="#666">行扫描法：逐行输出低电平，检测列线电平</text>
</svg>"""

SVGS["serial_timing"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 150">
<rect x="10" y="10" width="380" height="130" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="200" y="30" text-anchor="middle" font-size="14" font-weight="bold">串行异步通信时序图</text>
<!-- 起始位 -->
<line x1="30" y1="50" x2="370" y2="50" stroke="#333" stroke-width="1"/>
<line x1="30" y1="50" x2="30" y2="130" stroke="#ccc" stroke-width="1"/>
<!-- 高电平基线 -->
<line x1="30" y1="60" x2="370" y2="60" stroke="#999" stroke-width="0.5" stroke-dasharray="3,3"/>
<text x="20" y="55" text-anchor="end" font-size="8" fill="#999">高</text>
<text x="20" y="105" text-anchor="end" font-size="8" fill="#999">低</text>
<!-- 起始位 -->
<rect x="50" y="62" width="30" height="38" fill="#e2e8f0" stroke="#333" stroke-width="1"/>
<text x="65" y="115" text-anchor="middle" font-size="8">起始</text>
<!-- 数据位 -->
<rect x="90" y="62" width="30" height="38" fill="#fee" stroke="#d00" stroke-width="1"/>
<text x="105" y="115" text-anchor="middle" font-size="8">D0</text>
<rect x="125" y="62" width="30" height="38" fill="#fee" stroke="#d00" stroke-width="1"/>
<text x="140" y="115" text-anchor="middle" font-size="8">D1</text>
<rect x="160" y="62" width="30" height="38" fill="#fee" stroke="#d00" stroke-width="1"/>
<text x="175" y="115" text-anchor="middle" font-size="8">D2</text>
<rect x="195" y="62" width="30" height="38" fill="#fee" stroke="#d00" stroke-width="1"/>
<text x="210" y="115" text-anchor="middle" font-size="8">D3</text>
<rect x="230" y="62" width="30" height="38" fill="#fee" stroke="#d00" stroke-width="1"/>
<text x="245" y="115" text-anchor="middle" font-size="8">D4</text>
<rect x="265" y="62" width="30" height="38" fill="#fee" stroke="#d00" stroke-width="1"/>
<text x="280" y="115" text-anchor="middle" font-size="8">D5</text>
<rect x="300" y="62" width="30" height="38" fill="#fee" stroke="#d00" stroke-width="1"/>
<text x="315" y="115" text-anchor="middle" font-size="8">D6</text>
<rect x="335" y="62" width="30" height="38" fill="#fee" stroke="#d00" stroke-width="1"/>
<text x="350" y="115" text-anchor="middle" font-size="8">D7</text>
<!-- 停止位 -->
<rect x="370" y="62" width="15" height="38" fill="#dfd" stroke="#080" stroke-width="1"/>
<text x="378" y="115" text-anchor="middle" font-size="7">停</text>
<text x="200" y="140" text-anchor="middle" font-size="9" fill="#666">一帧数据 = 起始位(1) + 数据位(8) + 停止位(1)</text>
</svg>"""

SVGS["interrupt_flow"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 220">
<rect x="10" y="10" width="300" height="200" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="160" y="30" text-anchor="middle" font-size="14" font-weight="bold">中断响应流程图</text>
<!-- 主程序 -->
<rect x="100" y="50" width="120" height="35" rx="6" fill="#e8f4fd" stroke="#2563eb" stroke-width="2"/>
<text x="160" y="72" text-anchor="middle" font-size="10" fill="#2563eb">主程序执行</text>
<line x1="160" y1="85" x2="160" y2="100" stroke="#333" stroke-width="1.5"/>
<!-- 判断 -->
<polygon points="160,100 200,120 160,140 120,120" fill="#fff" stroke="#d0870a" stroke-width="2"/>
<text x="160" y="123" text-anchor="middle" font-size="8" fill="#d0870a">中断请求？</text>
<!-- 否分支 -->
<line x1="200" y1="120" x2="240" y2="120" stroke="#999" stroke-width="1"/>
<text x="250" y="124" font-size="9" fill="#999">否</text>
<line x1="240" y1="120" x2="240" y2="55" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
<line x1="240" y1="55" x2="220" y2="55" stroke="#999" stroke-width="1" stroke-dasharray="4,3"/>
<!-- 是分支 -->
<line x1="160" y1="140" x2="160" y2="158" stroke="#333" stroke-width="1.5"/>
<rect x="100" y="158" width="120" height="35" rx="6" fill="#fef6e4" stroke="#d0870a" stroke-width="2"/>
<text x="160" y="180" text-anchor="middle" font-size="10" fill="#d0870a">中断服务程序</text>
<!-- 返回 -->
<line x1="160" y1="193" x2="160" y2="202" stroke="#333" stroke-width="1.5"/>
<line x1="160" y1="202" x2="70" y2="202" stroke="#333" stroke-width="1"/>
<line x1="70" y1="202" x2="70" y2="68" stroke="#333" stroke-width="1" stroke-dasharray="4,3"/>
<line x1="70" y1="68" x2="100" y2="68" stroke="#333" stroke-width="1" stroke-dasharray="4,3"/>
<text x="55" y="135" text-anchor="middle" font-size="8" fill="#666" transform="rotate(-90,55,135)">中断返回</text>
</svg>"""

# ==================== 物联网系统设计 (5 diagrams) ====================

SVGS["iot_architecture"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 240">
<rect x="10" y="10" width="300" height="220" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="160" y="30" text-anchor="middle" font-size="14" font-weight="bold">物联网三层架构</text>
<!-- 应用层 -->
<rect x="60" y="50" width="200" height="40" rx="6" fill="#e8f4fd" stroke="#2563eb" stroke-width="2"/>
<text x="160" y="72" text-anchor="middle" font-size="12" font-weight="bold" fill="#2563eb">应用层</text>
<text x="160" y="84" text-anchor="middle" font-size="8" fill="#2563eb">智能家居 / 智慧城市 / 工业监控</text>
<!-- 网络层 -->
<rect x="60" y="110" width="200" height="40" rx="6" fill="#fef6e4" stroke="#d0870a" stroke-width="2"/>
<text x="160" y="132" text-anchor="middle" font-size="12" font-weight="bold" fill="#d0870a">网络层</text>
<text x="160" y="144" text-anchor="middle" font-size="8" fill="#d0870a">WiFi / 4G/5G / LoRa / NB-IoT</text>
<!-- 感知层 -->
<rect x="60" y="170" width="200" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
<text x="160" y="192" text-anchor="middle" font-size="12" font-weight="bold" fill="#16a34a">感知层</text>
<text x="160" y="204" text-anchor="middle" font-size="8" fill="#16a34a">传感器 / RFID / 摄像头</text>
<!-- 箭头 -->
<line x1="160" y1="90" x2="160" y2="108" stroke="#999" stroke-width="2" marker-end="url(#a)"/>
<line x1="160" y1="150" x2="160" y2="168" stroke="#999" stroke-width="2"/>
<text x="160" y="228" text-anchor="middle" font-size="9" fill="#999">数据流 ↑ 控制流 ↓</text>
</svg>"""

SVGS["mqtt_protocol"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 200">
<rect x="10" y="10" width="340" height="180" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="180" y="30" text-anchor="middle" font-size="14" font-weight="bold">MQTT发布/订阅模型</text>
<!-- Broker -->
<rect x="130" y="70" width="100" height="60" rx="30" fill="#e8f4fd" stroke="#2563eb" stroke-width="2.5"/>
<text x="180" y="100" text-anchor="middle" font-size="12" font-weight="bold" fill="#2563eb">Broker</text>
<text x="180" y="115" text-anchor="middle" font-size="8" fill="#2563eb">消息代理</text>
<!-- Publisher -->
<rect x="20" y="80" width="80" height="40" rx="6" fill="#fef6e4" stroke="#d0870a" stroke-width="2"/>
<text x="60" y="105" text-anchor="middle" font-size="11" fill="#d0870a">发布者</text>
<line x1="100" y1="100" x2="128" y2="95" stroke="#d0870a" stroke-width="1.5"/>
<text x="114" y="88" font-size="8" fill="#d0870a">发布</text>
<!-- Subscriber -->
<rect x="260" y="60" width="80" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
<text x="300" y="85" text-anchor="middle" font-size="11" fill="#16a34a">订阅者</text>
<line x1="232" y1="90" x2="258" y2="78" stroke="#16a34a" stroke-width="1.5"/>
<text x="245" y="82" font-size="8" fill="#16a34a">订阅</text>
<!-- subscriber 2 -->
<rect x="260" y="120" width="80" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
<text x="300" y="145" text-anchor="middle" font-size="11" fill="#16a34a">订阅者</text>
<line x1="232" y1="100" x2="258" y2="138" stroke="#16a34a" stroke-width="1.5"/>
<text x="245" y="128" font-size="8" fill="#16a34a">订阅</text>
<text x="180" y="185" text-anchor="middle" font-size="9" fill="#666">Topic：消息主题，用于消息分类和路由</text>
</svg>"""

SVGS["mqtt_qos"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 200">
<rect x="10" y="10" width="360" height="180" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="190" y="30" text-anchor="middle" font-size="14" font-weight="bold">MQTT 服务质量（QoS）</text>
<!-- QoS 0 -->
<rect x="20" y="50" width="100" height="40" rx="6" fill="#e2e8f0" stroke="#94a3b8" stroke-width="2"/>
<text x="70" y="68" text-anchor="middle" font-size="11" fill="#475569">QoS 0</text>
<text x="70" y="82" text-anchor="middle" font-size="8" fill="#64748b">最多一次</text>
<text x="70" y="96" text-anchor="middle" font-size="7" fill="#94a3b8">可能丢失</text>
<!-- QoS 1 -->
<rect x="140" y="50" width="100" height="40" rx="6" fill="#fef6e4" stroke="#d0870a" stroke-width="2"/>
<text x="190" y="68" text-anchor="middle" font-size="11" fill="#d0870a">QoS 1</text>
<text x="190" y="82" text-anchor="middle" font-size="8" fill="#d0870a">至少一次</text>
<text x="190" y="96" text-anchor="middle" font-size="7" fill="#d0870a">可能重复</text>
<!-- QoS 2 -->
<rect x="260" y="50" width="100" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="2"/>
<text x="310" y="68" text-anchor="middle" font-size="11" fill="#16a34a">QoS 2</text>
<text x="310" y="82" text-anchor="middle" font-size="8" fill="#16a34a">恰好一次</text>
<text x="310" y="96" text-anchor="middle" font-size="7" fill="#16a34a">最可靠</text>
<!-- 说明 -->
<rect x="20" y="110" width="340" height="60" rx="4" fill="#fff" stroke="#e2e8f0" stroke-width="1"/>
<text x="30" y="130" font-size="10" fill="#475569">• QoS 0：发送后不确认，性能最高</text>
<text x="30" y="145" font-size="10" fill="#475569">• QoS 1：保证送达，接收方回传 PUBACK</text>
<text x="30" y="160" font-size="10" fill="#475569">• QoS 2：四次握手，保证不重不漏</text>
</svg>"""

SVGS["smart_home"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 230">
<rect x="10" y="10" width="340" height="210" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="180" y="30" text-anchor="middle" font-size="14" font-weight="bold">智能家居系统架构</text>
<!-- 云端 -->
<rect x="120" y="45" width="120" height="35" rx="8" fill="#e8f4fd" stroke="#2563eb" stroke-width="2"/>
<text x="180" y="67" text-anchor="middle" font-size="11" font-weight="bold" fill="#2563eb">云平台</text>
<!-- 网关 -->
<rect x="130" y="95" width="100" height="35" rx="6" fill="#fef6e4" stroke="#d0870a" stroke-width="2"/>
<text x="180" y="117" text-anchor="middle" font-size="11" fill="#d0870a">智能网关</text>
<!-- 设备行 -->
<rect x="20" y="155" width="70" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
<text x="55" y="172" text-anchor="middle" font-size="9" fill="#16a34a">智能灯泡</text>
<text x="55" y="184" text-anchor="middle" font-size="7" fill="#16a34a">WiFi/Zigbee</text>
<rect x="105" y="155" width="70" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
<text x="140" y="172" text-anchor="middle" font-size="9" fill="#16a34a">温湿度传感器</text>
<text x="140" y="184" text-anchor="middle" font-size="7" fill="#16a34a">Zigbee</text>
<rect x="190" y="155" width="70" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
<text x="225" y="172" text-anchor="middle" font-size="9" fill="#16a34a">智能门锁</text>
<text x="225" y="184" text-anchor="middle" font-size="7" fill="#16a34a">蓝牙</text>
<rect x="275" y="155" width="70" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
<text x="310" y="172" text-anchor="middle" font-size="9" fill="#16a34a">智能插座</text>
<text x="310" y="184" text-anchor="middle" font-size="7" fill="#16a34a">WiFi</text>
<!-- 连线 -->
<line x1="180" y1="80" x2="180" y2="93" stroke="#999" stroke-width="1.5"/>
<line x1="180" y1="130" x2="180" y2="153" stroke="#999" stroke-width="1.5"/>
<line x1="55" y1="155" x2="140" y2="130" stroke="#999" stroke-width="1" stroke-dasharray="3,3"/>
<line x1="310" y1="155" x2="220" y2="130" stroke="#999" stroke-width="1" stroke-dasharray="3,3"/>
</svg>"""

SVGS["iot_gateway"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 200">
<rect x="10" y="10" width="340" height="180" fill="#f8f9fa" stroke="#ccc" stroke-width="1"/>
<text x="180" y="30" text-anchor="middle" font-size="14" font-weight="bold">物联网网关组网示意图</text>
<!-- 网关 -->
<rect x="130" y="55" width="100" height="40" rx="8" fill="#e8f4fd" stroke="#2563eb" stroke-width="2.5"/>
<text x="180" y="80" text-anchor="middle" font-size="13" font-weight="bold" fill="#2563eb">物联网网关</text>
<!-- 云端 -->
<rect x="130" y="10" width="100" height="28" rx="6" fill="#dfd" stroke="#080" stroke-width="1.5"/>
<text x="180" y="29" text-anchor="middle" font-size="10" fill="#080">☁ 云端</text>
<!-- 协议转换 -->
<rect x="20" y="110" width="80" height="30" rx="4" fill="#fef6e4" stroke="#d0870a" stroke-width="1.5"/>
<text x="60" y="129" text-anchor="middle" font-size="9" fill="#d0870a">Zigbee节点</text>
<rect x="140" y="110" width="80" height="30" rx="4" fill="#fef6e4" stroke="#d0870a" stroke-width="1.5"/>
<text x="180" y="129" text-anchor="middle" font-size="9" fill="#d0870a">LoRa节点</text>
<rect x="260" y="110" width="80" height="30" rx="4" fill="#fef6e4" stroke="#d0870a" stroke-width="1.5"/>
<text x="300" y="129" text-anchor="middle" font-size="9" fill="#d0870a">蓝牙设备</text>
<!-- 传感器 -->
<circle cx="40" cy="165" r="6" fill="#fcc" stroke="#d00" stroke-width="1"/>
<circle cx="90" cy="165" r="6" fill="#fcc" stroke="#d00" stroke-width="1"/>
<circle cx="160" cy="165" r="6" fill="#fcc" stroke="#d00" stroke-width="1"/>
<circle cx="210" cy="165" r="6" fill="#fcc" stroke="#d00" stroke-width="1"/>
<circle cx="290" cy="165" r="6" fill="#fcc" stroke="#d00" stroke-width="1"/>
<circle cx="330" cy="165" r="6" fill="#fcc" stroke="#d00" stroke-width="1"/>
<!-- 连线 -->
<line x1="180" y1="38" x2="180" y2="53" stroke="#999" stroke-width="1.5"/>
<line x1="60" y1="110" x2="155" y2="95" stroke="#999" stroke-width="1"/>
<line x1="180" y1="110" x2="175" y2="95" stroke="#999" stroke-width="1"/>
<line x1="300" y1="110" x2="205" y2="95" stroke="#999" stroke-width="1"/>
<line x1="40" y1="158" x2="55" y2="140" stroke="#999" stroke-width="0.8"/>
<line x1="90" y1="158" x2="65" y2="140" stroke="#999" stroke-width="0.8"/>
<line x1="160" y1="158" x2="155" y2="140" stroke="#999" stroke-width="0.8"/>
<line x1="210" y1="158" x2="195" y2="140" stroke="#999" stroke-width="0.8"/>
<line x1="290" y1="158" x2="285" y2="140" stroke="#999" stroke-width="0.8"/>
<line x1="330" y1="158" x2="315" y2="140" stroke="#999" stroke-width="0.8"/>
<text x="180" y="195" text-anchor="middle" font-size="9" fill="#666">协议转换 · 数据汇聚 · 远程管理</text>
</svg>"""

# Create data URLs
images = {}
for name, svg in SVGS.items():
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    images[name] = "data:image/svg+xml;base64," + b64

# Build analysis questions
questions = []

# 传感器技术 - analysis questions
sensor_analysis = [
    {"id": 401, "text": "根据电阻应变片结构示意图，指出敏感栅、基底和引出线的作用。",
     "answer": "敏感栅是应变片的核心部分，将应变转换为电阻变化；基底起绝缘和支撑作用；引出线用于连接测量电路。",
     "explanation": "电阻应变片基于金属的应变效应工作，敏感栅材料通常为康铜或镍铬合金。"},
    {"id": 402, "text": "分析热电偶工作原理图中热端和冷端的作用，说明热电动势产生的条件。",
     "answer": "热端（T1）感受被测温度，冷端（T2）作为参考温度。当两端存在温差时，两种不同金属导体中产生热电动势，该电动势与温差成正比。",
     "explanation": "这就是塞贝克效应，热电动势大小取决于两种金属的材料特性和两端温度差。"},
    {"id": 403, "text": "根据电容式传感器原理图，分析极板间距 d 变化对电容量的影响，写出电容公式。",
     "answer": "电容公式为 C = εS/d，当极板间距 d 增大时电容量减小，d 减小时电容量增大。Δd 表示可动极板的位移量。",
     "explanation": "电容式传感器灵敏度高、动态响应快，适用于微小位移和压力测量。"},
    {"id": 404, "text": "分析压电效应原理图，说明外力 F 如何影响压电晶体的电荷分布。",
     "answer": "外力作用于压电晶体时，晶体内部发生极化，正负电荷中心分离，在晶体两端表面产生等量异号电荷。外力越大，产生的电荷量越多。",
     "explanation": "压电传感器只能测量动态信号，静态信号会因电荷泄漏而无法保持。"},
    {"id": 405, "text": "根据霍尔传感器原理图，说明霍尔电压 VH 与哪些因素有关，写出其表达式。",
     "answer": "霍尔电压 VH = k·I·B/d，与控制电流 I 成正比，与磁感应强度 B 成正比，与元件厚度 d 成反比。当 I 恒定时，VH 反映磁场强度。",
     "explanation": "霍尔传感器广泛用于位置检测、电流测量和转速测量等领域。"},
]
for q in sensor_analysis:
    q["type"] = "analysis"
    q["image"] = images[["strain_gage","thermocouple","capacitive_sensor","piezoelectric","hall_sensor"][q["id"]-401]]
    questions.append(q)

# 单片机技术 - analysis questions
mcu_analysis = [
    {"id": 401, "text": "分析51单片机最小系统原理图，指出构成最小系统的必要组件及各自的作用。",
     "answer": "最小系统包含单片机芯片（AT89C51）、晶振电路（提供时钟）、复位电路（初始化CPU）和电源（VCC和GND）。晶振决定了指令执行速度，复位电路使程序从初始地址开始运行。",
     "explanation": "51单片机最小系统是单片机正常工作的基本保障，缺一不可。"},
    {"id": 402, "text": "根据LED数码管结构图，说明共阴极与共阳极数码管的区别，以及段选和位选的概念。",
     "answer": "共阴极数码管公共端接地，段选端送高电平点亮；共阳极公共端接VCC，段选端送低电平点亮。段选控制显示数字，位选控制哪个数码管亮。",
     "explanation": "动态扫描显示利用人眼视觉暂留，逐位快速点亮数码管可减少I/O口占用。"},
    {"id": 403, "text": "分析4×4矩阵键盘原理图，说明行扫描法识别按键的工作原理。",
     "answer": "行扫描法逐行输出低电平（该行置0），同时读取各列线电平。当某键按下时，该行和该列的交点导通，列线被拉低。通过记录低电平的行号和列号即可确定按键位置。",
     "explanation": "矩阵键盘用8个I/O口可支持16个按键，比独立式键盘节省I/O资源。"},
    {"id": 404, "text": "根据串行异步通信时序图，说明一帧数据的组成及各部分的时间含义。",
     "answer": "一帧数据由起始位（1位低电平）、数据位（8位，D0~D7，低位在前）、停止位（1位高电平）组成。起始位通知接收方开始接收，数据位传输实际数据，停止位表示传输结束。",
     "explanation": "串行通信中波特率决定了每位数据的传输时间，需收发双方约定一致才行。"},
    {"id": 405, "text": "根据中断响应流程图，说明CPU响应中断的完整过程。",
     "answer": "主程序执行时，若有中断请求且中断允许，CPU暂停主程序执行，保存断点地址，跳转到中断服务程序执行，执行完毕后通过中断返回指令回到主程序被中断处继续执行。",
     "explanation": "中断系统提高了CPU的效率，使其能及时响应外部事件。"},
]
for q in mcu_analysis:
    q["type"] = "analysis"
    q["image"] = images[["mcu_min_sys","led_display","matrix_keypad","serial_timing","interrupt_flow"][q["id"]-401]]
    questions.append(q)

# 物联网系统设计 - analysis questions
iot_analysis = [
    {"id": 401, "text": "根据物联网三层架构图，说明各层的功能及数据流向。",
     "answer": "感知层采集数据，网络层传输数据，应用层处理和展示数据。数据流自下而上（感知→网络→应用），控制流自上而下（应用→网络→感知）。",
     "explanation": "物联网三层架构是最基本的体系结构，实际系统中网络层还可细分为传输层和网络层。"},
    {"id": 402, "text": "分析MQTT发布/订阅模型图，说明Broker、Publisher和Subscriber三者的关系。",
     "answer": "Publisher向Broker发送消息，Subscriber向Broker订阅特定Topic，Broker负责接收消息并转发给所有订阅该Topic的Subscriber。三者通过Topic解耦。",
     "explanation": "MQTT协议的发布/订阅模式实现了发送者和接收者的完全解耦。"},
    {"id": 403, "text": "对比分析MQTT三种QoS级别的特点和适用场景。",
     "answer": "QoS 0（最多一次）适合温湿度等周期性数据；QoS 1（至少一次）适合控制指令；QoS 2（恰好一次）适合计费等关键数据。级别越高可靠性越好但网络开销越大。",
     "explanation": "实际开发中QoS 0最常用（性能高），关键控制用QoS 1，极少用QoS 2。"},
    {"id": 404, "text": "根据智能家居系统架构图，说明各设备如何通过网关实现联动。",
     "answer": "各智能设备通过WiFi/Zigbee/蓝牙等不同协议连接至智能网关，网关统一管理并转发数据至云平台。用户通过手机App从云平台获取数据或发送控制指令，实现设备联动。",
     "explanation": "智能网关是智能家居的核心，负责协议转换和设备管理。"},
    {"id": 405, "text": "分析物联网网关的作用，说明网关如何连接不同协议的设备到云端。",
     "answer": "物联网网关连接Zigbee、LoRa、蓝牙等不同协议的网络节点，完成协议转换后将数据通过TCP/IP上传至云端。网关还可进行本地数据处理和缓存，降低云平台压力。",
     "explanation": "物联网网关是连接感知层和网络层的桥梁，是物联网系统中的关键设备。"},
]
for q in iot_analysis:
    q["type"] = "analysis"
    q["image"] = images[["iot_architecture","mqtt_protocol","mqtt_qos","smart_home","iot_gateway"][q["id"]-401]]
    questions.append(q)

# Save
with open("analysis_questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Generated {len(questions)} analysis questions with SVG data:image diagrams")
for q in questions:
    img_size = len(q["image"])
    print(f"  id={q['id']} text={q['text'][:40]}... img={img_size} bytes")
