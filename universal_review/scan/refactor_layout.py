#!/usr/bin/env python3
"""重构设计稿：课程切换移到顶部"""
import re

with open("/Users/zzzzed/opencodes/electest/universal_review/scan/design_draft.html", "r", encoding="utf-8") as f:
    html = f.read()

# ---- 1. CSS: 添加课程切换栏样式 ----
css_add = """
.csb{display:flex;gap:6px;background:#f1f5f9;border-radius:10px;padding:4px;margin-bottom:20px}
.csb-item{flex:1;text-align:center;padding:10px 0;cursor:pointer;font-size:14px;font-weight:600;color:var(--muted);border-radius:8px;transition:all .12s}
.csb-item.a{background:var(--card);color:var(--text);box-shadow:0 1px 3px rgba(0,0,0,.08)}
.csb-item:active{transform:scale(.97)}
"""

# Insert after the @media block in CSS
html = html.replace(
    '@media(max-width:600px){.grid4{grid-template-columns:repeat(2,1fr)}.mg{grid-template-columns:repeat(2,1fr)}.cc{grid-template-columns:1fr}.app{max-width:100%;padding:16px 16px 0}}',
    '@media(max-width:600px){.grid4{grid-template-columns:repeat(2,1fr)}.mg{grid-template-columns:repeat(2,1fr)}.app{max-width:100%;padding:16px 16px 0}}' + css_add
)

# ---- 2. HTML: 替换课程卡片 + 看板内容 ----
# Find the dashboard section between <div class="pg a" id="p0"> and </div> (next page)
old_dashboard = '''  <div class="pg a" id="p0">
    <div class="hd"><div class="tt">数据看板</div><div class="info">复习进度总览</div></div>
    <div class="card">
      <div class="h3">选择科目</div>
      <div class="cc" style="margin-top:4px">
        <div class="ccd" onclick="switchCourse(0)">
          <div class="ci">📡</div>
          <div class="cn">传感器技术</div>
          <div class="cd">《传感器技术及应用》思考练习</div>
          <div class="cp"><span id="sensorTotal">165</span> 题 · 24 页</div>
        </div>
        <div class="ccd" onclick="switchCourse(1)">
          <div class="ci">💻</div>
          <div class="cn">单片机技术</div>
          <div class="cd">单片机应用系统设计 思考与练习题</div>
          <div class="cp"><span id="mcuTotal">165</span> 题 · 15 页</div>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="h3">科目信息</div>
      <div class="grid4" id="dashboardStats">
        <div class="g4"><div class="n" style="color:#2563eb">165</div><div class="l">总题数</div></div>
        <div class="g4"><div class="n" style="color:#16a34a">24</div><div class="l">PDF页数</div></div>
        <div class="g4"><div class="n" style="color:#7c3aed">330</div><div class="l">条目数</div></div>
        <div class="g4"><div class="n" style="color:#d97706">-</div><div class="l">含附图</div></div>
      </div>
    </div>
    <div class="card" id="overviewCard">
      <div class="h3">总体掌握度</div>
      <div style="text-align:center;padding:20px;color:var(--muted)">选择一个科目开始练习</div>
    </div>
  </div>'''

new_dashboard = '''  <div class="pg a" id="p0">
    <div class="hd"><div class="tt">数据看板</div><div class="info">复习进度总览</div></div>
    <div class="csb" id="csb"></div>
    <div class="card">
      <div class="grid4" id="dashboardStats">
        <div class="g4"><div class="n" style="color:#2563eb">0</div><div class="l">总题数</div></div>
        <div class="g4"><div class="n" style="color:#16a34a">0</div><div class="l">PDF页数</div></div>
        <div class="g4"><div class="n" style="color:#7c3aed">0</div><div class="l">条目数</div></div>
        <div class="g4"><div class="n" style="color:#d97706">0</div><div class="l">含附图</div></div>
      </div>
    </div>
    <div class="card" id="overviewCard">
      <div class="h3">总体掌握度</div>
      <div style="text-align:center;padding:20px;color:var(--muted)">选择一个科目开始练习</div>
    </div>
  </div>'''

html = html.replace(old_dashboard, new_dashboard)

# ---- 3. 练习页: 添加课程切换栏 ----
old_practice = '''  <div class="pg" id="p1">
    <div class="hd"><div class="tt" id="courseTitle">传感器技术</div><div class="info" id="progressInfo">已答 0/55 题</div></div>
    <div id="mArea"><div class="mg" id="mg"></div></div>
    <div id="qa" style="display:none"></div>
  </div>'''

new_practice = '''  <div class="pg" id="p1">
    <div class="hd"><div class="tt" id="courseTitle">传感器技术</div><div class="info" id="progressInfo">已答 0/165 题</div></div>
    <div class="csb" id="csb2"></div>
    <div id="mArea"><div class="mg" id="mg"></div></div>
    <div id="qa" style="display:none"></div>
  </div>'''

