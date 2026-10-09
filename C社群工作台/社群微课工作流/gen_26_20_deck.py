#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周五微课堂 26-20期《张医生日常的营养方案》— Yellow × Black Editorial
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
CREAM  = RGBColor(0xFF, 0xF9, 0xE3)
GRAY   = RGBColor(0x5A, 0x5A, 0x5A)
RED    = RGBColor(0xD4, 0x1C, 0x2A)

SERIF = "Songti SC"     # 中文衬线（标题）
SANS  = "PingFang SC"   # 中文无衬线（正文）
LATIN = "Georgia"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

M = Inches(0.85)          # margin
CW = W - 2 * M            # content width


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
    """paras: list of list-of-runs; run = (txt, size, bold, color) or (txt,size,bold,color,font)"""
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
    """左上角黑色标签块"""
    box = rect(s, M, Inches(0.5), Inches(0.16), Inches(0.34), fill=BLACK)
    text(s, M + Inches(0.34), Inches(0.48), Inches(7.6), Inches(0.4),
         [[(label, 12, True, BLACK, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
    if num is not None:
        text(s, W - M - Inches(1.4), Inches(0.48), Inches(1.4), Inches(0.4),
             [[(num, 12, True, GRAY, SANS)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def title(s, txt, size=40, top=Inches(1.18), color=INK):
    text(s, M, top, CW, Inches(1.1), [[(txt, size, True, color, SERIF)]], spacing=1.0)
    rect(s, M, top + Inches(0.92), Inches(1.7), Pt(5), fill=BLACK)


def bullets(s, items, top=Inches(2.5), size=19, gap=0.62, width=None, l=None):
    """items: list of (bold_prefix, rest) or plain str"""
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
    text(s, l, top, width, H - top - Inches(0.6), paras, spacing=1.12, space_after=int(gap * 10))


def stat(s, l, t, w, big, label, big_size=54, label_size=13, big_color=BLACK):
    text(s, l, t, w, Inches(0.95), [[(big, big_size, True, big_color, LATIN)]], spacing=1.0)
    text(s, l, t + Inches(0.82), w, Inches(0.8), [[(label, label_size, False, INK, SANS)]], spacing=1.15)


def table(s, l, t, w, headers, rows, col_w, row_h=0.52, head_h=0.5, fs=14):
    """极简黑线表"""
    x = l
    rect(s, l, t, w, head_h, fill=BLACK)
    for i, htxt in enumerate(headers):
        text(s, x + Inches(0.16), t, Inches(col_w[i]) - Inches(0.24), head_h,
             [[(htxt, fs, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
        x += Inches(col_w[i])
    y = t + head_h
    for ri, row in enumerate(rows):
        if ri % 2 == 1:
            rect(s, l, y, w, row_h, fill=CREAM)
        rect(s, l, y + row_h - Pt(1.2), w, Pt(1.2), fill=BLACK)
        x = l
        for i, cell in enumerate(row):
            bold = (i == 0)
            text(s, x + Inches(0.16), y, Inches(col_w[i]) - Inches(0.24), row_h,
                 [[(cell, fs, bold, INK, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
            x += Inches(col_w[i])
        y += row_h
    return y


def footer(s, txt, fill=BLACK, color=YELLOW, size=16, top=Inches(6.05)):
    rect(s, M, top, CW, Inches(0.8), fill=fill)
    text(s, M + Inches(0.24), top, CW - Inches(0.48), Inches(0.8),
         [[(txt, size, True, color, SANS)]], anchor=MSO_ANCHOR.MIDDLE)


# ══════════════ 1 · 封面 ══════════════
s = slide()
rect(s, 0, 0, W, Inches(0.42), fill=BLACK)
text(s, M, Inches(0.02), CW, Inches(0.4), [[("每周五健康共修微课堂", 12, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, W - M - Inches(3.0), Inches(0.02), Inches(3.0), Inches(0.4),
     [[("26-20 期", 12, True, YELLOW, SANS)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

text(s, M, Inches(1.42), CW, Inches(0.6), [[("十年营养 + 十年临床 · 我的日常", 15, True, GRAY, SANS)]])
text(s, M, Inches(2.02), Inches(11.6), Inches(1.9),
     [[("张医生日常的", 46, True, BLACK, SERIF)], [("营养方案", 78, True, BLACK, SERIF)]], spacing=1.05)
rect(s, M, Inches(4.42), Inches(2.6), Pt(7), fill=BLACK)
text(s, M, Inches(4.78), Inches(10.6), Inches(0.7),
     [[("补够量，养好肝——我每天只做两件事", 22, False, INK, SANS)]])
rect(s, M, Inches(5.58), Inches(4.6), Inches(0.62), fill=BLACK)
text(s, M + Inches(0.22), Inches(5.58), Inches(4.4), Inches(0.62),
     [[("主讲 · 本群主理人 张医生", 16, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(6.5), CW, Inches(0.4), [[("今晚 19:30 · 社群开讲", 13, False, GRAY, SANS)]])

# ══════════════ 2 · 目录 ══════════════
s = slide()
eyebrow(s, "目 录", "02")
title(s, "今天讲五件事")
items = [("01", "什么叫「日常的营养方案」"),
         ("02", "逻辑一：营养均衡充足——关键在量"),
         ("03", "逻辑二：每天养肝——维C + 奶蓟草"),
         ("04", "我的一天 · 我为什么做得"),
         ("05", "三样东西 + 一件让它便宜的事")]
y = Inches(2.72)
for num, txt in items:
    rect(s, M, y, Inches(0.62), Inches(0.62), fill=BLACK)
    text(s, M, y, Inches(0.62), Inches(0.62), [[(num, 20, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(0.95), y, Inches(10.2), Inches(0.62), [[(txt, 24, True, INK, SERIF)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.78)

# ══════════════ 3 · 我每天只做两件事 ══════════════
s = slide()
eyebrow(s, "开场", "03")
title(s, "我每天只做两件事", size=36)
text(s, M, Inches(2.5), CW, Inches(1.6),
     [[("一个管「进料」，", 30, True, INK, SERIF)],
      [("一个管「转化」。", 30, True, INK, SERIF)]], spacing=1.3)
rect(s, M, Inches(4.05), CW, Inches(0.05), fill=BLACK)
bullets(s, [
    ("身体就像一座工厂  ", "——原料要备足、备齐，流水线要保养好"),
    ("原料不够，工厂停工  ", "——机器不转，原料堆在仓库里也是废的"),
    ("我每天做的  ", "——早上把原料送进厂，晚上把机器保养好"),
], top=Inches(4.45), size=20, gap=0.68)

# ══════════════ 4 · 为什么是这两件事 ══════════════
s = slide()
eyebrow(s, "开场 · 两个逻辑", "04")
title(s, "为什么是这两件事", size=36)
cards = [("01", "营养均衡充足", "所有抗衰、保养、调理的「底牌」——是身体健康的底色。底色不牢，上面刷什么都白刷"),
         ("02", "每天养肝", "肝是全身的运化中枢——肝的效率，决定你补进去的营养有多少能变成修复力")]
y = Inches(2.75)
for num, head, sub in cards:
    rect(s, M, y, CW, Inches(1.5), fill=None, line=BLACK, lw=2.5)
    rect(s, M, y, Inches(1.1), Inches(1.5), fill=BLACK)
    text(s, M, y, Inches(1.1), Inches(1.5), [[(num, 30, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(1.35), y + Inches(0.22), CW - Inches(1.6), Inches(0.55),
         [[(head, 25, True, INK, SERIF)]])
    text(s, M + Inches(1.35), y + Inches(0.82), CW - Inches(1.6), Inches(0.55),
         [[(sub, 14, False, GRAY, SANS)]])
    y += Inches(1.68)
footer(s, "营养均衡充足到位，每天坚持养肝——就这么简单。", top=Inches(6.2))

# ══════════════ 5 · 营养均衡卡在量 ══════════════
s = slide()
eyebrow(s, "逻辑一 · 关键在「量」", "05")
title(s, "营养均衡，卡在那个「量」")
text(s, M, Inches(2.5), CW, Inches(0.7),
     [[("没有量的均衡，都是假的。", 28, True, BLACK, SANS)]], spacing=1.0)
bullets(s, [
    ("吃了蔬菜水果，但只吃两口  ", "——对身体来说，跟没吃差不了多少"),
    ("最容易缺的两样  ", "——蛋白质 · 维生素和矿物质"),
    ("你现在多半不是「健康人」  ", "——是亚健康。按健康人的标准吃，就是不够"),
], top=Inches(3.5), size=20, gap=0.72)

# ══════════════ 6 · 我按调理的量定标准 ══════════════
s = slide()
eyebrow(s, "逻辑一 · 我的标准", "06")
title(s, "我按「调理的量」给自己定", size=34)
stat(s, M, Inches(2.55), Inches(5.6), "1.5 g/kg", "蛋白质——每公斤体重 1.5 克（60kg → 一天 90 克）", big_size=46)
rect(s, M + Inches(5.9), Inches(2.5), Pt(3), Inches(2.3), fill=BLACK)
stat(s, M + Inches(6.3), Inches(2.55), Inches(5.6), "+ 额外补", "维生素、矿物质——靠现在的果蔬，补不到那个量", big_size=46)
rect(s, M, Inches(5.2), CW, Inches(0.95), fill=BLACK)
text(s, M + Inches(0.24), Inches(5.2), CW - Inches(0.48), Inches(0.95),
     [[("这两样到位，营养的地基就打牢了——每天都有稳定的原材料供应。", 20, True, YELLOW, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(6.42), CW, Inches(0.5),
     [[("注意：我定的是「调理档」，不是「推荐量」——因为我现在也不是健康人的状态。", 14, False, GRAY, SANS)]])

# ══════════════ 7 · 靠吃饭补不到 ══════════════
s = slide()
eyebrow(s, "逻辑一 · 我的做法", "07")
title(s, "靠吃饭补不到这个量，我怎么办", size=32)
bullets(s, [
    ("靠三餐硬吃  ", "——胃根本受不了，吃不下、消化不了"),
    ("我一天蛋白粉约 5–6 勺  ", "——早上先喝 2 勺，下午空档再补 1–2 勺"),
    ("三餐正常吃  ", "——鱼肉蛋奶照吃，不节食、不硬撑"),
    ("两头加起来  ", "——稳稳落在调理档上"),
], top=Inches(2.8), size=20, gap=0.72)
footer(s, "不要硬吃肉，要「像吃药一样」精准补——这是量的思路。", top=Inches(6.15))

# ══════════════ 8 · 为什么必须养肝 ══════════════
s = slide()
eyebrow(s, "逻辑二 · 养肝", "08")
title(s, "为什么我每天都要养肝", size=34)
bullets(s, [
    ("肝是运化中枢  ", "——所有营养先经肝分解、转化、解毒，才能被细胞用上"),
    ("肝一累，全身效率往下掉  ", "——工作压力 · 情绪憋着 · 熬夜 · 喝酒 · 外卖"),
    ("肝没有痛觉  ", "——它受了伤不吭声，更不能等它喊疼才管"),
], top=Inches(2.8), size=20, gap=0.78)
footer(s, "养肝，是保养身体最高效、最划算的一件事——肝好了，五脏六腑都跟着顺。", size=17, top=Inches(6.1))

# ══════════════ 9 · 养肝组合 ══════════════
s = slide()
eyebrow(s, "逻辑二 · 组合", "09")
title(s, "养肝组合：维生素 C + 奶蓟草", size=32)
cw = (CW - Inches(0.5)) / 2
x = M
combos = [("维生素 C", "帮肝脏解毒、减轻氧化压力", "肝每天干的活本质是「氧化处理」，\n维C 就是它干活时要用的那个「灭火器」", BLACK, YELLOW, WHITE),
          ("奶蓟草（水飞蓟素）", "加速肝细胞复制换新 + 稳住肝细胞膜", "进入肝细胞，加速肝细胞复制换新；\n给肝细胞膜加一层保护，拦住氧化破坏", WHITE, INK, GRAY)]
for head, sub, body, fill, tc, sc in combos:
    rect(s, x, Inches(2.6), cw, Inches(2.9), fill=fill, line=BLACK, lw=2.5)
    text(s, x + Inches(0.28), Inches(2.85), cw - Inches(0.56), Inches(0.6),
         [[(head, 25, True, tc, SERIF)]], spacing=1.05)
    text(s, x + Inches(0.28), Inches(3.52), cw - Inches(0.56), Inches(0.5),
         [[(sub, 14, True, tc, SANS)]], spacing=1.2)
    text(s, x + Inches(0.28), Inches(4.15), cw - Inches(0.56), Inches(1.1),
         [[(body, 13.5, False, sc, SANS)]], spacing=1.3)
    x += cw + Inches(0.5)
footer(s, "一个修，一个清——一边清垃圾，一边修房子。", top=Inches(5.85))

# ══════════════ 10 · 养肝是长线 ══════════════
s = slide()
eyebrow(s, "逻辑二 · 时间账", "10")
title(s, "养肝，是长线工程", size=36)
stat(s, M, Inches(2.65), CW, "5–6 个月", "肝细胞更新一轮，大约要 5 到 6 个月", big_size=72, label_size=16)
rect(s, M, Inches(4.75), CW, Inches(0.05), fill=BLACK)
bullets(s, [
    ("别指望一个月见分晓  ", "——养肝是长线，急不来"),
    ("我的一天口诀  ", "——早上吃好营养早餐，晚上坚持每日护肝"),
], top=Inches(5.1), size=20, gap=0.7)

# ══════════════ 11 · 我的一天 ══════════════
s = slide()
eyebrow(s, "第四部分 · 我的一天", "11")
title(s, "我的一天，就排成这样", size=34)
table(s, M, Inches(2.35), CW,
      ["时间", "我做什么"],
      [["早上 7:30", "营养早餐 + 蛋白粉 2 勺 + 维生素 C 1 片　—　早上吃好"],
       ["中午 / 下午", "正常吃饭，鱼肉蛋奶照吃；空档补 1–2 勺蛋白粉"],
       ["晚上 7:30", "男士组合 1 包（自带维矿 + 鱼油 + 奶蓟草）+ 维生素 C　—　晚上护肝"],
       ["睡前", "晚餐少吃、吃素一点，11:30 前睡——给肝留出修复窗口"]],
      col_w=[3.1, 8.53], row_h=0.68, head_h=0.56, fs=17)

# ══════════════ 12 · 我平时就用这三样 ══════════════
s = slide()
eyebrow(s, "第四部分 · 三样东西", "12")
title(s, "我平时就用这三样", size=36)
combo = [("蛋白粉", "补足蛋白质那个「量」\n—— 进料"),
         ("男士组合", "维矿 + 好脂肪 + 奶蓟草\n一次补齐 —— 转化"),
         ("维生素 C", "帮肝解毒\n白天晚上都用得上")]
cw = (CW - Inches(0.6)) / 3
x = M
for i, (head, sub) in enumerate(combo):
    fill = BLACK if i % 2 == 0 else WHITE
    tc = YELLOW if i % 2 == 0 else INK
    sc = WHITE if i % 2 == 0 else GRAY
    rect(s, x, Inches(2.85), cw, Inches(2.5), fill=fill, line=BLACK, lw=2.5)
    text(s, x + Inches(0.24), Inches(3.05), cw - Inches(0.48), Inches(0.5),
         [[("0" + str(i + 1), 15, True, tc, LATIN)]])
    text(s, x + Inches(0.24), Inches(3.6), cw - Inches(0.48), Inches(0.6),
         [[(head, 25, True, tc, SERIF)]], spacing=1.05)
    text(s, x + Inches(0.24), Inches(4.35), cw - Inches(0.48), Inches(0.9),
         [[(sub, 14, False, sc, SANS)]], spacing=1.3)
    x += cw + Inches(0.3)
text(s, M, Inches(5.65), CW, Inches(0.6),
     [[("这个组合不是男士专属——男女老少都能用，因为人人都有肝。", 16, True, BLACK, SANS)]])

# ══════════════ 13 · 我为什么能天天坚持 ══════════════
s = slide()
eyebrow(s, "第四部分 · 坚持", "13")
title(s, "为什么我能天天坚持？", size=36)
text(s, M, Inches(2.5), CW, Inches(0.8),
     [[("不是靠意志力，是靠机制。", 28, True, BLACK, SANS)]], spacing=1.0)
bullets(s, [
    ("短期吃是消费，长期吃才是投资  ", "——断断续续三个月，身体还没开始修，你就停了"),
    ("身体要的是一年、两年的节奏  ", "——像刷牙一样自然，不是三个月的突击"),
    ("所以我把它变成了一件事  ", "——把「吃多久」交给机制来管，不靠每天下决心"),
], top=Inches(3.5), size=19, gap=0.72)

# ══════════════ 14 · 长客会 ══════════════
s = slide()
eyebrow(s, "第四部分 · 让它便宜", "14")
title(s, "长客会——让「坚持」变得便宜", size=32)
bullets(s, [
    ("说穿了就是「长期约定」  ", "——按月锁定要吃的量，公司按长期会员的价给你"),
    ("现在长客会 6.5 折  ", "——本来一个月的量，打个六五折就拿到"),
    ("自动续上  ", "——不用每个月光想着去买，也不会断供"),
], top=Inches(2.75), size=19, gap=0.7)
rect(s, M, Inches(5.05), CW, Inches(1.15), fill=BLACK)
text(s, M + Inches(0.3), Inches(5.05), CW - Inches(0.6), Inches(1.15),
     [[("因为便宜，所以吃得起；因为吃得起，所以坚持得下去；", 17, True, YELLOW, SANS)],
      [("因为坚持得下去，所以身体才有机会给你反馈。", 17, True, YELLOW, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE, spacing=1.25)
text(s, M, Inches(6.45), CW, Inches(0.5),
     [[("这件事，每一个人都能做——没有什么门槛。", 15, False, GRAY, SANS)]])

# ══════════════ 15 · 总结 ══════════════
s = slide()
eyebrow(s, "总结", "15")
text(s, M, Inches(1.5), Inches(3.4), Inches(0.5), [[("总结", 14, True, GRAY, SANS)]])
text(s, M, Inches(2.1), Inches(11.8), Inches(1.6),
     [[("补够量，", 44, True, BLACK, SERIF), ("养好肝。", 44, True, BLACK, SERIF)]], spacing=1.15)
rect(s, M, Inches(3.55), Inches(2.4), Pt(6), fill=BLACK)
bullets(s, [
    ("① 营养均衡充足到位：蛋白质 1.5 g/kg，维生素矿物质额外补"),
    ("② 每天养肝：维生素 C + 奶蓟草——一个清，一个修"),
    ("早上吃好营养早餐，晚上坚持每日护肝——每天就这两件小事"),
], top=Inches(4.05), size=18, gap=0.6)

# ══════════════ 16 · 行动号召 ══════════════
s = slide()
rect(s, 0, 0, W, H, fill=BLACK)
rect(s, 0, Inches(2.3), W, Inches(0.09), fill=YELLOW)
text(s, M, Inches(0.9), CW, Inches(0.5), [[("行动号召", 14, True, YELLOW, SANS)]])
text(s, M, Inches(1.18), Inches(11.6), Inches(1.0),
     [[("慢病和亚健康，很多不是被治好的", 34, True, YELLOW, SERIF)]], spacing=1.0)
text(s, M, Inches(2.72), Inches(11.8), Inches(1.6),
     [[("是被日复一日养回来的——", 22, False, WHITE, SANS)],
      [("早上吃好营养早餐，晚上坚持每日护肝。剩下的，交给身体自己修。", 20, False, WHITE, SANS)]], spacing=1.35)
rect(s, M, Inches(4.68), Inches(7.6), Inches(0.68), fill=YELLOW)
text(s, M + Inches(0.22), Inches(4.68), Inches(7.3), Inches(0.68),
     [[("想算出「你自己一天该吃的量」·趁 6.5 折配好长客会 → 私信张医生", 15, True, BLACK, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(5.75), CW, Inches(0.5),
     [[("下周五，健康微课堂，不见不散！", 15, False, YELLOW, SANS)]])
text(s, M, Inches(6.6), CW, Inches(0.4),
     [[("以上为健康科普分享，不构成诊疗建议，个体情况请咨询专业医师。", 11, False, GRAY, SANS)]])

# ───────────── Save ─────────────
out = "/Users/mac/Documents/zfc最强大脑/C社群工作台/社群微课工作流/张医生日常的营养方案-26-20期.pptx"
prs.save(out)
print("Saved:", out, "| slides:", len(prs.slides._sldIdLst))
