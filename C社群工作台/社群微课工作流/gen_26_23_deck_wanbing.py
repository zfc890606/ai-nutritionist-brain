#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周二故事分享 26-23期《AI大健康赛道副业怎么做？》— 万病寻源样板风格
米白纸感底 · 信息图色块 · 小标签+大标题 · 页脚编号
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

# ───────────── Palette（取自万病寻源样板） ─────────────
PAPER  = RGBColor(0xF5, 0xF0, 0xE8)
CREAM  = RGBColor(0xFA, 0xF6, 0xEF)
CARD   = RGBColor(0xFF, 0xFD, 0xF7)
PINK   = RGBColor(0xFF, 0x3A, 0x8D)
YELLOW = RGBColor(0xFF, 0xD4, 0x00)
CYAN   = RGBColor(0x00, 0xD4, 0xE6)
GREEN  = RGBColor(0x16, 0xA3, 0x4A)
RED    = RGBColor(0xDC, 0x26, 0x26)
BLACK  = RGBColor(0x12, 0x12, 0x12)
INK    = RGBColor(0x1A, 0x1A, 0x1A)
GRAY   = RGBColor(0x6B, 0x6B, 0x6B)
LGRAY  = RGBColor(0xA8, 0xA0, 0x94)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

BODY = "PingFang SC"
NUM  = "Helvetica Neue"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

M = Inches(0.6)
CW = W - 2 * M
TOTAL = 19


def _set_ea(run, typeface):
    rPr = run._r.get_or_add_rPr()
    for tag in ('a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is None:
            el = parse_xml('<%s xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="%s"/>' % (tag, typeface))
            rPr.append(el)
        else:
            el.set('typeface', typeface)


def slide(bg=PAPER):
    s = prs.slides.add_slide(BLANK)
    f = s.background.fill
    f.solid()
    f.fore_color.rgb = bg
    return s


def rect(s, l, t, w, h, fill=None, line=None, lw=1.5, shape=MSO_SHAPE.RECTANGLE):
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
         spacing=1.2, space_after=4):
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
            fname = r[4] if len(r) > 4 else BODY
            run = p.add_run()
            run.text = txt
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = color
            run.font.name = fname
            _set_ea(run, fname)
    return tb


def head(s, label, ttl, page, tsize=38, label_color=PINK, tcolor=INK):
    text(s, M, Inches(0.30), Inches(2.4), Inches(0.34),
         [[(label, 13, True, label_color, BODY)]], spacing=1.0)
    text(s, M, Inches(0.72), CW, Inches(0.95), [[(ttl, tsize, True, tcolor, BODY)]], spacing=1.06)
    pageno(s, page)


def pageno(s, page, color=LGRAY):
    text(s, Inches(11.9), Inches(7.02), Inches(1.3), Inches(0.3),
         [[("%d / %d" % (page, TOTAL), 10, False, color, BODY)]], align=PP_ALIGN.RIGHT)


def note(s, txt, top=Inches(6.62), color=GRAY, size=11):
    text(s, M, top, CW, Inches(0.32), [[(txt, size, False, color, BODY)]])


def band(s, txt, top, h=0.72, fill=BLACK, color=WHITE, size=20, left=None, width=None):
    left = M if left is None else left
    width = CW if width is None else width
    rect(s, left, top, width, h, fill=fill)
    text(s, left + Inches(0.26), top, width - Inches(0.52), h,
         [[(txt, size, True, color, BODY)]], anchor=MSO_ANCHOR.MIDDLE)


# ══════════════ 1 · 封面 ══════════════
s = slide()
rect(s, 0, 0, W, Inches(0.18), fill=PINK)
text(s, M, Inches(0.62), Inches(8.0), Inches(0.34),
     [[("HEALTH TALK  ·  每周二 · 26-23 期", 13, True, PINK, BODY)]])