html = html.replace(old_practice, new_practice)

# ---- 4. 移除底部脚本中过时的 total 更新 ----
html = html.replace(
    'document.getElementById("sensorTotal").textContent = SUBJECTS[0].total;\ndocument.getElementById("mcuTotal").textContent = SUBJECTS[1].total;\n',
    ''
)

# ---- 5. 更新 JS 逻辑 ----
# Replace switchCourse to also update course switcher
old_switch = """function switchCourse(idx){
  curSubject = idx;
  document.getElementById("courseTitle").textContent = SUBJECTS[idx].name;
  document.getElementById("dashboardStats").innerHTML =
    '<div class="g4"><div class="n" style="color:#2563eb">'+SUBJECTS[idx].total+'</div><div class="l">总题数</div></div>'+
    '<div class="g4"><div class="n" style="color:#16a34a">'+SUBJECTS[idx].pages+'</div><div class="l">PDF页数</div></div>'+
    '<div class="g4"><div class="n" style="color:#7c3aed">'+SUBJECTS[idx].questions.length+'</div><div class="l">条目数</div></div>'+
    '<div class="g4"><div class="n" style="color:#d97706">'+(SUBJECTS[idx].questions.filter(function(q){return q.diagram}).length)+'</div><div class="l">含附图</div></div>';
  updateStats();
  buildPracticeGrid();
  document.querySelectorAll(".ti").forEach(function(t){ t.classList.remove("a"); });
  document.querySelectorAll(".pg").forEach(function(p){ p.classList.remove("a"); });
  document.querySelector('.ti[data-t="1"]').classList.add("a");
  document.getElementById("p1").classList.add("a");
}"""

new_switch = """function switchCourse(idx){
  curSubject = idx;
  document.getElementById("courseTitle").textContent = SUBJECTS[idx].name;
  document.getElementById("dashboardStats").innerHTML =
    '<div class="g4"><div class="n" style="color:#2563eb">'+SUBJECTS[idx].total+'</div><div class="l">总题数</div></div>'+
    '<div class="g4"><div class="n" style="color:#16a34a">'+SUBJECTS[idx].pages+'</div><div class="l">PDF页数</div></div>'+
    '<div class="g4"><div class="n" style="color:#7c3aed">'+SUBJECTS[idx].questions.length+'</div><div class="l">条目数</div></div>'+
    '<div class="g4"><div class="n" style="color:#d97706">0</div><div class="l">含附图</div></div>';
  document.querySelectorAll(".csb-item").forEach(function(e,i){ e.classList.toggle("a", i===idx); });
  updateStats();
  buildPracticeGrid();
  document.querySelectorAll(".ti").forEach(function(t){ t.classList.remove("a"); });
  document.querySelectorAll(".pg").forEach(function(p){ p.classList.remove("a"); });
  document.querySelector('.ti[data-t="1"]').classList.add("a");
  document.getElementById("p1").classList.add("a");
}"""

html = html.replace(old_switch, new_switch)

# ---- 6. 添加 buildCourseSwitcher 函数 ----
switcher_func = """
function buildCourseSwitcher(){
  var h = '';
  for(var i=0;i<SUBJECTS.length;i++){
    h += '<div class="csb-item'+(i===curSubject?' a':'')+'" onclick="switchCourse('+i+')">'+SUBJECTS[i].icon+' '+SUBJECTS[i].name+'</div>';
  }
  var e1 = document.getElementById("csb");
  if(e1) e1.innerHTML = h;
  var e2 = document.getElementById("csb2"); 
  if(e2) e2.innerHTML = h;
}"""

# Insert after buildPracticeGrid function
old_bpg = """function buildPracticeGrid(){
  var mg = document.getElementById("mg");
  mg.innerHTML = "";
  var total = SUBJECTS[curSubject].questions.filter(function(q){ return q.type !== 'title' && q.type !== 'heading'; }).length;
  var modes = ["""

html = html.replace(
    old_bpg,
    switcher_func + "\n" + old_bpg
)

# ---- 7. 初始化时调用 buildCourseSwitcher ----
html = html.replace(
    'loadProgress();\nupdateStats();\nbuildPracticeGrid();',
    'loadProgress();\nbuildCourseSwitcher();\nupdateStats();\nbuildPracticeGrid();'
)

# ---- 8. updateStats 使用动态 total 而非写死 ----
# Fix the progress info to use actual question count
old_prog = 'document.getElementById("progressInfo").textContent = "已答 "+done+"/"+total+" 题";'
# This is already dynamic, which is good. But the total number in static HTML was wrong.
# Let me fix the default progress text
html = html.replace('已答 0/165 题', '已答 0 题')

with open("/Users/zzzzed/opencodes/electest/universal_review/scan/design_draft.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✓ 重构完成")
