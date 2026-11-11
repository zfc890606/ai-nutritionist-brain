# 🎬 视频号创作 Skill 清单

> 本目录收录可执行技能源码/说明副本。`~/.claude/skills` 中 `content-risk-detector` / `ai-detector` 为指向本目录的符号链接。

## 已收录（物理副本）
- `content-risk-detector/` — 内容风险检测（合规网关闸口，内含 `ai-detector`）
- **`sepia` + `humanizer-zh` 双引擎去 AI 味（主力）** — sepia 先修结构（write / review / refactor / recreate；实体在 [[F技能库skill/02-其他技能/sepia/README|F技能库]]），humanizer-zh 再扫中文词句；01–05 模块共用
- `humanizer-zh/` — 中文词句扫描（第二道 · 内置 24 条 AI 痕迹清单）
- `short-video-opening-optimizer/` — 短视频开头优化
- `ai-font-36prompts/` — AI 生图/字体提示词 36 法
- `chapter-progress-bar/` — 章节进度条
- `封面提示词/` — 视频封面提示词

## 发布技能（全局已装 · 非本库实体）
`~/.claude/skills/`：`douyin-upload` · `kuaishou-upload` · `bilibili-upload` · `xiaohongshu-upload`（程序本体：social-auto-upload）
