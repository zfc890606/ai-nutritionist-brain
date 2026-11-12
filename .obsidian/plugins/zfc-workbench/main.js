const {
	Plugin,
	ItemView,
	Modal,
	Notice,
	PluginSettingTab,
	Setting,
	setIcon
} = require("obsidian");

const VIEW_TYPE = "zfc-workbench-view";

/* ============================================================
 * 模块（六张卡片 + 两个隐藏挖矿模块）
 * ============================================================ */

const MODULES = [
	{
		key: "video",
		title: "写视频号",
		icon: "video",
		color: "#e5534b",
		desc: "从选题到成片脚本，全流程走完，写完自动入库。",
		steps: [
			["过两道关", "涨粉配比闸门 + 0 号闸门，一票否决"],
			["两条一级铁律", "身份独占（我在医院那几年）+ 转发三件套，缺一不交付"],
			["读痛点", "读痛点排行榜 + 知识库"],
			["定选题", "选爆款元素 → 词根变换 → 2-3 个候选"],
			["开头句式", "按词根查映射表，必轮换；优先争议场景／数字反差"],
			["过决策卡", "6 问 8 分 + 涨粉复核 + 味道嵌入"],
			["写稿", "四支柱 + 老师式表达 + 真实感写作法"],
			["自检", "开头 3 秒 + 身份安全线 + 转发复核 + 风格自检"],
			["质检", "去 AI 味 + 内容风险 + 医疗红线 + 文献双层对账"],
			["交付", "入脚本库 + 更新选题 + 配朋友圈 + 评论区回复"]
		],
		files: [
			["选题库", "B自媒体大脑/00-选题库/选题矿脉库.md"],
			["脚本规则", "B自媒体大脑/01-视频号创作/创作脚本规则/视频号脚本风格系统.md"],
			["味道库", "B自媒体大脑/01-视频号创作/创作脚本规则/张医生个人味道库.md"],
			["风控总表", "B自媒体大脑/01-视频号创作/创作脚本规则/视频号风控总表.md"],
			["涨粉配比台账", "B自媒体大脑/01-视频号创作/创作脚本规则/涨粉配比闸门-台账.md"],
			["交付库", "B自媒体大脑/01-视频号创作/交付脚本库/index.md"]
		],
		inputLabel: "这条视频号想讲什么",
		placeholder: "例如：为什么医生自己也在吃营养素 / 鱼油是不是智商税",
		build: (input) => `写一条视频号脚本，主题是：${input}

严格按《视频号脚本风格系统》v1.50 完整流程执行，不得简化、跳步或只做概要。动笔前先读规则正文，不要只按这条摘要写：
第 0 步：过两道闸门——① 涨粉配比闸门（每连拍 3 条流量型，下一条必须是「医生为什么」身份独占型）② 0 号闸门（无认证期落点，疾病／功效／指标层一票否决）。
1、读痛点排行榜 + 知识库
2、定选题（已验证爆款元素 → 词根变换 → 2-3 个候选 → 选题决策卡）
3、开头句式（按词根查映射表，必轮换，不默认「我告诉你」；优先争议场景／数字反差，慎用单纯悬念型）
4、选题决策卡（6 问 + 8 分 + 涨粉复核 + 张医生个人味道嵌入）
5、四支柱风格写稿（选题驱动 × 嘴替感 × 自信自然 × 真实感）
6、两条一级铁律（一票否决）：A 身份独占——每条 ≥1 处「我在医院那几年」的具体场景／原话／画面，只作故事层、不作专业背书；B 转发三件套——社交货币 + 关心型转发对象写进结尾② + 转发包 ≥2，缺一件不交付
7、自检（开头 3 秒亮牌 + 铁律 18 身份用法安全线 + 转发复核 + 风格自检 + 老师式终极检验）
8、质检（风险清零才交付）：查重 → sepia 去 AI 味 → humanizer-zh → content-risk-detector → 视频号 7 类风险 → 医疗三条红线 → 事实核验 → 文献双层对账（正文嵌入 ≥2·≤4 条，国外 ≥1＋国内 ≥1；交付清单全量不设上限，每条四要素齐全、链接能点开）
9、文末锚点按定死格式：① 结论／数字 ＋（机构／期刊 · 篇名／法条号 · 年份）｜🔗 [点击查看](链接)
10、交付（标题过卡 + 测试变量 + 入交付脚本库 + 更新选题标记 + 章节进度条 + 自动配 1 条朋友圈 + 评论区回复）
写作时套用「二十四、脚本创作 10 条硬建议」，交付前逐条过。`
	},
	{
		key: "article",
		title: "写公众号",
		icon: "file-text",
		color: "#e08a3c",
		desc: "选题、标题、正文、配图、排版到草稿箱，一条线。",
		steps: [
			["读总控台", "唯一入口，9 步全流程在这里"],
			["① 定线", "商业定位 v3：超级个体线（IP／商业定位／一人公司）"],
			["② 定交付件+选题", "读者拿走哪 3 个提示词／表／流程 + 决策卡"],
			["③ 标题", "主用证据型：一个人 + 结果数字 + 全公开 + 复制即用"],
			["④ 写作", "7 段 100 字开头 + 3 模块并列 + 绑定身份"],
			["⑤ 质检", "去 AI 味 → 风险 → AI 痕迹 → 医疗合规"],
			["⑥ 发布区", "PUBLISH 标记之间的纯净版"],
			["⑦ 排版推送", "细字呼吸版 v4.0 → 草稿箱"],
			["⑧⑨ 交付+贴图", "纯净版入库 + 3:4 浅版 3-5 张"]
		],
		files: [
			["总控台（唯一入口）", "B自媒体大脑/02-公众号创作/创作脚本规则/公众号创作总控台.md"],
			["商业定位", "B自媒体大脑/02-公众号创作/创作脚本规则/公众号商业定位.md"],
			["写作手册", "B自媒体大脑/02-公众号创作/创作脚本规则/公众号写作手册.md"],
			["贴图方法论", "B自媒体大脑/02-公众号创作/创作脚本规则/公众号贴图（小绿书）方法论.md"],
			["交付库", "B自媒体大脑/02-公众号创作/交付脚本库/index.md"]
		],
		inputLabel: "这篇公众号想写什么",
		placeholder: "例如：为什么一提营养素就想到智商税 / 把 script-114 改成公众号",
		build: (input) => `写一篇公众号文章，主题是：${input}

先读《公众号创作总控台》（唯一入口），再按其中「全流程 9 步」完整执行，不得简化或跳步：
① 定线：读《公众号商业定位 v3》定人群/痛点/价值/方向（超级个体线：IP／商业定位／一人公司，营养线只作案例）
② 选题：从《公众号选题弹药库》A–E 按业务环节取题；第 0 步先定交付件——这篇让读者拿走哪 3 个提示词／表／流程？说不出就换题；再过选题决策卡（6 问 + 8 分 + 搜一搜 + 三价值检验）
③ 标题：主用证据型（一个人 + 结果数字 + 全公开 + 复制即用），给 3 个备选
④ 写作：按《公众号写作手册 v2》四~八节（7 段 100 字开头 + 3 模块并列 + 金句 + 绑定身份）
⑤ 质检：sepia（review→refactor）→ humanizer-zh 词句扫描 → content-risk-detector → ai-detector → 医疗合规 → 2026 新规避坑，风险清零
⑥ 发布区：提取 PUBLISH 标记之间的纯净版（内部记录不推）
⑦ 排版推送：排版固定令 v4.0「细字呼吸版」（纯白底 · 正文 15px · 行高 2.5 · 字距 0.3 · 首行缩进 2em · 段距 40px · 墨靛 #252F3D · 一条 1px 虚线脊 · 卡片 ≤3 个）→ 推草稿箱
⑧ 交付复盘：交付纯净版 + 存 公众号草稿/article-XXX
⑨ 贴图浅版：同主题 3:4 卡 3-5 张（xhs-note-creator zhangshi-medical），进同一草稿箱
完成后自动附评论区回复（置顶 1 条 + 认同共鸣型 2-3 条），并存入公众号交付脚本库。`
	},
	{
		key: "moments",
		title: "写朋友圈",
		icon: "message-circle",
		color: "#c19618",
		desc: "从灵感到可直接发的纯文字版，全流程出稿。",
		steps: [
			["灵感/选题", "创业／AI／活动／生活，先定这一条从哪来"],
			["过三道闸", "归哪块？只讲一个点？术语是「营养素」"],
			["先排 AI 味", "写之前先过 v3.3「三、先排 AI 味」那张表"],
			["定类型", "悬念／痛点／干货／证言／福利／人设／认知暴击"],
			["套模板+指纹", "九种语气带 1-2 个 + 说话指纹 + 洞见五步"],
			["填肉", "我的真实故事和数字；AI 类补「到底干了什么」"],
			["去 AI 味", "sepia review→refactor → humanizer-zh 扫词"],
			["过检查清单", "18 条铁律 + 四问六眼 + 固定结尾"],
			["输出+入库", "纯文字直发版 + 【图】占位 + 入库 + 同步飞书"]
		],
		files: [
			["v3.3 规则", "B自媒体大脑/05-朋友圈创作/创作脚本规则/张医生-朋友圈写作流程规则-v3.3-说人话版.md"],
			["底层详版", "B自媒体大脑/05-朋友圈创作/创作脚本规则/张医生-朋友圈写作模板与规则.md"],
			["文案样板", "B自媒体大脑/05-朋友圈创作/创作脚本规则/星光私董会-朋友圈文案库（模板×样板）.md"],
			["交付库", "B自媒体大脑/05-朋友圈创作/交付脚本库/index.md"]
		],
		inputLabel: "这条朋友圈想说什么",
		placeholder: "例如：今天有人问我为什么医生不学营养学 / 为什么医生自己也在吃营养素",
		build: (input) => `写一条朋友圈，主题是：${input}

先读《张医生-朋友圈写作流程规则 v3.3 说人话版》全文，再按「十二、写朋友圈总流程」执行，不得简化：
1、灵感/选题（创业／AI／活动／生活）
2、过三道闸：归哪块？只讲一个点吗？术语是「营养素」吗
3、先排 AI 味：过一遍 v3.3「三、先排 AI 味」那张表
4、定类型（悬念／痛点／干货／证言／福利／人设／认知暴击）+ 套对应模板
5、带 1-2 个语气开关 + 我的说话指纹（观点型走洞见五步）
6、填肉：用我的真实故事和数字；AI 类补一个「AI 到底干了什么」的细节
7、去 AI 味：sepia（review→refactor）→ humanizer-zh 词句扫描，别整篇换皮
8、过出稿检查清单（四问 + 六眼；认知暴击型再查六项）
9、输出纯文字直发版（含【图】占位，标签选加），配图我自己负责
固定结尾（定死）：最后一行永远是「相信未来」超级个体俱乐部～，原样照抄不加句号，【图】接在这句下面；结尾不呼吁、不给指令、不挂互动钩子。朋友圈免质检，唯一底线是术语「营养素」。
生成后存入朋友圈交付脚本库，并同步飞书。`
	},
	{
		key: "knowledge",
		title: "知识整理入库",
		icon: "inbox",
		color: "#3f9e5c",
		desc: "一条内容进来，成卡、沉淀、再反哺选题。",
		steps: [
			["入盒", "贴内容／丢链接／说录音路径"],
			["查重", "先过查重网关，重复内容不建卡"],
			["筛选", "过入盒标准，不合格直接丢"],
			["成卡", "按 4K 制式：金句先出洞见卡 DJ-*"],
			["沉淀知识库", "够深再写知识卡片 KC-*，归对应库"],
			["沉淀选题库", "按内容线写入安利／AI／公众号选题库"],
			["反哺调用", "下次写稿优先从这些选题里取"]
		],
		files: [
			["入盒规则", "A知识沉淀大脑/00-新知识入库/00-灵感库·入盒规则.md"],
			["洞见卡库", "A知识沉淀大脑/00-新知识入库/洞见卡/洞见卡库.md"],
			["知识卡片库", "A知识沉淀大脑/00-新知识入库/知识卡片/知识卡片库.md"],
			["卡片模板", "A知识沉淀大脑/00-新知识入库/知识卡片/卡片模板.md"],
			["选题矿脉库", "B自媒体大脑/00-选题库/选题矿脉库.md"],
			["超级个体选题库", "B自媒体大脑/00-选题库/超级个体选题库.md"],
			["公众号选题库", "B自媒体大脑/00-选题库/公众号选题弹药库.md"],
			["评论区选题池", "B自媒体大脑/00-选题库/评论区选题池.md"]
		],
		inputLabel: "要入库的内容 / 链接 / 来源",
		placeholder: "直接把内容贴进来，或写：飞书录音 2026-10-19 那场",
		build: (input) => `这条知识入库：${input}

请按《00-灵感库·入盒规则》执行，先过查重网关（01-合规网关 0a），再走完两条沉淀线，缺一条都算没入库：
A、知识沉淀：入盒 → 查重 → 筛选 → 按 4K 制式成卡（金句先出洞见卡 DJ-*，够深再写知识卡片 KC-*）→ 归入洞见卡库／知识卡片库。
B、选题沉淀：从卡片里提炼可写角度，按内容线写入对应选题库——
营养／创业／团队／成长 → B自媒体大脑/00-选题库/选题矿脉库.md
AI 相关 / 个人成长 / 自媒体 → B自媒体大脑/00-选题库/超级个体选题库.md
适合写成公众号长文（超级个体／一人公司／IP 线）→ B自媒体大脑/00-选题库/公众号选题弹药库.md
来自评论区的问题 → B自媒体大脑/00-选题库/评论区选题池.md

每条选题必须标注：来源卡片编号 + 核心观点 + 可写角度 + 建议平台。
完成后回报两处结果：落在哪个知识库、进了哪个选题库（附链接）。`
	},
	{
		key: "profile",
		title: "张大侠个人档案",
		icon: "user",
		color: "#8e6bd1",
		desc: "底色、信念、梦想、事业路径、真痛点、身体线和说话方式。给建议前先过这层。",
		steps: [
			["我是谁", "农村娃 → 麻醉医生 → 亏损 → 安利 → AI 营养师"],
			["我要什么", "梦想清单：FC／演唱会／父母／帮更多人"],
			["真痛点", "身体在漏、聚焦在散、系统在缺"],
			["事业路径", "安利创业：目标、业务版图、七张卡、复制"],
			["身体线", "薄肌训练：公园三件套 + 作息恢复"],
			["家庭线", "张翊南 0-9 岁音乐培养执行表"],
			["怎么说话", "医生式逻辑、数字、对比、金句"]
		],
		files: [
			["人物档案（四合一）", "A知识沉淀大脑/06-张大侠/人物档案-张大侠.md"],
			["梦想清单", "A知识沉淀大脑/06-张大侠/梦想清单-张大侠.md"],
			["安利创业", "A知识沉淀大脑/06-张大侠/安利创业-张大侠.md"],
			["薄肌训练计划", "A知识沉淀大脑/06-张大侠/张大侠-薄肌训练计划.md"],
			["音乐执行表", "A知识沉淀大脑/06-张大侠/张翊南-音乐培养执行表.md"]
		],
		inputLabel: "要我按你的底色回答什么",
		placeholder: "例如：我下个月该聚焦哪件事 / 帮我判断这个合作值不值得做",
		build: (input) => `按我的个人档案来回答：${input}

读法（强制）：《人物档案-张大侠》是四合一总档案、十万字符级，禁止整读，按章节定向读：
· 第一部分「我」＝底色／信念／真痛点／沟通口味（必读）
· 第二部分「父母」、第三部分「儿子张翊南」、第四部分「AI 张大侠 · 三大治理开关」按问题需要再读
再按需读：《梦想清单-张大侠》（我要去哪）、《安利创业-张大侠》（事业路径与业务现场）、《张大侠-薄肌训练计划》（身体线）、《张翊南-音乐培养执行表》（家庭执行）。

回答要求：
1、先「懂我」再给建议——顺着我验证过的信念体系（选对圈子 / 专业死磕 / 方向对就够 / 越挫越勇 / 利他极客），别推一套跟我底色拧着来的方案。
2、心力不足＝认知不足：不讲鸡血，讲把本质看透。
3、说话方式：医生式逻辑（首先／第二／为什么）+ 数字敏感 + 对比制造冲击 + 金句收尾。
4、建议落到我的真痛点上：身体在漏、聚焦在散、系统在缺。`
	},
	{
		key: "lecture",
		title: "社群微课",
		icon: "presentation",
		color: "#2fa3a3",
		desc: "推广文案、讲稿、PPT 大纲到成品 .pptx，一次出全。",
		steps: [
			["定场次主题", "周五健康微课堂／周二故事分享，定期号和主题"],
			["推广文案", "按模板出 @所有人 预热文案"],
			["生成讲稿", "周五四段式／周二六段式图文"],
			["PPT 大纲", "逐页标题 + 核心要点 + 配图建议"],
			["渲染 PPT", "万病寻源版 · deck_style_wanbing.py 直出 .pptx"],
			["交付归档", "四样一次给全，按日期+期号命名入库"]
		],
		files: [
			["微课总流程", "C社群工作台/社群微课工作流/README.md"],
			["周五健康微课堂", "C社群工作台/社群微课工作流/每周五-健康微课堂.md"],
			["周二故事分享", "C社群工作台/社群微课工作流/每周二-健康故事分享.md"],
			["PPT 风格规范", "C社群工作台/社群微课工作流/PPT风格规范-万病寻源版.md"]
		],
		inputLabel: "这场微课讲什么",
		placeholder: "例如：周五 26-25期 蛋白质不同人群怎么吃 / 周二 我的减脂故事",
		build: (input) => `做一场社群微课：${input}

先读《社群微课工作流 README》《每周五-健康微课堂》《每周二-健康故事分享》《PPT风格规范-万病寻源版》，判断是周五知识干货型还是周二案例见证型，然后按对应完整流程执行，不得简化：
1、定场次、主题、期号（期号延续上期数字）
2、写社群推广文案（按模板：@所有人 + 主题期号 + 一个震撼事实/数据 + 2-3 句价值描述 + 今晚 19:30 + 本群主理人张医生 + 鼓掌表情）
3、生成完整讲稿：周五按四段式（欢迎 2 分钟 / 名词解释 4 分钟 / 知识分解+痛点 6 分钟 / 纽崔莱方案 4 分钟，总 15-20 分钟）；周二按六段式图文（每段标 [插入图片]）
4、生成 PPT 大纲（逐页：标题 / 核心要点 / 配图建议，用 --- 分页）
5、用 deck_style_wanbing.py 直接渲染 .pptx，固定「万病寻源版」：米白纸感底 + 玫红/青/黄信息块 + 左上小标签＋大标题 + 右下页码 + 页脚出处小字。不再出 NotebookLM 提示词、不用黄底黑字版、不出粘贴包
6、按命名规范交付：《主题》-YYYY-MM-DD-期号.pptx 和 《主题》-讲稿-YYYY-MM-DD-期号.md，存 C社群工作台/社群微课工作流/；日期用 date 实取，期号延续上期
四样一次给全，不要只给大纲。`
	},
	{
		key: "gzhmine",
		title: "公众号选题挖矿",
		icon: "gem",
		color: "#2f8f5b",
		hidden: true,
		desc: "按业务链条五环扫一轮，从对标博主身上挖题，直接写回公众号弹药库。",
		steps: [
			["定环节", "A 选行业／B 定位／C 执行／D AI／E 闭环，缺哪环挖哪环"],
			["扫博主", "按环节选 1–2 个对标博主，只看最近 10 条"],
			["抽观点", "只记观点＋靶子＋原话，不抄全文"],
			["过四换", "换身份→换靶子→换数字→换落点"],
			["写回库", "按 A–E 编号顺延写回，标 ❌/⭐；跨库不查重"]
		],
		files: [
			["公众号选题弹药库", "B自媒体大脑/00-选题库/公众号选题弹药库.md"],
			["商业定位", "B自媒体大脑/02-公众号创作/创作脚本规则/公众号商业定位.md"],
			["写作手册", "B自媒体大脑/02-公众号创作/创作脚本规则/公众号写作手册.md"],
			["超级个体选题库", "B自媒体大脑/00-选题库/超级个体选题库.md"]
		],
		inputLabel: "这次挖哪一环 / 哪个博主（可留空）",
		placeholder: "例如：D AI 应用 / 挖亦仁 / 留空就五环全扫",
		optionalInput: true,
		build: (input) => `公众号选题挖矿：${input || "五环全扫"}

先读《公众号选题弹药库》v3（业务链条 A–E 五组 + 博主供给图 + 4 换公式），再按下面执行，不写正文，只出选题：
1、定环节：A 选对行业 / B 商业定位 / C 执行细节（朋友圈·短视频·表现力·研究）/ D AI 应用（知识库·工作流·选题文案放大·一人公司）/ E 闭环与俱乐部；缺哪环挖哪环，输入为空则五环各扫一轮。
2、选博主：按《1.1 环节供给图》选 1–2 个对标博主，只看他最近 10 条内容，只记观点、靶子、原话，不抄全文。
3、过 4 换：换身份（医院那几年／35 岁辞职／亏 30 万）→ 换靶子（能被指认的人）→ 换数字（5000 台手术／700 粉／2 万粉／100 万播放）→ 换落点（筛人，不硬招商）。
4、不查重：不与《超级个体选题库》或其他库查重；公众号是改写发布，同一观点可以再写。只避免同一组里完全相同的标题。
5、写回《公众号选题弹药库》对应组：编号顺延（A-017、B-023……），每条填「选题 / 挖自 / 可写角度／证据」，状态标 ❌；本周要写的标 ⭐。
6、产出 10–15 条，按可写性排序，至少 3 条带「医生身份」独占角度；最后回报新增数量、写到哪几组、编号区间。`
	},
	{
		key: "spmine",
		title: "超级个体选题挖矿",
		icon: "gem",
		color: "#5b7bd5",
		hidden: true,
		desc: "从对标博主身上挖口播选题，按 S/T/M/P 编号顺延写回超级个体选题库。",
		steps: [
			["定矿口", "S 身份／T 认知／M 方法／P 观点／L·D 对标改写，选一个"],
			["扫博主", "按矿口选 1–2 个对标，只看最近 10 条"],
			["抽观点", "只记观点＋靶子＋原话，不抄全文"],
			["过四换", "换身份→换靶子→换数字→换落点"],
			["写回库", "按 S/T/M/P 编号顺延，标 ⭐ 的留本周拍"]
		],
		files: [
			["超级个体选题库", "B自媒体大脑/00-选题库/超级个体选题库.md"],
			["公众号选题弹药库", "B自媒体大脑/00-选题库/公众号选题弹药库.md"],
			["脚本风格系统", "B自媒体大脑/01-视频号创作/创作脚本规则/视频号脚本风格系统.md"]
		],
		inputLabel: "这次挖哪个矿口 / 哪个博主（可留空）",
		placeholder: "例如：T 认知 / 挖亦仁 / M 方法 / 留空就 S、T 两个矿口各扫一轮",
		optionalInput: true,
		build: (input) => `超级个体选题挖矿：${input || "S、T 两个矿口各扫一轮"}

先读《超级个体选题库》的「编号分工」「取材地图」两节（不整读全库），再读《公众号选题弹药库》第 1 节博主表；定一个主矿口 → 选 1–2 个对标只记观点 → 过 4 换 → 按 S/T/M/P 顺延写回、标 ❌/⭐ → 产出 10–15 条、至少 3 条身份独占 → 不承诺收益、不写月入包会。
具体执行：
1、定矿口：S 身份 / T 认知 / M 方法 / P 观点 / L·D 对标改写，输入为空时 S、T 各扫一轮
2、扫博主：按矿口选 1–2 个对标，只看最近 10 条，只记观点＋靶子＋原话，不抄全文
3、过 4 换：换身份（医院那几年／35 岁辞职／亏 30 万）→ 换靶子（能被指认的人）→ 换数字（5000 台手术／700 粉／2 万粉／100 万播放）→ 换落点（筛人，不硬招商）
4、写回《超级个体选题库》：按 S/T/M/P 编号顺延，状态标 ❌，本周要拍的标 ⭐
5、产出 10–15 条，按可写性排序，至少 3 条「医生为什么」身份独占角度
最后回报新增数量、写到哪个矿口、编号区间。`
	}
];

