// ============================================
// 配置 — 修改这里适配任何科目
// ============================================
var CONFIG = {
  subject: "电工电子技术",           // 科目名称
  subtitle: "复习系统",              // 副标题
  chapters: [                        // 章节列表
    "电路基本概念",
    "电路分析方法", 
    "交流电路",
    "安全用电",
    "半导体器件"
  ],
  types: {                           // 题型
    choice: "选择题",
    tf: "判断题",
    fill: "填空题", 
    calc: "计算题"
  },
  typeOrder: ["choice","tf","fill","calc"],  // 出题顺序
  modes: [                           // 练习模式
    { id: 0, icon: "🎲", name: "随机练习", desc: "所有题型混合抽题" },
    { id: 1, icon: "📋", name: "顺序练习", desc: "按类型顺序出题" },
    { id: "chapter", icon: "📂", name: "章节练习", desc: "选择章节专项练习" },
    { id: "type", icon: "🎯", name: "题型专练", desc: "选择题型集中训练" },
    { id: 2, icon: "🔄", name: "错题重练", desc: "只做之前答错的题" },
    { id: 3, icon: "🤖", name: "薄弱推荐", desc: "优先出掌握度低的题" }
  ],
  masteryLevels: ["未掌握","需加强","一般","良好","掌握"],  // 掌握度等级
  masteryColors: ["#d32f2f","#ef6c00","#fbc02d","#7cb342","#2e7d32"],  // 等级颜色
  defaultRoundSize: 20,              // 每轮默认题数
  autoNext: false,                   // 默认不自动下一题
};
