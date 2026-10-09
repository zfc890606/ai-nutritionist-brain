#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周五微课堂 26-19期《蛋白质如何科学补充》— Yellow × Black Editorial
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
    text(s, M + Inches(0.34), Inches(0.48), Inches(7.0), Inches(0.4),
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
    # header row
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


# ══════════════ 1 · 封面 ══════════════
s = slide()
rect(s, 0, 0, W, Inches(0.42), fill=BLACK)
text(s, M, Inches(0.02), CW, Inches(0.4), [[("每周五健康共修微课堂", 12, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, W - M - Inches(3.0), Inches(0.02), Inches(3.0), Inches(0.4),
     [[("26-19 期", 12, True, YELLOW, SANS)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

text(s, M, Inches(1.55), CW, Inches(0.6), [[("PROTEIN · 科学补充", 15, True, GRAY, SANS)]])
text(s, M, Inches(2.15), Inches(11.0), Inches(1.9),
     [[("蛋白质", 78, True, BLACK, SERIF), ("如何科学补充", 44, True, BLACK, SERIF)]], spacing=1.05)
rect(s, M, Inches(4.35), Inches(2.6), Pt(7), fill=BLACK)
text(s, M, Inches(4.72), Inches(10.6), Inches(0.7),
     [[("从标准到缺口，把量补对——", 22, False, INK, SANS)]])
rect(s, M, Inches(5.55), Inches(4.6), Inches(0.62), fill=BLACK)
text(s, M + Inches(0.22), Inches(5.55), Inches(4.4), Inches(0.62),
     [[("主讲 · 本群主理人 张医生", 16, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(6.5), CW, Inches(0.4), [[("今晚 19:30 · 社群开讲", 13, False, GRAY, SANS)]])

# ══════════════ 2 · 目录 ══════════════
s = slide()
eyebrow(s, "目 录", "02")
title(s, "今天讲五件事")
items = [("01", "蛋白质，为什么是生命的基石"),
         ("02", "不同的人，需要量完全不一样"),
         ("03", "现代人普遍的「蛋白缺口」"),
         ("04", "对标准 · 算缺口 · 补到位"),
         ("05", "我每天喝的那一杯")]
y = Inches(2.72)
for num, txt in items:
    rect(s, M, y, Inches(0.62), Inches(0.62), fill=BLACK)
    text(s, M, y, Inches(0.62), Inches(0.62), [[(num, 20, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(0.95), y, Inches(9.6), Inches(0.62), [[(txt, 24, True, INK, SERIF)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.78)

# ══════════════ 3 · 没有蛋白质就没有生命 ══════════════
s = slide()
eyebrow(s, "第一部分 · 生命的基石", "03")
title(s, "没有蛋白质，就没有生命")
bullets(s, [
    ("占体重 16%–20%  ", "——60kg 的人，身上有 9.6–12kg 都是蛋白质"),
    ("皮肤 28 天换一次 · 胃黏膜 3 天换一次  ", "——拿什么换？拿蛋白质"),
    ("抗体、白细胞 7 天更新一次  ", "——抗体的原料，就是蛋白质"),
    ("胶原蛋白  ", "——它是人体含量最大的一种蛋白质"),
], top=Inches(2.85), size=20, gap=0.72)

# ══════════════ 4 · 缺了会怎样 ══════════════
s = slide()
eyebrow(s, "第一部分 · 缺乏的表现", "04")
title(s, "缺了会怎样？14 种表现挑重点")
bullets(s, [
    ("免疫力低下  ", "——容易感冒、发炎 · 伤口好得慢、容易留疤"),
    ("加速老化 · 能量不足  ", "——肌肉萎缩、皮肤没光泽，总觉得累"),
    ("骨质疏松  ", "——胶原蛋白是「钢筋」，钙是「水泥」；钢筋没了，水泥往哪浇？"),
    ("消化道松弛  ", "——贲门松了会反酸，幽门松了容易溃疡"),
], top=Inches(2.85), size=20, gap=0.78)
rect(s, M, Inches(6.15), CW, Inches(0.72), fill=BLACK)
text(s, M + Inches(0.24), Inches(6.15), CW - Inches(0.48), Inches(0.72),
     [[("很多人的反流性胃炎，本质是蛋白质不够、细胞「饿」了——光吃药不补原料，补不回来。", 16, True, YELLOW, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 5 · 一个通用公式 ══════════════
s = slide()
eyebrow(s, "第二部分 · 需要量", "05")
title(s, "一个通用公式", size=34)
text(s, M, Inches(2.55), CW, Inches(1.0),
     [[("每天需要的蛋白质（克） = 体重（公斤） × 系数", 34, True, BLACK, SANS)]], spacing=1.0)
rect(s, M, Inches(3.62), Inches(3.2), Pt(6), fill=BLACK)
bullets(s, [
    ("系数不是固定的  ", "——看你是谁、处在什么状态"),
    ("八个字  ", "——张旭老师：因人而异、因时而异"),
    ("关键问题  ", "——你现在是「维持档」，还是「修复档」？"),
], top=Inches(4.15), size=20, gap=0.68)

# ══════════════ 6 · 不同人群需要量一张表 ══════════════
s = slide()
eyebrow(s, "第二部分 · 分人群", "06")
title(s, "不同人群，一张表看清", size=34)
table(s, M, Inches(2.42), CW,
      ["人群", "每日系数", "60kg 相当于"],
      [["健康成年人（维持）", "0.8–1.0 g/kg", "48–60 g"],
       ["慢病调理 / 修复期", "1.2–1.5 g/kg", "72–90 g"],
       ["中老年人（50岁+）", "1.0–1.2 g/kg", "60–72 g"],
       ["孕妇", "孕早 +1g / 中 +15g / 晚 +30g", "—"],
       ["哺乳期", "+25 g", "—"],
       ["肿瘤 / 大手术 / 创伤", "1.2–2.0 g/kg", "72–120 g"]],
      col_w=[4.5, 4.4, 2.73], row_h=0.56, head_h=0.52, fs=15)

# ══════════════ 7 · 三句话记住这张表 ══════════════
s = slide()
eyebrow(s, "第二部分 · 划重点", "07")
title(s, "三句话，记住这张表")
cards = [("01", "普通成人不是 1.2，是 0.8–1.0", "很多人记的「每公斤 1.2 克」，那已经是修复档了"),
         ("02", "年龄越大，需要的反而越多", "合成代谢抵抗——吸收效率下降。DRIs 2023 已把 65+ 上调到 1.17 g/kg"),
         ("03", "肿瘤患者不是不能补，是必须加强补", "一碗饭的比喻，下一页讲")]
y = Inches(2.8)
for num, head, sub in cards:
    rect(s, M, y, CW, Inches(1.2), fill=None, line=BLACK, lw=2.5)
    rect(s, M, y, Inches(0.9), Inches(1.2), fill=BLACK)
    text(s, M, y, Inches(0.9), Inches(1.2), [[(num, 26, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(1.15), y + Inches(0.16), CW - Inches(1.4), Inches(0.5),
         [[(head, 21, True, INK, SERIF)]])
    text(s, M + Inches(1.15), y + Inches(0.66), CW - Inches(1.4), Inches(0.45),
         [[(sub, 13, False, GRAY, SANS)]])
    y += Inches(1.36)

# ══════════════ 8 · 一碗饭的比喻 ══════════════
s = slide()
eyebrow(s, "第二部分 · 一个比喻", "08")
title(s, "「一碗饭」的比喻", size=36)
text(s, M, Inches(2.5), CW, Inches(2.0),
     [[("普通人每天吃一碗饭；", 26, True, INK, SERIF)],
      [("肿瘤每天固定消耗半碗。", 26, True, INK, SERIF)]], spacing=1.35)
rect(s, M, Inches(4.35), CW, Inches(0.05), fill=BLACK)
bullets(s, [
    ("不加量  ", "——身体就只剩半碗"),
    ("不吃  ", "——肿瘤照样消耗半碗，身体只能拆脂肪和肌肉去供养它"),
], top=Inches(4.75), size=20, gap=0.7)
rect(s, M, Inches(6.2), CW, Inches(0.78), fill=BLACK)
text(s, M + Inches(0.24), Inches(6.2), CW - Inches(0.48), Inches(0.78),
     [[("营养不是在支持疾病，而是在治疗疾病。—— 石汉平教授", 17, True, YELLOW, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 9 · 三重折损 ══════════════
s = slide()
eyebrow(s, "第三部分 · 蛋白缺口", "09")
title(s, "你吃进去的 ≠ 细胞拿到的", size=34)
labels = [("−20%", "原料折损", "速生、水培\n高水分、低营养密度"),
          ("−30%", "高温烹饪折损", "外卖重油煎炸\n产生吸收不了的「死结」"),
          ("−20%", "消化酶亏空", "胃酸活性低\n大颗粒蛋白消化不彻底")]
cw = (CW - Inches(0.6)) / 3
x = M
for big, head, sub in labels:
    rect(s, x, Inches(2.55), cw, Inches(2.75), fill=BLACK)
    text(s, x + Inches(0.2), Inches(2.75), cw - Inches(0.4), Inches(0.9),
         [[(big, 46, True, YELLOW, LATIN)]], align=PP_ALIGN.CENTER, spacing=1.0)
    text(s, x + Inches(0.2), Inches(3.72), cw - Inches(0.4), Inches(0.5),
         [[(head, 18, True, WHITE, SANS)]], align=PP_ALIGN.CENTER)
    text(s, x + Inches(0.2), Inches(4.28), cw - Inches(0.4), Inches(0.9),
         [[(sub, 12.5, False, YELLOW, SANS)]], align=PP_ALIGN.CENTER, spacing=1.2)
    x += cw + Inches(0.3)
text(s, M, Inches(5.65), CW, Inches(0.8),
     [[("三重下来，标称量到细胞实际「到账」，大概只剩一半。", 21, True, BLACK, SANS)]])

# ══════════════ 10 · 缺口有多大 ══════════════
s = slide()
eyebrow(s, "第三部分 · 算笔账", "10")
title(s, "缺口有多大？", size=36)
stat(s, M, Inches(2.6), Inches(5.6), "55 g", "60kg 上班族，一天标称吃进去的蛋白")
rect(s, M + Inches(5.9), Inches(2.55), Pt(3), Inches(2.3), fill=BLACK)
stat(s, M + Inches(6.3), Inches(2.6), Inches(5.6), "< 30 g", "三重折损之后，细胞真正到账的量")
rect(s, M, Inches(5.25), CW, Inches(0.92), fill=BLACK)
text(s, M + Inches(0.24), Inches(5.25), CW - Inches(0.48), Inches(0.92),
     [[("慢病调理需要 72–90 g ——缺口 40 g 以上，不是「多吃两口肉」能解决的。", 20, True, YELLOW, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(6.45), CW, Inches(0.5),
     [[("隐性饥饿：热量超标，营养不足。", 15, False, GRAY, SANS)]])

# ══════════════ 11 · 补的原则 ══════════════
s = slide()
eyebrow(s, "第四部分 · 怎么补", "11")
title(s, "不硬吃肉，像吃药一样补")
bullets(s, [
    ("吃不够时，不要强迫自己多吃肉  ", "——消化不了，胃口反而更差"),
    ("两餐之间 / 睡前  ", "——补已经提纯、免消化、优质蛋白"),
    ("大豆分离蛋白打底  ", "——去掉四个短板：抑制因子、产气因子、多余脂肪、粗纤维"),
    ("豌豆 + 小麦蛋白补蛋氨酸  ", "——把大豆缺的那块「短板」补齐"),
], top=Inches(2.85), size=19, gap=0.72)
rect(s, M, Inches(6.05), CW, Inches(0.82), fill=BLACK)
text(s, M + Inches(0.24), Inches(6.05), CW - Inches(0.48), Inches(0.82),
     [[("PDCAAS = 1 · 吸收利用率接近 100% · 零胆固醇——吸收越好，对肝肾压力越小。", 17, True, YELLOW, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 12 · 每天补多少 ══════════════
s = slide()
eyebrow(s, "第四部分 · 剂量", "12")
title(s, "每天补多少？一条阶梯", size=34)
table(s, M, Inches(2.42), Inches(8.2),
      ["你的状态", "每日蛋白粉参考量"],
      [["起步期（前 1–2 周）", "0.5–1 勺"],
       ["日常维持、打底", "1–2 勺"],
       ["普通慢病调理", "3 勺"],
       ["中重度消耗 / 合成抵抗", "5 勺"]],
      col_w=[5.0, 3.2], row_h=0.6, head_h=0.54, fs=16)
rect(s, M + Inches(8.6), Inches(2.42), Inches(3.03), Inches(2.94), fill=BLACK)
text(s, M + Inches(8.85), Inches(2.72), Inches(2.5), Inches(2.4),
     [[("一平勺", 16, False, YELLOW, SANS)],
      [("≈ 8 g", 34, True, YELLOW, LATIN)],
      [("蛋白", 16, False, YELLOW, SANS)],
      [("", 8, False, YELLOW, SANS)],
      [("分次补充，", 13, False, WHITE, SANS)],
      [("比一次灌下去好", 13, False, WHITE, SANS)]], spacing=1.25)

# ══════════════ 13 · 小量开始 一周一周加 ══════════════
s = slide()
eyebrow(s, "第四部分 · 加量原则", "13")
title(s, "最重要的一条：小量开始，一周一周加")
bullets(s, [
    ("一吃就拉肚子？  ", "——恰恰说明太缺了，消化能力跟不上；从极少量起步，慢慢加，不是不吃"),
    ("一吃就「上火」？  ", "——身体处在过度氧化状态；同时把维生素 C 补上，发生率大大降低"),
    ("同样是补蛋白  ", "——有人要配维C，有人得从半勺起步，有人反而要减量"),
], top=Inches(2.85), size=20, gap=0.78)
rect(s, M, Inches(6.05), CW, Inches(0.8), fill=BLACK)
text(s, M + Inches(0.24), Inches(6.05), CW - Inches(0.48), Inches(0.8),
     [[("量不对，补了也白补——所以必须一格一格地加，让身体接得住。", 18, True, YELLOW, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 14 · 一套完整的修复组合 ══════════════
s = slide()
eyebrow(s, "第四部分 · 组合", "14")
title(s, "一套完整的修复组合", size=34)
combo = [("蛋白质粉", "修复的原料"),
         ("姜黄维生素C", "抗炎、抗氧化\n护住身体别过度氧化"),
         ("硒", "抗氧化酶的核心零件\n可从倍立健多种维矿补"),
         ("卵磷脂", "修复细胞膜")]
cw = (CW - Inches(0.9)) / 4
x = M
for i, (head, sub) in enumerate(combo):
    fill = BLACK if i % 2 == 0 else WHITE
    tc = YELLOW if i % 2 == 0 else INK
    sc = WHITE if i % 2 == 0 else GRAY
    rect(s, x, Inches(2.85), cw, Inches(2.6), fill=fill, line=BLACK, lw=2.5)
    text(s, x + Inches(0.2), Inches(3.05), cw - Inches(0.4), Inches(0.55),
         [[("0" + str(i + 1), 15, True, tc, LATIN)]])
    text(s, x + Inches(0.2), Inches(3.62), cw - Inches(0.4), Inches(0.6),
         [[(head, 21, True, tc, SERIF)]], spacing=1.05)
    text(s, x + Inches(0.2), Inches(4.32), cw - Inches(0.4), Inches(1.0),
         [[(sub, 13, False, sc, SANS)]], spacing=1.25)
    x += cw + Inches(0.3)

# ══════════════ 15 · 我每天喝的那一杯 ══════════════
s = slide()
eyebrow(s, "第五部分 · 我的经验", "15")
title(s, "我每天喝的那一杯")
bullets(s, [
    ("第一件 · 每天一杯  ", "——蛋白质粉 + 姜黄维生素C + 含硒的多种维矿，一起冲开喝"),
    ("第二件 · 早餐换抗炎早餐  ", "——破壁机打蔬果昔：蔬果 + 蛋白粉 + 优质脂肪 + 姜黄维C + 卵磷脂"),
    ("五分钟搞定  ", "——高蛋白、高纤维、优质脂肪，一上午精力都稳"),
], top=Inches(2.85), size=20, gap=0.78)
rect(s, M, Inches(6.05), CW, Inches(0.8), fill=BLACK)
text(s, M + Inches(0.24), Inches(6.05), CW - Inches(0.48), Inches(0.8),
     [[("我的感受：不容易累了，也不那么容易感冒了。你可以先从半勺蛋白粉开始试。", 17, True, YELLOW, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 16 · 总结 ══════════════
s = slide()
eyebrow(s, "总结", "16")
text(s, M, Inches(1.5), Inches(3.4), Inches(0.5), [[("总结", 14, True, GRAY, SANS)]])
text(s, M, Inches(2.15), Inches(11.4), Inches(2.2),
     [[("脱离剂量谈疗效，", 46, True, BLACK, SERIF)],
      [("就是耍流氓。", 46, True, BLACK, SERIF)]], spacing=1.15)
rect(s, M, Inches(4.55), Inches(2.4), Pt(6), fill=BLACK)
bullets(s, [
    ("健康人 48g，慢病调理 72–90g；老人需要的，反而比年轻人多"),
    ("肿瘤患者不是不能吃，是要多吃"),
    ("营养一定要专业——先算缺口，再按身体反应，一点一点加"),
], top=Inches(5.0), size=17, gap=0.55)

# ══════════════ 17 · 行动号召 ══════════════
s = slide()
rect(s, 0, 0, W, H, fill=BLACK)
rect(s, 0, Inches(2.25), W, Inches(0.09), fill=YELLOW)
text(s, M, Inches(0.9), CW, Inches(0.5), [[("行动号召", 14, True, YELLOW, SANS)]])
text(s, M, Inches(1.15), Inches(11.4), Inches(1.0),
     [[("先算缺口，再补到位", 40, True, YELLOW, SERIF)]], spacing=1.0)
text(s, M, Inches(2.75), Inches(11.4), Inches(1.6),
     [[("营养不是「多吃点好的」，是精准定量——", 22, False, WHITE, SANS)],
      [("先算出你的缺口，再按你身体的反应，把量一点一点加上去。", 22, False, WHITE, SANS)]], spacing=1.35)
rect(s, M, Inches(4.62), Inches(6.6), Inches(0.68), fill=YELLOW)
text(s, M + Inches(0.22), Inches(4.62), Inches(6.3), Inches(0.68),
     [[("想算出「你一天该补多少蛋白」→ 私信张医生", 16, True, BLACK, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(5.72), CW, Inches(0.5),
     [[("下期预告：蛋白质的木桶效应——缺一样，其他都白搭", 15, False, YELLOW, SANS)]])
text(s, M, Inches(6.6), CW, Inches(0.4),
     [[("以上为健康科普分享，不构成诊疗建议，个体情况请咨询专业医师。", 11, False, GRAY, SANS)]])

# ───────────── Save ─────────────
out = "/Users/mac/Documents/zfc最强大脑/C社群工作台/社群微课工作流/蛋白质如何科学补充-26-19期.pptx"
prs.save(out)
print("Saved:", out, "| slides:", len(prs.slides._sldIdLst))
