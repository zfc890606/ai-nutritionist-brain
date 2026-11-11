#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周五微课堂 26-22期《家庭健康管理员的价值》— Yellow × Black Editorial
黄底黑字 · 大号现代衬线 · 时尚杂志编辑风 · 波普黑块贴纸感
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

# ───────────── Palette ─────────────
YELLOW = RGBColor(0xFF, 0xD4, 0x00)
BLACK  = RGBColor(0x12, 0x12, 0x12)
INK    = RGBColor(0x1A, 0x1A, 0x1A)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GRAY   = RGBColor(0x5A, 0x5A, 0x5A)
RED    = RGBColor(0xD4, 0x1C, 0x2A)

SERIF = "Songti SC"
SANS  = "PingFang SC"
LATIN = "Georgia"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

M = Inches(0.85)
CW = W - 2 * M


def _set_ea(run, typeface):
    rPr = run._r.get_or_add_rPr()
    for tag in ('a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is None:
            el = parse_xml('<%s xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="%s"/>' % (tag, typeface))
            rPr.append(el)
        else:
            el.set('typeface', typeface)


def slide():
    s = prs.slides.add_slide(BLANK)
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = YELLOW
    return s


def rect(s, l, t, w, h, fill=None, line=None, lw=2.0, shape=MSO_SHAPE.RECTANGLE):
    sh = s.shapes.add_shape(shape, l, t, w, h)
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(lw)
    sh.shadow.inherit = False
    return sh


def text(s, l, t, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         serif=True, spacing=1.15, space_after=6):
    tb = s.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        for r in runs:
            txt = r[0]
            size = r[1]
            bold = r[2] if len(r) > 2 else False
            color = r[3] if len(r) > 3 else INK
            fname = r[4] if len(r) > 4 else (SERIF if serif else SANS)
            run = p.add_run()
            run.text = txt
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color
            run.font.name = fname
            _set_ea(run, fname)
    return tb


def eyebrow(s, label, num=None):
    rect(s, M, Inches(0.5), Inches(0.16), Inches(0.34), fill=BLACK)
    text(s, M + Inches(0.34), Inches(0.48), Inches(7.6), Inches(0.4),
         [[(label, 12, True, BLACK, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
    if num is not None:
        text(s, W - M - Inches(1.4), Inches(0.48), Inches(1.4), Inches(0.4),
             [[(num, 12, True, GRAY, SANS)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def title(s, txt, size=40, top=Inches(1.18), color=INK):
    text(s, M, top, CW, Inches(1.1), [[(txt, size, True, color, SERIF)]], spacing=1.0)
    rect(s, M, top + Inches(0.92), Inches(1.7), Pt(5), fill=BLACK)


def bullets(s, items, top=Inches(2.5), size=19, gap=0.62, width=None, l=None):
    l = l or M
    width = width or CW
    paras = []
    for it in items:
        if isinstance(it, tuple):
            pref, rest = it
            paras.append([("■  ", size, True, BLACK, SANS),
                          (pref, size, True, INK, SANS),
                          (rest, size, False, INK, SANS)])
        else:
            paras.append([("■  ", size, True, BLACK, SANS),
                          (it, size, False, INK, SANS)])
    text(s, l, top, width, H - top - Inches(0.55), paras, spacing=1.12, space_after=int(gap * 10))


def stat(s, l, t, w, big, label, big_size=54, label_size=13, big_color=BLACK):
    text(s, l, t, w, Inches(0.95), [[(big, big_size, True, big_color, LATIN)]], spacing=1.0)
    text(s, l, t + Inches(0.82), w, Inches(0.8), [[(label, label_size, False, INK, SANS)]], spacing=1.15)


def footer(s, txt, fill=BLACK, color=YELLOW, size=16, top=Inches(6.05)):
    rect(s, M, top, CW, Inches(0.8), fill=fill)
    text(s, M + Inches(0.24), top, CW - Inches(0.48), Inches(0.8),
         [[(txt, size, True, color, SANS)]], anchor=MSO_ANCHOR.MIDDLE)


def source(s, txt, top=Inches(6.62)):
    text(s, M, top, CW, Inches(0.4), [[(txt, 11, False, GRAY, SANS)]])


# ══════════════ 1 · 封面 ══════════════
s = slide()
rect(s, 0, 0, W, Inches(0.42), fill=BLACK)
text(s, M, Inches(0.02), CW, Inches(0.4), [[("每周五健康共修微课堂", 12, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, W - M - Inches(3.0), Inches(0.02), Inches(3.0), Inches(0.4),
     [[("26-22 期", 12, True, YELLOW, SANS)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

text(s, M, Inches(1.32), CW, Inches(0.5), [[("家庭健康管理系列 · 第一讲", 15, True, GRAY, SANS)]])
text(s, M, Inches(1.85), Inches(12.0), Inches(2.1),
     [[("家庭健康管理员", 66, True, BLACK, SERIF)], [("的 价 值", 52, True, BLACK, SERIF)]], spacing=1.08)
rect(s, M, Inches(4.32), Inches(2.6), Pt(7), fill=BLACK)
text(s, M, Inches(4.66), Inches(10.8), Inches(0.8),
     [[("一人懂健康，全家少生病", 38, True, BLACK, SERIF)]])
text(s, M, Inches(5.55), Inches(10.8), Inches(0.5),
     [[("管的是餐桌，防的是十年后的那张病床", 18, False, INK, SANS)]])
rect(s, M, Inches(6.18), Inches(4.6), Inches(0.62), fill=BLACK)
text(s, M + Inches(0.22), Inches(6.18), Inches(4.4), Inches(0.62),
     [[("主讲 · 本群主理人 张医生", 16, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, M + Inches(4.95), Inches(6.18), Inches(4.0), Inches(0.62),
     [[("今晚 19:30 · 社群开讲", 13, False, GRAY, SANS)]], anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 2 · 目录 ══════════════
s = slide()
eyebrow(s, "目 录", "02")
title(s, "今天讲五件事")
items = [("01", "慢病的现状：它离我们有多近"),
         ("02", "慢病的原因：60% 在生活方式"),
         ("03", "到底管什么：餐桌 + 慢病五项技术"),
         ("04", "为什么非得是家里的一个人"),
         ("05", "怎么学：观念 · 知识 · 方案")]
y = Inches(2.72)
for num, txt in items:
    rect(s, M, y, Inches(0.62), Inches(0.62), fill=BLACK)
    text(s, M, y, Inches(0.62), Inches(0.62), [[(num, 20, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(0.95), y, Inches(10.4), Inches(0.62), [[(txt, 23, True, INK, SERIF)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.78)

# ══════════════ 3 · 88.5% ══════════════
s = slide()
eyebrow(s, "第一部分 · 现状", "03")
title(s, "中国人走的时候，近九成是因为它", size=34)
text(s, M, Inches(2.55), Inches(6.0), Inches(1.6), [[("88.5", 128, True, BLACK, LATIN)]], spacing=0.95)
text(s, M + Inches(4.05), Inches(2.95), Inches(1.0), Inches(1.0), [[("%", 54, True, BLACK, LATIN)]])
rect(s, M + Inches(5.5), Inches(2.72), Pt(4), Inches(1.5), fill=BLACK)
text(s, M + Inches(5.95), Inches(2.78), Inches(5.5), Inches(1.5),
     [[("中国居民死亡原因里，", 20, False, INK, SANS)],
      [("慢性病占 88.5%", 26, True, BLACK, SANS)],
      [("十个走，将近九个是它带走的", 16, False, GRAY, SANS)]], spacing=1.3)
footer(s, "心脑血管 · 肿瘤 · 糖尿病 · 慢阻肺——不是意外，是慢慢磨出来的。", size=16, top=Inches(5.2))
source(s, "数据来源：《中国居民营养与慢性病状况报告（2020年）》")

# ══════════════ 4 · 数字墙 ══════════════
s = slide()
eyebrow(s, "第一部分 · 现状", "04")
title(s, "这些病，就在我们家里", size=36)
rows = [("27.5%", "高血压", "2.45 亿人 · 每 4 个成年人就有 1 个"),
        ("11.9%", "糖尿病", "1 亿多，还有大批人不知道自己的血糖已经不对"),
        ("40.4%", "血脂异常", "十个人里四个"),
        ("50.7%", "超重 + 肥胖", "成年人合计——两个人里就有一个"),
        ("1.8 亿", "高尿酸血症", "很多是二三十岁的年轻人")]
y = Inches(2.42)
for num, name, sub in rows:
    text(s, M, y, Inches(2.4), Inches(0.55), [[(num, 30, True, BLACK, LATIN)]], spacing=1.0)
    text(s, M + Inches(2.55), y - Inches(0.02), Inches(2.5), Inches(0.6), [[(name, 19, True, INK, SERIF)]])
    text(s, M + Inches(5.05), y + Inches(0.04), Inches(6.6), Inches(0.6), [[(sub, 15, False, GRAY, SANS)]])
    rect(s, M, y + Inches(0.62), CW, Pt(1.2), fill=BLACK)
    y += Inches(0.78)
source(s, "数据来源：《中国居民营养与慢性病状况报告（2020年）》· 中国慢性病与营养监测", top=Inches(6.85))

# ══════════════ 5 · 年轻化 ══════════════
s = slide()
eyebrow(s, "第一部分 · 现状", "05")
title(s, "而且它在往下压年龄", size=38)
bullets(s, [
    ("过去叫「老年病」  ", "——现在三十几岁心梗、二十几岁脂肪肝，门诊里不稀奇"),
    ("最年轻的脸  ", "——十几岁的孩子，血脂异常、体重超标"),
    ("为什么  ", "——高油高盐高糖 + 久坐 + 熬夜 + 压力，四件事一起上"),
    ("结果  ", "——病不再等老了才来，它在提前排队"),
], top=Inches(2.75), size=19, gap=0.72)
footer(s, "慢病不是运气不好，是生活方式在收账。", size=18, top=Inches(6.15))

# ══════════════ 6 · 四大因素 ══════════════
s = slide()
eyebrow(s, "第二部分 · 原因", "06")
title(s, "健康的账，60% 在自己手里", size=36)

rect(s, M, Inches(2.5), Inches(2.9), Inches(2.75), fill=BLACK)
text(s, M + Inches(0.2), Inches(2.68), Inches(2.5), Inches(1.0), [[("60%", 52, True, YELLOW, LATIN)]], spacing=0.95)
text(s, M + Inches(0.2), Inches(3.72), Inches(2.5), Inches(1.3),
     [[("生活方式与行为", 17, True, YELLOW, SANS)],
      [("吃 · 动 · 睡 · 烟酒 · 情绪", 12, False, YELLOW, SANS)]], spacing=1.3)

cols = [("17%", "环境因素", "社会环境 · 空气 · 水"),
        ("15%", "遗传", "父母给的底子"),
        ("8%",  "医疗卫生服务", "医院 · 药 · 手术")]
x = M + Inches(3.18)
for num, name, sub in cols:
    text(s, x, Inches(2.62), Inches(2.7), Inches(0.9), [[(num, 42, True, BLACK, LATIN)]], spacing=0.95)
    text(s, x, Inches(3.58), Inches(2.7), Inches(0.45), [[(name, 16, True, INK, SANS)]])
    text(s, x, Inches(4.05), Inches(2.7), Inches(1.0), [[(sub, 12, False, GRAY, SANS)]], spacing=1.3)
    x += Inches(2.85)

footer(s, "医疗只占 8%——它能救火，救不了天天点火的人。", size=17, top=Inches(5.72))
source(s, "归因框架：世界卫生组织 · 影响健康的主要因素", top=Inches(6.72))

# ══════════════ 7 · 观念转折 ══════════════
s = slide()
eyebrow(s, "第二部分 · 观念转折", "07")
title(s, "药管的是结果，生活方式管的是源头", size=32)

rect(s, M, Inches(2.55), Inches(5.6), Inches(2.55), fill=None, line=BLACK, lw=2.5)
text(s, M + Inches(0.28), Inches(2.72), Inches(5.0), Inches(0.5), [[("医 院 / 药", 20, True, BLACK, SANS)]])
text(s, M + Inches(0.28), Inches(3.25), Inches(5.0), Inches(1.7),
     [[("管结果：血压高了压下去，", 15, False, INK, SANS)],
      [("血糖高了降下来，血脂高了拦一拦。", 15, False, INK, SANS)],
      [("指标动了，人还在原地。", 15, True, RED, SANS)]], spacing=1.45)

rect(s, M + Inches(5.95), Inches(2.55), Inches(5.68), Inches(2.55), fill=BLACK)
text(s, M + Inches(6.23), Inches(2.72), Inches(5.0), Inches(0.5), [[("生 活 方 式", 20, True, YELLOW, SANS)]])
text(s, M + Inches(6.23), Inches(3.25), Inches(5.0), Inches(1.7),
     [[("管源头：今天放几勺盐，", 15, False, WHITE, SANS)],
      [("几点睡，动不动，吃多少。", 15, False, WHITE, SANS)],
      [("源头不动，账就一直在记。", 15, True, YELLOW, SANS)]], spacing=1.45)

footer(s, "慢病的主力战场，不在医院，在自己家的餐桌。", size=18, top=Inches(5.45))

# ══════════════ 8 · 1 : 8.5 : 100 ══════════════
s = slide()
eyebrow(s, "第二部分 · 一笔账", "08")
title(s, "预防这 1 块钱，值多少钱", size=36)
xs = [M, M + Inches(4.0), M + Inches(8.0)]
vals = [("1", "元", "花在预防上", "学知识 · 改餐桌 · 定期监测"),
        ("8.5", "元", "省下的治疗费", "少一次住院，少一次长期用药"),
        ("100", "元", "省下的抢救费", "ICU 一天 · 一次支架 · 一次透析")]
for (x, (num, unit, label, sub)) in zip(xs, vals):
    text(s, x, Inches(2.5), Inches(3.6), Inches(1.0), [[(num, 82, True, BLACK, LATIN),
                                                       (" " + unit, 24, True, GRAY, SANS)]], spacing=0.95)
    text(s, x, Inches(3.62), Inches(3.6), Inches(0.45), [[(label, 18, True, INK, SANS)]])
    text(s, x, Inches(4.08), Inches(3.5), Inches(0.9), [[(sub, 13, False, GRAY, SANS)]], spacing=1.3)
footer(s, "平时舍不得那 1 块，最后都花在那 100 块上。", size=18, top=Inches(5.35))
source(s, "健康管理经济学经典测算：预防投入 : 治疗费用 : 抢救费用 ≈ 1 : 8.5 : 100", top=Inches(6.38))

# ══════════════ 9 · 两块战场 ══════════════
s = slide()
eyebrow(s, "第三部分 · 管什么", "09")
title(s, "要管的是两块战场", size=38)
blocks = [("01", "还没病 —— 防", "一家人的餐桌：膳食指南 · 膳食宝塔 · 三个动作"),
          ("02", "已经病了 —— 管", "慢病管理五项技术：体重 · 血糖 · 血脂 · 血压 · 尿酸")]
y = Inches(2.62)
for num, head, sub in blocks:
    rect(s, M, y, CW, Inches(1.75), fill=None, line=BLACK, lw=2.5)
    rect(s, M, y, Inches(1.35), Inches(1.75), fill=BLACK)
    text(s, M, y, Inches(1.35), Inches(1.75), [[(num, 32, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(1.62), y + Inches(0.3), CW - Inches(1.9), Inches(0.6),
         [[(head, 27, True, INK, SERIF)]])
    text(s, M + Inches(1.62), y + Inches(1.04), CW - Inches(1.9), Inches(0.5),
         [[(sub, 15, False, GRAY, SANS)]])
    y += Inches(1.98)

# ══════════════ 10 · 膳食指南八条 ══════════════
s = slide()
eyebrow(s, "第三部分 · 防", "10")
title(s, "国家早就把答案写好了", size=36)
text(s, M, Inches(2.20), CW, Inches(0.4), [[("《中国居民膳食指南（2022）》· 八条准则", 15, True, GRAY, SANS)]])
rules = ["食物多样，合理搭配", "吃动平衡，健康体重", "多吃蔬果、奶类、全谷、大豆", "适量吃鱼、禽、蛋、瘦肉",
         "少盐少油，控糖限酒", "规律进餐，足量饮水", "会烹会选，会看标签", "公筷分餐，杜绝浪费"]
for i, r in enumerate(rules):
    col = i // 4
    row = i % 4
    x = M + Inches(6.0) * col
    y = Inches(2.72) + Inches(0.86) * row
    text(s, x, y, Inches(0.6), Inches(0.5), [[("0%d" % (i + 1), 14, True, GRAY, LATIN)]])
    text(s, x + Inches(0.55), y - Inches(0.02), Inches(5.2), Inches(0.6), [[(r, 18, True, INK, SERIF)]])
rect(s, M, Inches(6.25), CW, Pt(2), fill=BLACK)
text(s, M, Inches(6.42), CW, Inches(0.4), [[("标准答案给了，缺的是——家里有一个人真的照着做。", 15, True, GRAY, SANS)]])

# ══════════════ 11 · 膳食宝塔 ══════════════
s = slide()
eyebrow(s, "第三部分 · 防", "11")
title(s, "一天到底吃多少", size=38)
text(s, M, Inches(2.20), CW, Inches(0.4), [[("平衡膳食宝塔 · 成年人 1600–2400 千卡", 15, True, GRAY, SANS)]])

rect(s, M, Inches(2.62), Inches(6.0), Inches(3.4), fill=None, line=BLACK, lw=2.5)
text(s, M + Inches(0.25), Inches(2.74), Inches(5.5), Inches(0.4), [[("要吃够", 15, True, BLACK, SANS)]])
left = [("谷类 200–300g", "全谷杂豆 50–150g"),
        ("蔬菜 300–500g", "水果 200–350g"),
        ("奶及奶制品 300–500g", ""),
        ("大豆坚果 25–35g", ""),
        ("鱼 40–75g · 肉 40–75g · 蛋 40–50g", "")]
y = Inches(3.14)
for a, b in left:
    text(s, M + Inches(0.25), y, Inches(5.6), Inches(0.58),
         [[(a, 15, True, INK, SANS)] + ([("　" + b, 12, False, GRAY, SANS)] if b else [])])
    y += Inches(0.55)

rect(s, M + Inches(6.35), Inches(2.62), Inches(5.28), Inches(3.4), fill=BLACK)
text(s, M + Inches(6.6), Inches(2.74), Inches(4.8), Inches(0.4), [[("要管住", 15, True, YELLOW, SANS)]])
right = [("盐 < 5g", "中国人平均近 10g"),
         ("油 25–30g", ""),
         ("水 1500–1700ml", ""),
         ("添加糖 < 25g", "最好 0")]
y = Inches(3.14)
for a, b in right:
    text(s, M + Inches(6.6), y, Inches(4.8), Inches(0.58),
         [[(a, 15, True, WHITE, SANS)] + ([("　" + b, 12, False, YELLOW, SANS)] if b else [])])
    y += Inches(0.55)

source(s, "数据来源：《中国居民膳食指南（2022）》", top=Inches(6.35))

# ══════════════ 12 · 三件事 ══════════════
s = slide()
eyebrow(s, "第三部分 · 今晚就能开始", "12")
title(s, "先改这三件，见效最快", size=36)
cards = [("01", "盐减到 5 克", "一个 2 克限盐勺，一天两勺半封顶"),
         ("02", "每天 300 毫升奶", "钙和优质蛋白，一家老小都缺"),
         ("03", "主食掺全谷杂豆", "白米里加一把糙米、燕麦、红豆")]
y = Inches(2.7)
for num, head, sub in cards:
    rect(s, M, y, CW, Inches(1.24), fill=None, line=BLACK, lw=2.5)
    rect(s, M, y, Inches(1.1), Inches(1.24), fill=BLACK)
    text(s, M, y, Inches(1.1), Inches(1.24), [[(num, 28, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(1.35), y + Inches(0.18), CW - Inches(1.6), Inches(0.5),
         [[(head, 23, True, INK, SERIF)]])
    text(s, M + Inches(1.35), y + Inches(0.68), CW - Inches(1.6), Inches(0.5),
         [[(sub, 15, False, GRAY, SANS)]])
    y += Inches(1.34)
text(s, M, Inches(6.72), CW, Inches(0.4),
     [[("不花钱、不额外花时间——只要家里有一个人盯着。", 15, True, GRAY, SANS)]])

# ══════════════ 13 · 五项技术 ══════════════
s = slide()
eyebrow(s, "第三部分 · 管", "13")
title(s, "已经病了，这五项技术得会", size=34)
rows = [("01", "体重与腰围", "BMI 18.5–23.9 ｜ 男 <90cm · 女 <85cm"),
        ("02", "血糖", "控总量 · 低升糖 · 先菜后肉再主食"),
        ("03", "血脂", "少反式脂肪 · 加膳食纤维 · 控精制糖"),
        ("04", "血压", "减盐 · 控体重 · 补钾 · 规律运动 · 睡够"),
        ("05", "尿酸", "限嘌呤 · 戒酒 · 控果糖 · 水 2000ml 以上")]
y = Inches(2.5)
for num, head, sub in rows:
    rect(s, M, y, Inches(0.55), Inches(0.55), fill=BLACK)
    text(s, M, y, Inches(0.55), Inches(0.55), [[(num, 13, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(0.75), y - Inches(0.03), Inches(2.5), Inches(0.6),
         [[(head, 19, True, INK, SERIF)]])
    text(s, M + Inches(3.25), y, Inches(8.3), Inches(0.6), [[(sub, 15, False, GRAY, SANS)]])
    rect(s, M, y + Inches(0.66), CW, Pt(1), fill=BLACK)
    y += Inches(0.78)
text(s, M, Inches(6.52), CW, Inches(0.5),
     [[("这些不是天生的，是学来的——学一次，能管一家人几十年。", 15, True, GRAY, SANS)]])

# ══════════════ 14 · 营养素 ══════════════
s = slide()
eyebrow(s, "第三部分 · 管", "14")
title(s, "再加一件：把缺口补上", size=38)
text(s, M, Inches(2.5), CW, Inches(0.8),
     [[("长期吃不到标准，缺口是真实存在的。", 26, True, BLACK, SANS)]], spacing=1.0)
bullets(s, [
    ("缺口在哪  ", "——蛋白质、膳食纤维、维生素、矿物质，一样样都对不上"),
    ("营养素是什么  ", "——不是替代一顿饭，是补结构、补材料"),
    ("为什么有用  ", "——身体要修复，得有材料；没材料，它只能硬撑"),
    ("怎么配  ", "——按人的情况配，不按广告配"),
], top=Inches(3.42), size=19, gap=0.72)
footer(s, "饭是地基，营养素是补缝——两个都到位，才叫全营养。", size=17, top=Inches(6.15))

# ══════════════ 15 · 凭什么是一个人 ══════════════
s = slide()
eyebrow(s, "第四部分 · 为什么是家里那一个", "15")
text(s, M, Inches(1.45), CW, Inches(1.0), [[("这件事，外包不出去。", 52, True, BLACK, SERIF)]], spacing=1.0)
rect(s, M, Inches(2.72), Inches(2.4), Pt(6), fill=BLACK)
bullets(s, [
    ("医院  ", "——管不了你家今晚放几勺盐"),
    ("外卖  ", "——不会替你算这一顿蛋白质够不够"),
    ("体检报告  ", "——只告诉你结果，它不跟你回家"),
], top=Inches(3.25), size=20, gap=0.78)
footer(s, "一个家，只要有一个人真懂了，健康曲线就和隔壁不一样。", size=17, top=Inches(5.95))

# ══════════════ 16 · 怎么学 ══════════════
s = slide()
eyebrow(s, "第五部分 · 怎么学", "16")
title(s, "零散知识让人焦虑，体系才能变能力", size=30)
steps = ["建观念", "补知识", "练技术", "家人用", "调反馈"]
x = M
for i, st in enumerate(steps):
    rect(s, x, Inches(2.85), Inches(2.15), Inches(1.55), fill=None, line=BLACK, lw=2.5)
    text(s, x, Inches(3.0), Inches(2.15), Inches(0.4), [[("0%d" % (i + 1), 13, True, GRAY, LATIN)]], align=PP_ALIGN.CENTER)
    text(s, x, Inches(3.45), Inches(2.15), Inches(0.6), [[(st, 24, True, INK, SERIF)]], align=PP_ALIGN.CENTER)
    if i < 4:
        text(s, x + Inches(2.15), Inches(3.3), Inches(0.2), Inches(0.5), [[("→", 20, True, BLACK, SANS)]],
             align=PP_ALIGN.CENTER)
    x += Inches(2.35)
bullets(s, [
    ("跟着体系走  ", "——医生 + 营养师 + 社群 + 持续更新的课程与案例"),
    ("不用从零摸索  ", "——你只需要跟着走，然后在自家人身上用"),
], top=Inches(4.85), size=19, gap=0.72)
text(s, M, Inches(6.35), CW, Inches(0.4), [[("一个人做不大，一群人才能走远。", 16, True, GRAY, SANS)]])

# ══════════════ 17 · 总结三件事 ══════════════
s = slide()
eyebrow(s, "总 结", "17")
title(s, "合格的家庭健康管理员，就三件事", size=32)
cards = [("01", "观念", "慢病的主战场在家里，不在医院；预防那 1 块，值后面 100 块"),
         ("02", "知识", "膳食指南 + 膳食宝塔 + 慢病五项技术——国家给的标准答案，认真学"),
         ("03", "方案", "落到一周的菜单、一把盐勺、一台体重秤上，才叫管理")]
y = Inches(2.65)
for num, head, sub in cards:
    rect(s, M, y, CW, Inches(1.3), fill=None, line=BLACK, lw=2.5)
    rect(s, M, y, Inches(1.85), Inches(1.3), fill=BLACK)
    text(s, M, y, Inches(0.9), Inches(1.3), [[(num, 24, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(0.9), y, Inches(0.95), Inches(1.3), [[(head, 21, True, YELLOW, SERIF)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(2.1), y + Inches(0.22), CW - Inches(2.4), Inches(0.95),
         [[(sub, 15, False, INK, SANS)]], spacing=1.35)
    y += Inches(1.42)

# ══════════════ 18 · 号召 ══════════════
s = slide()
rect(s, 0, 0, W, H, fill=BLACK)
rect(s, 0, Inches(2.3), W, Inches(0.09), fill=YELLOW)
text(s, M, Inches(0.9), CW, Inches(0.5), [[("行动号召", 14, True, YELLOW, SANS)]])
text(s, M, Inches(1.15), Inches(11.6), Inches(1.0),
     [[("一人懂健康，全家少生病", 38, True, YELLOW, SERIF)]], spacing=1.0)
text(s, M, Inches(2.72), Inches(11.8), Inches(1.7),
     [[("往小里说，你护住了父母、爱人、孩子；", 21, False, WHITE, SANS)],
      [("往大里说，你把这件事做透了，身边一定有人需要你。", 21, False, WHITE, SANS)]], spacing=1.4)
rect(s, M, Inches(4.62), Inches(9.2), Inches(0.68), fill=YELLOW)
text(s, M + Inches(0.22), Inches(4.62), Inches(8.9), Inches(0.68),
     [[("想要一份「家庭健康管理清单」→ 课后私信张医生", 15, True, BLACK, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(5.7), CW, Inches(0.5),
     [[("观念 · 知识 · 方案　|　下周五，健康微课堂，不见不散！", 15, False, YELLOW, SANS)]])
text(s, M, Inches(6.6), CW, Inches(0.4),
     [[("以上为健康科普分享，不构成诊疗建议，个体情况请咨询专业医师。", 11, False, GRAY, SANS)]])

# ───────────── Save ─────────────
out = "/Users/mac/Documents/zfc最强大脑/C社群工作台/社群微课工作流/家庭健康管理员的价值-2026-10-30-26-22期.pptx"
prs.save(out)
print("Saved:", out, "| slides:", len(prs.slides._sldIdLst))