/* ============================================================
 * 题库横条
 * ============================================================ */

const LIBRARY_LINKS = [
	["公众号选题弹药库", "B自媒体大脑/00-选题库/公众号选题弹药库.md", "#3f9e5c"],
	["超级个体选题库", "B自媒体大脑/00-选题库/超级个体选题库.md", "#5b7bd5"],
	["评论区选题池", "B自媒体大脑/00-选题库/评论区选题池.md", "#e08a3c"],
	["选题矿脉库", "B自媒体大脑/00-选题库/选题矿脉库.md", "#e8b13a"]
];

const LIBRARY_GROUPS = [
	{ tag: "公众号 · IP 线", libs: ["公众号选题弹药库"] },
	{ tag: "视频号 · 超级个体", libs: ["超级个体选题库"] },
	{ tag: "视频号 · 营养账号", libs: ["选题矿脉库", "评论区选题池"] }
];

const LIBRARY_MINE = {
	"B自媒体大脑/00-选题库/公众号选题弹药库.md": {
		key: "gzhmine",
		label: "📝 挖矿 →",
		cls: "zfc-library-gzh"
	},
	"B自媒体大脑/00-选题库/超级个体选题库.md": {
		key: "spmine",
		label: "⛏ 挖矿 →",
		cls: "zfc-library-gzh"
	},
	"B自媒体大脑/00-选题库/选题矿脉库.md": {
		key: "mine",
		label: "⛏ 开矿 →",
		cls: "zfc-library-mine"
	}
};

