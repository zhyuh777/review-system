#!/usr/bin/env python3
"""按 parent index.html 框架重构 design_draft.html"""
import json

with open("/Users/zzzzed/opencodes/electest/universal_review/scan/questions.js", "r", encoding="utf-8") as f:
    js = f.read()
# strip "var SUBJECTS = " prefix and trailing ";"
import re
m = re.search(r"var SUBJECTS\s*=\s*(\[.*?\])\s*;", js, re.DOTALL)
if not m:
    raise ValueError("Could not parse SUBJECTS from questions.js")
SUBJECTS = json.loads(m.group(1))

# 读取并合并分析题到对应科目
try:
    with open("/Users/zzzzed/opencodes/electest/universal_review/scan/analysis_questions.json", "r", encoding="utf-8") as af:
        analysis_questions = json.load(af)
    # 分析题 id: 401-405 = 传感器, 406-410 = 单片机, 411-415 = 物联网
    per_subject = len(analysis_questions) // len(SUBJECTS)
    for i, q in enumerate(analysis_questions):
        sub_idx = i // per_subject
        SUBJECTS[sub_idx]["questions"].append(q)
    print(f"  合并分析题：{len(analysis_questions)} 题")
except FileNotFoundError:
    print("  未找到 analysis_questions.json，跳过分析题")

# 合并所有题目为扁平 QUESTION_BANK 格式，带 subject 字段
flat = []
for si, sub in enumerate(SUBJECTS):
    for q in sub["questions"]:
        item = {
            "id": f"S{si+1}-{q['id']}",
            "sub": si,
            "type": q["type"],
            "q": q.get("text", q.get("q", "")),
            "opts": q.get("options", []),
            "ans": q.get("answer"),
            "exp": q.get("explanation", ""),
        }
        if "image" in q:
            item["image"] = q["image"]
        flat.append(item)
QUESTION_BANK = flat

# 科目名列表
SUBJECT_NAMES = [s["name"] for s in SUBJECTS]

# 生成 types/chapters 配置
has_choice = any(q["type"]=="choice" for q in QUESTION_BANK)
has_tf = any(q["type"]=="tf" for q in QUESTION_BANK)  
has_fill = any(q["type"]=="fill" for q in QUESTION_BANK)
has_short = any(q["type"]=="short" for q in QUESTION_BANK)
has_analysis = any(q["type"]=="analysis" for q in QUESTION_BANK)
types_dict = {}
if has_choice: types_dict["choice"] = "选择题"
if has_tf: types_dict["tf"] = "判断题"
if has_fill: types_dict["fill"] = "填空题"
if has_short: types_dict["short"] = "简答题"
if has_analysis: types_dict["analysis"] = "分析题"
type_order = [k for k in ["choice","tf","fill","short","analysis"] if k in types_dict]

# 生成章节（直接用科目名）
chapters = list(SUBJECT_NAMES)

# Config
CONFIG = {
    "subject": "复习系统",
    "subjects": SUBJECT_NAMES,
    "chapters": chapters,
    "types": types_dict,
    "typeOrder": type_order,
    "modes": [
        {"id":0,"icon":"🎲","name":"随机练习","desc":"所有题型混合抽题"},
        {"id":1,"icon":"📋","name":"顺序练习","desc":"按类型顺序出题"},
        {"id":"chapter","icon":"📂","name":"章节练习","desc":"选择章节专项练习"},
        {"id":"type","icon":"🎯","name":"题型专练","desc":"选择题型集中训练"},
        {"id":2,"icon":"🔄","name":"错题重练","desc":"只做之前答错的题"},
        {"id":3,"icon":"🤖","name":"薄弱推荐","desc":"优先出掌握度低的题"},
    ],
    "masteryLevels": ["未掌握","需加强","一般","良好","掌握"],
    "masteryColors": ["#d32f2f","#ef6c00","#fbc02d","#7cb342","#2e7d32"],
    "defaultRoundSize": 20,
    "autoNext": False,
}

# 把 SUBJECTS 和 CONFIG 转为 JS 文本
subjects_js = "var SUBJECTS = " + json.dumps(SUBJECTS, ensure_ascii=False, indent=2) + ";\n"
config_js = "var CONFIG = " + json.dumps(CONFIG, ensure_ascii=False, indent=2) + ";\n"
qbank_js = "var QUESTION_BANK = " + json.dumps(QUESTION_BANK, ensure_ascii=False) + ";\n"

