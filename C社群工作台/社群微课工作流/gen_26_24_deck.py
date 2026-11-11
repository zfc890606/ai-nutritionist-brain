#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
26-24期《朋友问「你在做安利啊」，你怎么答》— 万病寻源版固定风格（20 页）
引擎：deck_style_wanbing.py
"""

import deck_style_wanbing as D
from deck_style_wanbing import *
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

D.TOTAL = 20
TOTAL = 20
PAGES = 20


def band(s, txt, top, h=0.72, fill=BLACK, color=WHITE, size=20, left=None, width=None):
    """覆盖引擎版：引擎把 h 当 EMU 传，0.72 会变成不可见细条；这里统一按英寸。"""
    left = M if left is None else left
    width = CW if width is None else width
    rect(s, left, top, width, Inches(h), fill=fill)
    text(s, left + Inches(0.26), top, width - Inches(0.52), Inches(h),
         [[(txt, size, True, color, BODY)]], anchor=MSO_ANCHOR.MIDDLE)


def num_box(s, x, y, w, h, num, col, size=22):
    rect(s, x, y, w, h, fill=col)
    text(s, x, y, w, h, [[(num, size, True, BLACK, BODY)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


new_deck()

# ══════════════ 1 · 封面 ══════════════
s = slide()
rect(s, 0, 0, W, Inches(0.18), fill=PINK)
text(s, M, Inches(0.62), Inches(8.0), Inches(0.34),
     [[("HEALTH TALK  ·  社群微课  ·  26-24 期", 13, True, PINK, BODY)]])
text(s, M, Inches(1.16), Inches(9.6), Inches(1.9),
     [[("「你在做安利啊？」", 50, True, BLACK, BODY)]], spacing=1.1)
text(s, M, Inches(2.10), Inches(9.2), Inches(1.1),
     [[("你 怎 么 答", 56, True, BLACK, BODY)]], spacing=1.1)
rect(s, M, Inches(3.42), Inches(2.3), Inches(0.09), fill=PINK)
text(s, M, Inches(3.74), Inches(9.2), Inches(0.6),
     [[("一套完整的事业说明", 30, True, INK, BODY)]])
text(s, M, Inches(4.42), Inches(9.2), Inches(0.5),
     [[("五段话，从「我」讲到「你」，最后才讲机会", 16, False, GRAY, BODY)]])
text(s, M, Inches(5.10), Inches(9.2), Inches(0.5),
     [[("不讲产品 · 不讲收入 · 只讲怎么讲清楚", 16, False, GRAY, BODY)]])

rect(s, Inches(10.65), Inches(1.05), Inches(2.10), Inches(2.10), fill=CYAN)
text(s, Inches(10.65), Inches(1.28), Inches(2.10), Inches(1.2),
     [[("5", 64, True, BLACK, NUM)]], align=PP_ALIGN.CENTER, spacing=0.95)
text(s, Inches(10.65), Inches(2.42), Inches(2.10), Inches(0.4),
     [[("段 话 · 25 分钟", 13, True, BLACK, BODY)]], align=PP_ALIGN.CENTER)

rect(s, 0, Inches(6.30), W, Inches(1.20), fill=BLACK)
text(s, M, Inches(6.30), Inches(6.4), Inches(1.20),
     [[("主讲 · 本群主理人 张医生", 18, True, WHITE, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, W - M - Inches(5.2), Inches(6.30), Inches(5.2), Inches(1.20),
     [[("2026-11-02 · 社群微课", 15, False, YELLOW, BODY)]],
     align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 2 · 目录 ══════════════
s = slide()
head(s, "CONTENTS", "今天讲四件事", 2)
items = [("01", "先破误解：他到底在防什么"),
         ("02", "五段话：从「我」讲到「你」"),
         ("03", "三个必答题：收入 · 职位 · 跟谁学"),
         ("04", "三个坑：讲错一句，全盘皆输")]
y = Inches(2.35)
for i, (num, ttl) in enumerate(items):
    rect(s, M, y, CW, Inches(0.86), fill=CREAM if i % 2 == 0 else None)
    text(s, M + Inches(0.26), y, Inches(0.9), Inches(0.86),
         [[(num, 22, True, PINK, NUM)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(1.20), y, Inches(10.2), Inches(0.86),
         [[(ttl, 22, True, INK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, W - M - Inches(0.6), y, Inches(0.6), Inches(0.86),
         [[("→", 18, True, LGRAY, BODY)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.94)

# ══════════════ 3 · 开场问句 ══════════════
s = slide()
head(s, "开场 · 一句话", "你第一句话，说什么？", 3, tsize=34)
text(s, M, Inches(1.80), Inches(11.8), Inches(3.4),
     [[("朋友抬起头，问你一句：", 26, False, GRAY, BODY)],
      [("「你在做安利啊？」", 50, True, BLACK, BODY)],
      [("第一反应如果是解释——", 26, False, GRAY, BODY)],
      [("先解释，就输了。", 54, True, PINK, BODY)]], spacing=1.15, space_after=6)
rect(s, M, Inches(5.42), CW, Inches(1.15), fill=BLACK)
text(s, M + Inches(0.34), Inches(5.42), CW - Inches(0.68), Inches(1.15),
     [[("他真正想问的不是「你是不是拉人」，", 20, True, WHITE, BODY)],
      [("是「这生意到底长什么样」。", 20, True, YELLOW, BODY)]],
     anchor=MSO_ANCHOR.MIDDLE, spacing=1.35)

# ══════════════ 4 · 三种错法 ══════════════
s = slide()
head(s, "第一部分 · 先破误解", "三种最常见的错法", 4, tsize=36)
rows = [("01", "先撇清：我不是拉人，我不卖东西",
         "一开口就把自己放在被审判的位置，后面每句都在自证"),
        ("02", "先讲制度：我们几级几级，做到什么级别多少钱",
         "他连「你在干嘛」都没搞清楚，你已经在讲钱"),
        ("03", "先讲产品：这个营养素怎么怎么好",
         "他心里只剩一句：哦，你就是来卖货的")]
y = Inches(1.92)
for num, hd, body in rows:
    rect(s, M, y, CW, Inches(1.22), fill=CARD, line=HAIR, lw=1)
    rect(s, M, y, Inches(0.10), Inches(1.22), fill=RED)
    text(s, M + Inches(0.34), y + Inches(0.16), Inches(0.7), Inches(0.42),
         [[(num, 18, True, RED, NUM)]])
    text(s, M + Inches(0.90), y + Inches(0.16), Inches(10.9), Inches(0.5),
         [[(hd, 19, True, BLACK, BODY)]])
    text(s, M + Inches(0.90), y + Inches(0.70), Inches(10.9), Inches(0.42),
         [[(body, 14, False, GRAY, BODY)]])
    y += Inches(1.34)
band(s, "三种错法，错在同一个地方：跳过了「你是什么人」。", Inches(5.98), h=0.72, size=18)

# ══════════════ 5 · 他以为 vs 真实 ══════════════
s = slide()
head(s, "第一部分 · 画面差在哪", "他以为的，和你正在做的", 5, tsize=36)
pairs = [("他 以 为 的", ["拉人", "卖货", "找亲戚"], "所以他一张嘴就是防你", RED, CREAM),
         ("真 实 的", ["解决问题", "两条线同时走", "一个团队"], "所以他听完会说：原来是这么回事", GREEN, CARD)]
for i, (hd, words, foot, col, bgc) in enumerate(pairs):
    x = M + Inches(i * 6.22)
    rect(s, x, Inches(1.95), Inches(5.92), Inches(3.30), fill=bgc, line=HAIR, lw=1)
    rect(s, x, Inches(1.95), Inches(5.92), Inches(0.14), fill=col)
    text(s, x + Inches(0.32), Inches(2.28), Inches(5.2), Inches(0.5), [[(hd, 20, True, col, BODY)]])
    paras = [[("· ", 20, True, col, BODY), (w_, 24, True, BLACK, BODY)] for w_ in words]
    text(s, x + Inches(0.32), Inches(3.00), Inches(5.3), Inches(1.7), paras, spacing=1.5, space_after=8)
    text(s, x + Inches(0.32), Inches(4.62), Inches(5.3), Inches(0.5), [[(foot, 13, False, GRAY, BODY)]])
band(s, "他不是不信你，是不信这生意长什么样。", Inches(5.58), h=0.78, size=20)

# ══════════════ 6 · 两条线结构 ══════════════
s = slide()
head(s, "第一部分 · 真实结构", "这生意，就两条线", 6, tsize=38)
boxes = [("第一条线", "找 顾 客", ["学：基础营养 → 临床营养 → 考证",
                              "讲：朋友圈 · 社群 · 讲座 · 聚会",
                              "方案：一对一营养方案",
                              "陪跑：陪他落地，改生活方式"], CYAN),
         ("第二条线", "找 伙 伴", ["分享：为什么创业 · 为什么这个平台",
                              "吸引：他看到你在变好，来了解",
                              "兼职：他也学、也找顾客",
                              "复制：他也找伙伴，市场才长大"], YELLOW)]
for i, (tag, hd, lines, col) in enumerate(boxes):
    x = M + Inches(i * 6.22)
    rect(s, x, Inches(1.88), Inches(5.92), Inches(2.62), fill=col)
    text(s, x + Inches(0.30), Inches(2.02), Inches(5.2), Inches(0.3), [[(tag, 12, True, BLACK, BODY)]])
    text(s, x + Inches(0.30), Inches(2.32), Inches(5.2), Inches(0.52), [[(hd, 26, True, BLACK, BODY)]])
    paras = [[(t, 12, False, INK, BODY)] for t in lines]
    text(s, x + Inches(0.30), Inches(2.92), Inches(5.3), Inches(1.5), paras, spacing=1.5, space_after=3)
rect(s, Inches(3.60), Inches(4.50), Pt(5), Inches(0.28), fill=BLACK)
rect(s, Inches(9.80), Inches(4.50), Pt(5), Inches(0.28), fill=BLACK)
rect(s, Inches(3.63), Inches(4.76), Inches(6.20), Pt(5), fill=BLACK)
rect(s, Inches(6.70), Inches(4.76), Pt(5), Inches(0.30), fill=BLACK)
rect(s, Inches(2.90), Inches(5.06), Inches(7.55), Inches(0.82), fill=BLACK)
text(s, Inches(2.90), Inches(5.06), Inches(7.55), Inches(0.82),
     [[("同一个动作，两面：健康 ＋ 机会", 22, True, WHITE, BODY)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
band(s, "一边解决人需要健康，一边解决人需要机会。", Inches(6.10), h=0.68, fill=PINK, size=17)

# ══════════════ 7 · 两条线各自的四步 ══════════════
s = slide()
head(s, "第一部分 · 拆开看", "左边找顾客，右边找伙伴", 7, tsize=34)
cols = [("找顾客 · 解决问题", ["学：基础营养 → 临床营养 → 考证",
                        "讲：朋友圈 · 社群 · 讲座 · 家庭聚会",
                        "方案：一对一营养方案",
                        "陪跑：陪他落地，改生活方式"], CYAN),
        ("找伙伴 · 给机会", ["分享：为什么创业 · 为什么这个平台",
                        "吸引：他看到你在变好，来了解",
                        "兼职：他也学专业、也找顾客",
                        "复制：他也找伙伴，市场才长大"], YELLOW)]
for i, (hd, lines, col) in enumerate(cols):
    x = M + Inches(i * 6.22)
    rect(s, x, Inches(1.86), Inches(5.92), Inches(0.56), fill=col)
    text(s, x + Inches(0.24), Inches(1.86), Inches(5.4), Inches(0.56),
         [[(hd, 17, True, BLACK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    y = Inches(2.56)
    for j, ln in enumerate(lines):
        rect(s, x, y, Inches(5.92), Inches(0.84), fill=CREAM if j % 2 == 0 else None)
        text(s, x + Inches(0.20), y, Inches(0.55), Inches(0.84),
             [[("%d" % (j + 1), 17, True, PINK, NUM)]], anchor=MSO_ANCHOR.MIDDLE)
        text(s, x + Inches(0.78), y, Inches(5.0), Inches(0.84),
             [[(ln, 13, False, INK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
        y += Inches(0.88)
band(s, "方案 ＋ 陪跑，才叫服务；团队是陪出来的，不是管出来的。", Inches(6.14), h=0.66, size=15)

# ══════════════ 8 · 两句关键 ══════════════
s = slide()
head(s, "第一部分 · 记住两句", "这两句话，决定别人信不信你", 8, tsize=32)
text(s, M, Inches(1.98), Inches(12.0), Inches(1.0),
     [[("方案 ＋ 陪跑，才叫服务。", 42, True, PINK, BODY)]])
text(s, M, Inches(3.02), Inches(12.0), Inches(1.0),
     [[("团队是陪出来的，不是管出来的。", 40, True, BLACK, BODY)]])
rect(s, M, Inches(4.18), Inches(2.2), Inches(0.06), fill=HAIR)
text(s, M, Inches(4.40), Inches(11.6), Inches(1.3),
     [[("卖货 = 一锤子买卖，他下次不来了。", 17, False, GRAY, BODY)],
      [("方案 + 陪跑 = 他真的变了，他会带人来。", 17, False, GRAY, BODY)]], spacing=1.5)
band(s, "专业让人信你一次，陪跑让人留下来。", Inches(5.72), h=0.72, size=18)

# ══════════════ 9 · 五段总览 ══════════════
s = slide()
head(s, "第二部分 · 核心", "五段话，任何场合都能讲", 9, tsize=34)
five = [("01", "你为什么走到这儿", "不是干不下去才走，是想清楚了才走"),
        ("02", "你为什么走进大健康", "先被改变，再做买卖"),
        ("03", "这生意怎么做", "两条线，用你自己的话说"),
        ("04", "为什么是这个", "两个刚需 ＋ 亏得起"),
        ("05", "我可以教你", "自媒体不改变逻辑，只放大半径")]
y = Inches(1.88)
for i, (num, hd, sub) in enumerate(five):
    rect(s, M, y, CW, Inches(0.78), fill=CREAM if i % 2 == 0 else None)
    text(s, M + Inches(0.24), y, Inches(0.8), Inches(0.78),
         [[(num, 18, True, PINK, NUM)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(1.10), y, Inches(3.9), Inches(0.78),
         [[(hd, 19, True, BLACK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(5.20), y, Inches(6.6), Inches(0.78),
         [[(sub, 14, False, GRAY, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.86)
band(s, "顺序不能乱：从「我」讲到「你」，最后才讲机会。", Inches(6.24), h=0.62, size=16)

# ══════════════ 10 · 第一段 · 三卡 ══════════════
s = slide()
head(s, "第三部分 · 第一段", "我不是干不下去了才走", 10, tsize=34)
cards = [("第三年", "想清楚一件事", "十年后的生活，跟今天\n不会有太大变化", PINK),
         ("七年", "一直在找路", "做了很多行业\n也开过店", YELLOW),
         ("2020", "全职转身", "不是逃，是提前\n想清楚要什么", CYAN)]
for i, (big, hd, body, col) in enumerate(cards):
    x = M + Inches(i * 4.06)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(3.25), fill=CARD, line=HAIR, lw=1)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(0.58), fill=col)
    text(s, x + Inches(0.24), Inches(1.95), Inches(3.4), Inches(0.58),
         [[(big, 15, True, BLACK, NUM)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.24), Inches(2.72), Inches(3.4), Inches(0.55),
         [[(hd, 21, True, INK, BODY)]])
    rect(s, x + Inches(0.24), Inches(3.42), Inches(0.9), Inches(0.05), fill=col)
    text(s, x + Inches(0.24), Inches(3.66), Inches(3.38), Inches(1.3),
         [[(ln, 14, False, GRAY, BODY)] for ln in body.split("\n")], spacing=1.5)
band(s, "讲「我想要什么」，不要讲「那里有多糟」。", Inches(5.52), h=0.72, size=17)
note(s, "※ 个人经历分享；不评价任何机构与职业。", top=Inches(6.40))

# ══════════════ 11 · 第二段 · 三步 ══════════════
s = slide()
head(s, "第三部分 · 第二段", "先被改变，再做买卖", 11, tsize=36)
steps = [("第一步", "身体先出问题", "想去考营养师证\n跟着老师从零学", PINK),
         ("第二步", "学进去才看见", "医院治的是结果\n营养管的是前端", YELLOW),
         ("第三步", "自己先受益", "鼻炎慢慢好了\n免疫力也上来了", CYAN)]
for i, (tag, hd, body, col) in enumerate(steps):
    x = M + Inches(i * 4.06)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(3.25), fill=CARD, line=HAIR, lw=1)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(0.58), fill=col)
    text(s, x + Inches(0.24), Inches(1.95), Inches(3.4), Inches(0.58),
         [[(tag, 14, True, BLACK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.24), Inches(2.72), Inches(3.4), Inches(0.55),
         [[(hd, 21, True, INK, BODY)]])
    rect(s, x + Inches(0.24), Inches(3.42), Inches(0.9), Inches(0.05), fill=col)
    text(s, x + Inches(0.24), Inches(3.66), Inches(3.38), Inches(1.3),
         [[(ln, 14, False, GRAY, BODY)] for ln in body.split("\n")], spacing=1.5)
band(s, "这一段最抗质疑 —— 因为它是体感，不是案例。", Inches(5.52), h=0.72, size=17)
note(s, "※ 个人体感分享，不构成诊疗建议；个体情况请咨询专业医师。", top=Inches(6.40))

# ══════════════ 12 · 反色金句 ══════════════
s = slide(BLACK)
text(s, M, Inches(0.40), Inches(6.0), Inches(0.34),
     [[("第三部分 · 一句我心里的话", 13, True, YELLOW, BODY)]])
text(s, M, Inches(1.42), Inches(11.9), Inches(3.2),
     [[("医院治的，", 40, True, WHITE, BODY)],
      [("是已经病了的那个结果。", 40, True, WHITE, BODY)],
      [("营养管的，", 40, True, YELLOW, BODY)],
      [("是还没病的那段生活。", 40, True, YELLOW, BODY)]], spacing=1.2)
rect(s, M, Inches(4.86), Inches(2.2), Inches(0.09), fill=PINK)
text(s, M, Inches(5.18), Inches(11.6), Inches(1.4),
     [[("所以我从「救火」的位置，走到「防火」的位置。", 21, False, WHITE, BODY)]],
     spacing=1.4)
text(s, M, Inches(6.78), Inches(11.6), Inches(0.34),
     [[("—— 一个做过十年麻醉的医生", 12, False, RGBColor(0x8C, 0x86, 0x7E), BODY)]])
pageno(s, 12, RGBColor(0x7A, 0x74, 0x6C))

# ══════════════ 13 · 第四段 · 三卡 ══════════════
s = slide()
head(s, "第三部分 · 第四段", "为什么是这个：三个理由", 13, tsize=36)
cards = [("健 康", "人人需要", "抓的是慢病最前面的\n那段生活方式", PINK),
         ("机 会", "人人需要", "裁员、焦虑的人\n缺一个不压本钱的入口", CYAN),
         ("门 槛", "亏得起", "做错了亏不到本金\n比「赚得多」更重要", YELLOW)]
for i, (tag, hd, body, col) in enumerate(cards):
    x = M + Inches(i * 4.06)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(3.25), fill=col)
    text(s, x + Inches(0.26), Inches(2.14), Inches(3.3), Inches(0.4),
         [[(tag, 14, True, BLACK, BODY)]])
    text(s, x + Inches(0.26), Inches(2.55), Inches(3.3), Inches(0.62),
         [[(hd, 26, True, BLACK, BODY)]])
    rect(s, x + Inches(0.26), Inches(3.32), Inches(0.9), Inches(0.05), fill=BLACK)
    text(s, x + Inches(0.26), Inches(3.56), Inches(3.3), Inches(1.3),
         [[(ln, 14, True, INK, BODY)] for ln in body.split("\n")], spacing=1.5)
band(s, "三个理由讲完，他自己会算这笔账。", Inches(5.52), h=0.72, size=18)

# ══════════════ 14 · 路径 vs 结果 ══════════════
s = slide()
head(s, "第三部分 · 制度怎么讲", "讲路径，不讲结果", 14, tsize=36)
pairs = [("讲 路 径", ["第一年，做一个市场", "第三年，做三个市场", "三个市场做稳，进到制度里的高阶"],
          "这是制度算出来的路", GREEN, CARD),
         ("讲 结 果", ["你三年也能年薪百万", "保证你做到", "做不到退钱"],
          "这是自己挖的坑", RED, CREAM)]
for i, (hd, lines, foot, col, bgc) in enumerate(pairs):
    x = M + Inches(i * 6.22)
    rect(s, x, Inches(1.95), Inches(5.92), Inches(3.20), fill=bgc, line=HAIR, lw=1)
    rect(s, x, Inches(1.95), Inches(5.92), Inches(0.14), fill=col)
    text(s, x + Inches(0.32), Inches(2.26), Inches(5.2), Inches(0.5),
         [[(hd, 22, True, col, BODY)]])
    paras = [[("· ", 16, True, col, BODY), (t, 15, False, INK, BODY)] for t in lines]
    text(s, x + Inches(0.32), Inches(2.94), Inches(5.3), Inches(1.6),
         paras, spacing=1.55, space_after=6)
    text(s, x + Inches(0.32), Inches(4.60), Inches(5.3), Inches(0.4),
         [[(foot, 13, True, GRAY, BODY)]])
band(s, "路径是制度算出来的，结果是市场跑出来的。", Inches(5.52), h=0.72, size=18)
note(s, "※ 同一套制度，人是变量：师傅领进门，修行靠个人。", top=Inches(6.40))

# ══════════════ 15 · 六步 ══════════════
s = slide()
head(s, "第三部分 · 第五段", "我能教你的，是一条路径", 15, tsize=34)
six = [("01", "定位", "先商业定位\n再个人 IP 定位"),
       ("02", "借 AI 出内容", "找选题 · 写文案"),
       ("03", "写成脚本", "能开口讲的口播稿"),
       ("04", "录口播", "拿稿子去表达"),
       ("05", "剪辑", "一条一条磨"),
       ("06", "发布", "让更多人看见")]
for i, (num, hd, body) in enumerate(six):
    col_i, row_i = i % 2, i // 2
    x = M + Inches(col_i * 6.13)
    y = Inches(1.92 + row_i * 1.22)
    rect(s, x, y, Inches(5.72), Inches(1.06), fill=CREAM)
    num_box(s, x + Inches(0.18), y + Inches(0.22), Inches(0.60), Inches(0.60), num,
            PINK if col_i == 0 else YELLOW, 18)
    text(s, x + Inches(0.96), y + Inches(0.14), Inches(4.6), Inches(0.42),
         [[(hd, 18, True, BLACK, BODY)]])
    text(s, x + Inches(0.96), y + Inches(0.58), Inches(4.6), Inches(0.42),
         [[(ln, 13, False, GRAY, BODY)] for ln in body.split("\n")])
band(s, "收口一句：我就是线上做起来的。", Inches(5.62), h=0.72, fill=PINK, size=18)

# ══════════════ 16 · 三个必答题 ══════════════
s = slide()
head(s, "第四部分 · 他一定会问", "三个问题，提前准备好", 16, tsize=36)
qa = [("你现在收入多少？",
       "个人隐私，不细说。能告诉你的是：2020 全职、六年、比医院好，正在往年薪百万这个目标靠近。"),
      ("你这个职位、身份怎么样？",
       "别拿我当标准。有人做到百万，也有人十年原地踏步；可以超越，但不会自动到手。"),
      ("我该跟谁学？",
       "找一个能一对一带你走完前几步的人，跟一个团队走；我们主线线上，没成本，可以先试。")]
y = Inches(1.86)
for q, a in qa:
    rect(s, M, y, CW, Inches(1.32), fill=CARD, line=HAIR, lw=1)
    rect(s, M, y, Inches(0.10), Inches(1.32), fill=PINK)
    text(s, M + Inches(0.34), y + Inches(0.14), Inches(11.2), Inches(0.40),
         [[("问｜", 14, True, PINK, BODY), (q, 19, True, BLACK, BODY)]])
    text(s, M + Inches(0.34), y + Inches(0.66), Inches(11.3), Inches(0.55),
         [[("答｜", 14, True, GRAY, BODY), (a, 13, False, GRAY, BODY)]])
    y += Inches(1.44)
band(s, "三个答法一个共同点：不承诺、不神化、不推。", Inches(6.16), h=0.66, size=16)

# ══════════════ 17 · 三个坑 ══════════════
s = slide()
head(s, "第四部分 · 三个坑", "踩一个，前面讲的都白讲", 17, tsize=34)
rows = [("01", "一上来讲奖金", "他还没信「健康是真的」，你已经在讲「钱是真的」"),
        ("02", "把营养讲成治病", "一句「能治」，就把专业变成了风险"),
        ("03", "讲成「你来跟我干」", "他问，你才答；他不问，你不追")]
y = Inches(1.95)
for num, hd, body in rows:
    rect(s, M, y, CW, Inches(1.24), fill=CARD, line=HAIR, lw=1)
    rect(s, M, y, Inches(0.10), Inches(1.24), fill=RED)
    text(s, M + Inches(0.34), y + Inches(0.16), Inches(0.7), Inches(0.42),
         [[(num, 18, True, RED, NUM)]])
    text(s, M + Inches(0.92), y + Inches(0.16), Inches(3.7), Inches(0.9),
         [[(hd, 20, True, BLACK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(4.80), y, Inches(7.0), Inches(1.24),
         [[(body, 15, False, INK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(1.36)
band(s, "顺序错了，后面全在解释。", Inches(6.02), h=0.70, fill=BLACK, size=18)

# ══════════════ 18 · 玫红金句 ══════════════
s = slide(PINK)
text(s, M, Inches(0.40), Inches(6.0), Inches(0.34),
     [[("第四部分 · 一句清醒的话", 13, True, BLACK, BODY)]])
text(s, M, Inches(1.55), Inches(11.9), Inches(2.4),
     [[("顺序一颠倒，", 46, True, WHITE, BODY)],
      [("后面全在解释。", 54, True, BLACK, BODY)]], spacing=1.36)
rect(s, M, Inches(4.05), Inches(2.2), Inches(0.09), fill=BLACK)
text(s, M, Inches(4.40), Inches(11.4), Inches(1.6),
     [[("先讲「我的故事」 → 再讲「路径」 → 最后才讲「机会」", 22, True, BLACK, BODY)]])
text(s, M, Inches(5.10), Inches(11.4), Inches(1.2),
     [[("他不是不想做，是还没看清你这条路走不走得通。", 18, False, WHITE, BODY)],
      [("把画面给他，他自己会算。", 18, False, WHITE, BODY)]], spacing=1.5)
text(s, M, Inches(6.85), Inches(11.4), Inches(0.34),
     [[("这一句，比任何话术都管用", 12, False, RGBColor(0xFF, 0xD9, 0xE8), BODY)]])
pageno(s, 18, RGBColor(0xFF, 0xD9, 0xE8))

# ══════════════ 19 · 课后动作 ══════════════
s = slide()
head(s, "课后 · 今天就做", "把五段话，变成你自己的", 19, tsize=34)
steps = [("第一步", "各写三句", "五段 × 三句\n先写出来，别求好", PINK),
         ("第二步", "对着镜子讲", "不许看稿\n讲三遍，讲到顺", YELLOW),
         ("第三步", "录一条发我", "一分钟版本\n我帮你看哪里像背的", CYAN)]
for i, (tag, hd, body, col) in enumerate(steps):
    x = M + Inches(i * 4.06)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(3.25), fill=CARD, line=HAIR, lw=1)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(0.58), fill=col)
    text(s, x + Inches(0.24), Inches(1.95), Inches(3.4), Inches(0.58),
         [[(tag, 14, True, BLACK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.24), Inches(2.72), Inches(3.4), Inches(0.55),
         [[(hd, 22, True, INK, BODY)]])
    rect(s, x + Inches(0.24), Inches(3.40), Inches(0.9), Inches(0.05), fill=col)
    text(s, x + Inches(0.24), Inches(3.64), Inches(3.38), Inches(1.3),
         [[(ln, 14, False, GRAY, BODY)] for ln in body.split("\n")], spacing=1.5)
band(s, "讲得出来，才是真的开始。", Inches(5.52), h=0.72, fill=PINK, size=19)

# ══════════════ 20 · 结尾 ══════════════
s = slide(BLACK)
text(s, M, Inches(0.45), Inches(6.0), Inches(0.34), [[("结 语", 13, True, PINK, BODY)]])
text(s, M, Inches(1.30), Inches(11.9), Inches(1.9),
     [[("他不是不信你，", 34, True, WHITE, BODY)],
      [("是不信这生意长什么样。", 34, True, YELLOW, BODY)]], spacing=1.4)
rect(s, M, Inches(3.06), Inches(2.2), Inches(0.09), fill=PINK)
text(s, M, Inches(3.38), Inches(11.6), Inches(1.0),
     [[("先给画面，再给结论。", 20, True, WHITE, BODY)],
      [("我的故事 → 路径 → 机会：这个顺序，别改。", 20, False, WHITE, BODY)]],
     spacing=1.55)
rect(s, M, Inches(4.78), CW, Inches(0.80), fill=PINK)
text(s, M + Inches(0.28), Inches(4.78), CW - Inches(0.56), Inches(0.80),
     [[("今晚八点前，把你的五段话发我，我一条条给你改。", 18, True, WHITE, BODY)]],
     anchor=MSO_ANCHOR.MIDDLE)
note(s, "以上为个人经历与制度路径分享，不构成收入承诺或诊疗建议；个体情况请咨询专业人士。",
     top=Inches(6.30), color=RGBColor(0x8C, 0x86, 0x7E), size=11)

out = "朋友问你在做安利啊怎么答-2026-11-02-26-24期.pptx"
save(out)

# ── 边界自检 ──
bad = []
for i, sl in enumerate(D.prs.slides, 1):
    for sh in sl.shapes:
        try:
            l, t, w_, h_ = sh.left, sh.top, sh.width, sh.height
        except Exception:
            continue
        if l is None:
            continue
        if l < 0 or t < 0 or l + w_ > W or t + h_ > H:
            bad.append((i, sh.shape_type, round(l / 914400, 2), round(t / 914400, 2),
                        round((l + w_) / 914400, 2), round((t + h_) / 914400, 2)))
print("slides:", len(D.prs.slides), "| overflow:", len(bad))
for b in bad:
    print("  !", b)