const MINE_MODULE = {
	key: "mine",
	title: "开矿 · 选题开采",
	icon: "gem",
	color: "#e8b13a",
	optionalInput: true,
	desc: "四个矿口扫一轮，只记靶子和原话，三格填满后直接写回选题矿脉库。",
	steps: [
		["扫", "身份／共识／靶子／情绪四个矿口各扫 15 条"],
		["抽", "每题填三格，填不满直接扔"],
		["换", "身份换成「麻醉医生→AI 营养师」"],
		["查重", "对已拍脚本＋020 池＋评论区池"],
		["写回", "靶子登记表＋产出池＋本周记录"]
	],
	files: [
		["选题矿脉库", "B自媒体大脑/00-选题库/选题矿脉库.md"],
		["黄金选题池", "B自媒体大脑/01-视频号创作/交付脚本库/爆款素材库/020-黄金选题池：两条已验证公式×新靶子.md"],
		["已拍脚本库", "B自媒体大脑/01-视频号创作/交付脚本库/index.md"],
		["评论区选题池", "B自媒体大脑/00-选题库/评论区选题池.md"],
		["脚本风格系统", "B自媒体大脑/01-视频号创作/创作脚本规则/视频号脚本风格系统.md"]
	],
	inputLabel: "这次想侧重哪个矿口／方向（可留空）",
	placeholder: "例如：身份矿 / 靶子矿 / 儿童零食 / 留空就四个矿口全扫",
	build: (input) => `开矿：按《选题矿脉库》的四个矿口做一轮选题开采${input ? `\n本次侧重：${input}` : ""}

先读《选题矿脉库》和《视频号脚本风格系统》，不写脚本，只出选题：
1、四矿口各扫一轮——身份矿（医院那几年）／共识矿（范志红、顾中一、辟谣榜）／靶子矿（大瑞瑞、黑皮、老爸评测、货架）／情绪矿（慢病博主评论区、热搜、自己的评论区）
2、只记靶子和原话，每题填满三格（靶子 / 原话 / 可写角度），填不满直接扔
3、身份换成「麻醉医生 → AI 营养师」
4、查重：对已拍脚本库、020 黄金选题池、评论区选题池
5、过 0 号闸门：无认证期落点，疾病／功效／指标层一票否决
6、出 10–15 条，按预判分排序，至少 3 条「医生为什么」身份独占型
7、直接写回《选题矿脉库》：靶子登记表（T 编号顺延）、产出池（S 编号顺延）、本周开采记录
最后回报新增数量与改动位置。`
};

