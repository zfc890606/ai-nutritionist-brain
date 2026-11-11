# -*- coding: utf-8 -*-
"""
AI 艺人公司 · 大健康落地实战  ——  全篇黑底版 v2
风格：Modern Newspaper × 瑞士/包豪斯 · 纯黑底 + 白字 + 电光黄点缀 · 非对称布局 · 超大标题
v2 改动：
  板块一整体重写 —— 依《07·易洋·AI超级个体与一人公司》讲「艺人公司」的定义与趋势
    （一个人+AI军团=一支团队 / AI一年≈十年 / 3.2亿灵活用工 / 未来10年只有稳定能力 / AI平权 / 三种换钱方式）
  板块二结尾新增「我的版本答案」：Agent + 薄肌 + 个人IP + 自媒体 + 睡觉8小时
（函数风格复刻自 gen_ai_deck.py）
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------- 调色板（黑底） ----------
BG    = RGBColor(0x11, 0x11, 0x11)
SURF  = RGBColor(0x1B, 0x1B, 0x1B)
LINE  = RGBColor(0x33, 0x33, 0x33)
T1    = RGBColor(0xFF, 0xFF, 0xFF)
T2    = RGBColor(0xA8, 0xA8, 0xA8)
T3    = RGBColor(0x6E, 0x6E, 0x6E)
YEL   = RGBColor(0xFF, 0xCC, 0x00)
RED   = RGBColor(0xFF, 0x3B, 0x3B)

F_HEI = 'Hiragino Sans GB'
F_IMP = 'Impact'
F_HEL = 'Helvetica Neue'
F_SER = 'Songti SC'

W, H = 13.333, 7.5
N_TOTAL = 30

prs = Presentation()
prs.slide_width  = Inches(W)
prs.slide_height = Inches(H)


def _cjk(run, font):
    rPr = run._r.get_or_add_rPr()
    for tag in ('a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set('typeface', font)


def style_run(r, text, size, color, bold, font, spc=None):
    r.text = text
    f = r.font
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = color
    f.name = font
    _cjk(r, font)
    if spc is not None:
        r._r.get_or_add_rPr().set('spc', str(int(spc * 100)))


def new_slide(bg=BG):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg
    return s


def rect(s, l, t, w, h, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE):
    shp = s.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
    shp.shadow.inherit = False
    shp.text_frame.word_wrap = True
    return shp


def card(s, l, t, w, h, fill=SURF, border=LINE, accent=False, accent_w=0.13):
    shp = rect(s, l, t, w, h, fill=fill, line=border, lw=0.75)
    if accent:
        rect(s, l, t, accent_w, h, fill=YEL)
    return shp


def add_text(s, l, t, w, h, text, size=14, color=T1, bold=False, font=F_HEI,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, ls=1.15, spc=None,
             wrap=True, rich=None):
    box = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    try:
        tf.vertical_anchor = anchor
    except Exception:
        pass
    lines = rich if rich is not None else [(text, size, color, bold, font)]
    for i, item in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = ls
        runs = item if isinstance(item, list) else [item]
        for rspec in runs:
            txt, sz, col, bd, fn = rspec[:5]
            r = p.add_run()
            style_run(r, txt, sz, col, bd, fn)
    return box


def shape_text(shp, text, size=12, color=T1, bold=False, font=F_HEI,
               align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, ls=1.25,
               pad=(0.18, 0.18, 0.12, 0.12)):
    tf = shp.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(pad[0]); tf.margin_right = Inches(pad[1])
    tf.margin_top = Inches(pad[2]);  tf.margin_bottom = Inches(pad[3])
    try:
        tf.vertical_anchor = anchor
    except Exception:
        pass
    for i, line in enumerate(text.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = ls
        r = p.add_run()
        style_run(r, line, size, color, bold, font)
    return shp


def crop_marks(s, color=T1, m=0.20, L=0.14, th=0.014):
    for (cx, cy, sx, sy) in [(m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)]:
        x = cx if sx > 0 else cx - L
        rect(s, x, cy - th / 2, L, th, fill=color)
        y = cy if sy > 0 else cy - L
        rect(s, cx - th / 2, y, th, L, fill=color)


def chrome(s, page, sec=''):
    if sec:
        add_text(s, 0.85, 0.44, 8.5, 0.28, sec, size=9, color=T3, font=F_HEI, spc=1.4)
    crop_marks(s)
    frac = page / N_TOTAL
    rect(s, 0, H - 0.055, W * frac, 0.055, fill=YEL)
    rect(s, W * frac, H - 0.055, W * (1 - frac), 0.055, fill=LINE)
    add_text(s, 11.4, H - 0.44, 1.1, 0.24, "%02d / %02d" % (page, N_TOTAL),
             size=9, color=T2, font=F_HEL, align=PP_ALIGN.RIGHT)


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


def row_cards(s, items, y, h, title_size=17, desc_size=10.5, hot_last=False):
    """一排等宽卡片：[(num, title, desc), ...]"""
    n = len(items)
    GAP = 0.22
    CW = (11.55 - (n - 1) * GAP) / n
    for i, (num, t, d) in enumerate(items):
        x = 0.9 + i * (CW + GAP)
        hot = hot_last and (i == n - 1)
        card(s, x, y, CW, h, fill=(YEL if hot else SURF), border=(None if hot else LINE))
        add_text(s, x + 0.22, y + 0.20, CW - 0.4, 0.3, num, size=12,
                 color=(BG if hot else YEL), bold=True, font=F_IMP)
        add_text(s, x + 0.22, y + 0.66, CW - 0.36, 0.6, t, size=title_size,
                 color=(BG if hot else T1), bold=True, ls=1.1)
        add_text(s, x + 0.22, y + 1.30, CW - 0.36, 0.9, d, size=desc_size,
                 color=(BG if hot else T2), ls=1.3)


# ============================================================
# S1 封面
# ============================================================
s = new_slide()
add_text(s, 0.9, 0.55, 6, 0.3, "张医生 · AI 营养师", size=11, color=T1, spc=1.8)
add_text(s, 7.6, 0.55, 4.8, 0.3, "艺人公司 · 大健康落地实战", size=11, color=T2,
         align=PP_ALIGN.RIGHT, spc=1.8)
add_text(s, 0.85, 2.05, 9.5, 3.2, "",
         rich=[[("一", 175, T1, True, F_HEI), ("人", 175, YEL, True, F_HEI)]], ls=1.0)
rect(s, 0.9, 5.22, 2.6, 0.045, fill=YEL)
add_text(s, 0.9, 5.48, 8.6, 0.6, "一个人，一家公司 —— 一个人 ＋ AI，干出一支团队",
         size=19, color=YEL, font=F_SER)
add_text(s, 8.75, 5.44, 3.75, 1.2,
         "定义与趋势 × 大健康实战\n授课 + 实操",
         size=10.5, color=T2, ls=1.5)
add_text(s, 0.9, 6.50, 8, 0.3, "2026.10 · 内部实战分享", size=10, color=T3, font=F_HEL, spc=1.2)
crop_marks(s)
notes(s, "开场：今天讲一件事 —— 什么是艺人公司，为什么它一定是未来，以及怎么用 AI 把大健康做成它。")


# ============================================================
# S2 目录
# ============================================================
s = new_slide()
chrome(s, 2, "CONTENTS · 今晚讲什么")
add_text(s, 0.9, 1.32, 11, 1.0, "三个部分", size=60, color=T1, bold=True)
rows = [
    ("01", "观念重塑", "重新理解「艺人公司」：定义 · 为什么是未来"),
    ("02", "落地大健康", "AI 打通专业与创作：两个大脑 · 我的版本答案"),
    ("03", "现场实操", "看我的电脑，现场搭「营养师大脑」与「自媒体大脑」"),
]
y0 = 2.62
for i, (num, title, desc) in enumerate(rows):
    y = y0 + i * 1.30
    rect(s, 0.9, y, 11.55, 0.02, fill=LINE)
    add_text(s, 0.9, y + 0.12, 2.0, 1.0, num, size=58, color=YEL, bold=True, font=F_IMP)
    add_text(s, 2.70, y + 0.30, 9.5, 0.5, title, size=26, color=T1, bold=True)
    add_text(s, 2.75, y + 0.86, 9.5, 0.4, desc, size=13.5, color=T2)
rect(s, 0.9, y0 + 3 * 1.30, 11.55, 0.02, fill=LINE)
notes(s, "三部分：先讲清楚艺人公司是什么、为什么是未来；再讲 AI 怎么落在大健康；最后现场动手搭两个大脑。")


# ============================================================
# S3 章节页 01 · 观念重塑
# ============================================================
s = new_slide()
chrome(s, 3, "PART 01 / 03")
add_text(s, 0.85, 1.05, 3.0, 1.6, "01", size=104, color=YEL, bold=True, font=F_IMP)
add_text(s, 0.85, 2.70, 9.5, 2.2, "观念重塑", size=128, color=T1, bold=True, ls=1.0)
rect(s, 0.9, 5.30, 2.4, 0.045, fill=YEL)
add_text(s, 0.9, 5.52, 11, 0.5, "什么是艺人公司 · 为什么它是未来", size=18, color=T2)
notes(s, "第一部分，先把观念掰正。很多人做不大、做不赚，不是能力问题，是观念一开始就错了。")


# ============================================================
# S4 艺人公司是什么（定义）
# ============================================================
s = new_slide()
chrome(s, 4, "01 · 观念重塑 — 定义")
add_text(s, 0.9, 1.10, 11.5, 1.0, "「艺人公司」是什么？", size=56, color=T1, bold=True)
add_text(s, 0.9, 2.20, 11.4, 0.5, "一句话，先把定义说清楚。", size=16, color=T3)
band = rect(s, 0.9, 2.85, 11.55, 1.45, fill=YEL)
shape_text(band, "一个人 ＋ 一堆 AI 工具 ＝ 一家公司的产出",
           size=30, color=BG, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
cards = [("老板", "你", "决定做什么、卖给谁、怎么卖"),
         ("员工", "AI", "随时扩编、随时替换、不拿工资")]
for i, (tag, k, d) in enumerate(cards):
    x = 0.9 + i * 6.35
    card(s, x, 4.65, 5.65, 1.55, accent=True)
    add_text(s, x + 0.48, 4.88, 3, 0.3, tag, size=12, color=T3, spc=1.2)
    add_text(s, x + 1.45, 4.86, 4.2, 0.5, k, size=26, color=YEL, bold=True)
    add_text(s, x + 1.55, 5.50, 4.2, 0.4, d, size=12.5, color=T2)
add_text(s, 0.9, 6.42, 11.5, 0.4, "你是操盘手，AI 是你的员工 —— 一个人，干出一支团队的产出。",
         size=15, color=YEL, bold=True)
notes(s, "艺人公司的定义就一句话：一个人加一堆 AI 工具，等于一家公司的产出。你是老板，AI 是员工。"
         "它还有个别名，叫「AI 艺人公司」—— 一个人，干出一支团队。")


# ============================================================
# S5 一个人 + AI 军团 = 一支团队
# ============================================================
s = new_slide()
chrome(s, 5, "01 · 观念重塑 — 核心转变")
add_text(s, 0.9, 1.15, 11.5, 1.0, "一个人，干出一支团队", size=52, color=T1, bold=True)
add_text(s, 0.9, 2.24, 11.4, 0.5, "核心不是你自己多能干，而是你能调动多少 AI 替你干。", size=18, color=T2)
row_cards(s, [
    ("01", "总管", "统筹与决策"),
    ("02", "运营", "内容与社群"),
    ("03", "工程", "产品与工具"),
    ("04", "设计", "画面与排版"),
    ("05", "分析", "数据与复盘"),
], y=3.05, h=2.35, title_size=20, desc_size=11)
band = rect(s, 0.9, 5.72, 11.55, 0.85, fill=YEL)
shape_text(band, "你是老板，AI 是员工 —— 而且随时可扩编、可替换。", size=17, color=BG, bold=True,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "一个人怎么干出一支团队？靠的是 AI 数字员工军团：总管、运营、工程、设计、分析。"
         "核心不是你能干，而是你能调动多少 AI 替你干。你是老板，AI 是员工。")


# ============================================================
# S6 为什么是现在？AI 一年 ≈ 传统十年
# ============================================================
s = new_slide()
chrome(s, 6, "01 · 观念重塑 — 为什么是现在")
add_text(s, 0.9, 1.25, 11.5, 1.0, "为什么，是现在？", size=54, color=T1, bold=True)
add_text(s, 0.9, 2.42, 11.5, 1.2, "",
         rich=[[("AI 一年 ", 46, T1, True, F_HEI), ("≈", 46, YEL, True, F_HEI),
                (" 传统十年", 46, T1, True, F_HEI)]], ls=1.1)
rect(s, 0.9, 3.90, 5.4, 0.11, fill=YEL)
cards = [("起点", "2023.3.18", "GPT-4 诞生。2026 年，才真正开始加速。"),
         ("性质", "底层革命", "这是「生产力」的革命，不是「消费场景」的变化。")]
for i, (tag, k, d) in enumerate(cards):
    x = 0.9 + i * 6.35
    card(s, x, 4.30, 5.65, 1.95)
    add_text(s, x + 0.35, 4.56, 3, 0.35, tag, size=12, color=YEL, bold=True, spc=1.2)
    add_text(s, x + 0.35, 4.96, 5.0, 0.6, k, size=28, color=T1, bold=True)
    add_text(s, x + 0.35, 5.64, 5.0, 0.5, d, size=12.5, color=T2, ls=1.35)
notes(s, "为什么是现在？因为 AI 一年，约等于传统时代十年。起点是 2023 年 3 月 18 号的 GPT-4，到 2026 年才真正加速。"
         "这是生产力底层的革命，不是互联网那种消费场景的变化。")


# ============================================================
# S7 · 3.2 亿灵活用工
# ============================================================
s = new_slide()
chrome(s, 7, "01 · 观念重塑 — 就业现状")
add_text(s, 0.9, 0.88, 6, 0.5, "先看一个数字 ——", size=18, color=T3)
add_text(s, 0.72, 1.68, 8.5, 4.2, "3.2亿", size=200, color=YEL, bold=True, font=F_IMP, ls=0.9)
cd = card(s, 7.55, 3.75, 4.95, 2.20, accent=True)
shape_text(cd, "中国社科院数据：\n中国已有 3.2 亿灵活用工。\n人，早就不在「一份工作」里了。",
           size=19, color=T1, bold=True, ls=1.35, anchor=MSO_ANCHOR.MIDDLE,
           pad=(0.55, 0.35, 0.28, 0.28))
add_text(s, 0.9, 6.42, 11.5, 0.4,
         "稳定工作，正在被重新定义 —— 不是你有没有一份工，而是你有没有一份能带去任何地方的能力。",
         size=11, color=T3)
notes(s, "看一个数字：3.2 亿。中国社科院数据，中国已有 3.2 亿灵活用工。也就是说，人早就不在「一份工作」里了。"
         "稳定工作正在被重新定义。")


# ============================================================
# S8 未来 10 年，只有稳定能力
# ============================================================
s = new_slide()
chrome(s, 8, "01 · 观念重塑 — 最大前提")
add_text(s, 0.9, 1.35, 11.5, 1.6, "未来 10 年，\n没有稳定工作", size=58, color=T1, bold=True, ls=1.12)
rect(s, 0.9, 3.62, 5.4, 0.11, fill=YEL)
add_text(s, 0.9, 4.00, 11.4, 1.0, "只有「基于 AI 的稳定能力」。", size=30, color=YEL, bold=True)
add_text(s, 0.9, 5.32, 11.4, 1.0,
         "真正抢你饭碗的，不是 AI ——\n是已经学会用 AI 的老板、同事、同龄人。",
         size=17, color=T2, ls=1.5)
notes(s, "最大的前提结论：未来十年，不再有稳定工作，只有基于 AI 的稳定能力。"
         "记住 —— 抢你饭碗的不是 AI，是已经学会用 AI 的老板、同事、同龄人。")


# ============================================================
# S9 AI 平权：普通人第一次和精英站同一起跑线
# ============================================================
s = new_slide()
chrome(s, 9, "01 · 观念重塑 — AI 平权")
add_text(s, 0.9, 1.15, 11.5, 1.2, "普通人，第一次和精英\n站在同一起跑线", size=50, color=T1, bold=True, ls=1.15)
rect(s, 0.9, 3.20, 5.4, 0.11, fill=YEL)
cards = [("过去", "工具是壁垒", "好用的工具、算力，是精英和大厂才玩得起的东西。"),
         ("现在", "工具人人可用", "AI 工具暴跌到每月约 20 美金 —— 门槛，被推平了。")]
for i, (tag, k, d) in enumerate(cards):
    x = 0.9 + i * 6.35
    last = (i == 1)
    card(s, x, 3.62, 5.65, 2.20, fill=(SURF if not last else SURF))
    rect(s, x, 3.62, 5.65, 0.10, fill=(YEL if last else LINE))
    add_text(s, x + 0.35, 3.90, 3, 0.35, tag, size=13, color=(YEL if last else T3), bold=True)
    add_text(s, x + 0.35, 4.30, 5.0, 0.6, k, size=26, color=(T1 if last else T2), bold=True)
    add_text(s, x + 0.35, 5.00, 5.0, 0.7, d, size=12.5, color=T2, ls=1.4)
add_text(s, 0.9, 6.10, 11.5, 0.4, "AI 时代，是平权的时代。", size=17, color=YEL, bold=True)
notes(s, "为什么普通人这次有机会？因为 AI 是平权时代。过去工具和算力是精英的壁垒，"
         "现在 AI 工具暴跌到每月二十美金左右，人人都用得起 —— 普通人第一次和精英站在同一条起跑线上。")


# ============================================================
# S10 三种把时间换钱的方式
# ============================================================
s = new_slide()
chrome(s, 10, "01 · 观念重塑 — 财富逻辑")
add_text(s, 0.9, 1.05, 11.5, 1.0, "三种，把时间换钱的方式", size=48, color=T1, bold=True)
row_cards(s, [
    ("A", "卖给一个人", "打工人。买家有绝对议价权，工资必然不高。"),
    ("B", "卖给很多人", "艺人 · 网红。边际成本≈0，一份时间卖无数次。"),
    ("C", "采买别人的时间", "企业家。把产品卖给无限多的人。"),
], y=2.30, h=2.75, title_size=19, desc_size=11.5)
add_text(s, 0.9, 5.35, 11.5, 0.9,
         "用 AI，你能同时拿到后两种 ——\n把一份时间卖给很多人，再把生产力变成生产资料。",
         size=18, color=YEL, bold=True, ls=1.4)
notes(s, "把时间换成钱，只有三种方式：A，卖给一个人，就是打工人，议价权在别人手里；"
         "B，卖给很多人，就是艺人、网红，边际成本几乎为零；C，采买别人的时间再卖产品，就是企业家。"
         "艺人公司要做的，是用 AI 同时拿到 B 和 C —— 一份时间卖给很多人，再把生产力变成生产资料。")


# ============================================================
# S11 所以，它一定是未来
# ============================================================
s = new_slide()
chrome(s, 11, "01 · 观念重塑 — 小结")
add_text(s, 0.9, 1.10, 11.5, 1.0, "所以，它一定是未来", size=54, color=T1, bold=True)
row_cards(s, [
    ("01", "就业在变", "3.2 亿灵活用工，人不再属于一份工作"),
    ("02", "工具在平权", "AI 人人可用，普通人第一次与精英同线"),
    ("03", "组织在变小", "一个人 + AI 军团 = 一支团队"),
], y=2.45, h=2.55, title_size=20, desc_size=12)
band = rect(s, 0.9, 5.40, 11.55, 1.05, fill=YEL)
shape_text(band, "  一个人，就是一家公司。 —— 观念掰正了，下一步是落地。",
           size=18, color=BG, bold=True, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "所以，艺人公司一定是未来：就业在变、工具在平权、组织在变小。一句话 —— 一个人，就是一家公司。"
         "观念掰正了，下一步就是落地。")


# ============================================================
# S12 章节页 02 · 落地大健康
# ============================================================
s = new_slide()
chrome(s, 12, "PART 02 / 03")
add_text(s, 0.85, 1.05, 3.0, 1.6, "02", size=104, color=YEL, bold=True, font=F_IMP)
add_text(s, 0.85, 2.70, 11.5, 2.2, "落地大健康", size=118, color=T1, bold=True, ls=1.0)
rect(s, 0.9, 5.30, 2.4, 0.045, fill=YEL)
add_text(s, 0.9, 5.52, 11, 0.5, "AI 打通专业与创作，落在大健康", size=18, color=T2)
notes(s, "观念有了，往下落地。为什么是 AI？为什么落在大健康？这一部分讲清楚。")


# ============================================================
# S13 金钱的本质
# ============================================================
s = new_slide()
chrome(s, 13, "02 · 落地 — 一句话立底")
add_text(s, 0.9, 1.50, 11.5, 2.6, "金钱的本质，\n是信息在创造价值", size=60, color=T1, bold=True, ls=1.18)
rect(s, 0.9, 4.26, 4.6, 0.11, fill=YEL)
add_text(s, 0.9, 4.54, 6, 0.4, "——《人类简史》", size=15, color=T2, font=F_SER)
add_text(s, 0.9, 5.30, 11.4, 1.4,
         "所有生意，本质上都在处理同一件事：信息。\n信息差，就是财富差。",
         size=19, color=T1, ls=1.5)
add_text(s, 0.9, 6.55, 11.4, 0.4,
         "过去一切生意，都建立在「我知道的，你不知道」之上。这一层，AI 把它推平了。",
         size=13, color=T3)
notes(s, "只立一个底：《人类简史》讲得很清楚，金钱是一套共同相信的信息。商业的底层，从头到尾都是信息在创造价值。")


# ============================================================
# S14 AI 把信息推平了
# ============================================================
s = new_slide()
chrome(s, 14, "02 · 落地 — 一句话带过")
add_text(s, 0.9, 1.55, 11.5, 1.6, "",
         rich=[[("AI，把信息", 60, T1, True, F_HEI),
                ("推平", 60, YEL, True, F_HEI),
                ("了", 60, T1, True, F_HEI)]], ls=1.1)
rect(s, 0.9, 3.28, 6.6, 0.11, fill=YEL)
add_text(s, 0.9, 3.66, 11.2, 1.6,
         "任何人、任何行业，一键就能拿到最核心的信息与技术。\n信息差正在消失 —— 靠「我知道你不知道」赚钱的时代，结束了。",
         size=18, color=T2, ls=1.5)
add_text(s, 0.9, 5.70, 11.4, 0.5, "这件事不用再论证。AI 已经是既定事实。", size=22, color=T1, bold=True)
notes(s, "一句话带过：AI 已经把信息门槛推平。不用再论证 AI 行不行，它已经是既定事实。")


# ============================================================
# S15 · 84%
# ============================================================
s = new_slide()
chrome(s, 15, "02 · 落地 — 但是")
add_text(s, 0.9, 0.88, 6, 0.5, "但是 ——", size=18, color=T3)
add_text(s, 0.72, 1.68, 8.5, 4.2, "84%", size=250, color=YEL, bold=True, font=F_IMP, ls=0.9)
cd = card(s, 7.55, 3.85, 4.95, 2.10, accent=True)
shape_text(cd, "全球约 68 亿人，\n从未用过 AI。\n真正付费使用的，只有 0.3%。",
           size=20, color=T1, bold=True, ls=1.35, anchor=MSO_ANCHOR.MIDDLE,
           pad=(0.55, 0.35, 0.28, 0.28))
add_text(s, 0.9, 6.62, 11.5, 0.4,
         "数据：2026 年全球 AI 使用分布统计（各机构估算区间 72%–84%，取最广泛引用的 84%）· Microsoft Q1 2026：仅 17.8% 劳动年龄人口用过生成式 AI",
         size=8.5, color=T3)
notes(s, "全场最重要的一个数字：全球 84% 的人从没用过 AI，付费的只有 0.3%。AI 推平了门槛，但绝大多数人还没进门。")


# ============================================================
# S16 那么，普通人怎么布局
# ============================================================
s = new_slide()
chrome(s, 16, "02 · 落地 — 那么")
add_text(s, 0.9, 1.40, 11.5, 0.7, "那么，普通人怎么布局？", size=56, color=T1, bold=True)
rect(s, 0.9, 2.45, 5.4, 0.11, fill=YEL)
dirs = [("方向一", "专业", "让 AI 打通你的专业", "把行业最核心的信息，装进 AI"),
        ("方向二", "流量", "让 AI 打通你的创作", "把有价值的信息，交付给人")]
for i, (tag, key, title, desc) in enumerate(dirs):
    y = 3.05 + i * 1.72
    card(s, 0.9, y, 11.55, 1.50, accent=True)
    add_text(s, 1.30, y + 0.28, 2.0, 0.35, tag, size=12, color=T3, spc=1.2)
    add_text(s, 3.10, y + 0.22, 2.6, 0.7, key, size=32, color=YEL, bold=True)
    add_text(s, 5.70, y + 0.26, 6.4, 0.6, title, size=22, color=T1, bold=True)
    add_text(s, 5.72, y + 0.86, 6.4, 0.4, desc, size=13, color=T2)
notes(s, "普通人怎么布局？就两个方向：用 AI 打通专业，用 AI 打通创作。")


# ============================================================
# S17 方向一 · 专业
# ============================================================
s = new_slide()
chrome(s, 17, "02 · 落地 — 方向一 · 专业")
add_text(s, 0.9, 1.15, 11.5, 0.6, "方向一 · 专业", size=18, color=YEL, bold=True)
add_text(s, 0.9, 1.75, 11.5, 1.2, "AI 打通专业", size=64, color=T1, bold=True)
rect(s, 0.9, 3.10, 5.0, 0.11, fill=YEL)
add_text(s, 0.9, 3.52, 11.3, 1.6,
         "把最权威的专业信息装进 AI ——\n你的专业能力，不再只长在你一个人身上。",
         size=19, color=T2, ls=1.5)
steps = [("01", "喂进专业信息", "权威书籍 · 行业资料"), ("02", "给它方案样板", "你的标准 = 它的标准"), ("03", "营养师大脑", "可复制 · 可交付")]
for i, (num, t, d) in enumerate(steps):
    x = 0.9 + i * 3.95
    last = (i == 2)
    card(s, x, 5.10, 3.45, 1.35, fill=(YEL if last else SURF), border=(None if last else LINE))
    add_text(s, x + 0.28, 5.28, 2, 0.3, num, size=12, color=(BG if last else T3), bold=True, font=F_IMP)
    add_text(s, x + 0.28, 5.60, 3.0, 0.4, t, size=18, color=(BG if last else T1), bold=True)
    add_text(s, x + 0.28, 6.02, 3.0, 0.3, d, size=11, color=(BG if last else T2))
    if i < 2:
        add_text(s, x + 3.45, 5.62, 0.55, 0.4, "→", size=20, color=YEL, bold=True,
                 align=PP_ALIGN.CENTER, wrap=False)
notes(s, "方向一，专业。把权威信息喂进 AI，给它一个方案样板，就得到可复制的营养师大脑。")


# ============================================================
# S18 方向二 · 创作
# ============================================================
s = new_slide()
chrome(s, 18, "02 · 落地 — 方向二 · 创作")
add_text(s, 0.9, 1.15, 11.5, 0.6, "方向二 · 流量", size=18, color=YEL, bold=True)
add_text(s, 0.9, 1.75, 11.5, 1.2, "AI 打通创作", size=64, color=T1, bold=True)
rect(s, 0.9, 3.10, 5.0, 0.11, fill=YEL)
add_text(s, 0.9, 3.52, 11.3, 1.6,
         "信息不等于商业 —— 必须交付出去，才产生价值。\n而自媒体，就是那个交付的出口。",
         size=19, color=T2, ls=1.5)
steps = [("01", "给创作规则", "选题 · 结构 · 爆款逻辑"), ("02", "给一个选题", "一句话就够"), ("03", "自媒体大脑", "脚本 · 成片 · 触达")]
for i, (num, t, d) in enumerate(steps):
    x = 0.9 + i * 3.95
    last = (i == 2)
    card(s, x, 5.10, 3.45, 1.35, fill=(YEL if last else SURF), border=(None if last else LINE))
    add_text(s, x + 0.28, 5.28, 2, 0.3, num, size=12, color=(BG if last else T3), bold=True, font=F_IMP)
    add_text(s, x + 0.28, 5.60, 3.0, 0.4, t, size=18, color=(BG if last else T1), bold=True)
    add_text(s, x + 0.28, 6.02, 3.0, 0.3, d, size=11, color=(BG if last else T2))
    if i < 2:
        add_text(s, x + 3.45, 5.62, 0.55, 0.4, "→", size=20, color=YEL, bold=True,
                 align=PP_ALIGN.CENTER, wrap=False)
notes(s, "方向二，流量。给 AI 一套创作规则，再给一个选题，它就能出脚本、出成片。")


# ============================================================
# S19 而这一切，落在大健康
# ============================================================
s = new_slide()
chrome(s, 19, "02 · 落地 — 落地行业")
add_text(s, 0.9, 1.30, 11.5, 1.6, "而这一切，落在大健康", size=62, color=T1, bold=True)
rect(s, 0.9, 3.05, 5.4, 0.11, fill=YEL)
add_text(s, 0.9, 3.50, 11.3, 1.6,
         "人群最广、需求最刚、复购最强。\n慢病解决方案与营养管理 —— 周期长、信任重、极度依赖专业，正是 AI 最能放大的地方。",
         size=19, color=T2, ls=1.5)
add_text(s, 0.9, 5.85, 11.2, 0.4,
         "以上为健康科普分享，不构成诊疗建议，个体情况请咨询专业医师。",
         size=9.5, color=T3)
notes(s, "为什么落在大健康？人群最广、需求最刚、复购最强。慢病和营养周期长、信任重、极度依赖专业。")


# ============================================================
# S20 AI 营养师 = 两个大脑
# ============================================================
s = new_slide()
chrome(s, 20, "02 · 落地 — 落地模型")
add_text(s, 0.9, 1.20, 11.5, 0.9, "AI 营养师 = 两个大脑", size=54, color=T1, bold=True)
cards = [("01", "营养师大脑", "行业里最有价值的专业信息", "慢病 · 营养 · 方案"),
         ("02", "自媒体大脑", "内容创作与流量的信息", "选题 · 脚本 · 爆款")]
for i, (num, title, desc, tag) in enumerate(cards):
    x = 0.9 + i * 6.35
    card(s, x, 2.55, 5.65, 3.35)
    rect(s, x, 2.55, 5.65, 0.10, fill=YEL)
    add_text(s, x + 0.35, 2.90, 2, 0.5, num, size=22, color=YEL, bold=True, font=F_IMP)
    add_text(s, x + 0.35, 3.35, 5.0, 0.8, title, size=32, color=T1, bold=True)
    add_text(s, x + 0.35, 4.28, 5.0, 0.7, desc, size=15, color=T2)
    add_text(s, x + 0.35, 5.20, 5.0, 0.4, tag, size=12, color=T3, font=F_SER)
add_text(s, 6.30, 3.95, 1.0, 0.6, "+", size=40, color=YEL, bold=True,
         align=PP_ALIGN.CENTER, wrap=False)
notes(s, "落地就靠两个大脑：营养师大脑解决专业，自媒体大脑解决流量。")


# ============================================================
# S21 成为专家，找到人群
# ============================================================
s = new_slide()
chrome(s, 21, "02 · 落地 — 闭环")
add_text(s, 0.9, 1.35, 11.5, 1.0, "成为专家，找到人群", size=58, color=T1, bold=True)
steps = [("用 AI 成为\n行业专家", False), ("用 AI 触达\n更多人群", False),
         ("完成交付\n形成闭环", True), ("获得\n商业回报", True)]
for i, (txt, hot) in enumerate(steps):
    x = 0.9 + i * 3.02
    card(s, x, 2.85, 2.72, 2.35, fill=(YEL if hot else SURF), border=(None if hot else LINE))
    add_text(s, x + 0.25, 3.35, 2.3, 1.4, txt, size=19,
             color=(BG if hot else T1), bold=True, ls=1.35)
    if i < 3:
        add_text(s, x + 2.74, 3.75, 0.30, 0.5, "→", size=22, color=YEL, bold=True,
                 align=PP_ALIGN.CENTER, wrap=False)
add_text(s, 0.9, 5.70, 11.5, 0.8, "商业的本质，就这样被你完整跑通了一遍。",
         size=18, color=T2, font=F_SER)
notes(s, "专家 + 人群 + 交付 = 闭环。这不是理论，是可以一步步做出来的路径。")


# ============================================================
# S22 一个人，抵一个团队
# ============================================================
s = new_slide()
chrome(s, 22, "02 · 落地 — 一个人抵一个团队")
add_text(s, 0.9, 0.98, 11.5, 0.9, "一个人，抵一个团队", size=44, color=T1, bold=True)
add_text(s, 0.9, 1.74, 11.5, 0.4, "过去这些活儿，要请 6 个人来做。", size=15, color=T2)
JOBS = [("文案编辑", 6000), ("内容运营", 7000), ("拍摄", 7000),
        ("剪辑", 7000), ("课程教研", 10000), ("客户服务", 5000)]
TOT = sum(v for _, v in JOBS)
BARW = 10.50
TONES = [0x24, 0x30, 0x3C, 0x48, 0x54, 0x60]
add_text(s, 0.9, 2.34, 9.0, 0.3, "过去 · 6 个岗位 · 每月", size=11, color=T3, spc=1.2)
x = 0.9
for i, (name, val) in enumerate(JOBS):
    wseg = BARW * val / TOT
    rect(s, x, 2.62, wseg, 0.95, fill=RGBColor(TONES[i], TONES[i], TONES[i]), line=BG, lw=1.0)
    add_text(s, x + 0.13, 2.78, wseg - 0.22, 0.3, name, size=10.5, color=T1, bold=True)
    add_text(s, x + 0.13, 3.08, wseg - 0.22, 0.35, "¥%s" % format(val, ","),
             size=12.5, color=YEL, bold=True, font=F_HEL)
    x += wseg
add_text(s, 0.9, 3.70, 6.0, 0.4, "合计 ¥%s / 月" % format(TOT, ","), size=19, color=T1, bold=True)
add_text(s, 6.6, 3.76, 5.9, 0.3, "参考市场月薪测算 · 按你当地行情调整",
         size=9.5, color=T3, align=PP_ALIGN.RIGHT)
add_text(s, 0.9, 4.32, 9.0, 0.3, "现在 · 一个人 + AI · 每月", size=11, color=T3, spc=1.2)
rect(s, 0.9, 4.58, 0.34, 0.95, fill=YEL)
add_text(s, 1.48, 4.62, 4.5, 0.5, "¥350 / 月", size=22, color=YEL, bold=True)
add_text(s, 1.48, 5.16, 8.5, 0.35,
         "大模型会员 ¥200 ＋ AI 剪辑 ¥100 ＋ 素材工具 ¥50", size=10.5, color=T2)
add_text(s, 0.9, 5.92, 7.5, 1.0, "成本 ≈ 1%", size=54, color=YEL, bold=True)
add_text(s, 7.6, 6.38, 4.9, 0.4, "同样的活儿，一个人 ＋ AI 跑完。",
         size=14, color=T2, align=PP_ALIGN.RIGHT)
notes(s, "过去 6 个岗位一个月四万二；现在一个人加 AI 一个月三百五，成本约 1%。这里讲的不是省钱，是产能。")


# ============================================================
# S23 我的版本答案
# ============================================================
s = new_slide()
chrome(s, 23, "02 · 落地 — 我的版本答案")
add_text(s, 0.9, 1.05, 11.5, 1.0, "我坚信的版本答案", size=52, color=T1, bold=True)
add_text(s, 0.9, 2.14, 11.4, 0.5, "大健康艺人公司的未来，我押这五样 ——", size=17, color=T2)
row_cards(s, [
    ("01", "Agent", "让 AI 替我干活"),
    ("02", "薄肌", "把身体练回来"),
    ("03", "个人 IP", "医生人设 · 信任"),
    ("04", "自媒体", "内容持续触达"),
    ("05", "睡觉 8 小时", "把作息修回来"),
], y=2.80, h=2.55, title_size=19, desc_size=11)
band = rect(s, 0.9, 5.62, 11.55, 0.95, fill=YEL)
shape_text(band, "  生意要做，身体也要修回来 —— 这，就是我的版本答案。",
           size=18, color=BG, bold=True, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "第二部分收口。大健康艺人公司的未来，我的版本答案是这五个词：Agent、薄肌、个人 IP、自媒体、睡觉 8 小时。"
         "一边用 AI 把生意做成一个人的公司，一边把身体和作息修回来 —— 这才是我真正相信的答案。")


# ============================================================
# S24 章节页 03 · 现场实操
# ============================================================
s = new_slide()
chrome(s, 24, "PART 03 / 03")
add_text(s, 0.85, 1.05, 3.0, 1.6, "03", size=104, color=YEL, bold=True, font=F_IMP)
add_text(s, 0.85, 2.70, 9.5, 2.2, "现场实操", size=128, color=T1, bold=True, ls=1.0)
rect(s, 0.9, 5.30, 2.4, 0.045, fill=YEL)
add_text(s, 0.9, 5.52, 11, 0.5, "看我的电脑 · 现场搭两个大脑", size=18, color=T2)
notes(s, "下半场不讲道理，只动手。先看我的电脑，然后一步步教你搭。")


# ============================================================
# S25 先看我的电脑
# ============================================================
s = new_slide()
chrome(s, 25, "03 · 实操 — 先看结果")
add_text(s, 0.9, 1.20, 11.5, 1.0, "先看我的电脑", size=58, color=T1, bold=True)
two = [("A", "知识沉淀大脑", "这些年积累的营养 · 慢病 · 方案素材，全部结构化沉淀"),
       ("B", "自媒体大脑", "选题库 · 爆款库 · 脚本规则，全部沉淀成可调用的资产")]
for i, (k, title, desc) in enumerate(two):
    x = 0.9 + i * 6.35
    card(s, x, 2.70, 5.65, 2.05, accent=True)
    add_text(s, x + 0.48, 3.05, 2, 0.5, k, size=26, color=YEL, bold=True, font=F_IMP)
    add_text(s, x + 1.10, 3.08, 4.4, 0.6, title, size=26, color=T1, bold=True)
    add_text(s, x + 1.10, 3.75, 4.4, 0.9, desc, size=13, color=T2, ls=1.45)
band = rect(s, 0.9, 5.25, 11.55, 1.05, fill=YEL)
shape_text(band, "  这两个大脑不是天生的，也不是买的 —— 是攒出来的。\n  接下来，我教你怎么从零搭起来。",
           size=16, color=BG, bold=True, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "先看成品。两个大脑，一个是专业知识，一个是自媒体能力。看完了，我们开始搭。")


# ============================================================
# S26 实操一
# ============================================================
s = new_slide()
chrome(s, 26, "03 · 实操 一 — 营养师大脑")
add_text(s, 0.9, 1.15, 11.5, 0.7, "实操一", size=20, color=YEL, bold=True)
add_text(s, 0.9, 1.70, 11.5, 1.0, "用豆包，搭一个营养师大脑", size=46, color=T1, bold=True)
rect(s, 0.9, 2.95, 5.2, 0.11, fill=YEL)
add_text(s, 0.9, 3.35, 11.5, 0.5, "两步，就两步：", size=17, color=T2)
for i, (num, t, d) in enumerate([
        ("第一步", "先把专业书「喂」进去", "让大脑拥有这个行业最核心的信息"),
        ("第二步", "再给它一个方案样板", "让它照着样板，直接出解决方案")]):
    x = 0.9 + i * 6.35
    card(s, x, 4.05, 5.65, 1.95)
    add_text(s, x + 0.35, 4.32, 3, 0.4, num, size=14, color=RED, bold=True)
    add_text(s, x + 0.35, 4.72, 5.0, 0.6, t, size=24, color=T1, bold=True)
    add_text(s, x + 0.35, 5.32, 5.0, 0.5, d, size=13, color=T2)
notes(s, "营养师大脑的搭建只有两步：喂书，给样板。下面把提示词一条一条给你。")


# ============================================================
# S27 提示词 ①
# ============================================================
s = new_slide()
chrome(s, 27, "03 · 实操 一 — 提示词 ①")
add_text(s, 0.9, 1.05, 11.5, 0.9, "提示词 ①：把书喂进去", size=42, color=T1, bold=True)
box = card(s, 0.9, 2.20, 7.6, 4.25, accent=True)
shape_text(box,
           "请你作为一位资深临床营养师。\n\n"
           "以下内容是你必须掌握的专业知识基础：\n"
           "·《科学营养圣经》\n"
           "·《中国营养学会 · 膳食营养素参考摄入量》\n"
           "·《临床药学》\n"
           "·（以及你手上所有权威营养学资料）\n\n"
           "请全部学习并记住，作为你后续所有方案的依据。",
           size=14, color=T1, ls=1.55, anchor=MSO_ANCHOR.TOP, pad=(0.45, 0.35, 0.35, 0.3))
add_text(s, 8.85, 2.25, 3.7, 0.4, "为什么要喂书？", size=15, color=T1, bold=True)
rect(s, 8.85, 2.72, 1.6, 0.06, fill=YEL)
add_text(s, 8.85, 3.00, 3.7, 3.3,
         "· 让回答有据可依，不瞎编\n\n· 统一口径，避免前后矛盾\n\n"
         "· 权威来源 = 专业感与信任感\n\n· 一次喂好，长期复用",
         size=13.5, color=T2, ls=1.5)
notes(s, "第一条提示词，把书喂进去。书单要写具体，越权威越好。这一步决定这个大脑的天花板。")


# ============================================================
# S28 提示词 ②
# ============================================================
s = new_slide()
chrome(s, 28, "03 · 实操 一 — 提示词 ②")
add_text(s, 0.9, 1.05, 11.5, 0.9, "提示词 ②：给它一个方案样板", size=42, color=T1, bold=True)
box = card(s, 0.9, 2.20, 7.6, 4.25, accent=True)
shape_text(box,
           "这是我们的标准方案样板：\n〔此处粘贴一份你写好的完整方案〕\n\n"
           "从现在起，请严格按照这个样板的\n结构、语气、颗粒度来输出。\n\n"
           "接下来我会给你客户的疾病与症状，\n请你直接输出一份完整、可交付的\n调理解决方案。",
           size=14, color=T1, ls=1.55, anchor=MSO_ANCHOR.TOP, pad=(0.45, 0.35, 0.35, 0.3))
add_text(s, 8.85, 2.25, 3.7, 0.4, "工作方式", size=15, color=T1, bold=True)
rect(s, 8.85, 2.72, 1.6, 0.06, fill=YEL)
flow = ["疾病 · 症状", "按样板生成", "完整解决方案"]
for i, f in enumerate(flow):
    y = 3.05 + i * 0.92
    last = (i == 2)
    shape_text(card(s, 8.85, y, 3.7, 0.66, fill=(YEL if last else SURF),
                    border=(None if last else LINE)),
               f, size=15, color=(BG if last else T1), bold=True, align=PP_ALIGN.CENTER)
    if i < 2:
        add_text(s, 10.6, y + 0.68, 0.4, 0.24, "↓", size=14, color=YEL, bold=True,
                 align=PP_ALIGN.CENTER, wrap=False)
notes(s, "第二条提示词，给它一个样板。样板就是标准，你给多好的样板，它就出多好的方案。")


# ============================================================
# S29 实操二
# ============================================================
s = new_slide()
chrome(s, 29, "03 · 实操 二 — 自媒体大脑")
add_text(s, 0.9, 1.15, 11.5, 0.7, "实操二", size=20, color=YEL, bold=True)
add_text(s, 0.9, 1.70, 11.5, 1.0, "一个提示词，直接出爆款脚本", size=46, color=T1, bold=True)
rect(s, 0.9, 2.95, 5.2, 0.11, fill=YEL)
box = card(s, 0.9, 3.35, 7.6, 3.10, accent=True)
shape_text(box,
           "你是我的短视频创作助手。\n\n这是我的脚本创作规则：\n〔粘贴你的创作脚本提示词〕\n\n"
           "现在我给你一个选题，\n请直接输出一条完整、可拍的口播脚本。",
           size=14, color=T1, ls=1.55, anchor=MSO_ANCHOR.TOP, pad=(0.45, 0.35, 0.35, 0.3))
add_text(s, 8.85, 3.40, 3.7, 0.4, "拿到就能拍", size=15, color=T1, bold=True)
rect(s, 8.85, 3.87, 1.6, 0.06, fill=YEL)
for i, f in enumerate(["给一个选题", "生成爆款脚本", "直接开拍"]):
    y = 4.20 + i * 0.62
    last = (i == 2)
    shape_text(card(s, 8.85, y, 3.7, 0.48, fill=(YEL if last else SURF),
                    border=(None if last else LINE)),
               f, size=14, color=(BG if last else T1), bold=True, align=PP_ALIGN.CENTER)
notes(s, "自媒体大脑更简单：一条提示词加一个选题，脚本直接出来。你只需要判断好不好，然后去拍。")


# ============================================================
# S30 结尾
# ============================================================
s = new_slide()
chrome(s, 30, "THE END · 现在开始")
add_text(s, 0.9, 1.55, 11.5, 2.4, "做自己的老板", size=96, color=T1, bold=True, ls=1.05)
rect(s, 0.9, 4.25, 5.0, 0.12, fill=YEL)
add_text(s, 0.9, 4.72, 11.4, 1.8,
         "艺人公司 × 大健康\n一个人，也能跑完整个闭环。",
         size=26, color=YEL, ls=1.5, font=F_SER)
add_text(s, 0.9, 6.40, 8, 0.4, "张医生 · AI 营养师｜2026.10", size=11, color=T3, font=F_HEL, spc=1.2)
notes(s, "收尾：控制权拿回自己手里，用 AI 把大健康做成一个人的公司 —— 做小、做赚、做自由。")


# ---------- 保存 ----------
out_dir = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(out_dir, 'AI艺人公司·大健康落地实战.pptx')
prs.save(out)
print('SAVED:', out)
print('SLIDES:', len(prs.slides))
