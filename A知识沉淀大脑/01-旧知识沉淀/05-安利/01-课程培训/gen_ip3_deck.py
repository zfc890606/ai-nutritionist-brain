# -*- coding: utf-8 -*-
"""
AI 未来时代 · 个人 IP 三步  ——  团队内部分享（12 页）
风格：Modern Newspaper × 瑞士/包豪斯 · 纯黑底 + 白字 + 电光黄点缀（沿用「大健康落地实战」终版视觉）
主题：① 找到自己是谁 ② 被更多人看见 ③ 把过程变成产品
来源：张医生 2026-10-13 口述整理（自媒体实操zfc 第四十八节）
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
N_TOTAL = 12

prs = Presentation()
prs.slide_width  = Inches(W)
prs.slide_height = Inches(H)


# ---------- 基础工具 ----------
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
        add_text(s, 0.85, 0.44, 9.5, 0.28, sec, size=9, color=T3, font=F_HEI, spc=1.4)
    crop_marks(s)
    frac = page / N_TOTAL
    rect(s, 0, H - 0.055, W * frac, 0.055, fill=YEL)
    rect(s, W * frac, H - 0.055, W * (1 - frac), 0.055, fill=LINE)
    add_text(s, 11.4, H - 0.44, 1.1, 0.24, "%02d / %02d" % (page, N_TOTAL),
             size=9, color=T2, font=F_HEL, align=PP_ALIGN.RIGHT)


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


# ============================================================
# S1 封面
# ============================================================
s = new_slide()
add_text(s, 0.9, 0.55, 6, 0.3, "张医生 · AI 营养师", size=11, color=T1, spc=1.8)
add_text(s, 7.5, 0.55, 4.9, 0.3, "自媒体 · 个人 IP · 创业", size=11, color=T2,
         align=PP_ALIGN.RIGHT, spc=1.8)

add_text(s, 0.85, 2.00, 11.5, 3.0, "", ls=1.0,
         rich=[[("个人 IP ", 150, T1, True, F_HEI), ("三步", 150, YEL, True, F_HEI)]])

rect(s, 0.9, 5.30, 2.6, 0.045, fill=YEL)
add_text(s, 0.9, 5.56, 11.5, 0.6, "找到自己 → 被更多人看见 → 变成产品",
         size=22, color=YEL, font=F_SER)
add_text(s, 0.9, 6.55, 8, 0.3, "2026.10 · 团队内部分享", size=10, color=T3, font=F_HEL, spc=1.2)
crop_marks(s)
notes(s, "开场一句话：AI 未来时代真正重要的就三件事——先找到自己是谁，再被更多人看见，最后把过程变成产品。今晚只讲这三步。")

# ============================================================
# S2 目录
# ============================================================
s = new_slide()
chrome(s, 2, "CONTENTS · 今晚讲三件事")
add_text(s, 0.9, 1.25, 11, 1.0, "三件事", size=56, color=T1, bold=True)

rows = [("01", "找到自己是谁", "IP 的底层 = 定位 · 从一段真实的历程里挖"),
        ("02", "被更多人看见", "传播 = 一切链接的基础 · 自媒体 + 社群 + 朋友圈"),
        ("03", "把过程变成产品", "产品思维 · 让后期的辅助变简单")]
for i, (num, t, d) in enumerate(rows):
    y = 2.72 + i * 1.28
    rect(s, 0.9, y, 11.55, 0.02, fill=LINE)
    add_text(s, 0.9, y + 0.08, 2.0, 1.2, num, size=60, color=YEL, bold=True, font=F_IMP)
    add_text(s, 2.75, y + 0.26, 8.8, 0.6, t, size=30, color=T1, bold=True)
    add_text(s, 2.80, y + 0.84, 9.5, 0.4, d, size=13.5, color=T2)
rect(s, 0.9, 2.72 + 3 * 1.28, 11.55, 0.02, fill=LINE)
notes(s, "把整场收成三件事：找到自己、被看见、变成产品。一环扣一环，缺一个都跑不通。")

# ============================================================
# S3 立底 · 一句话
# ============================================================
s = new_slide()
chrome(s, 3, "立底 · 一句话")
add_text(s, 0.9, 1.55, 11.5, 2.6, "", ls=1.15,
         rich=[("自媒体和创业，", 52, T1, True, F_HEI),
               [("本质是", 52, T1, True, F_HEI), ("同一件事", 52, YEL, True, F_HEI)]])
rect(s, 0.9, 4.35, 5.4, 0.11, fill=YEL)
add_text(s, 0.9, 4.80, 11.4, 1.4, "", ls=1.4,
         rich=[("真实的你，那股能量——", 22, T1, False, F_SER),
               ("被呈现出去、传递出去的过程。", 22, YEL, False, F_SER)])
add_text(s, 0.9, 6.45, 11.4, 0.4, "其实，没有多复杂。", size=14, color=T3)
notes(s, "先立一个底：自媒体也好、创业也好，本质上是同一件事——你这个人、那股真实的能量，被呈现、被传递出去。想通这一点，后面都不复杂。")

# ============================================================
# S4 第一步
# ============================================================
s = new_slide()
chrome(s, 4, "第一步 · 找到自己是谁")
add_text(s, 0.9, 1.25, 11.5, 0.5, "第一步", size=18, color=YEL, bold=True)
add_text(s, 0.9, 1.78, 11.5, 1.2, "找到自己是谁", size=70, color=T1, bold=True)
rect(s, 0.9, 3.20, 5.0, 0.11, fill=YEL)
add_text(s, 0.9, 3.65, 11.3, 1.7, "", ls=1.5,
         rich=[("IP 的本质，是为了让自己被更多人看见；", 20, T2, False, F_HEI),
               ("而被看见的前提——是你先知道自己是谁。", 20, T1, False, F_HEI)])
band = rect(s, 0.9, 5.90, 11.55, 0.72, fill=YEL)
shape_text(band, "先知道自己是谁，才有后面的一切。", size=17, color=BG, bold=True,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "第一步，也是 IP 的地基：你如果不知道自己是谁，后面所有传播都是空转。先回答这个问题。")

# ============================================================
# S5 每一段历程都是一幅作品
# ============================================================
s = new_slide()
chrome(s, 5, "第一步 · 每一段历程，都是一幅作品")
add_text(s, 0.9, 1.20, 11.5, 1.9, "", ls=1.1,
         rich=[("每一段历程，", 50, T1, True, F_HEI),
               [("都是一幅", 50, T1, True, F_HEI), ("作品", 50, YEL, True, F_HEI)]])

cards = [("①", "IP 的本质", "让自己被更多人看见"),
         ("②", "被看见的前提", "先知道自己是谁"),
         ("③", "关键的能力", "把这段历程，构建成故事")]
CW = (11.55 - 2 * 0.35) / 3
for i, (num, t, d) in enumerate(cards):
    x = 0.9 + i * (CW + 0.35)
    card(s, x, 3.35, CW, 1.90, accent=True)
    add_text(s, x + 0.36, 3.56, 2.0, 0.4, num, size=16, color=YEL, bold=True)
    add_text(s, x + 0.36, 4.02, CW - 0.6, 0.5, t, size=20, color=T1, bold=True)
    add_text(s, x + 0.36, 4.56, CW - 0.6, 0.6, d, size=13, color=T2, ls=1.35)

add_text(s, 0.9, 5.65, 11.4, 0.6, "真正稀缺的不是经历，是你把经历讲成故事的能力。",
         size=16, color=YEL, font=F_SER)
notes(s, "把这句话讲透：每一段经历本身都是一幅作品，关键在于你有没有能力把它构建成一个故事。IP 定位，挖的就是你这段能讲成故事的真实历程。")

# ============================================================
# S6 去哪里挖
# ============================================================
s = new_slide()
chrome(s, 6, "第一步 · 去哪里挖")
add_text(s, 0.9, 1.15, 11.5, 0.9, "去你自己的产业里，挖那段真实历程", size=38, color=T1, bold=True)
add_text(s, 0.9, 2.02, 11.5, 0.4, "你真真实实走过、也真真实实做成过的那一段——", size=15, color=T2)

cases = ["痘痘\n调理好了", "减掉\n几十斤脂肪", "穿越低谷\n走到高光", "为家人健康\n走过一段路"]
CW = (11.55 - 3 * 0.30) / 4
for i, c in enumerate(cases):
    x = 0.9 + i * (CW + 0.30)
    sh = card(s, x, 2.72, CW, 1.75)
    shape_text(sh, c, size=16, color=T1, bold=True, align=PP_ALIGN.CENTER,
               anchor=MSO_ANCHOR.MIDDLE, ls=1.35)

band = rect(s, 0.9, 4.82, 11.55, 1.05, fill=YEL)
shape_text(band, "别人抄不走、复制不了 ——\n这，就是 IP 定位真正要挖的核心点。",
           size=17, color=BG, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ls=1.4)
add_text(s, 0.9, 6.15, 11.4, 0.4, "任何一段这样的历程，都可以成为你 IP 里最亮的一个闪光点。",
         size=13, color=T3)
notes(s, "怎么挖？打开你自己的产业、项目、产品，找那段你真正走过、也真正做成过的历程。痘痘、减脂、低谷到高光、为家人的健康……都能成为 IP 里最亮的那个点。因为它是真的，别人抄不走。")

# ============================================================
# S7 第二步
# ============================================================
s = new_slide()
chrome(s, 7, "第二步 · 被更多人看见")
add_text(s, 0.9, 1.15, 11.5, 0.5, "第二步", size=18, color=YEL, bold=True)
add_text(s, 0.9, 1.68, 11.5, 1.2, "被更多人看见", size=70, color=T1, bold=True)
add_text(s, 0.9, 2.88, 11.5, 0.4, "自媒体 + 社群 + 朋友圈，全方位把自己展示出去。", size=15, color=T2)
rect(s, 0.9, 3.45, 5.0, 0.11, fill=YEL)

flow = ["先表达 · 先输出", "让更多人看见", "才产生吸引力", "吸引 = 链接的基础"]
CW = (11.55 - 3 * 0.24) / 4
for i, f in enumerate(flow):
    x = 0.9 + i * (CW + 0.24)
    last = (i == 3)
    sh = card(s, x, 3.95, CW, 1.35, fill=(YEL if last else SURF),
              border=(None if last else LINE))
    shape_text(sh, f, size=15, color=(BG if last else T1), bold=True,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ls=1.3)
    if i < 3:
        add_text(s, x + CW, 4.45, 0.24, 0.4, "→", size=18, color=YEL, bold=True,
                 align=PP_ALIGN.CENTER, wrap=False)

add_text(s, 0.9, 5.62, 11.4, 0.6, "不是等别人来找你，是先把真实的自己，送到更多人面前。",
         size=17, color=YEL, bold=True)
notes(s, "第二步：核心点找到了，就大量传播、分享。用心地输出、表达、构建故事，把能量爆发出去。逻辑链是——先表达、被看见、才存在、才有吸引力，吸引就是一切链接的基础。")

# ============================================================
# S8 第三步
# ============================================================
s = new_slide()
chrome(s, 8, "第三步 · 把过程变成产品")
add_text(s, 0.9, 1.15, 11.5, 0.5, "第三步", size=18, color=YEL, bold=True)
add_text(s, 0.9, 1.68, 11.5, 1.2, "把过程变成产品", size=66, color=T1, bold=True)
rect(s, 0.9, 2.98, 5.0, 0.11, fill=YEL)

two = [("为什么", "越来越多人看见你、被你吸引\n→ 有人想成为你 · 想学 · 想被交付"),
       ("怎么做", "用产品思维，把这段路、这套方法\n做成一份可交付的产品")]
CW = (11.55 - 0.35) / 2
for i, (tag, body) in enumerate(two):
    x = 0.9 + i * (CW + 0.35)
    sheet = card(s, x, 3.42, CW, 1.85, accent=True)
    add_text(s, x + 0.55, 3.66, 2.4, 0.4, tag, size=15, color=YEL, bold=True)
    add_text(s, x + 0.55, 4.14, CW - 0.9, 1.0, body, size=15, color=T1, ls=1.5)

band = rect(s, 0.9, 5.55, 11.55, 0.85, fill=YEL)
shape_text(band, "有了产品，后期的辅助（成交 · 带人 · 复制）都会变简单。",
           size=17, color=BG, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "第三步：被看见、被吸引之后，一定会有人想成为你、想学、想被交付。这时候用产品思维，把你走过的路变成可交付的产品。有了产品，后面成交、带人、复制都会简单很多。")

# ============================================================
# S9 收口 · 本质
# ============================================================
s = new_slide()
chrome(s, 9, "收口 · 本质")
add_text(s, 0.9, 1.35, 11.5, 2.2, "", ls=1.15,
         rich=[("技巧遍地都是，", 50, T1, True, F_HEI),
               [("真实的你", 50, YEL, True, F_HEI), ("才是壁垒", 50, T1, True, F_HEI)]])
rect(s, 0.9, 3.88, 5.4, 0.11, fill=YEL)
add_text(s, 0.9, 4.32, 11.4, 1.6, "", ls=1.5,
         rich=[("不重视这一点，天天研究技巧和套路——这些东西遍地都是，", 19, T2, False, F_HEI),
               ("既没有竞争力，也构不成真正的壁垒。", 19, T2, False, F_HEI)])
add_text(s, 0.9, 6.05, 11.4, 0.6, "而我们借个人 IP 放大这股能量，一切都会变简单。",
         size=21, color=YEL, bold=True)
notes(s, "收口：反过来讲，如果你不重视这一点，天天研究技巧和套路——那东西遍地都是，没有竞争力，也构不成壁垒。而我们借个人 IP 放大这股能量，一切都会变简单。")

# ============================================================
# S10 落地三条
# ============================================================
s = new_slide()
chrome(s, 10, "落地 · 今晚就开始")
add_text(s, 0.9, 1.10, 11.5, 0.9, "三步，今晚就开始", size=48, color=T1, bold=True)

acts = [("01", "写下你做成过的那件事", "把它写成一段能讲 3 分钟的故事——这是你 IP 的地基。"),
        ("02", "把这段故事说出来", "一条朋友圈 + 一条短视频，先让身边人看见。"),
        ("03", "想清楚别人为什么买单", "想成为你 / 想学 / 想要你的方案——先写成一个产品雏形。")]
CW = (11.55 - 2 * 0.35) / 3
for i, (num, t, d) in enumerate(acts):
    x = 0.9 + i * (CW + 0.35)
    card(s, x, 2.35, CW, 3.15)
    rect(s, x, 2.35, CW, 0.10, fill=YEL)
    add_text(s, x + 0.36, 2.70, 2.0, 0.5, num, size=24, color=YEL, bold=True, font=F_IMP)
    add_text(s, x + 0.36, 3.35, CW - 0.65, 1.0, t, size=21, color=T1, bold=True, ls=1.25)
    add_text(s, x + 0.36, 4.40, CW - 0.65, 1.0, d, size=13.5, color=T2, ls=1.5)

add_text(s, 0.9, 5.95, 11.4, 0.4, "地基 → 被看见 → 变成产品 —— 一步一步来。", size=13, color=T3)
notes(s, "给三步各配一个今晚就能做的动作：写下那件事、把它说出来、想清楚别人为什么买单。今晚不用全做完，先做第一步。")

# ============================================================
# S11 金句
# ============================================================
s = new_slide()
chrome(s, 11, "金句 · 收藏")
add_text(s, 0.9, 1.15, 11.5, 0.8, "几句，记下来", size=40, color=T1, bold=True)

quotes = ["IP 的本质，是让自己被更多人看见。",
          "你走过的每一段路，都是一幅作品。",
          "先表达，再被看见——被看见了，你才存在。",
          "只有真实的你，才是壁垒。"]
for i, q in enumerate(quotes):
    y = 2.35 + i * 1.06
    rect(s, 0.9, y, 0.06, 0.66, fill=YEL)
    add_text(s, 1.20, y, 11.0, 0.66, q, size=20, color=T1, font=F_SER,
             anchor=MSO_ANCHOR.MIDDLE)
notes(s, "这四句可以慢慢念，也可以留给伙伴抄下来。核心就一句——只有真实的你，才是壁垒。")

# ============================================================
# S12 结尾
# ============================================================
s = new_slide()
chrome(s, 12, "THE END · 现在开始")
add_text(s, 0.9, 1.55, 11.5, 2.2, "", ls=1.05,
         rich=[[("先讲出", 96, T1, True, F_HEI), ("你的故事", 96, YEL, True, F_HEI)]])
rect(s, 0.9, 4.05, 5.0, 0.12, fill=YEL)
add_text(s, 0.9, 4.55, 11.4, 1.6, "", ls=1.45,
         rich=[("AI 未来时代，", 24, YEL, False, F_SER),
               ("真实，就是最大的竞争力。", 24, YEL, False, F_SER)])
add_text(s, 0.9, 6.35, 9, 0.4, "张医生 · AI 营养师｜2026.10 · 团队内部分享",
         size=11, color=T3, font=F_HEL, spc=1.2)
notes(s, "收尾：AI 未来时代，真实就是最大的竞争力。今天回去，先讲出你自己的那件事。")

# ---------- 保存 ----------
out_dir = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(out_dir, 'AI未来时代·个人IP三步.pptx')
prs.save(out)
print('SAVED:', out)
print('SLIDES:', len(prs.slides))
