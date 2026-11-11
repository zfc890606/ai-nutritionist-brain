#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周五微课堂 26-22期《家庭健康管理员的价值》— 万病寻源样板风
米色底 / 白卡片 + 彩色错位阴影 / 黑表头 / 洋红·明黄·青 点缀 / 微软雅黑
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

BG     = RGBColor(0xF5, 0xF0, 0xE8)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
INK    = RGBColor(0x1A, 0x1A, 0x1A)
BLACK  = RGBColor(0x00, 0x00, 0x00)
PINK   = RGBColor(0xFF, 0x3A, 0x8D)
YELLOW = RGBColor(0xFF, 0xD4, 0x00)
CYAN   = RGBColor(0x00, 0xD4, 0xE6)
GREEN  = RGBColor(0x16, 0xA3, 0x4A)
RED    = RGBColor(0xDC, 0x26, 0x26)
CREAM  = RGBColor(0xFA, 0xF6, 0xEF)
CREAM2 = RGBColor(0xFF, 0xFB, 0xE6)
GRAY   = RGBColor(0x66, 0x66, 0x66)

FONT = "微软雅黑"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]
L = Inches(0.5)
CW = Inches(12.3)


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
    f = s.background.fill
    f.solid()
    f.fore_color.rgb = BG
    return s


def rect(s, l, t, w, h, fill=None, line=None, lw=1.0):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
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
         spacing=1.15, space_after=4):
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
            txt, size = r[0], r[1]
            bold = r[2] if len(r) > 2 else False
            color = r[3] if len(r) > 3 else INK
            fname = r[4] if len(r) > 4 else FONT
            run = p.add_run()
            run.text = txt
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color
            run.font.name = fname
            _set_ea(run, fname)
    return tb


def card(s, l, t, w, h, fill=WHITE, shadow=PINK, off=0.09):
    if shadow is not None:
        rect(s, l + Inches(off), t + Inches(off), w, h, fill=shadow)
    rect(s, l, t, w, h, fill=fill)


def eyebrow(s, label, color=PINK):
    rect(s, L, Inches(0.33), Inches(0.12), Inches(0.22), fill=color)
    text(s, L + Inches(0.22), Inches(0.27), Inches(8.0), Inches(0.34),
         [[(label, 14, True, BLACK)]], anchor=MSO_ANCHOR.MIDDLE)


def h1(s, txt, size=40, t=Inches(0.8), w=None):
    text(s, L, t, w or CW, Inches(1.05), [[(txt, size, True, BLACK)]], spacing=1.0)


def pagenum(s, n, total=18):
    text(s, Inches(11.9), Inches(7.02), Inches(1.0), Inches(0.3),
         [[("%d / %d" % (n, total), 11, False, GRAY)]], align=PP_ALIGN.RIGHT)


def src(s, txt, t=Inches(6.86)):
    text(s, L, t, Inches(10.6), Inches(0.3), [[("📖 " + txt, 11, False, GRAY)]])


def bar(s, txt, t, h=Inches(0.62), fill=BLACK, color=WHITE, size=17, x=None, w=None):
    x = x or L
    w = w or CW
    rect(s, x, t, w, h, fill=fill)
    text(s, x + Inches(0.28), t, w - Inches(0.56), h, [[(txt, size, True, color)]],
         anchor=MSO_ANCHOR.MIDDLE)


def table(s, top, headers, rows, widths, head_h=0.48, row_h=0.6,
          size=14, head_size=13, hi=None, x=None):
    x = x or L
    y = top
    cx = x
    rect(s, cx, y, sum(widths, start=Inches(0)), head_h, fill=BLACK)
    for hd, wd in zip(headers, widths):
        text(s, cx + Inches(0.2), y, wd - Inches(0.3), head_h,
             [[(hd, head_size, True, WHITE)]], anchor=MSO_ANCHOR.MIDDLE)
        cx += wd
    y += head_h
    for i, row in enumerate(rows):
        fill = CREAM if i % 2 == 0 else WHITE
        rect(s, x, y, sum(widths, start=Inches(0)), row_h, fill=fill)
        cx = x
        for j, (cell, wd) in enumerate(zip(row, widths)):
            color = BLACK
            bold = (j == 0)
            if hi and (i, j) in hi:
                color, bold = PINK, True
            text(s, cx + Inches(0.2), y, wd - Inches(0.3), row_h,
                 [[(cell, size, bold, color)]], anchor=MSO_ANCHOR.MIDDLE)
            cx += wd
        y += row_h
    return y


