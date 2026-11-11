#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周二故事分享 26-23期《AI大健康赛道副业怎么做？》— Yellow × Black Editorial
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


def slide(bg=YELLOW):
    s = prs.slides.add_slide(BLANK)
    f = s.background.fill
    f.solid()
    f.fore_color.rgb = bg
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


def eyebrow(s, label, num=None, color=BLACK, muted=GRAY):
    rect(s, M, Inches(0.5), Inches(0.16), Inches(0.34), fill=color)
    text(s, M + Inches(0.34), Inches(0.48), Inches(7.6), Inches(0.4),
         [[(label, 12, True, color, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
    if num is not None:
        text(s, W - M - Inches(1.4), Inches(0.48), Inches(1.4), Inches(0.4),
             [[(num, 12, True, muted, SANS)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def title(s, txt, size=38, top=Inches(1.16), color=INK, rule=BLACK):
    text(s, M, top, CW, Inches(1.05), [[(txt, size, True, color, SERIF)]], spacing=1.02)
    rect(s, M, top + Inches(0.9), Inches(1.7), Pt(5), fill=rule)


def footer(s, txt, fill=BLACK, color=YELLOW, size=16, top=Inches(6.05)):
    rect(s, M, top, CW, Inches(0.8), fill=fill)
    text(s, M + Inches(0.24), top, CW - Inches(0.48), Inches(0.8),
         [[(txt, size, True, color, SANS)]], anchor=MSO_ANCHOR.MIDDLE)


def source(s, txt, top=Inches(6.78), color=GRAY):
    text(s, M, top, CW, Inches(0.34), [[(txt, 11, False, color, SANS)]])


# ══════════════ 1 · 封面 ══════════════
s = slide()
rect(s, 0, 0, W, Inches(0.42), fill=BLACK)
text(s, M, Inches(0.02), CW, Inches(0.4), [[("每周二 · 健康故事分享", 12, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, W - M - Inches(3.0), Inches(0.02), Inches(3.0), Inches(0.4),
     [[("26-23 期", 12, True, YELLOW, SANS)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

text(s, M, Inches(1.28), CW, Inches(0.46), [[("健康故事系列 · 从手术室到餐桌", 15, True, GRAY, SANS)]])
text(s, M, Inches(1.80), Inches(12.0), Inches(2.2),
     [[("AI 大健康赛道", 62, True, BLACK, SERIF)], [("副 业 怎 么 做", 56, True, BLACK, SERIF)]], spacing=1.06)
rect(s, M, Inches(4.34), Inches(2.6), Pt(7), fill=BLACK)
text(s, M, Inches(4.66), Inches(10.8), Inches(0.7),
     [[("一个麻醉医生的十年答卷", 34, True, BLACK, SERIF)]])
text(s, M, Inches(5.52), Inches(10.8), Inches(0.5),
     [[("手术室里近十年，我为什么走到了餐桌上", 18, False, INK, SANS)]])
rect(s, M, Inches(6.18), Inches(4.6), Inches(0.62), fill=BLACK)
text(s, M + Inches(0.22), Inches(6.18), Inches(4.4), Inches(0.62),
     [[("主讲 · 本群主理人 张医生", 16, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, M + Inches(4.95), Inches(6.18), Inches(4.0), Inches(0.62),
     [[("今晚 20:00 · 社群开讲", 13, False, GRAY, SANS)]], anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 2 · 目录 ══════════════
s = slide()
eyebrow(s, "目 录", "02")
title(s, "今天讲五件事")
items = [("01", "我是谁：手术室、奶茶店、大健康"),
         ("02", "我怎么看：这个行业的核心在慢病"),
         ("03", "怎么做：专业 + 传播，两条腿"),
         ("04", "AI 干什么：把两条腿接到一个人身上"),
         ("05", "为什么是我们：四个「已经」")]
y = Inches(2.72)
for num, txt in items:
    rect(s, M, y, Inches(0.62), Inches(0.62), fill=BLACK)
    text(s, M, y, Inches(0.62), Inches(0.62), [[(num, 20, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(0.95), y, Inches(10.4), Inches(0.62), [[(txt, 23, True, INK, SERIF)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.78)

# ══════════════ 3 · 开场问题 ══════════════
s = slide()
eyebrow(s, "开场 · 一个问题", "03")
text(s, M, Inches(1.62), Inches(7.9), Inches(0.5), [[("我用了整整十年，才想明白这个问题", 20, True, GRAY, SANS)]])
text(s, M, Inches(2.42), Inches(7.9), Inches(3.4),
     [[("健康这个行业，", 26, False, INK, SANS)],
      [("普通人", 74, True, BLACK, SERIF)],
      [("还有没有位置？", 60, True, BLACK, SERIF)]], spacing=1.12)
rect(s, M + Inches(7.95), Inches(2.30), Inches(3.68), Inches(2.95), fill=BLACK)
text(s, M + Inches(8.22), Inches(2.62), Inches(3.22), Inches(2.4),
     [[("「大公司、大专家的事，", 19, True, YELLOW, SERIF)],
      [("跟我有什么关系？」", 19, True, YELLOW, SERIF)],
      [("—— 我听过最多的一句话", 13, False, RGBColor(0x9A, 0x9A, 0x9A), SANS)]], spacing=1.5)
footer(s, "今晚，我用自己走过的十年，回答这一句。", size=18, top=Inches(6.02))

# ══════════════ 4 · 时间轴 ══════════════
s = slide()
eyebrow(s, "第一部分 · 我是谁", "04")
title(s, "我的十年，三步", size=36)
rect(s, M, Inches(3.86), CW, Pt(4), fill=BLACK)
stages = [
    ("01", "麻醉医生", "三甲医院 · 手术室近 10 年\n呼吸、心跳、血压，捏在手里"),
    ("02", "第一次创业", "开奶茶店 · 亏掉 30 多万\n交了最值的一笔学费"),
    ("03", "全职大健康", "2020 年转入 · 联盟核心专家组\n方案设计核心 · 带过上万学员"),
]
for i, (num, head, body) in enumerate(stages):
    x = M + Inches(i * 3.9)
    rect(s, x, Inches(3.68), Inches(0.30), Inches(0.30), fill=BLACK, shape=MSO_SHAPE.OVAL)
    text(s, x, Inches(2.60), Inches(3.2), Inches(0.7), [[(num, 40, True, YELLOW, LATIN)]])
    text(s, x, Inches(4.14), Inches(3.45), Inches(2.0),
         [[(head, 24, True, INK, SERIF)]] +
         [[(ln, 14, False, GRAY, SANS)] for ln in body.split("\n")], spacing=1.35, space_after=4)

# ══════════════ 5 · 转折（黑底） ══════════════
s = slide(BLACK)
text(s, M, Inches(0.55), CW, Inches(0.4), [[("第二部分 · 转折点", 12, True, YELLOW, SANS)]])
text(s, M, Inches(1.55), Inches(11.4), Inches(3.9),
     [[("医学的终点，", 54, True, WHITE, SERIF)],
      [("很多时候不在手术室，", 44, True, WHITE, SERIF)],
      [("在一个家庭过去二十年的饭桌上。", 44, True, YELLOW, SERIF)]], spacing=1.28)
rect(s, M, Inches(4.62), Inches(2.2), Pt(6), fill=RED)
text(s, M, Inches(4.95), Inches(11.2), Inches(1.4),
     [[("所以我决定：从「救火」的位置，", 22, False, WHITE, SANS)],
      [("走到「防火」的位置。", 22, True, WHITE, SANS)]], spacing=1.4)
text(s, M, Inches(6.55), CW, Inches(0.4),
     [[("—— 一个麻醉医生在手术室里的十年观察", 13, False, RGBColor(0x8A, 0x8A, 0x8A), SANS)]])

# ══════════════ 6 · 慢病 · 三个数字 ══════════════
s = slide()
eyebrow(s, "第三部分 · 我怎么看这个行业", "05")
title(s, "这个行业真正的核心，在慢病", size=36)
cols = [("3 亿+", "中国慢性病患者\n已经超过 3 亿人"),
        ("88.5%", "居民死亡原因里\n慢性病占 88.5%"),
        ("20%+", "60 岁以上人口接近 3 亿\n占比超过两成")]
for i, (big, label) in enumerate(cols):
    x = M + Inches(i * 3.9)
    rect(s, x, Inches(2.55), Inches(3.45), Inches(2.85), fill=None, line=BLACK, lw=3)
    text(s, x + Inches(0.28), Inches(2.78), Inches(2.9), Inches(1.0),
         [[(big, 52, True, BLACK, LATIN)]], spacing=1.0)
    text(s, x + Inches(0.28), Inches(3.85), Inches(2.95), Inches(1.3),
         [[(ln, 15, False, INK, SANS)] for ln in label.split("\n")], spacing=1.35, space_after=3)
footer(s, "不是「未来的市场」，是已经摆在桌面上、还在井喷式增长的现实。", size=15, top=Inches(5.82))
source(s, "数据来源：《中国居民营养与慢性病状况报告（2020年）》；国家统计局人口年龄结构数据")

# ══════════════ 7 · 60 / 17 / 15 / 8 ══════════════
s = slide()
eyebrow(s, "第三部分 · 慢病的源头", "06")
title(s, "慢病是怎么来的？不在医院", size=36)
rows = [("生活方式和行为", 60, BLACK), ("环境因素", 17, GRAY), ("遗传", 15, GRAY), ("医疗卫生服务", 8, RED)]
y = Inches(2.52)
for label, val, col in rows:
    text(s, M, y, Inches(2.55), Inches(0.5), [[(label, 18, True, INK, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
    bw = val / 60.0 * 6.1
    rect(s, M + Inches(2.75), y + Inches(0.10), Inches(max(bw, 0.16)), Inches(0.32), fill=col)
    text(s, M + Inches(2.75) + Inches(max(bw, 0.16)) + Inches(0.16), y, Inches(1.2), Inches(0.5),
         [[(str(val) + "%", 20, True, BLACK, LATIN)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.82)
footer(s, "生活方式占 60%，医疗只占 8%——战场根本不在医院。", size=17, top=Inches(5.86))
source(s, "归因来源：世界卫生组织（WHO）健康决定因素框架，健康管理领域通用表述")

# ══════════════ 8 · 医院 vs 家庭 ══════════════
s = slide()
eyebrow(s, "第三部分 · 观念转折", "07")
title(s, "医院治结果，家庭治源头", size=36)
rect(s, W / 2 - Inches(0.02), Inches(2.42), Pt(5), Inches(2.9), fill=BLACK)
text(s, M, Inches(2.45), Inches(4.9), Inches(0.6), [[("医 院", 30, True, GRAY, SERIF)]])
text(s, M, Inches(3.20), Inches(4.9), Inches(2.0),
     [[("压血压 · 降血糖 · 拦血脂", 18, False, INK, SANS)],
      [("管的是「结果」", 22, True, BLACK, SERIF)]], spacing=1.6)
text(s, W / 2 + Inches(0.55), Inches(2.45), Inches(4.9), Inches(0.6), [[("家 庭", 30, True, BLACK, SERIF)]])
text(s, W / 2 + Inches(0.55), Inches(3.20), Inches(4.9), Inches(2.0),
     [[("怎么吃 · 怎么动 · 怎么睡", 18, False, INK, SANS)],
      [("管的是「源头」", 22, True, BLACK, SERIF)]], spacing=1.6)
footer(s, "医院能救火，防火只能在自己家。", size=19, top=Inches(5.65))

# ══════════════ 9 · 价值锚 ══════════════
s = slide()
eyebrow(s, "第三部分 · 机会在哪", "08")
title(s, "行业真正的价值，落在这两件事", size=34)
boxes = [("①", "慢病整体解决方案", "成熟 · 专业 · 有效\n不是偏方，是被反复验证过的一套方案"),
         ("②", "家庭健康管理员", "把这套方案，复制到每一个家庭\n落在一日三餐，而不是 PPT 上")]
for i, (num, head, body) in enumerate(boxes):
    x = M + Inches(i * 5.95)
    rect(s, x, Inches(2.45), Inches(5.65), Inches(2.55), fill=None, line=BLACK, lw=3)
    text(s, x + Inches(0.28), Inches(2.62), Inches(0.8), Inches(0.8), [[(num, 32, True, BLACK, LATIN)]])
    text(s, x + Inches(0.28), Inches(3.16), Inches(5.0), Inches(0.6), [[(head, 27, True, BLACK, SERIF)]])
    text(s, x + Inches(0.28), Inches(3.82), Inches(5.1), Inches(1.0),
         [[(ln, 14, False, INK, SANS)] for ln in body.split("\n")], spacing=1.4, space_after=3)
footer(s, "方案 + 复制方案的人：医院做不了，大公司落不到餐桌。", size=15, top=Inches(5.62))

# ══════════════ 10 · 两条腿 ══════════════
s = slide()
eyebrow(s, "第四部分 · 怎么做", "09")
title(s, "普通人靠两条腿站住", size=36)
legs = [("第一条腿", "专 业", "成熟：被反复验证过\n专业：符合营养学原理\n有效：真的能看到变化"),
        ("第二条腿", "传 播", "不能再走老路：发传单、熟人一个个讲\n回到线上：短视频、社群、内容\n让更多人看见")]
for i, (tag, head, body) in enumerate(legs):
    x = M + Inches(i * 5.95)
    rect(s, x, Inches(2.40), Inches(5.65), Inches(3.05), fill=BLACK if i == 0 else None,
         line=None if i == 0 else BLACK, lw=3)
    c_head = YELLOW if i == 0 else BLACK
    c_body = WHITE if i == 0 else INK
    text(s, x + Inches(0.30), Inches(2.60), Inches(5.0), Inches(0.4), [[(tag, 13, True, YELLOW if i == 0 else GRAY, SANS)]])
    text(s, x + Inches(0.30), Inches(2.96), Inches(5.0), Inches(0.7), [[(head, 36, True, c_head, SERIF)]])
    text(s, x + Inches(0.30), Inches(3.85), Inches(5.05), Inches(1.4),
         [[(ln, 15, False, c_body, SANS)] for ln in body.split("\n")], spacing=1.5, space_after=2)
footer(s, "只有专业走不长，只有传播走不稳——缺一条都站不住。", size=15, top=Inches(5.78))

# ══════════════ 11 · 一条腿走不远 ══════════════
s = slide()
eyebrow(s, "第四部分 · 为什么必须两条", "10")
title(s, "只有一条腿，走不远", size=36)
rows2 = [("只有专业", "不会传播", "你再厉害，也只有身边那几个人知道 —— 被「人数」卡死"),
         ("只有传播", "没有专业", "你能火一阵子，但客户留不住 —— 被「信任」卡死")]
y = Inches(2.52)
for a, b, c in rows2:
    rect(s, M, y, CW, Inches(1.42), fill=None, line=BLACK, lw=3)
    text(s, M + Inches(0.32), y + Inches(0.18), Inches(2.4), Inches(0.6), [[(a, 24, True, BLACK, SERIF)]])
    text(s, M + Inches(0.32), y + Inches(0.82), Inches(2.4), Inches(0.45), [[(b, 17, True, RED, SANS)]])
    text(s, M + Inches(3.0), y, Inches(8.3), Inches(1.42), [[(c, 18, False, INK, SANS)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(1.62)
footer(s, "两条腿一起走，才叫事业。", size=20, top=Inches(5.95))

# ══════════════ 12 · 传播的证据 ══════════════
s = slide()
eyebrow(s, "第四部分 · 一个实证", "11")
title(s, "传播不是口号，是打出来的", size=34)
text(s, M, Inches(2.50), Inches(5.4), Inches(1.4), [[("2000", 108, True, BLACK, LATIN)]], spacing=0.95)
text(s, M + Inches(3.55), Inches(2.92), Inches(1.2), Inches(0.9), [[("+", 46, True, BLACK, LATIN)]])
text(s, M, Inches(3.86), Inches(5.2), Inches(1.1),
     [[("一期慢病管理实战班报名人数", 17, True, INK, SANS)],
      [("不是发传单来的，是靠内容、靠社群来的", 14, False, GRAY, SANS)]], spacing=1.4)
rect(s, M + Inches(5.95), Inches(2.50), Pt(4), Inches(2.6), fill=BLACK)
text(s, M + Inches(6.35), Inches(2.55), Inches(4.9), Inches(1.0), [[("4 × 500", 66, True, BLACK, LATIN)]])
text(s, M + Inches(6.35), Inches(3.86), Inches(4.9), Inches(1.1),
     [[("四个群，每个 500 人，全部满员", 17, True, INK, SANS)],
      [("线上传播跑通之后，规模是可以被复制的", 14, False, GRAY, SANS)]], spacing=1.4)
footer(s, "专业决定你能走多远，传播决定有多少人知道你。", size=16, top=Inches(5.6))

# ══════════════ 13 · AI 的角色 ══════════════
s = slide()
eyebrow(s, "第四部分 · AI 的角色", "12")
title(s, "AI 干的事：把两条腿接到一个人身上", size=32)
for i, (head, sub) in enumerate([("专 业", "营养学 · 慢病方案"), ("传 播", "内容 · 选题 · 脚本")]):
    x = M + Inches(i * 6.05)
    rect(s, x, Inches(2.35), Inches(4.55), Inches(1.25), fill=None, line=BLACK, lw=3)
    text(s, x + Inches(0.26), Inches(2.50), Inches(4.0), Inches(0.55), [[(head, 26, True, BLACK, SERIF)]])
    text(s, x + Inches(0.26), Inches(3.02), Inches(4.0), Inches(0.45), [[(sub, 14, False, GRAY, SANS)]])
rect(s, M + Inches(2.80), Inches(4.55), Inches(5.0), Inches(0.95), fill=BLACK)
text(s, M + Inches(2.80), Inches(4.55), Inches(5.0), Inches(0.95),
     [[("A I   +   知 识 库", 26, True, YELLOW, SANS)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
# 连接线：两个盒子 → 汇合 → AI
rect(s, M + Inches(2.26), Inches(3.62), Pt(4), Inches(0.34), fill=BLACK)   # 左竖线 x=3.11
rect(s, M + Inches(8.30), Inches(3.62), Pt(4), Inches(0.34), fill=BLACK)   # 右竖线 x=9.15
rect(s, M + Inches(2.28), Inches(3.94), Inches(6.90), Pt(4), fill=BLACK)   # 横线
rect(s, M + Inches(5.28), Inches(3.94), Pt(4), Inches(0.61), fill=BLACK)   # 中竖线 x=6.13
footer(s, "过去挡在普通人面前的两堵墙，现在变成了两扇门。", size=16, top=Inches(5.72))

# ══════════════ 14 · 过去 vs 现在 ══════════════
s = slide()
eyebrow(s, "第四部分 · 专业这条腿", "13")
title(s, "成为能接客户的营养专业人士", size=32)
text(s, M, Inches(2.30), Inches(5.5), Inches(0.4), [[("过 去", 15, True, GRAY, SANS)]])
text(s, M, Inches(2.72), Inches(5.5), Inches(1.1), [[("5 – 10 年", 56, True, GRAY, LATIN)]])
text(s, M, Inches(3.92), Inches(5.4), Inches(1.8),
     [[("学 · 考 · 在真实客户身上练", 16, False, INK, SANS)],
      [("练错了还得改 —— 没有捷径", 16, False, INK, SANS)]], spacing=1.45)
rect(s, W / 2 - Inches(0.02), Inches(2.28), Pt(4), Inches(3.2), fill=BLACK)
text(s, W / 2 + Inches(0.55), Inches(2.30), Inches(5.2), Inches(0.4), [[("现 在", 15, True, BLACK, SANS)]])
text(s, W / 2 + Inches(0.55), Inches(2.72), Inches(5.2), Inches(1.1), [[("一个知识库", 50, True, BLACK, SERIF)]])
text(s, W / 2 + Inches(0.55), Inches(3.92), Inches(5.2), Inches(1.8),
     [[("不用背下整本书，可以「调用」这本书", 16, False, INK, SANS)],
      [("起点不是「我什么都不懂」", 16, False, INK, SANS)],
      [("而是「我背后有一个专业的脑子」", 16, False, INK, SANS)]], spacing=1.45)
footer(s, "AI 是引擎，知识库是油。没有油，引擎再猛也跑不动。", size=16, top=Inches(5.85))

# ══════════════ 15 · 两个大脑 ══════════════
s = slide()
eyebrow(s, "第四部分 · 给每个人装两个大脑", "14")
title(s, "营养专业大脑 × 自媒体传播大脑", size=32)
brains = [("营养专业大脑", ["成体系的营养学", "慢病管理方案", "真实案例库", "常见问题的处理逻辑"], BLACK),
          ("自媒体传播大脑", ["各平台爆款方法", "选题逻辑", "脚本结构", "用户语言"], None)]
for i, (head, items_, fill) in enumerate(brains):
    x = M + Inches(i * 5.95)
    rect(s, x, Inches(2.40), Inches(5.65), Inches(3.15), fill=fill, line=None if fill else BLACK, lw=3)
    text(s, x + Inches(0.30), Inches(2.62), Inches(5.0), Inches(0.6),
         [[(head, 25, True, YELLOW if fill else BLACK, SERIF)]])
    paras = [[("■  ", 14, True, YELLOW if fill else BLACK, SANS), (t, 15, False, WHITE if fill else INK, SANS)]
             for t in items_]
    text(s, x + Inches(0.30), Inches(3.42), Inches(5.05), Inches(1.9), paras, spacing=1.35, space_after=8)
footer(s, "知识库比 AI 本身更重要 —— 它决定了这个脑子专不专业。", size=15, top=Inches(5.82))

# ══════════════ 16 · 清醒的话（黑底） ══════════════
s = slide(BLACK)
text(s, M, Inches(0.55), CW, Inches(0.4), [[("第四部分 · 一句清醒的话", 12, True, YELLOW, SANS)]])
text(s, M, Inches(1.62), Inches(11.4), Inches(3.3),
     [[("AI 不会让不专业的人变专业，", 40, True, WHITE, SERIF)],
      [("它只会让专业的人，快十倍。", 52, True, YELLOW, SERIF)]], spacing=1.35)
rect(s, M, Inches(4.30), Inches(2.2), Pt(6), fill=RED)
text(s, M, Inches(4.62), Inches(11.2), Inches(1.8),
     [[("AI 是放大器，不是替代品。", 22, False, WHITE, SANS)],
      [("你脑子里是空的，放大出来还是空的。", 22, False, WHITE, SANS)],
      [("所以顺序永远是：先建地基，再装引擎。", 22, True, WHITE, SANS)]], spacing=1.45)
text(s, M, Inches(6.62), CW, Inches(0.4),
     [[("这句话，比前面所有的话都重要", 13, False, RGBColor(0x8A, 0x8A, 0x8A), SANS)]])

# ══════════════ 17 · 四个已经 ══════════════
s = slide()
eyebrow(s, "第五部分 · 为什么是我们", "15")
title(s, "四个「已经」", size=38)
items = [("01", "专业已经验证", "方案是在真实顾客身上跑出来的，不是 PPT 上画出来的"),
         ("02", "传播已经验证", "一场实战班两千多人、四个五百人群满员"),
         ("03", "AI 应用已经验证", "不是在讲将来，是已经在用：知识库、工具、内容生产"),
         ("04", "可复制", "只有张医生一个人能用的东西，没有价值")]
y = Inches(2.35)
for num, head, body in items:
    rect(s, M, y, Inches(0.56), Inches(0.56), fill=BLACK)
    text(s, M, y, Inches(0.56), Inches(0.56), [[(num, 17, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(0.85), y - Inches(0.06), Inches(3.0), Inches(0.6), [[(head, 21, True, BLACK, SERIF)]])
    text(s, M + Inches(3.95), y - Inches(0.02), Inches(7.6), Inches(0.6), [[(body, 15, False, INK, SANS)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.92)
footer(s, "把一小部分人才能做的事，变成普通人也能做的事。", size=16, top=Inches(6.05))

# ══════════════ 18 · 三步走 ══════════════
s = slide()
eyebrow(s, "总结 · 怎么做", "16")
title(s, "所以，答案就三步", size=38)
steps = [("第一步", "选对地方", "有解决方案、有体系、有验证 —— 别自己从零摸索"),
         ("第二步", "打地基", "跟着体系学专业，别指望速成"),
         ("第三步", "装引擎", "用 AI 把专业变成内容，把内容变成客户，把客户变成口碑")]
y = Inches(2.42)
for tag, head, body in steps:
    rect(s, M, y, Inches(1.35), Inches(0.62), fill=BLACK)
    text(s, M, y, Inches(1.35), Inches(0.62), [[(tag, 14, True, YELLOW, SANS)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(1.62), y - Inches(0.04), Inches(2.4), Inches(0.62), [[(head, 24, True, BLACK, SERIF)]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(4.15), y, Inches(7.4), Inches(0.62), [[(body, 15, False, INK, SANS)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(1.02)
footer(s, "三步走完，你在这个行业里，就有自己的位置。", size=17, top=Inches(5.72))

# ══════════════ 19 · 行动号召 ══════════════
s = slide()
eyebrow(s, "结语", "17")
text(s, M, Inches(1.72), Inches(11.2), Inches(2.2),
     [[("机会在慢病，战场在家庭，", 34, True, BLACK, SERIF)],
      [("而这件事，只能由一个个普通人去做。", 34, True, BLACK, SERIF)]], spacing=1.3)
rect(s, M, Inches(3.92), Inches(2.2), Pt(6), fill=BLACK)
text(s, M, Inches(4.24), Inches(11.2), Inches(1.3),
     [[("我不承诺收入，也不保证结果 —— 这个行业里，跟你打包票的都要小心。", 17, False, INK, SANS)],
      [("我能说的是：这条路我自己走过，我们团队上万人走过，它是有路标的。", 17, True, BLACK, SANS)]],
     spacing=1.5)
rect(s, M, Inches(5.62), CW, Inches(0.78), fill=BLACK)
text(s, M + Inches(0.26), Inches(5.62), CW - Inches(0.52), Inches(0.78),
     [[("课后私信我，就聊你现在卡在哪 —— 聊什么都不卖。", 18, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
source(s, "以上为个人经历与行业观察分享，不构成任何收入承诺或诊疗建议，个体情况请咨询专业人士。",
       top=Inches(6.62))

prs.save("AI大健康赛道副业怎么做-26-23期.pptx")
print("saved:", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
