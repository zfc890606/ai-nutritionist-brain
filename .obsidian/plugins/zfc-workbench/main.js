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

const MODULES = [
	{
		key: "video",
		title: "写视频号",
		icon: "video",
		color: "#e5534b",
		desc: "从选题到成片脚本，五步走完，写完自动入库。",
		steps: [
			["过闸门", "第 0 步：涨粉配比 + 无认证期落点，一票否决"],
			["读痛点", "读痛点排行榜 + 知识库"],
			["定选题", "选爆款元素 → 词根变换 → 2-3 个候选"],
			["开头句式", "按词根查映射表，必轮换"],
			["过决策卡", "6 问 8 分 + 涨粉复核 6 要素 + 味道嵌入"],
			["写稿", "四支柱 + 老师式表达 + 真实感写作法"],
			["自检", "开头 3 秒 + 身份安全线 + 风格自检"],
			["质检", "去 AI 味 + 内容风险 + 医疗红线 + 事实核验"],
			["交付", "入脚本库 + 更新选题 + 配朋友圈 + 评论区回复"]
		],
		files: [
			["选题库", "B自媒体大脑/00-选题库/安利选题库.md"],
			["脚本规则", "B自媒体大脑/01-视频号创作/创作脚本规则/视频号脚本风格系统.md"],
			["风控总表", "B自媒体大脑/01-视频号创作/创作脚本规则/视频号风控总表.md"],
			["交付库", "B自媒体大脑/01-视频号创作/交付脚本库/index.md"]
		],
		inputLabel: "这条视频号想讲什么",
		placeholder: "例如：为什么医生自己也在吃营养素 / 鱼油是不是智商税",
		build: (input) => `写一条视频号脚本，主题是：${input}

严格按《视频号脚本风格系统》v1.39 的完整八步流程执行，不得简化、跳步或只做概要：
第 0 步：过涨粉配比闸门（连拍 3 条流量型后，下一条必须身份独占型）+ 无认证期落点闸门。
1. 读痛点排行榜 + 知识库
2. 定选题（已验证爆款元素 → 词根变换 → 2-3 个候选 → 选题决策卡）
3. 开头句式（按词根查映射表，必轮换，不默认「我告诉你」）
4. 选题决策卡（6 问 + 8 分 + 涨粉复核 6 要素 + 张医生个人味道嵌入）
5. 四支柱风格写稿（选题驱动 × 嘴替感 × 自信自然 × 真实感）
6. 自检（开头 3 秒亮牌 + 铁律 18 身份安全线 + 风格自检）
7. 质检（查重 → 去 AI 味 → 内容风险 → 视频号 7 类风险 → 医疗三条红线 → 事实核验），风险清零才交付
8. 交付（标题过卡 + 测试变量 + 入交付脚本库 + 更新选题标记 + 章节进度条 + 自动配 1 条朋友圈 + 评论区回复）
动笔前先读规则正文，不要只按这条摘要写。`
	},
	{
		key: "article",
		title: "写公众号",
		icon: "file-text",
		color: "#e08a3c",
		desc: "选题、标题、正文、配图、排版到草稿箱，一条线。",
		steps: [
			["读总控台", "唯一入口，9 步全流程在这里"],
			["定人群和线", "商业定位：涨粉线还是守 IP 线"],
			["选题决策卡", "6 问 + 8 分 + 搜一搜 + 三价值检验"],
			["标题决策卡", "结论前置 → 合规 → 3 个备选"],
			["写作", "阅读体 + 参考资料 + 免责声明"],
			["质检", "去 AI 味 → 风险 → AI 痕迹 → 医疗合规 7 条"],
			["提取发布区", "PUBLISH 标记之间的纯净版"],
			["配图", "正文图 1-2 张 + 结尾名片 + 封面"],
			["推送交付", "排版 → 草稿箱 → 纯净版 → 贴图浅版 → 入库"],
			["评论区回复", "置顶 1 条 + 共鸣回复 2-3 条，附文末"]
		],
		files: [
			["公众号流程", "B自媒体大脑/02-公众号创作/创作脚本规则/03-公众号流程.md"],
			["总控台", "B自媒体大脑/02-公众号创作/创作脚本规则/公众号创作总控台.md"],
			["标题决策卡", "B自媒体大脑/02-公众号创作/创作脚本规则/公众号标题决策卡.md"],
			["交付库", "B自媒体大脑/02-公众号创作/交付脚本库/index.md"]
		],
		inputLabel: "这篇公众号想写什么",
		placeholder: "例如：为什么一提营养素就想到智商税 / 把 script-114 改成公众号",
		build: (input) => `写一篇公众号文章，主题是：${input}

先读《公众号创作总控台》，然后严格按《03-公众号流程》完整 9 步执行，不得简化或跳步：
1. 读《公众号商业定位》定人群/痛点/价值/方向，明确涨粉线还是守 IP 线
2. 选题决策卡（6 问 + 8 分 + 搜一搜 + 三价值检验 + 阅读动力）
3. 标题决策卡（结论前置 → 合规 → 观看理由 → 3 个备选）
4. 写作（阅读体 + 参考资料 + 免责声明）
5. 质检（humanizer-zh → content-risk-detector → ai-detector → 医疗合规 7 条 → 2026 新规避坑）
6. 提取发布区（PUBLISH 标记之间的纯净版）
7. 配图（正文图 1-2 张 + 结尾固定名片 + 讲师照封面）
8. gzh-AI-Design 排版（暖蓝医养、正文 14px）→ 推送草稿箱 → 交付纯净版
9. 贴图浅版自动附带（xhs-note-creator 3:4 卡 3-5 张，进同一草稿箱）
完成后自动附评论区回复（置顶 1 条 + 认同共鸣型 2-3 条），并存入公众号交付脚本库。`
	},
	{
		key: "moments",
		title: "写朋友圈",
		icon: "message-circle",
		color: "#c19618",
		desc: "从灵感到可直接发的纯文字版，六步出稿。",
		steps: [
			["灵感/选题", "创业／AI／活动／生活，先定这一条从哪来"],
			["过三道闸", "板块？一点？术语是「营养素」"],
			["定板块+类型", "悬念／痛点／干货／证言／福利／人设／认知暴击"],
			["套模板+风格", "九种语气挑 1-2 个 + 洞见五步 + 万能结构"],
			["填肉", "你的真实素材 + 数字武器；AI 线补细节"],
			["过检查清单", "16 条铁律 + 出稿检查，全过才发"],
			["输出+发布", "纯文字直发版 + 【图】占位 + 入库 + 同步飞书"]
		],
		files: [
			["v3.2 规则", "B自媒体大脑/05-朋友圈创作/创作脚本规则/张医生-朋友圈写作流程规则-v3.2-融合版.md"],
			["模板规则", "B自媒体大脑/05-朋友圈创作/创作脚本规则/张医生-朋友圈写作模板与规则.md"],
			["文案样板", "B自媒体大脑/05-朋友圈创作/创作脚本规则/星光私董会-朋友圈文案库（模板×样板）.md"],
			["交付库", "B自媒体大脑/05-朋友圈创作/交付脚本库/index.md"]
		],
		inputLabel: "这条朋友圈想说什么",
		placeholder: "例如：今天有人问我为什么医生不学营养学 / 为什么医生自己也在吃营养素",
		build: (input) => `写一条朋友圈，主题是：${input}

先读《张医生-朋友圈写作流程规则 v3.2 融合版》全文，再严格按「十、写朋友圈总流程」执行，不得简化：
1. 灵感/选题（创业／AI／活动／生活）
2. 过三道闸（板块？一点？术语＝营养素；朋友圈免质检，唯一底线是术语）
3. 定板块 + 定类型（悬念／痛点／干货／证言／福利／人设／认知暴击）
4. 套对应模板 + 叠风格招式（九种语气开关至少带 1-2 个；观点型走洞见五步）
5. 用我的真实素材 + 数字武器填肉（AI 类补一个「AI 做了什么」的细节）
6. 过融合检查清单（16 条铁律 + 出稿检查清单，全过才发）
7. 输出纯文字直发版（含【图】占位 + 可选 #标签），配图我自己负责
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
			["筛选", "过入盒标准，不合格直接丢"],
			["成卡", "按 4K 制式做成洞见卡／知识卡片"],
			["沉淀知识库", "归入洞见卡库或知识卡片库"],
			["沉淀选题库", "按内容线写入安利／AI／公众号选题库"],
			["反哺调用", "下次写稿优先从这些选题里取"]
		],
		files: [
			["入盒规则", "A知识沉淀大脑/00-新知识入库/00-灵感库·入盒规则.md"],
			["洞见卡库", "A知识沉淀大脑/00-新知识入库/洞见卡/洞见卡库.md"],
			["知识卡片库", "A知识沉淀大脑/00-新知识入库/知识卡片/知识卡片库.md"],
			["卡片模板", "A知识沉淀大脑/00-新知识入库/知识卡片/卡片模板.md"],
			["安利选题库", "B自媒体大脑/00-选题库/安利选题库.md"],
			["AI 选题库", "B自媒体大脑/00-选题库/AI选题库.md"],
			["公众号选题库", "B自媒体大脑/00-选题库/公众号选题弹药库.md"],
			["评论区选题池", "B自媒体大脑/00-选题库/评论区选题池.md"]
		],
		inputLabel: "要入库的内容 / 链接 / 来源",
		placeholder: "直接把内容贴进来，或写：飞书录音 2026-10-19 那场",
		build: (input) => `这条知识入库：${input}

请按《00-灵感库·入盒规则》执行，必须走完两条沉淀线，缺一条都算没入库：
A. 知识沉淀：入盒 → 筛选 → 按 4K 制式成卡（洞见卡或知识卡片）→ 归入洞见卡库／知识卡片库。
B. 选题沉淀：从卡片里提炼可写角度，按内容线写入对应选题库——
· 营养／创业／团队／成长 → B自媒体大脑/00-选题库/安利选题库.md
· AI 相关 → B自媒体大脑/00-选题库/AI选题库.md
· 适合写成公众号长文 → B自媒体大脑/00-选题库/公众号选题弹药库.md
· 来自评论区的问题 → B自媒体大脑/00-选题库/评论区选题池.md

每条选题必须标注：来源卡片编号 + 核心观点 + 可写角度 + 建议平台。
完成后回报两处结果：落在哪个知识库、进了哪个选题库（附链接）。`
	},
	{
		key: "profile",
		title: "张大侠个人档案",
		icon: "user",
		color: "#8e6bd1",
		desc: "我的底色、信念、真痛点和说话方式。给建议前先过这层。",
		steps: [
			["我是谁", "农村娃 → 麻醉医生 → 亏损 → 安利 → AI 营养师"],
			["我要什么", "FC、演唱会、父母、帮更多人"],
			["真痛点", "身体在漏、聚焦在散、系统在缺"],
			["家庭线", "张翊南的音乐培养"],
			["怎么说话", "医生式逻辑、数字、对比、金句"]
		],
		files: [
			["人物档案", "A知识沉淀大脑/06-张大侠/人物档案-张大侠.md"],
			["AI 张大侠", "A知识沉淀大脑/06-张大侠/AI张大侠.md"],
			["张翊南", "A知识沉淀大脑/06-张大侠/张翊南.md"],
			["音乐执行表", "A知识沉淀大脑/06-张大侠/张翊南-音乐培养执行表.md"]
		],
		inputLabel: "要我按你的底色回答什么",
		placeholder: "例如：我下个月该聚焦哪件事 / 帮我判断这个合作值不值得做",
		build: (input) => `先读《人物档案-张大侠》《AI张大侠》，按我的底色、信念、真痛点和沟通口味来回答：${input}`
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
			["渲染 PPT", "python-pptx 直接出黄底黑字 .pptx"],
			["交付归档", "按日期+期号命名，存入微课工作流目录"]
		],
		files: [
			["微课总流程", "C社群工作台/社群微课工作流/README.md"],
			["周五健康微课堂", "C社群工作台/社群微课工作流/每周五-健康微课堂.md"],
			["周二故事分享", "C社群工作台/社群微课工作流/每周二-健康故事分享.md"],
			["PPT 技能", "F技能库skill/01-PPT技能/notebooklm-slide-prompts/SKILL.md"]
		],
		inputLabel: "这场微课讲什么",
		placeholder: "例如：周五 26-22期 蛋白质不同人群怎么吃 / 周二 我的减脂故事",
		build: (input) => `做一场社群微课：${input}

先读《社群微课工作流 README》《每周五-健康微课堂》《每周二-健康故事分享》，判断是周五知识干货型还是周二案例见证型，然后按对应完整流程执行，不得简化：
1、定场次、主题、期号（期号延续上期数字）
2、写社群推广文案（按模板：@所有人 + 主题期号 + 一个震撼事实/数据 + 2-3 句价值描述 + 今晚 19:30 + 本群主理人张医生 + 鼓掌表情）
3、生成完整讲稿：周五按四段式（欢迎 2 分钟 / 名词解释 4 分钟 / 知识分解+痛点 6 分钟 / 纽崔莱方案 4 分钟，总 15-20 分钟）；周二按六段式图文（每段标 [插入图片]）
4、生成 PPT 大纲（逐页：标题 / 核心要点 / 配图建议，用 --- 分页）
5、用 python-pptx 直接渲染 .pptx（黄底黑字·时尚杂志风，按《F技能库skill/01-PPT技能/notebooklm-slide-prompts/SKILL.md》），存 C社群工作台/社群微课工作流/
6、按命名规范交付：《主题》-YYYY-MM-DD-期号.pptx 和 《主题》-讲稿-YYYY-MM-DD-期号.md；日期用 date 实取，期号延续上期
四样一次给全，不要只给大纲。`
	}
];

const LIBRARY_LINKS = [
	["安利选题库", "B自媒体大脑/00-选题库/安利选题库.md", "#e5534b"],
	["AI 选题库", "B自媒体大脑/00-选题库/AI选题库.md", "#5b7bd5"],
	["公众号选题弹药库", "B自媒体大脑/00-选题库/公众号选题弹药库.md", "#3f9e5c"],
	["评论区选题池", "B自媒体大脑/00-选题库/评论区选题池.md", "#e08a3c"]
];

const LIBRARY_MODULE = {
	key: "library",
	title: "题库 · 按主题找选题",
	icon: "library",
	color: "#5b7bd5",
	desc: "从四个选题库里检索匹配的题，按可写性排序。",
	steps: [
		["说主题", "例如：鱼油／蛋白质／医生身份"],
		["检索", "四个库一起找，不只看安利库"],
		["给候选", "附来源、编号、核心观点、可写角度"]
	],
	files: LIBRARY_LINKS,
	inputLabel: "你想找什么方向的选题",
	placeholder: "例如：鱼油 / 蛋白质 / 医生为什么系列",
	build: (input) => `从我的四个选题库里找选题：${input}

请检索《安利选题库》《AI选题库》《公众号选题弹药库》《评论区选题池》，按与主题的相关度和可写性排序，给我 5-8 个候选。
每个候选标注：来源库 + 选题编号 + 核心观点 + 可写角度 + 建议平台。`
};

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

		const library = root.createDiv({ cls: "zfc-library" });

		const libraryHead = library.createDiv({ cls: "zfc-library-head" });
		libraryHead.createDiv({
			cls: "zfc-library-title",
			text: "📚 题库"
		});
		libraryHead.createDiv({
			cls: "zfc-library-sub",
			text: "四个选题库 · 一键进入"
		});

		const libraryList = library.createDiv({ cls: "zfc-library-list" });
		for (const [label, path, color] of LIBRARY_LINKS) {
			const button = libraryList.createEl("button", {
				cls: "zfc-library-btn",
				text: label
			});
			button.style.setProperty("--lib-color", color);
			button.addEventListener("click", () => {
				this.app.workspace.openLinkText(path, "", true);
			});
		}

		const findButton = library.createEl("button", {
			cls: "zfc-library-find",
			text: "按主题找选题 →"
		});
		findButton.addEventListener("click", () => {
			new ActionModal(this.app, LIBRARY_MODULE, this.plugin).open();
		});

		const grid = root.createDiv({ cls: "zfc-grid" });

		for (const mod of MODULES) {
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
		contentEl.createEl("p", {
			cls: "zfc-card-desc",
			text: this.mod.desc
		});

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
			text: "点「开始」后会自动复制标准指令、打开 Claudian 并填进输入框，你按回车就开工。⌘/Ctrl + Enter 也可以直接开始。"
		});

		setTimeout(() => this.inputEl.focus(), 50);
	}

	async run() {
		const input = (this.inputEl.value || "").trim();
		if (!input) {
			new Notice("先填一句主题，再开始。");
			this.inputEl.focus();
			return;
		}

		const prompt = this.mod.build(input);

		try {
			await navigator.clipboard.writeText(prompt);
		} catch (error) {
			new Notice("剪贴板不可用，指令已准备好但需要手动复制。");
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
			.setDesc("开启时工作台常驻：打开 Obsidian 自动显示，手动关掉也会自动重开。想彻底关闭，先关掉这个开关。")
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

class ZfcWorkbenchPlugin extends Plugin {
	async onload() {
		await this.loadSettings();

		this.registerView(
			VIEW_TYPE,
			(leaf) => new WorkbenchView(leaf, this)
		);

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
			plugins &&
				plugins.plugins &&
				plugins.plugins.realclaudian
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

		if (
			input.tagName === "TEXTAREA" ||
			input.tagName === "INPUT"
		) {
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