text(s, M, Inches(1.20), Inches(9.2), Inches(2.4),
     [[("AI 大健康赛道", 54, True, BLACK, BODY)],
      [("副 业 怎 么 做", 54, True, BLACK, BODY)]], spacing=1.14)
rect(s, M, Inches(3.52), Inches(2.3), Inches(0.09), fill=PINK)
text(s, M, Inches(3.86), Inches(9.0), Inches(0.6),
     [[("一个麻醉医生的十年答卷", 30, True, INK, BODY)]])
text(s, M, Inches(4.58), Inches(9.0), Inches(0.5),
     [[("手术室里近十年，我为什么走到了餐桌上", 16, False, GRAY, BODY)]])

rect(s, Inches(10.55), Inches(0.95), Inches(2.20), Inches(2.20), fill=CYAN)
text(s, Inches(10.55), Inches(1.16), Inches(2.20), Inches(1.3),
     [[("10", 66, True, BLACK, NUM)]], align=PP_ALIGN.CENTER, spacing=0.95)
text(s, Inches(10.55), Inches(2.42), Inches(2.20), Inches(0.4),
     [[("年 · 手术室", 13, True, BLACK, BODY)]], align=PP_ALIGN.CENTER)

rect(s, 0, Inches(6.30), W, Inches(1.20), fill=BLACK)
text(s, M, Inches(6.30), Inches(6.4), Inches(1.20),
     [[("主讲 · 本群主理人 张医生", 18, True, WHITE, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, W - M - Inches(5.2), Inches(6.30), Inches(5.2), Inches(1.20),
     [[("今晚 20:00 · 社群开讲", 15, False, YELLOW, BODY)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 2 · 目录 ══════════════
s = slide()
head(s, "CONTENTS", "今天讲五件事", 2)
items = [("01", "我是谁：手术室、奶茶店、大健康"),
         ("02", "我怎么看：这个行业的核心在慢病"),
         ("03", "怎么做：专业 + 传播，两条腿"),
         ("04", "AI 干什么：把两条腿接到一个人身上"),
         ("05", "为什么是我们：四个「已经」")]
y = Inches(2.05)
for i, (num, ttl) in enumerate(items):
    rect(s, M, y, CW, Inches(0.82), fill=CREAM if i % 2 == 0 else None)
    text(s, M + Inches(0.26), y, Inches(0.9), Inches(0.82),
         [[(num, 22, True, PINK, NUM)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(1.20), y, Inches(9.9), Inches(0.82),
         [[(ttl, 22, True, INK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, W - M - Inches(0.6), y, Inches(0.6), Inches(0.82),
         [[("→", 18, True, LGRAY, BODY)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.90)

# ══════════════ 3 · 开场问句 ══════════════
s = slide()
head(s, "开场 · 一个问题", "我用了整整十年，才想明白这个问题", 3, tsize=26)
text(s, M, Inches(2.10), Inches(11.8), Inches(3.0),
     [[("健康这个行业，", 30, False, GRAY, BODY)],
      [("普通人", 74, True, PINK, BODY)],
      [("还有没有位置？", 62, True, BLACK, BODY)]], spacing=1.16)
rect(s, M, Inches(5.05), CW, Inches(1.15), fill=BLACK)
text(s, M + Inches(0.34), Inches(5.05), CW - Inches(0.68), Inches(1.15),
     [[("「大公司、大专家的事，跟我有什么关系？」", 22, True, WHITE, BODY)],
      [("—— 这是我听过最多的一句话", 13, False, RGBColor(0xB0, 0xA8, 0x9C), BODY)]],
     anchor=MSO_ANCHOR.MIDDLE, spacing=1.35)

# ══════════════ 4 · 时间轴 ══════════════
s = slide()
head(s, "第一部分 · 我是谁", "我的十年，三步", 4)
stages = [("01", "麻醉医生", PINK, "三甲医院 · 手术室近 10 年", "呼吸、心跳、血压，全捏在手里"),
          ("02", "第一次创业", YELLOW, "开奶茶店 · 亏掉 30 多万", "交过最值的一笔学费"),
          ("03", "全职大健康", CYAN, "2020 年转入 · 联盟核心专家组", "方案设计核心 · 带过上万学员")]
for i, (num, hd, col, l1, l2) in enumerate(stages):
    x = M + Inches(i * 4.06)
    rect(s, x, Inches(2.05), Inches(3.86), Inches(4.05), fill=CARD, line=RGBColor(0xE5, 0xDE, 0xD2), lw=1)
    rect(s, x, Inches(2.05), Inches(3.86), Inches(0.62), fill=col)
    text(s, x + Inches(0.24), Inches(2.05), Inches(3.4), Inches(0.62),
         [[(num, 16, True, BLACK, NUM)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.24), Inches(2.92), Inches(3.4), Inches(0.6),
         [[(hd, 24, True, INK, BODY)]])
    rect(s, x + Inches(0.24), Inches(3.62), Inches(0.9), Inches(0.05), fill=col)
    text(s, x + Inches(0.24), Inches(3.86), Inches(3.38), Inches(1.8),
         [[(l1, 15, True, INK, BODY)], [(l2, 14, False, GRAY, BODY)]], spacing=1.5, space_after=8)
note(s, "※ 前后算下来，我在大健康这个行业也走过了十年。", top=Inches(6.42))

# ══════════════ 5 · 金句（黑底） ══════════════
s = slide(BLACK)
text(s, M, Inches(0.40), Inches(4.0), Inches(0.34),
     [[("第二部分 · 转折点", 13, True, YELLOW, BODY)]])
text(s, M, Inches(1.55), Inches(11.9), Inches(4.0),
     [[("医学的终点，", 52, True, WHITE, BODY)],
      [("很多时候不在手术室，", 42, True, WHITE, BODY)],
      [("在一个家庭过去二十年的饭桌上。", 42, True, YELLOW, BODY)]], spacing=1.34)
rect(s, M, Inches(4.75), Inches(2.2), Inches(0.09), fill=PINK)
text(s, M, Inches(5.10), Inches(11.6), Inches(1.2),
     [[("所以我决定：从「救火」的位置，走到「防火」的位置。", 22, False, WHITE, BODY)]], spacing=1.4)
text(s, M, Inches(6.80), Inches(11.6), Inches(0.34),
     [[("—— 一个麻醉医生在手术室里的十年观察", 12, False, RGBColor(0x8C, 0x86, 0x7E), BODY)]])
pageno(s, 5, RGBColor(0x7A, 0x74, 0x6C))

# ══════════════ 6 · 三个数字 ══════════════
s = slide()
head(s, "第三部分 · 我怎么看这个行业", "这个行业真正的核心，在慢病", 6, tsize=36)
cols = [("3 亿+", "中国慢性病患者\n已超过 3 亿人", PINK, BLACK),
        ("88.5%", "居民死亡原因里\n慢性病占 88.5%", CYAN, BLACK),
        ("20%+", "60 岁以上人口近 3 亿\n占比超过两成", YELLOW, BLACK)]
for i, (big, label, col, tc) in enumerate(cols):
    x = M + Inches(i * 4.06)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(3.55), fill=col)
    text(s, x + Inches(0.28), Inches(2.25), Inches(3.3), Inches(1.0),
         [[(big, 50, True, tc, NUM)]], spacing=1.0)
    rect(s, x + Inches(0.28), Inches(3.35), Inches(1.0), Inches(0.05), fill=BLACK)
    text(s, x + Inches(0.28), Inches(3.62), Inches(3.30), Inches(1.6),
         [[(ln, 15, True, tc, BODY)] for ln in label.split("\n")], spacing=1.5, space_after=4)
band(s, "不是「未来的市场」，是已经摆在桌面上、还在井喷式增长的现实。", Inches(5.78), h=0.72, size=17)
note(s, "数据来源：《中国居民营养与慢性病状况报告（2020年）》；国家统计局人口年龄结构数据", top=Inches(6.70))

# ══════════════ 7 · 60/17/15/8 ══════════════
s = slide()
head(s, "第三部分 · 慢病的源头", "慢病是怎么来的？不在医院", 7, tsize=36)
rows = [("生活方式和行为", 60, BLACK), ("环境因素", 17, LGRAY), ("遗传", 15, LGRAY), ("医疗卫生服务", 8, RED)]
y = Inches(1.95)
for i, (label, val, col) in enumerate(rows):
    rect(s, M, y, CW, Inches(0.78), fill=CREAM if i % 2 == 0 else None)
    text(s, M + Inches(0.24), y, Inches(2.5), Inches(0.78),
         [[(label, 17, True, INK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    bw = val / 60.0 * 6.0
    rect(s, M + Inches(2.95), y + Inches(0.22), Inches(max(bw, 0.14)), Inches(0.34), fill=col)
    text(s, M + Inches(2.95) + Inches(max(bw, 0.14)) + Inches(0.18), y, Inches(1.2), Inches(0.78),
         [[(str(val) + "%", 20, True, BLACK, NUM)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.82)
band(s, "生活方式占 60%，医疗只占 8% —— 慢病的战场根本不在医院。", Inches(5.42), h=0.72, fill=YELLOW, color=BLACK, size=17)
note(s, "归因来源：世界卫生组织（WHO）健康决定因素框架，健康管理领域通用表述", top=Inches(6.34))

# ══════════════ 8 · 医院 vs 家庭 ══════════════
s = slide()
head(s, "第三部分 · 观念转折", "医院治结果，家庭治源头", 8, tsize=36)
pairs = [("医 院", "压血压 · 降血糖 · 拦血脂", "管的是「结果」", GRAY, CREAM),
         ("家 庭", "怎么吃 · 怎么动 · 怎么睡", "管的是「源头」", GREEN, CARD)]
for i, (hd, l1, l2, col, bgc) in enumerate(pairs):
    x = M + Inches(i * 6.22)
    rect(s, x, Inches(1.95), Inches(5.92), Inches(3.30), fill=bgc,
         line=RGBColor(0xE5, 0xDE, 0xD2), lw=1)
    rect(s, x, Inches(1.95), Inches(5.92), Inches(0.14), fill=col)
    text(s, x + Inches(0.32), Inches(2.32), Inches(5.2), Inches(0.6), [[(hd, 30, True, col, BODY)]])
    text(s, x + Inches(0.32), Inches(3.18), Inches(5.25), Inches(1.7),
         [[(l1, 17, False, INK, BODY)], [(l2, 24, True, BLACK, BODY)]], spacing=1.7)
band(s, "医院能救火，防火只能在自己家。", Inches(5.58), h=0.78, size=20)

# ══════════════ 9 · 价值锚 ══════════════
s = slide()
head(s, "第三部分 · 机会在哪", "行业真正的价值，落在这两件事", 9, tsize=34)
boxes = [("①", "慢病整体解决方案", "成熟 · 专业 · 有效\n不是偏方，是被反复验证过的一套方案", PINK),
         ("②", "家庭健康管理员", "把这套方案复制到每一个家庭\n落在一日三餐，而不是 PPT 上", CYAN)]
for i, (num, hd, body, col) in enumerate(boxes):
    x = M + Inches(i * 6.22)
    rect(s, x, Inches(1.95), Inches(5.92), Inches(3.15), fill=CARD, line=RGBColor(0xE5, 0xDE, 0xD2), lw=1)
    rect(s, x + Inches(0.32), Inches(2.22), Inches(0.62), Inches(0.62), fill=col)
    text(s, x + Inches(0.32), Inches(2.22), Inches(0.62), Inches(0.62),
         [[(num, 22, True, BLACK, BODY)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(1.12), Inches(2.28), Inches(4.6), Inches(0.6),
         [[(hd, 24, True, INK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.32), Inches(3.22), Inches(5.3), Inches(1.5),
         [[(ln, 14, False, GRAY, BODY)] for ln in body.split("\n")], spacing=1.6, space_after=6)
band(s, "方案 + 复制方案的人：医院做不了，大公司落不到餐桌。", Inches(5.42), h=0.72, size=15)

# ══════════════ 10 · 两条腿 ══════════════
s = slide()
head(s, "第四部分 · 怎么做", "普通人靠两条腿站住", 10, tsize=36)
legs = [("第一条腿", "专 业", ["成熟：被反复验证过", "专业：符合营养学原理", "有效：真的能看到变化"], PINK),
        ("第二条腿", "传 播", ["不能再走老路：发传单、熟人一个个讲", "回到线上：短视频、社群、内容", "让更多人看见"], CYAN)]
for i, (tag, hd, items_, col) in enumerate(legs):
    x = M + Inches(i * 6.22)
    rect(s, x, Inches(1.90), Inches(5.92), Inches(3.60), fill=col)
    text(s, x + Inches(0.34), Inches(2.16), Inches(5.0), Inches(0.34),
         [[(tag, 13, True, BLACK, BODY)]])
    text(s, x + Inches(0.34), Inches(2.52), Inches(5.0), Inches(0.62),
         [[(hd, 32, True, BLACK, BODY)]])
    rect(s, x + Inches(0.34), Inches(3.26), Inches(0.9), Inches(0.05), fill=BLACK)
    paras = [[("· ", 15, True, BLACK, BODY), (t, 14, False, INK, BODY)] for t in items_]
    text(s, x + Inches(0.34), Inches(3.48), Inches(5.28), Inches(1.8), paras, spacing=1.55, space_after=4)
band(s, "只有专业走不长，只有传播走不稳 —— 缺一条都站不住。", Inches(5.76), h=0.72, size=15)

# ══════════════ 11 · 一条腿走不远 ══════════════
s = slide()
head(s, "第四部分 · 为什么必须两条", "只有一条腿，走不远", 11, tsize=36)
rows2 = [("只有专业", "不会传播", "你再厉害，也只有身边那几个人知道 —— 被「人数」卡死"),
         ("只有传播", "没有专业", "你能火一阵子，但客户留不住 —— 被「信任」卡死")]
y = Inches(1.98)
for a, b, c in rows2:
    rect(s, M, y, CW, Inches(1.52), fill=CARD, line=RGBColor(0xE5, 0xDE, 0xD2), lw=1)
    rect(s, M, y, Inches(0.10), Inches(1.52), fill=RED)
    text(s, M + Inches(0.38), y + Inches(0.24), Inches(2.4), Inches(0.6),
         [[(a, 24, True, BLACK, BODY)]])
    text(s, M + Inches(0.38), y + Inches(0.90), Inches(2.4), Inches(0.4),
         [[(b, 16, True, RED, BODY)]])
    text(s, M + Inches(3.15), y, Inches(8.6), Inches(1.52),
         [[(c, 17, False, INK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(1.72)
band(s, "两条腿一起走，才叫事业。", Inches(5.55), h=0.78, fill=PINK, size=21)

# ══════════════ 12 · 实证 ══════════════
s = slide()
head(s, "第四部分 · 一个实证", "传播不是口号，是打出来的", 12, tsize=34)
rect(s, M, Inches(1.92), Inches(5.92), Inches(3.30), fill=CREAM)
text(s, M + Inches(0.32), Inches(2.16), Inches(5.2), Inches(1.1),
     [[("2000", 78, True, PINK, NUM), ("+", 34, True, PINK, NUM)]], spacing=1.0)
text(s, M + Inches(0.32), Inches(3.30), Inches(5.3), Inches(1.5),
     [[("一期慢病管理实战班报名人数", 16, True, INK, BODY)],
      [("不是发传单来的，是靠内容、靠社群来的", 13, False, GRAY, BODY)]], spacing=1.5, space_after=6)
rect(s, M + Inches(6.22), Inches(1.92), Inches(5.92), Inches(3.30), fill=CREAM)
text(s, M + Inches(6.54), Inches(2.16), Inches(5.2), Inches(1.1),
     [[("4 × 500", 66, True, CYAN, NUM)]], spacing=1.0)
text(s, M + Inches(6.54), Inches(3.44), Inches(5.2), Inches(1.5),
     [[("四个群，每个 500 人，全部满员", 16, True, INK, BODY)],
      [("线上传播跑通之后，规模是可以被复制的", 13, False, GRAY, BODY)]], spacing=1.5, space_after=6)
band(s, "专业决定你能走多远，传播决定有多少人知道你。", Inches(5.55), h=0.72, size=15)

# ══════════════ 13 · AI 的角色 ══════════════
s = slide()
head(s, "第四部分 · AI 的角色", "AI 干的事：把两条腿接到一个人身上", 13, tsize=32)
for i, (hd, sub, col) in enumerate([("专 业", "营养学 · 慢病方案", CYAN), ("传 播", "内容 · 选题 · 脚本", YELLOW)]):
    x = M + Inches(i * 6.22)
    rect(s, x, Inches(1.92), Inches(5.92), Inches(1.32), fill=col)
    text(s, x + Inches(0.32), Inches(2.10), Inches(5.1), Inches(0.55), [[(hd, 26, True, BLACK, BODY)]])
    text(s, x + Inches(0.32), Inches(2.70), Inches(5.1), Inches(0.4), [[(sub, 13, False, RGBColor(0x33, 0x33, 0x33), BODY)]])
# 连接线
rect(s, M + Inches(2.40), Inches(3.24), Pt(5), Inches(0.42), fill=BLACK)
rect(s, M + Inches(8.62), Inches(3.24), Pt(5), Inches(0.42), fill=BLACK)
rect(s, M + Inches(2.43), Inches(3.62), Inches(6.24), Pt(5), fill=BLACK)
rect(s, M + Inches(5.52), Inches(3.62), Pt(5), Inches(0.50), fill=BLACK)
rect(s, M + Inches(2.78), Inches(4.10), Inches(5.66), Inches(1.05), fill=BLACK)
text(s, M + Inches(2.78), Inches(4.10), Inches(5.66), Inches(1.05),
     [[("A I   +   知 识 库", 26, True, YELLOW, BODY)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(5.42), CW, Inches(0.5),
     [[("过去挡在普通人面前的两堵墙，现在变成了两扇门。", 17, True, PINK, BODY)]])

# ══════════════ 14 · 过去 vs 现在 ══════════════
s = slide()
head(s, "第四部分 · 专业这条腿", "成为能接客户的营养专业人士", 14, tsize=32)
text(s, M, Inches(1.92), Inches(5.4), Inches(0.34), [[("过 去", 13, True, GRAY, BODY)]])
text(s, M, Inches(2.26), Inches(5.4), Inches(1.0), [[("5 – 10 年", 52, True, LGRAY, NUM)]])
text(s, M, Inches(3.42), Inches(5.4), Inches(1.6),
     [[("学 · 考 · 在真实客户身上练", 16, False, INK, BODY)],
      [("练错了还得改 —— 没有捷径", 16, False, INK, BODY)]], spacing=1.55)
rect(s, W / 2 - Inches(0.02), Inches(1.90), Pt(2), Inches(3.20), fill=RGBColor(0xD8, 0xD0, 0xC2))
text(s, W / 2 + Inches(0.50), Inches(1.92), Inches(5.2), Inches(0.34), [[("现 在", 13, True, PINK, BODY)]])
text(s, W / 2 + Inches(0.50), Inches(2.26), Inches(5.2), Inches(1.0), [[("一个知识库", 46, True, BLACK, BODY)]])
text(s, W / 2 + Inches(0.50), Inches(3.42), Inches(5.2), Inches(1.8),
     [[("不用背下整本书，可以「调用」这本书", 15, False, INK, BODY)],
      [("起点不是「我什么都不懂」", 15, False, INK, BODY)],
      [("而是「我背后有一个专业的脑子」", 15, True, BLACK, BODY)]], spacing=1.55)
band(s, "AI 是引擎，知识库是油。没有油，引擎再猛也跑不动。", Inches(5.55), h=0.72, fill=CREAM, color=INK, size=15)

# ══════════════ 15 · 两个大脑 ══════════════
s = slide()
head(s, "第四部分 · 给每个人装两个大脑", "营养专业大脑 × 自媒体传播大脑", 15, tsize=32)
brains = [("营养专业大脑", ["成体系的营养学", "慢病管理方案", "真实案例库", "常见问题的处理逻辑"], BLACK, WHITE),
          ("自媒体传播大脑", ["各平台爆款方法", "选题逻辑", "脚本结构", "用户语言"], YELLOW, BLACK)]
for i, (hd, items_, bgc, tc) in enumerate(brains):
    x = M + Inches(i * 6.22)
    rect(s, x, Inches(1.92), Inches(5.92), Inches(3.35), fill=bgc)
    text(s, x + Inches(0.34), Inches(2.16), Inches(5.2), Inches(0.6), [[(hd, 24, True, tc, BODY)]])
    paras = [[("· ", 15, True, tc, BODY), (t, 15, False, tc, BODY)] for t in items_]
    text(s, x + Inches(0.34), Inches(2.92), Inches(5.28), Inches(2.1), paras, spacing=1.55, space_after=8)
band(s, "知识库比 AI 本身更重要 —— 它决定了这个脑子专不专业。", Inches(5.52), h=0.72, size=15)

# ══════════════ 16 · 清醒的话（PINK 满版） ══════════════
s = slide(PINK)
text(s, M, Inches(0.40), Inches(6.0), Inches(0.34),
     [[("第四部分 · 一句清醒的话", 13, True, BLACK, BODY)]])
text(s, M, Inches(1.55), Inches(11.9), Inches(3.4),
     [[("AI 不会让不专业的人变专业，", 40, True, WHITE, BODY)],
      [("它只会让专业的人，快十倍。", 48, True, BLACK, BODY)]], spacing=1.4)
rect(s, M, Inches(4.48), Inches(2.2), Inches(0.09), fill=BLACK)
text(s, M, Inches(4.82), Inches(11.4), Inches(1.8),
     [[("AI 是放大器，不是替代品。", 21, True, BLACK, BODY)],
      [("你脑子里是空的，放大出来还是空的。", 21, False, WHITE, BODY)],
      [("所以顺序永远是：先建地基，再装引擎。", 21, True, BLACK, BODY)]], spacing=1.55)
text(s, M, Inches(6.85), Inches(11.4), Inches(0.34),
     [[("这句话，比前面所有的话都重要", 12, False, RGBColor(0xFF, 0xD9, 0xE8), BODY)]])
pageno(s, 16, RGBColor(0xFF, 0xD9, 0xE8))

# ══════════════ 17 · 四个已经 ══════════════
s = slide()
head(s, "第五部分 · 为什么是我们", "四个「已经」", 17, tsize=38)
items = [("01", "专业已经验证", "方案是在真实顾客身上跑出来的，不是 PPT 上画出来的"),
         ("02", "传播已经验证", "一场实战班两千多人、四个五百人群满员"),
         ("03", "AI 应用已经验证", "不是在讲将来，是已经在用：知识库、工具、内容生产"),
         ("04", "可复制", "只有张医生一个人能用的东西，没有价值")]
y = Inches(1.95)
for i, (num, hd, body) in enumerate(items):
    rect(s, M, y, CW, Inches(0.94), fill=CREAM if i % 2 == 0 else None)
    text(s, M + Inches(0.24), y, Inches(0.9), Inches(0.94),
         [[(num, 20, True, PINK, NUM)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(1.20), y, Inches(3.1), Inches(0.94),
         [[(hd, 20, True, BLACK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(4.45), y, Inches(7.5), Inches(0.94),
         [[(body, 14, False, INK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(1.02)
band(s, "把一小部分人才能做的事，变成普通人也能做的事。", Inches(6.02), h=0.70, fill=PINK, size=15)

# ══════════════ 18 · 三步走 ══════════════
s = slide()
head(s, "总结 · 怎么做", "所以，答案就三步", 18, tsize=38)
steps = [("第一步", "选对地方", "有解决方案、有体系、有验证\n别自己从零摸索", PINK),
         ("第二步", "打地基", "跟着体系学专业\n别指望速成", YELLOW),
         ("第三步", "装引擎", "用 AI 把专业变成内容\n把内容变成客户", CYAN)]
for i, (tag, hd, body, col) in enumerate(steps):
    x = M + Inches(i * 4.06)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(3.35), fill=CARD, line=RGBColor(0xE5, 0xDE, 0xD2), lw=1)
    rect(s, x, Inches(1.95), Inches(3.86), Inches(0.58), fill=col)
    text(s, x + Inches(0.24), Inches(1.95), Inches(3.4), Inches(0.58),
         [[(tag, 14, True, BLACK, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.24), Inches(2.72), Inches(3.4), Inches(0.6),
         [[(hd, 24, True, INK, BODY)]])
    rect(s, x + Inches(0.24), Inches(3.40), Inches(0.9), Inches(0.05), fill=col)
    text(s, x + Inches(0.24), Inches(3.64), Inches(3.38), Inches(1.4),
         [[(ln, 14, False, GRAY, BODY)] for ln in body.split("\n")], spacing=1.5, space_after=6)
band(s, "三步走完，你在这个行业里，就有自己的位置。", Inches(5.58), h=0.72, size=17)

# ══════════════ 19 · 结尾 ══════════════
s = slide(BLACK)
text(s, M, Inches(0.45), Inches(6.0), Inches(0.34), [[("结 语", 13, True, PINK, BODY)]])
text(s, M, Inches(1.35), Inches(11.9), Inches(1.9),
     [[("机会在慢病，战场在家庭，", 34, True, WHITE, BODY)],
      [("而这件事，只能由一个个普通人去做。", 34, True, YELLOW, BODY)]], spacing=1.4)
rect(s, M, Inches(3.32), Inches(2.2), Inches(0.09), fill=PINK)
text(s, M, Inches(3.64), Inches(11.6), Inches(1.3),
     [[("我不承诺收入，也不保证结果 —— 这个行业里，跟你打包票的都要小心。", 16, False, WHITE, BODY)],
      [("我能说的是：这条路我自己走过，我们团队上万人走过，它是有路标的。", 17, True, WHITE, BODY)]],
     spacing=1.6)
rect(s, M, Inches(5.20), CW, Inches(0.80), fill=PINK)
text(s, M + Inches(0.28), Inches(5.20), CW - Inches(0.56), Inches(0.80),
     [[("课后私信我，就聊你现在卡在哪 —— 聊什么都不卖。", 18, True, WHITE, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
note(s, "以上为个人经历与行业观察分享，不构成任何收入承诺或诊疗建议，个体情况请咨询专业人士。",
     top=Inches(6.42), color=RGBColor(0x8C, 0x86, 0x7E), size=11)

prs.save("AI大健康赛道副业怎么做-万病寻源版-26-23期.pptx")
print("saved 19 slides")