# ══════════════ 1 · 封面 ══════════════
s = slide()
text(s, Inches(0.8), Inches(0.62), Inches(9.0), Inches(0.36),
     [[("家庭健康管理系列 · 第一讲", 14, True, PINK)]])
for i, c in enumerate((PINK, YELLOW, CYAN)):
    rect(s, Inches(0.8) + Inches(1.0) * i, Inches(1.02), Inches(0.9), Inches(0.08), fill=c)
text(s, Inches(0.8), Inches(1.55), Inches(11.5), Inches(1.2),
     [[("家庭健康管理员", 68, True, BLACK)]], spacing=1.0)
text(s, Inches(0.8), Inches(2.72), Inches(11.5), Inches(1.0),
     [[("的 价 值", 54, True, BLACK)]], spacing=1.0)
rect(s, Inches(0.8), Inches(4.32), Inches(2.2), Inches(0.07), fill=BLACK)
text(s, Inches(0.8), Inches(4.62), Inches(11.0), Inches(0.7),
     [[("一人懂健康，全家少生病", 36, True, BLACK)]])
text(s, Inches(0.8), Inches(5.36), Inches(11.0), Inches(0.45),
     [[("管的是餐桌，防的是十年后的那张病床", 17, False, GRAY)]])
rect(s, Inches(0.8), Inches(6.1), Inches(4.5), Inches(0.6), fill=BLACK)
text(s, Inches(1.04), Inches(6.1), Inches(4.2), Inches(0.6),
     [[("主讲 · 本群主理人 张医生", 16, True, YELLOW)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, Inches(5.5), Inches(6.1), Inches(4.0), Inches(0.6),
     [[("今晚 19:30 · 社群开讲", 14, False, GRAY)]], anchor=MSO_ANCHOR.MIDDLE)
pagenum(s, 1)

# ══════════════ 2 · 目录 ══════════════
s = slide()
eyebrow(s, "目 录")
h1(s, "今天讲五件事")
card(s, L, Inches(2.0), CW, Inches(4.28), fill=WHITE, shadow=CYAN)
items = [("01", "慢病的现状：它离我们有多近"),
         ("02", "慢病的原因：60% 在生活方式"),
         ("03", "到底管什么：餐桌 + 慢病五项技术"),
         ("04", "为什么非得是家里的一个人"),
         ("05", "怎么学：观念 · 知识 · 方案")]
y = Inches(2.22)
for num, txt in items:
    text(s, L + Inches(0.35), y, Inches(0.9), Inches(0.62), [[(num, 22, True, PINK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + Inches(1.35), y, Inches(9.8), Inches(0.62), [[(txt, 23, True, BLACK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.78)
    if num != "05":
        rect(s, L + Inches(0.35), y - Inches(0.08), CW - Inches(0.7), Pt(1), fill=RGBColor(0xDD, 0xD5, 0xC8))
pagenum(s, 2)

# ══════════════ 3 · 88.5% ══════════════
s = slide()
eyebrow(s, "第一部分 · 慢病的现状")
h1(s, "中国人走的时候，近九成是因为它", size=36)
text(s, L, Inches(2.15), Inches(6.2), Inches(2.0), [[("88.5", 130, True, BLACK)]], spacing=0.95)
text(s, Inches(4.55), Inches(2.6), Inches(1.0), Inches(1.0), [[("%", 56, True, BLACK)]])
card(s, Inches(5.65), Inches(2.15), Inches(7.15), Inches(2.0), fill=WHITE, shadow=PINK)
text(s, Inches(5.95), Inches(2.4), Inches(6.6), Inches(1.6),
     [[("慢性病死亡，占总死亡人数的", 18, False, INK)],
      [("88.5%", 30, True, PINK)],
      [("十个人走，将近九个是它带走的", 14, False, GRAY)]], spacing=1.35)
bar(s, "心脑血管 · 肿瘤 · 糖尿病 · 慢阻肺——不是意外，是慢慢磨出来的。", Inches(4.65), h=Inches(0.7), size=16)
text(s, L, Inches(5.75), CW, Inches(0.5),
     [[("它不突然。它是被一天一天的饭、一晚一晚的熬夜，养出来的。", 20, True, BLACK)]])
src(s, "《中国居民营养与慢性病状况报告（2020年）》")
pagenum(s, 3)

# ══════════════ 4 · 数字墙 ══════════════
s = slide()
eyebrow(s, "第一部分 · 慢病的现状")
h1(s, "这些病，就在我们家里", size=38)
table(s, Inches(1.95),
      ["疾病", "患病率", "规模 / 说明"],
      [["高血压", "27.5%", "约 2.45 亿 · 每 4 个成年人就有 1 个"],
       ["糖尿病", "11.9%", "1 亿多 · 还有大批人不知道自己血糖不对"],
       ["血脂异常", "40.4%", "十个人里四个"],
       ["超重 + 肥胖", "50.7%", "成年人合计 · 两个人里就有一个"],
       ["高尿酸血症", "13.3%", "约 1.8 亿 · 很多是二三十岁"]],
      [Inches(2.8), Inches(2.4), Inches(7.1)],
      row_h=0.62, hi={(0, 1), (4, 1)})
src(s, "《中国居民营养与慢性病状况报告（2020年）》· 中国慢性病与营养监测")
pagenum(s, 4)

# ══════════════ 5 · 年轻化 ══════════════
s = slide()
eyebrow(s, "第一部分 · 慢病的现状")
h1(s, "而且它在往下压年龄", size=38)
rows = [("过去叫「老年病」", "现在三十几岁心梗、二十几岁脂肪肝，门诊里不稀奇"),
        ("最年轻的脸", "十几岁的孩子，血脂异常、体重超标"),
        ("为什么", "高油高盐高糖 + 久坐 + 熬夜 + 压力，四件事一起上"),
        ("结果", "病不再等老了才来，它在提前排队")]
y = Inches(2.0)
for i, (k, v) in enumerate(rows):
    fill = CREAM if i % 2 == 0 else WHITE
    rect(s, L, y, CW, Inches(0.78), fill=fill)
    text(s, L + Inches(0.25), y, Inches(2.9), Inches(0.78), [[(k, 16, True, PINK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + Inches(3.2), y, Inches(8.9), Inches(0.78), [[(v, 15, False, INK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.86)
bar(s, "慢病不是运气不好，是生活方式在收账。", Inches(5.62), size=18)
pagenum(s, 5)

# ══════════════ 6 · 四大因素 ══════════════
s = slide()
eyebrow(s, "第二部分 · 慢病的原因")
h1(s, "健康的账，60% 在自己手里", size=38)
cards = [("60%", "生活方式与行为", "吃 · 动 · 睡 · 烟酒 · 情绪", PINK, WHITE),
         ("17%", "环境因素", "社会 · 空气 · 水", CYAN, BLACK),
         ("15%", "遗传", "父母给的底子", YELLOW, BLACK),
         ("8%", "医疗卫生服务", "医院 · 药 · 手术", BLACK, WHITE)]
x = Inches(0.55)
for pct, name, sub, fill, tc in cards:
    rect(s, x, Inches(1.95), Inches(2.88), Inches(2.55), fill=fill)
    text(s, x + Inches(0.22), Inches(2.12), Inches(2.5), Inches(0.85), [[(pct, 44, True, tc)]], spacing=0.95)
    text(s, x + Inches(0.22), Inches(3.02), Inches(2.5), Inches(0.4), [[(name, 15, True, tc)]])
    text(s, x + Inches(0.22), Inches(3.45), Inches(2.5), Inches(0.8), [[(sub, 12, False, tc)]], spacing=1.3)
    x += Inches(3.07)
bar(s, "医疗只占 8%——它能救火，救不了天天点火的人。", Inches(4.78), size=17)
text(s, L, Inches(5.65), CW, Inches(0.9),
     [[("所以慢病的源头，不在诊室，在厨房、在卧室、在每天走不走那几步路。", 19, True, BLACK)]])
src(s, "归因框架：世界卫生组织 · 影响健康的主要因素")
pagenum(s, 6)

# ══════════════ 7 · 观念转折 ══════════════
s = slide()
eyebrow(s, "第二部分 · 观念转折")
h1(s, "药管的是结果，生活方式管的是源头", size=32)
card(s, L, Inches(2.0), Inches(5.9), Inches(3.05), fill=WHITE, shadow=BLACK)
text(s, Inches(0.75), Inches(2.2), Inches(5.4), Inches(0.45), [[("🏥 医院 / 药", 20, True, BLACK)]])
text(s, Inches(0.75), Inches(2.78), Inches(5.4), Inches(2.0),
     [[("管结果：血压高了压下去，", 15, False, INK)],
      [("血糖高了降下来，血脂高了拦一拦。", 15, False, INK)],
      [("", 8)],
      [("指标动了，人还在原地。", 16, True, RED)]], spacing=1.4)

card(s, Inches(6.88), Inches(2.0), Inches(5.9), Inches(3.05), fill=WHITE, shadow=PINK)
text(s, Inches(7.13), Inches(2.2), Inches(5.4), Inches(0.45), [[("🏠 生活方式 · 你的家", 20, True, BLACK)]])
text(s, Inches(7.13), Inches(2.78), Inches(5.4), Inches(2.0),
     [[("管源头：今天放几勺盐，", 15, False, INK)],
      [("几点睡，动不动，吃多少。", 15, False, INK)],
      [("", 8)],
      [("源头不动，账就一直在记。", 16, True, PINK)]], spacing=1.4)

bar(s, "慢病的主力战场，不在医院，在自己家的餐桌。", Inches(5.45), size=18)
pagenum(s, 7)

# ══════════════ 8 · 1 : 8.5 : 100 ══════════════
s = slide()
eyebrow(s, "第二部分 · 算一笔账")
h1(s, "预防这 1 块钱，值多少钱", size=38)
cols = [("1", "元", "花在预防上", "学知识 · 改餐桌 · 定期监测", CYAN),
        ("8.5", "元", "省下的治疗费", "少一次住院，少一段长期用药", YELLOW),
        ("100", "元", "省下的抢救费", "ICU 一天 · 一次支架 · 一次透析", PINK)]
x = Inches(0.55)
for num, unit, label, sub, c in cols:
    rect(s, x, Inches(2.05), Inches(3.9), Inches(0.1), fill=c)
    text(s, x, Inches(2.3), Inches(3.8), Inches(1.1), [[(num, 74, True, BLACK), (" " + unit, 22, True, GRAY)]], spacing=0.95)
    text(s, x, Inches(3.5), Inches(3.8), Inches(0.42), [[(label, 18, True, BLACK)]])
    text(s, x, Inches(3.98), Inches(3.6), Inches(0.9), [[(sub, 13, False, GRAY)]], spacing=1.3)
    x += Inches(4.15)
bar(s, "平时舍不得那 1 块，最后都花在那 100 块上。", Inches(5.15), size=18)
src(s, "健康管理经济学经典测算：预防投入 : 治疗费用 : 抢救费用 ≈ 1 : 8.5 : 100")
pagenum(s, 8)

# ══════════════ 9 · 两块战场 ══════════════
s = slide()
eyebrow(s, "第三部分 · 到底管什么")
h1(s, "要管的是两块战场", size=40)
blocks = [("01", "还没病 —— 防", "一家人的餐桌：膳食指南 · 膳食宝塔 · 三个动作", CYAN, BLACK),
          ("02", "已经病了 —— 管", "慢病五项技术：体重 · 血糖 · 血脂 · 血压 · 尿酸", PINK, WHITE)]
y = Inches(2.0)
for num, head, sub, fill, tc in blocks:
    rect(s, L, y, CW, Inches(1.85), fill=fill)
    text(s, Inches(0.75), y + Inches(0.22), Inches(1.2), Inches(0.6), [[(num, 30, True, tc)]])
    text(s, Inches(0.75), y + Inches(0.85), Inches(11.5), Inches(0.6), [[(head, 28, True, tc)]])
    text(s, Inches(0.75), y + Inches(1.4), Inches(11.5), Inches(0.4), [[(sub, 15, False, tc)]])
    y += Inches(2.1)
pagenum(s, 9)

# ══════════════ 10 · 膳食指南八条 ══════════════
s = slide()
eyebrow(s, "第三部分 · 防")
h1(s, "国家早就把答案写好了", size=38)
text(s, L, Inches(1.72), CW, Inches(0.35), [[("《中国居民膳食指南（2022）》· 八条准则", 15, True, GRAY)]])
rules = ["食物多样，合理搭配", "吃动平衡，健康体重", "多吃蔬果、奶类、全谷、大豆", "适量吃鱼、禽、蛋、瘦肉",
         "少盐少油，控糖限酒", "规律进餐，足量饮水", "会烹会选，会看标签", "公筷分餐，杜绝浪费"]
for i, r in enumerate(rules):
    col, row = i // 4, i % 4
    x = L + Inches(6.3) * col
    y = Inches(2.2) + Inches(1.0) * row
    rect(s, x, y, Inches(6.0), Inches(0.85), fill=(CREAM if row % 2 == 0 else WHITE))
    text(s, x + Inches(0.22), y, Inches(0.55), Inches(0.85), [[("0%d" % (i + 1), 14, True, PINK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.8), y, Inches(5.0), Inches(0.85), [[(r, 17, True, BLACK)]],
         anchor=MSO_ANCHOR.MIDDLE)
src(s, "《中国居民膳食指南（2022）》· 标准给了，缺的是家里有一个人真的照着做")
pagenum(s, 10)

# ══════════════ 11 · 膳食宝塔 ══════════════
s = slide()
eyebrow(s, "第三部分 · 防")
h1(s, "一天到底吃多少", size=38)
table(s, Inches(1.9),
      ["类别", "一天的量", "关键提醒"],
      [["谷类", "200–300g", "全谷物和杂豆 50–150g"],
       ["蔬菜 / 水果", "蔬菜 300–500g · 水果 200–350g", "深色蔬菜要占一半"],
       ["奶及奶制品", "300–500g", "中国家庭普遍吃不够"],
       ["大豆 / 坚果", "25–35g", "一把豆、一小把坚果"],
       ["鱼 / 肉 / 蛋", "鱼 40–75g · 肉 40–75g · 蛋 40–50g", "优先鱼和禽"],
       ["油 / 盐", "油 25–30g · 盐 < 5g", "中国人平均吃盐接近 10g，翻倍超标"]],
      [Inches(2.7), Inches(5.1), Inches(4.5)],
      row_h=0.61, hi={(5, 1), (2, 2)})
src(s, "《中国居民膳食指南（2022）》· 平衡膳食宝塔（1600–2400 千卡）")
pagenum(s, 11)

# ══════════════ 12 · 三件事 ══════════════
s = slide()
eyebrow(s, "第三部分 · 今晚就能开始")
h1(s, "先改这三件，见效最快", size=38)
cards = [("🧂", "盐减到 5 克", "一个 2 克限盐勺，一天两勺半封顶", CYAN),
         ("🥛", "每天 300 毫升奶", "钙和优质蛋白，一家老小都缺", YELLOW),
         ("🌾", "主食掺全谷杂豆", "白米里加一把糙米、燕麦、红豆", PINK)]
x = Inches(0.55)
for emo, head, sub, fill in cards:
    rect(s, x, Inches(2.0), Inches(3.9), Inches(2.75), fill=fill)
    text(s, x + Inches(0.28), Inches(2.25), Inches(3.3), Inches(0.6), [[(emo, 30, False, BLACK)]])
    text(s, x + Inches(0.28), Inches(3.0), Inches(3.4), Inches(0.5), [[(head, 22, True, BLACK)]])
    text(s, x + Inches(0.28), Inches(3.55), Inches(3.3), Inches(0.9), [[(sub, 13, False, INK)]], spacing=1.35)
    x += Inches(4.15)
bar(s, "不花钱、不额外花时间——只要家里有一个人盯着。", Inches(5.15), size=17)
text(s, L, Inches(6.05), CW, Inches(0.5),
     [[("这三件事，就是我说的「把国家指南翻译成你家餐桌上的动作」。", 16, False, GRAY)]])
pagenum(s, 12)

# ══════════════ 13 · 五项技术 ══════════════
s = slide()
eyebrow(s, "第三部分 · 管")
h1(s, "已经病了，这五项技术得会", size=36)
rows = [("体重与腰围", "BMI 18.5–23.9 ｜ 男 <90cm · 女 <85cm"),
        ("血糖", "控总量 · 低升糖 · 先菜后肉再主食"),
        ("血脂", "少反式脂肪 · 加膳食纤维 · 控精制糖"),
        ("血压", "减盐 · 控体重 · 补钾 · 规律运动 · 睡够"),
        ("尿酸", "限嘌呤 · 戒酒 · 控果糖 · 水 2000ml 以上")]
y = Inches(1.95)
for i, (k, v) in enumerate(rows):
    rect(s, L, y, CW, Inches(0.72), fill=(CREAM if i % 2 == 0 else WHITE))
    text(s, L + Inches(0.25), y, Inches(0.55), Inches(0.72), [[("0%d" % (i + 1), 13, True, PINK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + Inches(0.95), y, Inches(2.6), Inches(0.72), [[(k, 17, True, BLACK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + Inches(3.7), y, Inches(8.4), Inches(0.72), [[(v, 14, False, INK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.8)
bar(s, "这些不是天生的，是学来的——学一次，能管一家人几十年。", Inches(6.0), size=16)
pagenum(s, 13)

# ══════════════ 14 · 营养素 ══════════════
s = slide()
eyebrow(s, "第三部分 · 管")
h1(s, "再加一件：把缺口补上", size=38)
text(s, L, Inches(1.95), CW, Inches(0.7),
     [[("长期吃不到标准，缺口是真实存在的。", 30, True, BLACK)]])
rows = [("缺口在哪", "蛋白质、膳食纤维、维生素、矿物质，一样样都对不上"),
        ("营养素是什么", "不是替代一顿饭，是补结构、补材料"),
        ("为什么有用", "身体要修复，得有材料；没材料，它只能硬撑"),
        ("怎么配", "按人的情况配，不按广告配")]
y = Inches(2.9)
for i, (k, v) in enumerate(rows):
    rect(s, L, y, CW, Inches(0.72), fill=(CREAM if i % 2 == 0 else WHITE))
    text(s, L + Inches(0.25), y, Inches(2.6), Inches(0.72), [[(k, 15, True, PINK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + Inches(3.0), y, Inches(9.1), Inches(0.72), [[(v, 15, False, INK)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.8)
bar(s, "饭是地基，营养素是补缝——两个都到位，才叫全营养。", Inches(6.05), size=16)
pagenum(s, 14)

# ══════════════ 15 · 为什么是一个人 ══════════════
s = slide()
eyebrow(s, "第四部分 · 为什么是家里那一个")
text(s, L, Inches(1.5), CW, Inches(0.9), [[("这件事，外包不出去。", 52, True, BLACK)]], spacing=1.0)
rect(s, L, Inches(2.55), Inches(2.2), Inches(0.07), fill=PINK)
rows = [("医院", "管不了你家今晚放几勺盐"),
        ("外卖平台", "不会替你算这一顿蛋白质够不够"),
        ("体检报告", "只告诉你结果，它不跟你回家")]
y = Inches(2.95)
for k, v in rows:
    text(s, L, y, Inches(0.4), Inches(0.6), [[("✕", 18, True, RED)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + Inches(0.45), y, Inches(2.2), Inches(0.6), [[(k, 20, True, BLACK)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + Inches(2.7), y, Inches(9.2), Inches(0.6), [[(v, 18, False, INK)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.75)
bar(s, "健康这件事，最后一定要落在某个具体的人身上——那就是家庭健康管理员。", Inches(5.55), size=16)
pagenum(s, 15)

# ══════════════ 16 · 怎么学 ══════════════
s = slide()
eyebrow(s, "第五部分 · 怎么学")
h1(s, "零散知识让人焦虑，体系才能变能力", size=31)
steps = [("01", "建观念", CYAN, BLACK), ("02", "补知识", YELLOW, BLACK),
         ("03", "练技术", PINK, WHITE), ("04", "家人用", CREAM, BLACK),
         ("05", "调反馈", BLACK, WHITE)]
x = Inches(0.55)
for num, name, fill, tc in steps:
    rect(s, x, Inches(2.0), Inches(2.28), Inches(1.75), fill=fill)
    text(s, x + Inches(0.2), Inches(2.15), Inches(2.0), Inches(0.35), [[(num, 12, True, tc)]])
    text(s, x + Inches(0.2), Inches(2.72), Inches(2.0), Inches(0.5), [[(name, 22, True, tc)]])
    x += Inches(2.45)
rows = [("跟着体系走", "医生 + 营养师 + 社群 + 持续更新的课程与案例"),
        ("不用从零摸索", "跟着走，然后在自家人身上用，用了有反馈再调整")]
y = Inches(4.15)
for i, (k, v) in enumerate(rows):
    rect(s, L, y, CW, Inches(0.72), fill=(CREAM if i % 2 == 0 else WHITE))
    text(s, L + Inches(0.25), y, Inches(2.6), Inches(0.72), [[(k, 15, True, PINK)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, L + Inches(3.0), y, Inches(9.1), Inches(0.72), [[(v, 15, False, INK)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.8)
bar(s, "一个人做不大，一群人才能走远。", Inches(5.95), size=17)
pagenum(s, 16)

# ══════════════ 17 · 总结 ══════════════
s = slide()
eyebrow(s, "总 结")
h1(s, "合格的家庭健康管理员，就三件事", size=33)
cards = [("观念", "慢病的主战场在家里，不在医院", "预防那 1 块，值后面 100 块", CYAN),
         ("知识", "膳食指南 + 膳食宝塔 + 五项技术", "国家给的标准答案，认真学", YELLOW),
         ("方案", "落到一周菜单、一把盐勺", "一台体重秤上，才叫管理", PINK)]
x = Inches(0.55)
for head, s1, s2, fill in cards:
    rect(s, x, Inches(1.95), Inches(3.9), Inches(2.9), fill=fill)
    text(s, x + Inches(0.28), Inches(2.18), Inches(3.4), Inches(0.5), [[(head, 24, True, BLACK)]])
    rect(s, x + Inches(0.28), Inches(2.75), Inches(0.9), Inches(0.06), fill=BLACK)
    text(s, x + Inches(0.28), Inches(2.98), Inches(3.4), Inches(1.6),
         [[(s1, 15, False, INK)], [(s2, 15, False, INK)]], spacing=1.5)
    x += Inches(4.15)
bar(s, "观念 · 知识 · 方案——三样齐了，你就是一个合格的家庭健康管理员。", Inches(5.25), size=17)
text(s, L, Inches(6.15), CW, Inches(0.5),
     [[("往小里说，护住父母爱人和孩子；往大里说，身边一定有人需要你。", 16, False, GRAY)]])
pagenum(s, 17)

# ══════════════ 18 · 结尾 ══════════════
s = slide()
rect(s, 0, 0, W, H, fill=BLACK)
rect(s, 0, Inches(2.05), W, Inches(0.1), fill=PINK)
text(s, L, Inches(0.75), CW, Inches(0.4), [[("行动号召", 14, True, PINK)]])
text(s, L, Inches(2.3), Inches(11.8), Inches(1.0), [[("一人懂健康，全家少生病", 44, True, YELLOW)]], spacing=1.0)
text(s, L, Inches(3.35), Inches(11.8), Inches(1.2),
     [[("往小里说，你护住了父母、爱人、孩子；", 20, False, WHITE)],
      [("往大里说，你把这件事做透了，身边一定有人需要你。", 20, False, WHITE)]], spacing=1.45)
rect(s, L, Inches(4.95), Inches(9.4), Inches(0.66), fill=YELLOW)
text(s, L + Inches(0.26), Inches(4.95), Inches(9.0), Inches(0.66),
     [[("想要一份「家庭健康管理清单」→ 课后私信张医生", 15, True, BLACK)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, L, Inches(5.95), CW, Inches(0.45),
     [[("下周五，健康微课堂，不见不散！", 16, True, YELLOW)]])
text(s, L, Inches(6.65), CW, Inches(0.4),
     [[("以上为健康科普分享，不构成诊疗建议，个体情况请咨询专业医师。", 11, False, GRAY)]])
pagenum(s, 18)

# ───────────── Save ─────────────
out = "/Users/mac/Documents/zfc最强大脑/C社群工作台/社群微课工作流/家庭健康管理员的价值-2026-10-30-26-22期.pptx"
prs.save(out)
print("Saved:", out, "| slides:", len(prs.slides._sldIdLst))