KERNEL = r"""
// ============================================
// 核心引擎 — 适配双科目
// ============================================
var C=CONFIG, QB=QUESTION_BANK;
var curSub=0, U="", N="", A={}, H=[], Q=[], I=0, Qc=null, MD="", CR={}, S={size:C.defaultRoundSize,auto:C.autoNext}, TM=null, SC={}, ST={};

function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
function sh(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}

// 按当前科目过滤题目
function qbs(){return QB.filter(function(q){return q.sub===curSub})}

function ld(){try{return JSON.parse(localStorage.getItem("_d"+U)||"{}")}catch(e){return{}}}
function sv(d){try{localStorage.setItem("_d"+U,JSON.stringify(d))}catch(e){}}
function rc(id){var p=ld();return p[id]||{a:0,c:0,lc:false,r5:[],f:false}}
function sr(id,r){var p=ld();p[id]=r;sv(p)}
function ms(id){var r=rc(id);if(r.a===0)return 0;var f=r.f?100:0;var re=r.r5.length>0?r.r5.filter(Boolean).length/r.r5.length*100:0;var pn=Math.max(0,(r.a-5)*3);return Math.max(0,Math.min(100,Math.round(.4*f+.5*re-.1*pn)))}
function ml(m){if(m<=20)return 1;if(m<=40)return 2;if(m<=60)return 3;if(m<=70)return 4;return 5}
function mc2(m){var i=ml(m)-1;return C.masteryColors[i]||"#ddd"}
function mb2(m){var i=ml(m)-1;return C.masteryLevels[i]||"未做"}
function ra(id,ok){var r=rc(id);r.a++;if(ok){r.c++;r.lc=true}else{r.lc=false}if(r.a===1)r.f=ok;r.r5.push(ok);if(r.r5.length>5)r.r5.shift();sr(id,r);A[id]=true;CR[id]=true}

function chM(ch){var si=C.subjects.indexOf(ch);if(si<0)return 0;var pool=QB.filter(function(q){return q.sub===si});var s=0;pool.forEach(function(q){s+=ms(q.id)});return pool.length?Math.round(s/pool.length):0}
function tpS(t){var pool=qbs().filter(function(q){return q.type===t});var d=0;pool.forEach(function(q){if(ms(q.id)>0)d++});return{t:pool.length,d:d}}
function st(){var pool=qbs(),t=pool.length,d=0,s=0;pool.forEach(function(q){var m=ms(q.id);if(m>0)d++;s+=m});return{t:t,d:d,m:t?Math.round(s/t):0}}

// 课程切换
function cs(idx){
  curSub=idx;
  document.querySelectorAll(".csb-item").forEach(function(e,i){e.classList.toggle("a",i===idx)});
  rd();buildPracticeGrid();
}
function buildCourseSwitcher(){
  var h='';SUBJECTS.forEach(function(s,i){h+='<div class="csb-item'+(i===curSub?' a':'')+'" onclick="cs('+i+')">'+s.icon+' '+s.name+'</div>'});
  document.querySelectorAll(".csb").forEach(function(e){e.innerHTML=h});
}

function buildPracticeGrid(){
  var mg=document.getElementById("mg");mg.innerHTML="";
  C.modes.forEach(function(m){
    var cls=typeof m.id==="number"?"":m.id;
    mg.innerHTML+='<div class="mc" onclick="sm('+(typeof m.id==="number"?m.id:"'"+m.id+"'")+')"><span class="mi">'+m.icon+'</span><div class="mn">'+m.name+'</div><div class="md">'+m.desc+'</div></div>';
  });
}

// 登录
(function(){
  document.getElementById("loginTitle").textContent="通用复习系统";
  document.getElementById("loginSub").textContent=C.subjects.join(" · ");
  buildCourseSwitcher();buildPracticeGrid();
  try{var s=localStorage.getItem("_ul");if(s){var d=JSON.parse(s);if(d.u&&d.n){U=d.u;N=d.n;go()}}}catch(e){}
})();

document.getElementById("lbtn").onclick=function(){
  var i=document.getElementById("si").value.trim(),n=document.getElementById("sn").value.trim();
  if(!i||!n){document.getElementById("le").style.display="block";return}
  document.getElementById("le").style.display="none";U=i;N=n;
  try{localStorage.setItem("_ul",JSON.stringify({u:U,n:N}))}catch(e){}go();
};

function go(){
  document.getElementById("lp").classList.add("hide");document.getElementById("app").classList.add("s");
  try{var p=JSON.parse(localStorage.getItem("_d"+U)||"{}");Object.keys(p).forEach(function(k){if(p[k].a>0)A[k]=true})}catch(e){}
  try{var hs=localStorage.getItem("_his"+U);if(hs)H=JSON.parse(hs);if(!Array.isArray(H))H=[]}catch(e){H=[]}
  rd();ins();
}
function lo(){if(!confirm("切换用户？"))return;U="";N="";A={};document.getElementById("app").classList.remove("s");document.getElementById("lp").classList.remove("hide")}

// 看板
function rd(){
  var d=new Date();document.getElementById("dt").textContent=d.getFullYear()+"."+(d.getMonth()+1)+"."+d.getDate();var s=st();
  document.getElementById("g1").innerHTML='<div class="g4"><div class="n" style="color:#2563eb">'+s.t+'</div><div class="l">总题库</div></div><div class="g4"><div class="n" style="color:#7c3aed">'+s.d+'</div><div class="l">已完成</div></div><div class="g4"><div class="n" style="color:#16a34a">'+s.m+'%</div><div class="l">掌握度</div></div><div class="g4"><div class="n" style="color:#d97706">'+(s.t-s.d)+'</div><div class="l">待攻克</div></div>';
  document.getElementById("ov").innerHTML='<div style="display:flex;justify-content:space-between;font-size:13px"><span>'+mb2(s.m)+'</span><span style="font-weight:700">'+s.m+'%</span></div><div class="bar"><div class="bf" style="width:'+s.m+'%;background:'+mc2(s.m)+'"></div></div><div class="leg"><span>●'+C.masteryLevels[0]+'</span><span>●'+C.masteryLevels[1]+'</span><span>●'+C.masteryLevels[2]+'</span><span>●'+C.masteryLevels[3]+'</span><span>●'+C.masteryLevels[4]+'</span></div>';
  var h="";C.chapters.forEach(function(ch){var m=chM(ch);h+='<div class="pr"><span class="dot" style="background:'+mc2(m)+'"></span><span style="flex:0 0 90px">'+ch+'</span><div class="tr"><div class="fl" style="width:'+m+'%;background:'+mc2(m)+'"></div></div><span class="pct" style="color:'+mc2(m)+'">'+m+'%</span></div>'});document.getElementById("ch").innerHTML=h;
  var th="";C.typeOrder.forEach(function(t){var st=tpS(t);var p=st.t?Math.round(st.d/st.t*100):0;th+='<div class="pr"><span style="flex:0 0 50px;font-size:12px;color:#64748b">'+(C.types[t]||t)+'</span><span style="font-size:11px;color:#64748b;flex:0 0 44px">'+st.d+'/'+st.t+'</span><div class="tr"><div class="fl" style="width:'+p+'%;background:#2563eb"></div></div><span class="pct" style="color:#2563eb">'+p+'%</span></div>'});document.getElementById("tp").innerHTML=th;
  document.getElementById("ps").textContent="已答 "+s.d+"/"+s.t+" 题";
  document.getElementById("sr").innerHTML=H&&H.length?renderHistory():'<div style="color:#64748b;text-align:center;padding:12px">暂无练习记录</div>';
}
function renderHistory(){
  var ms={};H.forEach(function(h){if(!ms[h.md])ms[h.md]={t:0,c:0};ms[h.md].t+=h.t;ms[h.md].c+=h.c});
  var hs="";for(var k in ms){var r=ms[k].t?Math.round(ms[k].c/ms[k].t*100):0;hs+='<div class="g4" style="display:inline-block;margin:4px;min-width:120px"><div class="n" style="font-size:24px;color:'+(r>=80?"#16a34a":r>=60?"#2563eb":r>=40?"#d97706":"#dc2626")+'">'+r+'%</div><div class="l">'+k+' ('+ms[k].c+'/'+ms[k].t+')</div></div>'}
  return hs;
}

// 练习
function sm(m){
  if(typeof m==="string"&&!isNaN(m))m=Number(m);
  var p=[],sz=S.size||20;
  if(m==="chapter"){scs();return}
  if(m==="type"){sts();return}
  var pool=qbs();
  if(typeof m==="number"){
    if(m===0){C.typeOrder.forEach(function(t){var p2=pool.filter(function(q){return q.type===t});sh(p2);p=p.concat(p2.slice(0,Math.ceil(sz/C.typeOrder.length)))});sh(p);}
    else if(m===1){C.typeOrder.forEach(function(t){pool.filter(function(q){return q.type===t}).slice(0,Math.ceil(sz/C.typeOrder.length)).forEach(function(q){p.push(q)})});}
    else if(m===2){p=pool.filter(function(q){var r=rc(q.id);return r.a>0&&!r.lc});sh(p);}
    else if(m===3){p=pool.slice().sort(function(a,b){return ms(a.id)-ms(b.id)});}
  }
  if(!p.length){alert("无题");return}
  p=p.slice(0,sz>0?sz:p.length);
  MD=typeof m==="string"?m:String(m);CR={};Q=p;I=0;
  document.getElementById("mArea").style.display="none";document.getElementById("qa").style.display="block";sq();
}
function ext(){var c=0;Q.forEach(function(x){if(x._ok)c++});if(Q.length>0){H.push({md:MD,t:Q.length,c:c,d:new Date().toISOString().slice(0,10)});if(H.length>30)H.shift();try{localStorage.setItem("_his"+U,JSON.stringify(H))}catch(e){}}Q=[];I=0;Qc=null;document.getElementById("mArea").style.display="block";document.getElementById("qa").style.display="none";rd()}

function sq(){
  if(I>=Q.length){var c=0;Q.forEach(function(x){if(x._ok)c++});H.push({md:MD,t:Q.length,c:c,d:new Date().toISOString().slice(0,10)});if(H.length>30)H.shift();try{localStorage.setItem("_his"+U,JSON.stringify(H))}catch(e){}alert("完成！"+Q.length+"题，正确"+c+"题("+Math.round(c/Q.length*100)+"%)");ext();return}
  Qc=Q[I];var q=Qc;
  var tc=q.type?q.type[0]:"c";
  var h='<div style="margin-bottom:8px;display:flex;gap:8px"><button class="btn bo" onclick="ext()" style="flex:none;padding:8px 16px">← 退出</button><button class="btn bo" onclick="regen()" style="flex:none;padding:8px 16px;color:#d97706">换一套</button></div><div class="qw"><div class="qm"><span><span class="qt qt'+tc+'">'+(C.types[q.type]||q.type)+'</span></span><span>'+(I+1)+'/'+Q.length+'</span></div>';
  if(q.image)h+='<div style="text-align:center;margin:12px 0"><img src="'+q.image+'" style="max-width:100%;min-width:200px;min-height:150px;border:1px solid var(--border);border-radius:8px"></div>';
  h+='<div class="qtx">'+(I+1)+'. '+esc(q.q)+'</div>';
  if(q.type==="choice"){h+='<div>';var lb=["A","B","C","D"];for(var i=0;i<(q.opts||[]).length;i++)h+='<div class="qo" onclick="so(this,'+i+')"><span class="lt">'+lb[i]+'</span>'+esc(q.opts[i])+'</div>';h+='</div>'}
  else if(q.type==="tf"){h+='<div style="display:flex;gap:10px"><div class="tfb" onclick="tf(this,true)">✓ 正确</div><div class="tfb" onclick="tf(this,false)">✗ 错误</div></div>'}
  else if(q.type==="fill"){h+='<input class="inp" id="fi" placeholder="输入答案...">'}
  else if(q.type==="analysis"){h+='<textarea class="inp" id="ci" placeholder="输入你的分析..." rows="4"></textarea>'}
  else{h+='<textarea class="inp" id="ci" placeholder="输入..." rows="3"></textarea>'}
  h+='<div class="res" id="res"></div><div class="btns"><button class="btn bp" id="ckB" onclick="ck()" '+(q.type==="choice"||q.type==="tf"?"disabled":"")+'>检查</button><button class="btn bo" id="nxB" style="display:none" onclick="nx()">下一题</button></div><div class="nd">';
  for(var i=0;i<Q.length;i++){var c2=(i===I)?"cu":(CR[Q[i].id]?(Q[i]._ok?"ok":"no"):"");h+='<span class="nd-d '+c2+'" onclick="jmp('+i+')"></span>'}
  h+='</div></div>';document.getElementById("qa").innerHTML=h;
}

function so(el,i){document.querySelectorAll(".qo").forEach(function(o){o.classList.remove("sel")});el.classList.add("sel");el._i=i;document.getElementById("ckB").disabled=false}
function tf(el,v){document.querySelectorAll(".tfb").forEach(function(b){b.classList.remove("st","sf")});el.classList.add(v?"st":"sf");el._v=v;document.getElementById("ckB").disabled=false}

function at(q){
  if(q.type==="choice"&&q.ans!==undefined&&q.ans!==null&&q.opts)
    return ["A","B","C","D"][q.ans]+". "+q.opts[q.ans];
  if(q.type==="tf")return q.ans?"正确":"错误";
  return ""
}

function ck(){
  if(!Qc)return;var q=Qc,ok=false;
  if(q.type==="choice"){var s=document.querySelector(".qo.sel");if(!s){alert("请选择");return}ok=(s._i===q.ans);document.querySelectorAll(".qo").forEach(function(o,i){if(i===q.ans)o.classList.add("ok");else if(o.classList.contains("sel")&&i!==q.ans)o.classList.add("no")})}
  else if(q.type==="tf"){var s=document.querySelector(".tfb.st,.tfb.sf");if(!s){alert("请选择");return}ok=(s._v===q.ans);document.querySelectorAll(".tfb").forEach(function(b){if(b._v===q.ans)b.style.borderColor="#16a34a";else if(b._v===s._v&&b._v!==q.ans)b.style.borderColor="#dc2626"})}
  else{
    var h='<div style="font-size:16px;font-weight:600;margin-bottom:8px">📖 解析</div>';
    if(q.ans!==undefined&&q.ans!==null)
      h+='<div style="margin-bottom:6px"><b>答案：</b>'+esc(String(q.ans))+'</div>';
    if(q.exp)
      h+='<div style="padding:12px;background:#f0fdf4;border-radius:8px;margin-bottom:10px;font-size:14px;line-height:1.8">'+esc(q.exp)+'</div>';
    h+='<div style="display:flex;gap:8px"><button class="btn bs" onclick="sj(true)" style="flex:1;padding:10px;border-radius:8px;font-size:14px">✓ 对</button><button class="btn be" onclick="sj(false)" style="flex:1;padding:10px;border-radius:8px;font-size:14px">✗ 错</button></div>';
    document.getElementById("res").className="res s";
    document.getElementById("res").innerHTML=h;
    document.getElementById("ckB").disabled=true;return}
  fi(ok);
}
function sj(ok){
  ra(Qc.id,ok);Qc._ok=ok;
  var r=document.getElementById("res"),q=Qc;
  r.innerHTML+='<div style="margin-top:10px;font-weight:600;font-size:15px;text-align:center">'+(ok?"✅ 正确":"❌ 错误")+'</div>';
  document.getElementById("ckB").disabled=true;document.getElementById("nxB").style.display="";if(S.auto)TM=setTimeout(nx,2000);rd()
}
function fi(ok){ra(Qc.id,ok);Qc._ok=ok;var r=document.getElementById("res"),q=Qc;r.className="res s "+(ok?"good":"bad");var h=(ok?"✅ 正确":"❌ 错误");h+='<div style="font-size:13px;margin-top:6px"><b>正确答案：</b>'+esc(at(q))+'</div>';if(q.exp)h+='<div style="font-size:13px;margin-top:4px;color:#475569;line-height:1.6">'+esc(q.exp)+'</div>';r.innerHTML=h;document.getElementById("ckB").disabled=true;document.getElementById("nxB").style.display="";if(S.auto)TM=setTimeout(nx,2000);rd()}
function nx(){clearTimeout(TM);I++;sq()}
function jmp(i){clearTimeout(TM);I=i;sq()}
function regen(){if(!confirm("换一套？"))return;sm(MD)}

function scs(){
  var h="";C.chapters.forEach(function(ch,i){var m=chM(ch);h+='<div class="cs" onclick="tglc(this,'+i+')"><div class="cbx"></div><div style="flex:1"><div>'+ch+'</div><div style="font-size:11px;color:#64748b">掌握度 '+m+'%</div></div></div>'});
  document.getElementById("m1b").innerHTML=h;SC={};
  document.getElementById("m1g").onclick=function(){var chs=[];for(var k in SC){if(SC[k])chs.push(k)}var pool=qbs();var p=chs.length?pool.filter(function(q){return chs.some(function(ch){return q.sub===C.subjects.indexOf(ch)})}):pool.slice();cx(1);if(!p.length){alert("无题");return}MD="chapter";CR={};Q=sh(p);var s=S.size;if(s>0&&Q.length>s)Q=Q.slice(0,s);I=0;document.getElementById("mArea").style.display="none";document.getElementById("qa").style.display="block";sq()};
  document.getElementById("m1").classList.add("s");
}
function tglc(el,i){var cb=el.querySelector(".cbx");cb.classList.toggle("on");if(cb.classList.contains("on"))SC[C.chapters[i]]=true;else delete SC[C.chapters[i]]}

function sts(){
  var h="";C.typeOrder.forEach(function(t,i){var st=tpS(t);h+='<div class="cs" onclick="tglt(this,'+i+')"><div class="cbx"></div><div style="flex:1"><div>'+(C.types[t]||t)+'</div><div style="font-size:11px;color:#64748b">'+st.d+'/'+st.t+'题</div></div></div>'});
  document.getElementById("m2b").innerHTML=h;ST={};
  document.getElementById("m2g").onclick=function(){var ks=[];for(var k in ST){if(ST[k])ks.push(k)}var pool=qbs();var p=ks.length?pool.filter(function(q){return ST[q.type]}):pool.slice();cx(2);if(!p.length){alert("无题");return}MD="type";CR={};Q=sh(p);var s=S.size;if(s>0&&Q.length>s)Q=Q.slice(0,s);I=0;document.getElementById("mArea").style.display="none";document.getElementById("qa").style.display="block";sq()};
  document.getElementById("m2").classList.add("s");
}
function tglt(el,i){var cb=el.querySelector(".cbx");cb.classList.toggle("on");if(cb.classList.contains("on"))ST[C.typeOrder[i]]=true;else delete ST[C.typeOrder[i]]}
function cx(n){document.getElementById("m"+n).classList.remove("s")}

function ins(){
  var sz=document.getElementById("sz");sz.innerHTML="";[10,20,30,50,0].forEach(function(n){var e=document.createElement("span");if(n===S.size)e.className="a";e.textContent=n||"全";e.onclick=function(){S.size=n;ins()};sz.appendChild(e)});
  var au=document.getElementById("au");au.innerHTML="";[1,0].forEach(function(v){var e=document.createElement("span");if(v===(S.auto?1:0))e.className="a";e.textContent=v?"自动":"手动";e.onclick=function(){S.auto=v===1;ins()};au.appendChild(e)});
}
function exp(){var d=localStorage.getItem("_d"+U)||"{}";var b=new Blob([d],{type:"application/json"});var a=document.createElement("a");a.href=URL.createObjectURL(b);a.download=U+"_"+new Date().toISOString().slice(0,10)+".json";document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(a.href)}
function rst(){if(confirm("确定重置？")){localStorage.removeItem("_d"+U);A={};H=[];rd();alert("已重置")}}
document.getElementById("fi").onchange=function(e){var f=e.target.files[0];if(!f)return;var r=new FileReader();r.onload=function(ev){try{var d=JSON.parse(ev.target.result);localStorage.setItem("_d"+U,JSON.stringify(d));A={};Object.keys(d).forEach(function(k){if(d[k].a>0)A[k]=true});rd();alert("成功")}catch(ex){alert("失败")}};r.readAsText(f)}

document.querySelectorAll(".ti").forEach(function(el){el.onclick=function(){document.querySelectorAll(".ti").forEach(function(t){t.classList.remove("a")});document.querySelectorAll(".pg").forEach(function(p){p.classList.remove("a")});el.classList.add("a");document.getElementById("p"+el.dataset.t).classList.add("a");if(el.dataset.t==="0")rd()}});
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>通用复习系统 · 传感器 · 单片机 · 物联网</title>
<style>
:root{--bg:#f5f7fa;--card:#fff;--text:#1e293b;--muted:#64748b;--border:#e2e8f0;--pri:#2563eb;--succ:#16a34a;--err:#dc2626;--r:16px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);padding-bottom:90px}
.login{position:fixed;inset:0;z-index:999;display:flex;align-items:center;justify-content:center;background:var(--bg);padding:20px}
.login.hide{display:none}
.lb{background:var(--card);border-radius:24px;padding:40px 32px;width:100%;max-width:360px;text-align:center;box-shadow:0 2px 16px rgba(0,0,0,.06)}
.lb h1{font-size:24px;font-weight:700;margin-bottom:4px}
.lb p{font-size:14px;color:var(--muted);margin-bottom:28px}
.lb input{width:100%;padding:14px 16px;border:1.5px solid var(--border);border-radius:12px;font-size:15px;margin-bottom:12px;outline:none}
.lb input:focus{border-color:var(--pri)}
.lb button{width:100%;padding:14px;border:none;border-radius:12px;background:var(--pri);color:#fff;font-size:15px;font-weight:600;cursor:pointer}
.lb .err{color:var(--err);font-size:12px;margin-top:10px;display:none}
.app{max-width:76vw;margin:0 auto;padding:24px 40px 0;display:none}
.app.s{display:block}
.hd{display:flex;justify-content:space-between;align-items:flex-end;padding:4px 0 20px;margin-bottom:20px;border-bottom:1px solid var(--border)}
.hd .tt{font-size:28px;font-weight:800}
.hd .info{font-size:13px;color:var(--muted)}
.csb{display:flex;gap:6px;background:#f1f5f9;border-radius:10px;padding:4px;margin-bottom:20px}
.csb-item{flex:1;text-align:center;padding:10px 0;cursor:pointer;font-size:14px;font-weight:600;color:var(--muted);border-radius:8px;transition:all .12s}
.csb-item.a{background:var(--card);color:var(--text);box-shadow:0 1px 3px rgba(0,0,0,.08)}
.csb-item:active{transform:scale(.97)}
.card{background:var(--card);border-radius:var(--r);padding:24px 28px;margin-bottom:16px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
.h3{font-size:15px;font-weight:600;color:var(--muted);margin-bottom:14px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.g4{background:var(--card);border-radius:var(--r);padding:24px 16px;text-align:center}
.g4 .n{font-size:32px;font-weight:800}.g4 .l{font-size:12px;color:var(--muted);margin-top:4px}
.bar{height:10px;background:#e5e7eb;border-radius:5px;overflow:hidden;margin:6px 0 12px}
.bf{height:100%;border-radius:5px;transition:width .6s}
.leg{display:flex;justify-content:space-between;font-size:10px;color:var(--muted)}
.pr{display:flex;align-items:center;gap:12px;padding:10px 0;font-size:14px}
.pr+.pr{border-top:1px solid #f1f5f9}
.pr .tr{flex:1;height:7px;background:#e5e7eb;border-radius:4px;overflow:hidden}
.pr .fl{height:100%;border-radius:4px;transition:width .5s}
.pr .pct{font-weight:600;min-width:36px;text-align:right;font-size:13px}
.pr .dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.mg{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.mc{padding:24px 14px;background:var(--card);border-radius:var(--r);text-align:center;cursor:pointer;transition:all .12s}
.mc:active{transform:scale(.97)}
.mc .mi{font-size:30px;margin-bottom:8px;display:block}
.mc .mn{font-size:14px;font-weight:600}
.mc .md{font-size:11px;color:var(--muted);margin-top:4px}
.qw{background:var(--card);border-radius:var(--r);padding:24px}
.qm{display:flex;justify-content:space-between;margin-bottom:14px;font-size:12px;color:var(--muted)}
.qt{padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600}
.qtc{background:#eff6ff;color:var(--pri)}.qtt{background:#fef3c7;color:#d97706}.qtf{background:#f3e8ff;color:#7c3aed}.qtp{background:#fce4ec;color:var(--err)}.qts{background:#e0f2fe;color:#0284c7}.qta{background:#fce7f3;color:#db2777}
.qtx{font-size:16px;line-height:1.7;margin-bottom:18px}
.qo{display:flex;align-items:center;gap:10px;padding:13px 16px;border:1.5px solid var(--border);border-radius:10px;margin-bottom:6px;cursor:pointer}
.qo .lt{width:28px;height:28px;border-radius:50%;background:#f1f5f9;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:600;color:var(--muted);flex-shrink:0}
.qo.sel{border-color:var(--pri);background:#eff6ff}.qo.sel .lt{background:var(--pri);color:#fff}
.qo.ok{border-color:var(--succ);background:#f0fdf4}.qo.ok .lt{background:var(--succ);color:#fff}
.qo.no{border-color:var(--err);background:#fef2f2}.qo.no .lt{background:var(--err);color:#fff}
.tfb{flex:1;padding:15px;border:1.5px solid var(--border);border-radius:10px;text-align:center;cursor:pointer;font-size:14px;font-weight:600}
.tfb.st{border-color:var(--succ);color:var(--succ);background:#f0fdf4}
.tfb.sf{border-color:var(--err);color:var(--err);background:#fef2f2}
.inp{width:100%;padding:12px 16px;border:1.5px solid var(--border);border-radius:10px;font-size:15px;outline:none;margin-bottom:8px}
.inp:focus{border-color:var(--pri)}
.res{padding:14px 18px;border-radius:10px;font-size:15px;display:none;margin-bottom:8px}
.res.s{display:block}.res.good{background:#f0fdf4;color:var(--succ)}.res.bad{background:#fef2f2;color:var(--err)}
.btns{display:flex;gap:8px;padding:6px 0 2px}
.btn{flex:1;padding:12px;border:none;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit}
.bp{background:var(--pri);color:#fff}.bo{background:transparent;border:1.5px solid var(--border)}
.bs{background:var(--succ);color:#fff}.be{background:var(--err);color:#fff}
.nd{display:flex;gap:4px;justify-content:center;padding:10px 0 2px;flex-wrap:wrap}
.nd-d{width:10px;height:10px;border-radius:50%;background:#d1d5db;cursor:pointer;flex-shrink:0}
.nd-d.cu{border:2px solid var(--pri);background:var(--pri);transform:scale(1.3)}
.nd-d.ok{background:var(--succ)}.nd-d.no{background:var(--err)}
.tab{position:fixed;bottom:12px;left:50%;transform:translateX(-50%);width:92%;max-width:560px;background:var(--card);border-radius:20px;box-shadow:0 2px 12px rgba(0,0,0,.08);display:flex;padding:4px;z-index:100}
.ti{flex:1;text-align:center;padding:14px 0;cursor:pointer;font-size:15px;font-weight:600;color:var(--muted);border-radius:16px}
.ti.a{background:var(--pri);color:#fff}
.pg{display:none}.pg.a{display:block}
.mo{display:none;position:fixed;inset:0;background:rgba(0,0,0,.25);z-index:200;align-items:flex-end;justify-content:center}
.mo.s{display:flex}
.ms{background:var(--card);border-radius:20px 20px 0 0;width:100%;max-width:500px;max-height:70vh;overflow:hidden;display:flex;flex-direction:column}
.mh{padding:16px 20px;border-bottom:1px solid var(--border);font-size:16px;font-weight:600;display:flex;justify-content:space-between}
.mb{padding:8px 20px 14px;overflow-y:auto;flex:1}
.mf{padding:12px 20px;border-top:1px solid var(--border);display:flex;gap:8px;justify-content:flex-end}
.cs{display:flex;align-items:center;gap:10px;padding:12px 0;cursor:pointer}
.cs+.cs{border-top:1px solid #f1f5f9}
.cbx{width:20px;height:20px;border:2px solid #d1d5db;border-radius:5px;flex-shrink:0;display:flex;align-items:center;justify-content:center}
.cbx.on{background:var(--pri);border-color:var(--pri)}
.cbx.on::after{content:"✓";color:#fff;font-size:11px;font-weight:700}
.sr{display:flex;justify-content:space-between;align-items:center;padding:12px 0;font-size:14px}
.sr+.sr{border-top:1px solid #f1f5f9}
.sgg{display:flex;gap:4px;background:#f1f5f9;border-radius:8px;padding:3px}
.sgg span{padding:6px 14px;border-radius:7px;font-size:12px;cursor:pointer}
.sgg span.a{background:var(--card);box-shadow:0 1px 2px rgba(0,0,0,.08)}
.sb{padding:6px 16px;border-radius:8px;border:1px solid var(--err);background:transparent;color:var(--err);font-size:12px;cursor:pointer}
.sb.bl{border-color:var(--pri);color:var(--pri)}
@media(max-width:600px){.grid4{grid-template-columns:repeat(2,1fr)}.mg{grid-template-columns:repeat(2,1fr)}.app{max-width:100%;padding:16px 16px 0}}
</style>
</head>
<body>

<div class="login" id="lp">
  <div class="lb">
    <h1 id="loginTitle"></h1>
    <p id="loginSub"></p>
    <input id="si" placeholder="学号"><input id="sn" placeholder="姓名">
    <button id="lbtn">进入系统</button>
    <div class="err" id="le">请填写学号和姓名</div>
  </div>
</div>

<div class="app" id="app">
  <div class="pg a" id="p0">
    <div class="hd"><div class="tt">数据看板</div><div class="info"><span id="dt"></span></div></div>
    <div class="csb" id="csb"></div>
    <div class="grid4" id="g1"></div>
    <div class="card"><div class="h3">总体掌握度</div><div id="ov"></div></div>
    <div class="card"><div class="h3">各章节</div><div id="ch"></div></div>
    <div class="card"><div class="h3">各题型</div><div id="tp"></div></div>
    <div class="card"><div class="h3">练习记录</div><div id="sr"></div></div>
  </div>
  <div class="pg" id="p1">
    <div class="hd"><div class="tt">练习中心</div><div class="info" id="ps"></div></div>
    <div class="csb" id="csb2"></div>
    <div id="mArea"><div class="mg" id="mg"></div></div>
    <div id="qa" style="display:none"></div>
  </div>
  <div class="pg" id="p2">
    <div class="hd"><div class="tt">设置</div></div>
    <div class="card">
      <div class="sr"><span style="font-weight:600">当前用户</span><button class="sb" onclick="lo()">切换</button></div>
      <div class="sr"><span style="font-weight:600">重置进度</span><button class="sb" onclick="rst()">重置</button></div>
      <div class="sr"><span style="font-weight:600">导出数据</span><button class="sb bl" onclick="exp()">导出</button></div>
      <div class="sr"><span style="font-weight:600">导入数据</span><button class="sb bl" onclick="document.getElementById('fi').click()">导入</button><input type="file" id="fi" accept=".json" style="display:none"></div>
    </div>
    <div class="card">
      <div class="sr"><span style="font-weight:600">每轮题数</span><div class="sgg" id="sz"></div></div>
      <div class="sr"><span style="font-weight:600">自动下一题</span><div class="sgg" id="au"></div></div>
      <div style="text-align:center;margin-top:10px;font-size:12px;color:var(--muted)" id="infoBar"></div>
    </div>
  </div>
</div>

<div class="tab"><div class="ti a" data-t="0">看板</div><div class="ti" data-t="1">练习</div><div class="ti" data-t="2">设置</div></div>

<div class="mo" id="m1"><div class="ms"><div class="mh"><span>选择章节</span><span style="cursor:pointer;font-size:20px;color:var(--muted)" onclick="cx(1)">✕</span></div><div class="mb" id="m1b"></div><div class="mf"><button class="btn bo" onclick="cx(1)">取消</button><button class="btn bp" id="m1g">开始</button></div></div></div>
<div class="mo" id="m2"><div class="ms"><div class="mh"><span>选择题型</span><span style="cursor:pointer;font-size:20px;color:var(--muted)" onclick="cx(2)">✕</span></div><div class="mb" id="m2b"></div><div class="mf"><button class="btn bo" onclick="cx(2)">取消</button><button class="btn bp" id="m2g">开始</button></div></div></div>

<script>
""" + subjects_js + config_js + qbank_js + KERNEL + """
</script>
</body>
</html>"""

with open("/Users/zzzzed/opencodes/electest/universal_review/scan/design_draft.html", "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

print("✓ 重构完成：登录 + 双科目 + 自动批改 + 设置页 + 模态框")
print(f"  题库：{len(QUESTION_BANK)} 题")
print(f"  全文件：{len(HTML_TEMPLATE)} 字节")