/* ============================================================
 * 前沿信息速递横条
 * ============================================================ */

function lastWeekRange() {
	const now = new Date();
	const end = new Date(now.getFullYear(), now.getMonth(), now.getDate());
	const start = new Date(end);
	start.setDate(start.getDate() - 6);
	const fmt = (d) =>
		`${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
	return `${fmt(start)} 至 ${fmt(end)}`;
}

const FRONTIER_MODULES = [
	{
		key: "ai-frontier",
		title: "AI 信息前沿",
		icon: "cpu",
		color: "#5b7bd5",
		optionalInput: true,
		path: "A知识沉淀大脑/04-AI前沿信息/index.md",
		desc: "最近一周 · AI builder 动态、播客、博客",
		steps: [
			["抓取", "follow-builders 拉最近一周 AI builder 动态"],
			["摘要", "中文摘要，讲清谁说了什么、为什么重要"],
			["落地", "存 04-AI前沿信息，更新 index"],
			["反哺", "AI 线选题写入超级个体选题库附录"]
		],
		files: [
			["AI 前沿索引", "A知识沉淀大脑/04-AI前沿信息/index.md"],
			["超级个体选题库", "B自媒体大脑/00-选题库/超级个体选题库.md"]
		],
		inputLabel: "额外聚焦方向（可留空）",
		placeholder: "例如：Agent / 一人公司 / 只留空就按最近一周全量",
		build: (input) => `采集最近一周（${lastWeekRange()}）的 AI 前沿信息。${input ? `\n额外聚焦：${input}` : ""}

用 follow-builders skill 拉最近一周 AI builder 动态、播客、博客，整理成中文摘要，按下面流程落地：
1、抓取最近 7 天动态，标注来源与日期
2、中文摘要：每条讲清「谁说了什么 + 为什么重要」
3、按《AI前沿-YYYY-MM-DD-主题.md》命名，存入 A知识沉淀大脑/04-AI前沿信息/
4、更新该文件夹 index.md 的期次索引
5、顺手抛可写选题进 B自媒体大脑/00-选题库/超级个体选题库.md（AI 线写入文末附录）`
	},
	{
		key: "nutrition-frontier",
		title: "营养信息前沿",
		icon: "leaf",
		color: "#3f9e5c",
		optionalInput: true,
		path: "A知识沉淀大脑/05-营养前沿信息/index.md",
		desc: "最近一周 · 顶刊与机构研究",
		steps: [
			["搜索", "agent-reach 搜最近一周顶刊、机构研究"],
			["速递", "整理成中文营养速递"],
			["落地", "追加到当月速递，不覆盖历史"],
			["反哺", "抛选题进选题矿脉库"]
		],
		files: [
			["营养前沿索引", "A知识沉淀大脑/05-营养前沿信息/index.md"],
			["选题矿脉库", "B自媒体大脑/00-选题库/选题矿脉库.md"]
		],
		inputLabel: "额外聚焦方向（可留空）",
		placeholder: "例如：蛋白质 / 维生素D / 留空就按最近一周全量",
		build: (input) => `采集最近一周（${lastWeekRange()}）的营养前沿信息。${input ? `\n额外聚焦：${input}` : ""}

用 agent-reach skill 搜最近一周顶刊/机构研究，整理成中文速递，按下面流程落地：
1、抓取最近 7 天顶刊与机构研究，标注期刊／机构与日期
2、中文速递：每条讲清「研究做了什么 + 结论 + 对普通人意味着什么」
3、更新当月「📡营养学前沿速递-YYYYMM.md」，追加「本周速递」章节，不覆盖历史
4、更新 A知识沉淀大脑/05-营养前沿信息/index.md
5、顺手抛可写选题进 B自媒体大脑/00-选题库/选题矿脉库.md`
	}
];

/* ============================================================
 * Claudian 注入
 * ============================================================ */

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function pickChatInput() {
	const scope =
		document.querySelector(".claudian-active-input-slot") || document;
	const selectors = [
		"textarea",
		'[contenteditable="true"]',
		".cm-content",
		'input[type="text"]'
	];
	for (const selector of selectors) {
		const candidates = Array.from(scope.querySelectorAll(selector)).filter(
			(el) => {
				const rect = el.getBoundingClientRect();
				return rect.width > 0 && rect.height > 0;
			}
		);
		if (candidates.length) {
			return candidates[candidates.length - 1];
		}
	}
	return null;
}

function findModule(key) {
	if (key === MINE_MODULE.key) return MINE_MODULE;
	return MODULES.find((mod) => mod.key === key);
}

/* ============================================================
 * 视图
 * ============================================================ */

class WorkbenchView extends ItemView {
	constructor(leaf, plugin) {
		super(leaf);
		this.plugin = plugin;
	}

	getViewType() {
		return VIEW_TYPE;
	}

	getDisplayText() {
		return "张医生工作台";
	}

	getIcon() {
		return "layout-dashboard";
	}

	async onOpen() {
		this.render();
	}

	render() {
		const root = this.contentEl;
		root.empty();
		root.addClass("zfc-workbench");

		const header = root.createDiv({ cls: "zfc-header" });
		header.createEl("h1", { text: "张医生 · 内容生产工作台" });
		header.createEl("p", {
			text: "点一个板块，填一句主题，指令会自动送进 Claudian 对话框。"
		});

		this.renderLibrary(root);
		this.renderFrontier(root);
		this.renderCards(root);
	}

	renderLibrary(root) {
		const library = root.createDiv({ cls: "zfc-library" });

		const head = library.createDiv({ cls: "zfc-library-head" });
		head.createDiv({ cls: "zfc-library-title", text: "📚 题库" });

		const list = library.createDiv({ cls: "zfc-library-list" });
		const linkMap = new Map(
			LIBRARY_LINKS.map(([label, path, color]) => [label, { path, color }])
		);

		for (const group of LIBRARY_GROUPS) {
			const row = list.createDiv({ cls: "zfc-library-row" });
			row.createDiv({ cls: "zfc-library-tag", text: group.tag });

			const items = row.createDiv({ cls: "zfc-library-items" });

			// mineFirst：挖矿 / 开矿按钮在前
			const mineEntry = group.libs
				.map((label) => {
					const info = linkMap.get(label);
					return info ? LIBRARY_MINE[info.path] : null;
				})
				.find(Boolean);

			if (mineEntry) {
				const mineButton = items.createEl("button", {
					cls: `zfc-library-mine-btn ${mineEntry.cls}`,
					text: mineEntry.label
				});
				mineButton.addEventListener("click", () => {
					const mod = findModule(mineEntry.key);
					if (mod) {
						new ActionModal(this.app, mod, this.plugin).open();
					}
				});
			}

			for (const label of group.libs) {
				const info = linkMap.get(label);
				if (!info) continue;
				const button = items.createEl("button", {
					cls: "zfc-library-btn",
					text: label
				});
				button.style.setProperty("--lib-color", info.color);
				button.addEventListener("click", () => {
					this.app.workspace.openLinkText(info.path, "", true);
				});
			}
		}
	}

	renderFrontier(root) {
		const frontier = root.createDiv({ cls: "zfc-frontier" });

		const head = frontier.createDiv({ cls: "zfc-frontier-head" });
		head.createDiv({ cls: "zfc-frontier-title", text: "📡 前沿信息速递" });
		head.createDiv({
			cls: "zfc-frontier-sub",
			text: "两条线 · 点开窗口采集最近 7 天"
		});

		const list = frontier.createDiv({ cls: "zfc-frontier-list" });
		for (const mod of FRONTIER_MODULES) {
			const button = list.createEl("button", { cls: "zfc-frontier-btn" });
			button.style.setProperty("--frontier-color", mod.color);

			const iconEl = button.createDiv({ cls: "zfc-frontier-icon" });
			setIcon(iconEl, mod.icon);

			const body = button.createDiv({ cls: "zfc-frontier-body" });
			body.createDiv({ cls: "zfc-frontier-name", text: mod.title });
			body.createDiv({ cls: "zfc-frontier-desc", text: mod.desc });

			button.createDiv({ cls: "zfc-frontier-arrow", text: "→" });

			button.addEventListener("click", () => {
				new ActionModal(this.app, mod, this.plugin).open();
			});
		}
	}

	renderCards(root) {
		const grid = root.createDiv({ cls: "zfc-grid" });

		for (const mod of MODULES) {
			if (mod.hidden) continue;

			const card = grid.createDiv({ cls: "zfc-card" });
			card.style.setProperty("--zfc-accent", mod.color);

			const head = card.createDiv({ cls: "zfc-card-head" });
			const iconEl = head.createDiv({ cls: "zfc-icon" });
			setIcon(iconEl, mod.icon);
			head.createEl("h3", { text: mod.title });

			card.createEl("p", { cls: "zfc-card-desc", text: mod.desc });

			const cta = card.createEl("button", {
				cls: "zfc-card-cta",
				text: "开始操作 →"
			});

			const open = () => {
				new ActionModal(this.app, mod, this.plugin).open();
			};
			card.addEventListener("click", open);
			cta.addEventListener("click", (event) => {
				event.stopPropagation();
				open();
			});
		}
	}
}

/* ============================================================
 * 操作弹窗
 * ============================================================ */

class ActionModal extends Modal {
	constructor(app, mod, plugin) {
		super(app);
		this.mod = mod;
		this.plugin = plugin;
	}

	onOpen() {
		this.modalEl.addClass("zfc-modal");
		const { contentEl } = this;

		contentEl.createEl("h2", { text: this.mod.title });
		contentEl.createEl("p", { cls: "zfc-card-desc", text: this.mod.desc });

		const flow = contentEl.createDiv({ cls: "zfc-modal-flow" });
		flow.createDiv({ cls: "zfc-modal-flow-title", text: "操作流程" });
		const list = flow.createEl("ol");
		this.mod.steps.forEach((step) => {
			const li = list.createEl("li");
			li.createEl("b", { text: step[0] });
			if (step[1]) {
				li.createSpan({ cls: "say", text: " · " + step[1] });
			}
		});

		contentEl.createEl("label", {
			cls: "zfc-field-label",
			text: this.mod.inputLabel
		});

		this.inputEl = contentEl.createEl("textarea", {
			cls: "zfc-input",
			attr: { placeholder: this.mod.placeholder || "" }
		});

		const links = contentEl.createDiv({ cls: "zfc-modal-links" });
		this.mod.files.forEach(([label, path]) => {
			const chip = links.createEl("span", {
				cls: "zfc-link-chip",
				text: label
			});
			chip.addEventListener("click", () => {
				this.close();
				this.app.workspace.openLinkText(path, "", true);
			});
		});

		const actions = contentEl.createDiv({ cls: "zfc-modal-actions" });
		const cancel = actions.createEl("button", { text: "取消" });
		cancel.addEventListener("click", () => this.close());

		const start = actions.createEl("button", {
			cls: "mod-cta",
			text: "开始 →"
		});
		start.addEventListener("click", () => this.run());

		this.inputEl.addEventListener("keydown", (event) => {
			if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
				event.preventDefault();
				this.run();
			}
		});

		contentEl.createDiv({
			cls: "zfc-modal-hint",
			text: "点开始后会自动复制标准指令、打开 Claudian 并填进输入框，你按回车就开工。⌘/Ctrl + Enter 也可以直接开始。"
		});

		setTimeout(() => this.inputEl.focus(), 50);
	}

	async run() {
		const input = (this.inputEl.value || "").trim();
		if (!input && !this.mod.optionalInput) {
			new Notice("先填一句主题，再开始。");
			this.inputEl.focus();
			return;
		}

		const prompt = this.mod.build(input);

		try {
			await navigator.clipboard.writeText(prompt);
		} catch (error) {
			// 剪贴板失败不中断，继续尝试注入
		}

		this.close();

		const filled = await this.plugin.openClaudian(prompt);
		if (filled) {
			new Notice("指令已填进 Claudian 对话框，按回车开始。", 5000);
		} else {
			new Notice(
				"指令已复制。打开 Claudian 对话，粘贴后发送即可。",
				6000
			);
		}
	}

	onClose() {
		this.contentEl.empty();
	}
}

/* ============================================================
 * 设置页
 * ============================================================ */

class WorkbenchSettingTab extends PluginSettingTab {
	constructor(app, plugin) {
		super(app, plugin);
		this.plugin = plugin;
	}

	display() {
		const { containerEl } = this;
		containerEl.empty();

		new Setting(containerEl)
			.setName("启动时自动打开工作台")
			.setDesc(
				"开启时工作台常驻：打开 Obsidian 自动显示，手动关掉也会自动重开。想彻底关闭，先关掉这个开关。"
			)
			.addToggle((toggle) =>
				toggle
					.setValue(this.plugin.settings.openOnStartup)
					.onChange(async (value) => {
						this.plugin.settings.openOnStartup = value;
						await this.plugin.saveSettings();
					})
			);

		containerEl.createEl("p", {
			cls: "setting-item-description",
			text:
				"工作台通过 realclaudian:open-view 打开 Claudian，并把指令填入输入框。如果 Claudian 升级后输入框结构变化，指令仍会复制到剪贴板，手动粘贴即可。"
		});
	}
}

/* ============================================================
 * 插件主体
 * ============================================================ */

class ZfcWorkbenchPlugin extends Plugin {
	async onload() {
		await this.loadSettings();

		this.registerView(VIEW_TYPE, (leaf) => new WorkbenchView(leaf, this));

		this.addRibbonIcon("layout-dashboard", "打开张医生工作台", () =>
			this.activateView()
		);

		this.addCommand({
			id: "open-workbench",
			name: "打开张医生工作台",
			callback: () => this.activateView()
		});

		this.addSettingTab(new WorkbenchSettingTab(this.app, this));

		this.layoutReady = false;
		this.reopening = false;
		this.app.workspace.onLayoutReady(() => {
			this.layoutReady = true;
			if (this.settings.openOnStartup) {
				this.activateView();
			}
		});

		this.registerEvent(
			this.app.workspace.on("layout-change", () => {
				if (
					!this.layoutReady ||
					!this.settings.openOnStartup ||
					this.reopening
				) {
					return;
				}
				if (!this.app.workspace.getLeavesOfType(VIEW_TYPE).length) {
					this.reopening = true;
					this.activateView()
						.catch(() => {})
						.finally(() => {
							this.reopening = false;
						});
				}
			})
		);
	}

	async activateView() {
		const { workspace } = this.app;
		let leaf = workspace.getLeavesOfType(VIEW_TYPE)[0];
		if (!leaf) {
			leaf = workspace.getLeaf("tab");
			await leaf.setViewState({ type: VIEW_TYPE, active: true });
		}
		workspace.revealLeaf(leaf);
	}

	async openClaudian(prompt) {
		const plugins = this.app.plugins;
		const available = Boolean(
			plugins && plugins.plugins && plugins.plugins.realclaudian
		);

		if (available) {
			try {
				this.app.commands.executeCommandById("realclaudian:open-view");
			} catch (error) {
				// 命令不可用时继续走剪贴板方案
			}
		}

		await sleep(available ? 800 : 100);

		if (!available) {
			return false;
		}

		const input = pickChatInput();
		if (!input) {
			return false;
		}

		input.focus();

		if (input.tagName === "TEXTAREA" || input.tagName === "INPUT") {
			const proto =
				input.tagName === "TEXTAREA"
					? window.HTMLTextAreaElement.prototype
					: window.HTMLInputElement.prototype;
			const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
			setter.call(input, prompt);
			input.dispatchEvent(new Event("input", { bubbles: true }));
			input.dispatchEvent(new Event("change", { bubbles: true }));
			return true;
		}

		if (input.isContentEditable) {
			try {
				document.execCommand("insertText", false, prompt);
			} catch (error) {
				input.textContent = prompt;
				input.dispatchEvent(
					new InputEvent("input", {
						bubbles: true,
						inputType: "insertText",
						data: prompt
					})
				);
			}
			return true;
		}

		return false;
	}

	async loadSettings() {
		this.settings = Object.assign(
			{ openOnStartup: true },
			await this.loadData()
		);
	}

	async saveSettings() {
		await this.saveData(this.settings);
	}
}

module.exports = ZfcWorkbenchPlugin;
