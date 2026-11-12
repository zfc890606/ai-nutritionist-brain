const { Plugin, Notice, Modal, MarkdownView, setIcon } = require("obsidian");

/* 撤销按钮 —— 每个笔记面板标题栏一个「撤销」按钮
 * 原理：监听文件内容变化，把「改动前的内容」存成历史版本；
 *       点按钮 = 把笔记恢复成上一版（不管是自己打字改的，还是 AI 帮你改的）。
 */

const MAX_VERSIONS = 12; // 每条笔记最多留几版
const MAX_FILE_CHARS = 150000; // 超过 15 万字符的大文件不记录（太吃内存）
const MAX_TOTAL_CHARS = 3000000; // 全部加起来的上限
const QUIET_MS = 1200; // 连续改动停顿多久算「一次改动」
const SAVE_DELAY_MS = 4000;

const BTN_CLASS = "zfc-undo-btn";

function fmtTime(t) {
	const d = new Date(t);
	const p = (n) => String(n).padStart(2, "0");
	return `${d.getMonth() + 1}月${d.getDate()}日 ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

class HistoryModal extends Modal {
	constructor(app, plugin, file) {
		super(app);
		this.plugin = plugin;
		this.file = file;
	}

	onOpen() {
		const { contentEl } = this;
		contentEl.empty();
		contentEl.createEl("h3", { text: "历史版本 · " + this.file.basename });
		const versions = this.plugin.getVersions(this.file.path);
		if (!versions.length) {
			contentEl.createEl("p", { text: "这条笔记还没有记录到历史版本。" });
			return;
		}
		contentEl.createEl("p", {
			cls: "zfc-undo-hint",
			text: "点任意一版，笔记立即恢复成那一版的内容。"
		});
		const list = contentEl.createDiv({ cls: "zfc-undo-list" });
		versions
			.slice()
			.reverse()
			.forEach((v) => {
				const row = list.createDiv({ cls: "zfc-undo-row" });
				row.createDiv({ cls: "zfc-undo-time", text: fmtTime(v.t) });
				const preview = (v.c || "").replace(/\s+/g, " ").slice(0, 100);
				row.createDiv({ cls: "zfc-undo-preview", text: preview || "（空）" });
				row.addEventListener("click", async () => {
					this.close();
					await this.plugin.restoreTo(this.file, v);
				});
			});
	}

	onClose() {
		this.contentEl.empty();
	}
}

module.exports = class ZfcUndoPlugin extends Plugin {
	async onload() {
		const data = await this.loadData();
		this.store = (data && data.store) || {};
		this.redoMap = new Map();
		this.live = new Map();
		this.timers = new Map();
		this.restoring = new Set();
		this.saveTimer = null;

		this.registerEvent(this.app.vault.on("modify", (f) => this.onModify(f)));
		this.registerEvent(
			this.app.workspace.on("file-open", (f) => {
				if (f) this.prime(f);
			})
		);
		this.registerEvent(
			this.app.workspace.on("layout-change", () => this.installActions())
		);
		this.registerEvent(
			this.app.workspace.on("active-leaf-change", () => {
				this.installActions();
				this.primeOpen();
			})
		);
		this.registerInterval(
			window.setInterval(() => this.installActions(), 2000)
		);

		this.app.workspace.onLayoutReady(() => {
			this.installActions();
			this.primeOpen();
		});

		this.addCommand({
			id: "undo-previous-version",
			name: "撤销：恢复上一版",
			checkCallback: (checking) => {
				const view = this.app.workspace.getActiveViewOfType(MarkdownView);
				if (!view || !view.file) return false;
				if (!checking) this.undo(view.file);
				return true;
			}
		});
		this.addCommand({
			id: "undo-pick-version",
			name: "撤销：选择历史版本恢复",
			checkCallback: (checking) => {
				const view = this.app.workspace.getActiveViewOfType(MarkdownView);
				if (!view || !view.file) return false;
				if (!checking) new HistoryModal(this.app, this, view.file).open();
				return true;
			}
		});
		this.addCommand({
			id: "undo-redo",
			name: "撤销：重做刚才撤销掉的修改",
			checkCallback: (checking) => {
				const view = this.app.workspace.getActiveViewOfType(MarkdownView);
				if (!view || !view.file) return false;
				if (!checking) this.redo(view.file);
				return true;
			}
		});
	}

	onunload() {
		this.timers.forEach((t) => clearTimeout(t));
		this.timers.clear();
		if (this.saveTimer) clearTimeout(this.saveTimer);
		document
			.querySelectorAll("." + BTN_CLASS)
			.forEach((el) => el.remove());
		this.saveNow();
	}

	/* ---------- 面板按钮 ---------- */

	installActions() {
		this.app.workspace.getLeavesOfType("markdown").forEach((leaf) => {
			const view = leaf.view;
			if (!(view instanceof MarkdownView)) return;
			const header = view.containerEl.querySelector(".view-header");
			if (!header) return;
			if (header.querySelector("." + BTN_CLASS)) return;

			const target =
				header.querySelector(".view-actions") ||
				header.querySelector(".view-header-title-container") ||
				header;

			const button = document.createElement("button");
			button.type = "button";
			button.className = BTN_CLASS;
			button.title = "撤销上一版（恢复改动前的文案）";
			button.setAttribute("aria-label", "撤销上一版");

			const icon = document.createElement("span");
			icon.className = "zfc-undo-icon";
			setIcon(icon, "undo-2");
			button.appendChild(icon);
			button.appendChild(document.createTextNode("撤销"));

			button.addEventListener("click", (event) => {
				event.preventDefault();
				event.stopPropagation();
				if (view.file) this.undo(view.file, button);
			});

			if (target === header) {
				header.appendChild(button);
			} else if (target.classList.contains("view-actions")) {
				target.prepend(button);
			} else {
				target.appendChild(button);
			}

			if (view.file) this.prime(view.file);
		});
	}

	primeOpen() {
		this.app.workspace.getLeavesOfType("markdown").forEach((leaf) => {
			const file = leaf.view && leaf.view.file;
			if (file) this.prime(file);
		});
	}

	/* ---------- 记录历史 ---------- */

	async prime(file) {
		if (!file || file.extension !== "md" || this.live.has(file.path)) return;
		try {
			const c = await this.app.vault.read(file);
			this.live.set(file.path, c);
		} catch (e) {}
	}

	onModify(file) {
		if (!file || file.extension !== "md") return;
		const path = file.path;
		if (this.restoring.has(path)) return;
		if (!this.live.has(path)) {
			this.prime(file);
			return;
		}
		const t = this.timers.get(path);
		if (t) clearTimeout(t);
		this.timers.set(
			path,
			setTimeout(() => {
				this.timers.delete(path);
				this.flush(file);
			}, QUIET_MS)
		);
	}

	async flush(file) {
		const path = file.path;
		const t = this.timers.get(path);
		if (t) {
			clearTimeout(t);
			this.timers.delete(path);
		}
		if (!this.live.has(path)) {
			await this.prime(file);
			return;
		}
		let cur;
		try {
			cur = await this.app.vault.read(file);
		} catch (e) {
			return;
		}
		const prev = this.live.get(path);
		if (prev === cur) return;
		if (cur.length > MAX_FILE_CHARS) {
			this.live.set(path, cur);
			return;
		}
		this.pushVersion(path, prev);
		this.live.set(path, cur);
	}

	pushVersion(path, content) {
		const stack = this.store[path] || (this.store[path] = []);
		const last = stack[stack.length - 1];
		if (last && last.c === content) return;
		stack.push({ t: Date.now(), c: content });
		while (stack.length > MAX_VERSIONS) stack.shift();
		this.trimTotal();
		this.scheduleSave();
	}

	trimTotal() {
		let total = 0;
		for (const p in this.store) {
			for (const v of this.store[p]) total += v.c.length;
		}
		while (total > MAX_TOTAL_CHARS) {
			let oldestPath = null;
			let oldestT = Infinity;
			for (const p in this.store) {
				const s = this.store[p];
				if (s.length && s[0].t < oldestT) {
					oldestT = s[0].t;
					oldestPath = p;
				}
			}
			if (!oldestPath) break;
			total -= this.store[oldestPath].shift().c.length;
			if (!this.store[oldestPath].length) delete this.store[oldestPath];
		}
	}

	getVersions(path) {
		return (this.store[path] || []).slice();
	}

	/* ---------- 撤销 / 重做 ---------- */

	async undo(file, button) {
		if (!file) return;
		await this.flush(file);
		const stack = this.store[file.path] || [];
		let cur = "";
		try {
			cur = await this.app.vault.read(file);
		} catch (e) {}
		while (stack.length && stack[stack.length - 1].c === cur) stack.pop();
		if (!stack.length) {
			new Notice("这条笔记没有可撤销的修改");
			return;
		}
		const target = stack.pop();
		this.redoMap.set(file.path, { t: Date.now(), c: cur });
		await this.applyContent(file, target.c);
		if (button) {
			button.classList.add("is-done");
			window.setTimeout(() => button.classList.remove("is-done"), 500);
		}
		new Notice("已撤销，恢复到 " + fmtTime(target.t) + " 的版本");
	}

	async restoreTo(file, version) {
		let cur = "";
		try {
			cur = await this.app.vault.read(file);
		} catch (e) {}
		this.redoMap.set(file.path, { t: Date.now(), c: cur });
		await this.applyContent(file, version.c);
		new Notice("已恢复到 " + fmtTime(version.t) + " 的版本");
	}

	async redo(file) {
		const r = file && this.redoMap.get(file.path);
		if (!r) {
			new Notice("没有可重做的修改");
			return;
		}
		this.redoMap.delete(file.path);
		let cur = "";
		try {
			cur = await this.app.vault.read(file);
		} catch (e) {}
		this.pushVersion(file.path, cur);
		await this.applyContent(file, r.c);
		new Notice("已重做刚才撤销掉的修改");
	}

	async applyContent(file, content) {
		this.restoring.add(file.path);
		this.live.set(file.path, content);
		try {
			await this.app.vault.modify(file, content);
		} catch (e) {
			new Notice("操作失败：" + (e && e.message ? e.message : e));
		}
		setTimeout(() => this.restoring.delete(file.path), 1500);
		this.scheduleSave();
	}

	/* ---------- 存储 ---------- */

	scheduleSave() {
		if (this.saveTimer) clearTimeout(this.saveTimer);
		this.saveTimer = setTimeout(() => {
			this.saveTimer = null;
			this.saveNow();
		}, SAVE_DELAY_MS);
	}

	saveNow() {
		this.saveData({ store: this.store }).catch(() => {});
	}
};
