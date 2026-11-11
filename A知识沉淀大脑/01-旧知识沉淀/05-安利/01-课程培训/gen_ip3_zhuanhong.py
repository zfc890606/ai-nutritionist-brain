# -*- coding: utf-8 -*-
"""
生成：AI未来时代·个人IP三步（砖红双栏版）
版式依据：D直播工作台/直播课件版式规范-砖红双栏版.md
内容依据：
  - 自媒体研究/10-Dan Koe·超级个体内容系统/03-爆款拆解·最赚钱的赛道是你自己.md
  - 自媒体研究/06-个人IP·商业定位.md
  - 05-安利/05-安利业务/张医生-做自己才是最大的杠杆-整理稿.md
  - 原课件 AI未来时代·个人IP三步.pptx
"""
import os
from copy import deepcopy

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.oxml.xmlchemy import OxmlElement

BASE = "/Users/mac/Documents/zfc最强大脑"
TEMPLATE = os.path.join(BASE, "D直播工作台", "直播课件模板-砖红双栏版.pptx")
OUT = os.path.join(BASE, "A知识沉淀大脑", "01-旧知识沉淀", "05-安利",
                   "01-课程培训", "AI未来时代·个人IP三步-砖红版.pptx")

RED = RGBColor(0x8B, 0x10, 0x02)
BLACK = RGBColor(0x00, 0x00, 0x00)
GREY = RGBColor(0x66, 0x66, 0x66)
FONT = "苹方-简"

L = 1.204
W = 10.925

prs = Presentation(TEMPLATE)

# 取模板的整屏渐变底（全屏版不要右侧摄像头区）
base_slide = prs.slides[0]
bg_elems = [deepcopy(sh._element) for sh in list(base_slide.shapes)[:2]]

# 删除模板自带的 6 页示例
sldIdLst = prs.slides._sldIdLst
for sldId in list(sldIdLst):
    rId = sldId.get(qn("r:id"))
    try:
        prs.part.drop_rel(rId)
    except Exception:
        pass
    sldIdLst.remove(sldId)


BLANK = next((lay for lay in prs.slide_layouts if lay.name == "Blank"), prs.slide_layouts[6])


def add_slide():
    slide = prs.slides.add_slide(BLANK)
    # 全屏版：只保留整屏渐变底，不再要右侧摄像头区
    slide.shapes._spTree.append(deepcopy(bg_elems[0]))
    return slide


def style_run(run, size, color, bold=True):
    f = run.font
    f.name = FONT
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            rPr.append(el)
        el.set("typeface", FONT)


def textbox(slide, left, top, width, height, paras,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, (txt, size, color) in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = 1.0
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        r = p.add_run()
        r.text = txt
        style_run(r, size, color)
    return tb


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def chapter_line(slide, text, color=RED):
    textbox(slide, L, 0.955, W, 0.6, [(text, 28, color)])


def point_page(chapter, lead, conclusion, note, chapter_color=RED):
    s = add_slide()
    chapter_line(s, chapter, chapter_color)
    textbox(s, L, 2.638, W, 0.85, [(lead, 48, RED)])
    textbox(s, L, 3.48, W, 1.2, [(conclusion, 72, RED)])
    textbox(s, L, 6.707, W, 0.55, [(note, 28, BLACK)], align=PP_ALIGN.RIGHT)
    return s


def chapter_page(num, line1, line2, lead):
    s = add_slide()
    textbox(s, L, 1.02, W, 0.6, [(num, 28, RED)])
    textbox(s, L, 2.45, W, 1.3, [(line1, 72, RED)])
    textbox(s, L, 3.76, W, 1.3, [(line2, 72, RED)])
    textbox(s, L, 5.55, W, 0.6, [(lead, 28, BLACK)])
    return s


def cover_page():
    s = add_slide()
    textbox(s, L, 1.02, W, 0.6, [("张医生 · AI 营养师｜团队内部分享", 28, GREY)])
    textbox(s, L, 2.42, W, 2.35, [("AI 未来时代", 48, RED), ("个人 IP 三步", 72, RED)])
    textbox(s, L, 5.05, W, 0.6, [("找到自己 → 被看见 → 变成产品", 28, BLACK)])
    textbox(s, L, 6.85, W, 0.4,
            [("2026.11 · 内部认知分享，不构成收入承诺", 18, GREY)])
    return s


def toc_page():
    s = add_slide()
    textbox(s, L, 1.02, W, 0.6, [("目录", 28, RED)])
    textbox(s, L, 2.4, W, 3.4,
            [("01  为什么现在做", 48, RED),
             ("02  我的来时路", 48, RED),
             ("03  个人品牌三步", 48, RED)])
    textbox(s, L, 5.9, W, 0.55, [("先想明白，再开始做", 28, BLACK)])
    return s


# ---------------- 内容 ----------------

slides = []

# 1 封面
slides.append(cover_page())
notes(slides[-1], "开场。今晚只讲一件事：AI 时代，个人 IP 不是可选项，是你自己的杠杆。先讲为什么，再讲我的故事，最后讲三步怎么做。")

# 2 目录
slides.append(toc_page())
notes(slides[-1], "三部分：先讲认知，再讲我的故事，最后讲方法。认知不到，方法都是空转。")

# 3 章节 01
slides.append(chapter_page("01", "为什么现在", "要做个人 IP", "这不是选择，是这个时代的生存方式"))
notes(slides[-1], "第一部分：为什么是现在。AI 来了，技能在贬值，但「你是谁」在升值。")

# 4 Dan Koe
slides.append(point_page("01 · 为什么现在做", "大多数人都在找", "赚钱的赛道",
                         "最赚钱的赛道，就是你自己"))
textbox(slides[-1], L, 7.18, W, 0.3,
        [("Dan Koe · thedankoe.com · 2023", 18, GREY)])
notes(slides[-1], "Dan Koe 是国外超级个体的代表。2023 年这篇文章的标题就是《最赚钱的赛道是你自己》。他讲：不要找关键词赛道，要成为观点的容器。此处引用原文标题，不做收入承诺。")

# 5 技能 vs 经历
slides.append(point_page("01 · 为什么现在做", "技能会被 AI 抹平", "经历不会",
                         "你是一个观点的容器"))
textbox(slides[-1], L, 7.18, W, 0.3, [("Dan Koe · 2023", 18, GREY)])
notes(slides[-1], "技能可以学、可以被 AI 替代；你的经历、判断、走过的路，AI 复制不了。这就是个人 IP 的底层资产。")

# 6 经营自己是杠杆
slides.append(point_page("01 · 为什么现在做", "经营自己", "是最大的杠杆",
                         "做一家叫「你」的公司"))
notes(slides[-1], "打工是把时间卖一次；经营自己，是把价值重复卖很多次。个人 IP 就是你的杠杆。这句话是今晚的核心。")

# 7 数据页
s = add_slide()
chapter_line(s, "01 · 为什么现在做")
for i, (num, label) in enumerate([
    ("600+", "哈佛实验的\n创业者样本"),
    ("+15%", "判断力强的人\n用 AI"),
    ("-8%", "判断力弱的人\n用 AI"),
]):
    x = 1.204 + i * 3.85
    textbox(s, x, 2.35, 3.2, 1.35, [(num, 72, RED)])
    textbox(s, x, 3.75, 3.2, 1.15, [(label, 28, BLACK)])
textbox(s, L, 6.55, W, 0.55, [("AI 只放大你本来就有的东西", 28, BLACK)], align=PP_ALIGN.RIGHT)
textbox(s, L, 7.18, W, 0.3, [("哈佛 600+ 创业者研究（转引自《审美之外》）", 18, GREY)])
notes(s, "这组数据来自他常引用的哈佛实验：600 多个创业者，判断力强的人用 AI 收入涨 15%，判断力弱的反而跌 8%。结论不是 AI 帮你赚钱，是 AI 放大你本来就有的东西。数据为研究结论，非收入承诺。")

# 8 章节 02
slides.append(chapter_page("02", "我的来时路", "就是我的底牌", "从医院十年，到 AI 营养师"))
notes(slides[-1], "第二部分：讲我自己。一个农村出来、做了十年麻醉医生、创业亏过钱的人，怎么走到今天。")

# 9 时间轴
s = add_slide()
chapter_line(s, "02 · 我的来时路")
for i, (year, event) in enumerate([
    ("2011", "进入三甲医院，做麻醉医生"),
    ("2019", "开奶茶店，亏掉 40 万"),
    ("2020", "辞职，全职做安利"),
    ("2026", "AI 营养师，重新出发"),
]):
    y = 2.3 + i * 1.1
    textbox(s, L, y, 1.9, 0.85, [(year, 48, RED)], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 3.4, y, 8.7, 0.85, [(event, 28, BLACK)], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, L, 6.707, W, 0.55, [("医院十年、亏 40 万、重新爬起来", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "四段路：2011 进三甲医院；2019 奶茶店亏 40 万；2020 辞职全职安利；2026 做 AI 营养师。每一段当时都很难，今天都是素材。")

# 10 底牌
slides.append(point_page("02 · 我的来时路", "奶茶店亏掉 40 万", "那是底牌",
                         "困难不是负债，是底牌"))
notes(slides[-1], "亏 40 万那段，当时觉得是负债；今天看是底牌。因为它让我读懂了创业、读懂了普通人缺什么。困难不是负债，是底牌。")

# 11 真实
slides.append(point_page("02 · 我的来时路", "我讲的每个字", "都是走出来的",
                         "IP 最怕的不是不专业，是不真实"))
notes(slides[-1], "我在台上讲的每个字，都是自己走出来的。IP 最怕的不是不专业，是不真实——真实才有信任。")

# 12 定位案例
s = add_slide()
chapter_line(s, "02 · 我的来时路")
for i, (name, path, word) in enumerate([
    ("董博士", "减重 40 斤", "脂肪"),
    ("阿娟", "痘痘调好了", "痘痘"),
    ("张医生", "亏 40 万再起来", "创业"),
]):
    x = 1.204 + i * 3.81
    textbox(s, x, 2.35, 3.3, 0.5, [(name, 28, RED)])
    textbox(s, x, 2.95, 3.3, 1.0, [(path, 28, BLACK)])
    textbox(s, x, 4.15, 3.3, 0.9, [(word, 48, RED)])
textbox(s, L, 6.707, W, 0.55, [("定位不在外面，在你走过的路上", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "三个人三个词：董博士是脂肪，阿娟是痘痘，我是创业。共同点：都不是包装出来的，是真实走完的一段路。定位就在你的来时路里。")

# 13 章节 03
slides.append(chapter_page("03", "打造个人品牌", "三部曲", "找到自己 → 被看见 → 变成产品"))
notes(slides[-1], "第三部分：方法。打造个人品牌三部曲：找到自己、被看见、变成产品。顺序不能反。")

# 14 三步总览
s = add_slide()
chapter_line(s, "03 · 个人品牌三部曲")
for i, (num, label) in enumerate([
    ("01", "找到自己是谁"),
    ("02", "被更多人看见"),
    ("03", "过程变产品"),
]):
    x = 1.204 + i * 2.36
    textbox(s, x, 2.35, 2.2, 1.35, [(num, 72, RED)])
    textbox(s, x, 3.75, 2.35, 1.15, [(label, 28, BLACK)])
textbox(s, L, 6.55, W, 0.55, [("一个闭环，顺序不能反", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "三步是一个闭环：先有定位，才有内容；先被看见，才有产品；有了产品，成交和复制才变简单。")

# 15 第一步
slides.append(point_page("第一步 · 找到自己是谁", "IP 的底层", "是定位",
                         "先知道自己是谁，才有后面的一切"))
notes(slides[-1], "第一步，找到自己是谁。IP 的底层不是技巧，是定位。先知道自己是谁，后面才有内容可讲。")

# 16 每一段历程
slides.append(point_page("第一步 · 找到自己是谁", "每一段历程", "都是一幅作品",
                         "稀缺的不是经历，是讲故事的能力"))
notes(slides[-1], "你走过的每一段历程，都是一幅作品。真正稀缺的不是经历，是你把经历讲成故事的能力。")

# 17 去哪里挖
s = add_slide()
chapter_line(s, "第一步 · 去哪里挖")
textbox(s, L, 2.35, W, 3.4,
        [("痘痘，调理好了", 48, RED),
         ("减掉几十斤脂肪", 48, RED),
         ("从低谷走到高光", 48, RED),
         ("陪家人把健康走回来", 48, RED)])
textbox(s, L, 6.707, W, 0.55, [("别人抄不走，这就是定位的核心", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "去哪里挖：痘痘、减脂、低谷到高光、陪家人把健康走回来。标准只有一个——你真真实实走过、也真真实实做成过。别人抄不走。")

# 18 不是每个价值点都要放大
slides.append(point_page("第一步 · 商业定位", "不是每个价值点", "都要放大",
                         "结合你当下的商业来选，才叫商业定位"))
notes(slides[-1], "注意：不是每个价值点都要放大。帮过邻居、捐过款都是价值，但要结合你当下的商业来选——结合商业选的，才叫商业定位。")

# 19 定位三问
s = add_slide()
chapter_line(s, "第一步 · 定位三问")
textbox(s, L, 2.45, W, 3.2,
        [("我真实是谁？", 48, RED),
         ("我走过什么？", 48, RED),
         ("我正在变成什么？", 48, RED)])
textbox(s, L, 6.707, W, 0.55, [("定位不在外面，在你身上", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "定位不在外面，在你身上。问自己三个问题：我真实是谁？我走过什么？我正在变成什么？讲清楚，定位自然清晰。")

# 20 第二步
slides.append(point_page("第二步 · 被更多人看见", "被看见的前提", "是先表达",
                         "自媒体、社群、朋友圈，先送出去"))
notes(slides[-1], "第二步，被更多人看见。被看见的前提是先表达。自媒体、社群、朋友圈，全方位把真实的自己送出去，不是等别人来找你。")

# 21 AI 放大
slides.append(point_page("第二步 · 被更多人看见", "定位 AI 替代不了", "放大交给 AI",
                         "AI 替代不了你是谁，但能把你放大一百倍"))
notes(slides[-1], "定位、故事、个人 IP，AI 替代不了你；但定位清晰之后，AI 能把你放大一百倍。找选题、写内容、练口播，都交给 AI。")

# 22 第三步
slides.append(point_page("第三步 · 把过程变成产品", "把这段路做成", "可交付的产品",
                         "有了产品，成交、带人、复制都会变简单"))
notes(slides[-1], "第三步，把过程变成产品。用产品思维，把这段路、这套方法做成一份可交付的东西。有了产品，成交、带人、复制都会变简单。")

# 23 产品案例
s = add_slide()
chapter_line(s, "第三步 · 把过程变成产品")
textbox(s, L, 1.95, 2.3, 0.5, [("谁", 28, BLACK)])
textbox(s, 4.2, 1.95, 3.2, 0.5, [("走过什么", 28, BLACK)])
textbox(s, 7.8, 1.95, 4.3, 0.5, [("变成什么", 28, BLACK)])
for i, (name, path, product) in enumerate([
    ("阿娟", "痘痘", "30 天战痘营"),
    ("董博士", "减重 40 斤", "减脂陪跑"),
    ("张医生", "创业", "付费陪跑 + 大脑"),
]):
    y = 2.6 + i * 1.0
    textbox(s, L, y, 2.3, 0.6, [(name, 28, RED)])
    textbox(s, 4.2, y, 3.2, 0.6, [(path, 28, BLACK)])
    textbox(s, 7.8, y, 4.3, 0.6, [(product, 28, RED)])
textbox(s, L, 6.707, W, 0.55, [("价值被看见，再变成产品，闭环就成立了", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "三个产品例子：阿娟的痘痘 → 战痘 30 天陪跑营；董博士的减重 → 减脂陪跑；我的创业经历 → 付费陪跑 + 我的大脑。价值被看见，再变成产品，闭环就成立了。")

# 24 收口
slides.append(point_page("第三步 · 收口", "技巧遍地都是", "真实才是壁垒",
                         "研究套路，构不成壁垒"))
notes(slides[-1], "收口：技巧遍地都是，真实的你才是壁垒。天天研究套路，既没有竞争力，也构不成壁垒。")

# 25 金句
s = add_slide()
textbox(s, L, 2.62, W, 2.4, [("最赚钱的赛道", 72, RED), ("就是你自己", 72, RED)])
textbox(s, L, 6.75, W, 0.5, [("—— Dan Koe · 2023", 28, GREY)], align=PP_ALIGN.RIGHT)
notes(s, "金句收尾：最赚钱的赛道，就是你自己。这是 Dan Koe 的原话，也是今晚最想让你记住的一句。")

# 26 结尾
s = add_slide()
textbox(s, L, 1.02, W, 0.6, [("下一步", 28, GREY)])
textbox(s, L, 2.45, W, 1.3, [("先讲出你的故事", 72, RED)])
textbox(s, L, 5.55, W, 1.0, [("今晚写 3 分钟，先发一条朋友圈", 28, BLACK)])
textbox(s, L, 6.85, W, 0.4, [("张医生｜AI 营养师 · 2026.11", 18, GREY)])
notes(s, "今晚就做一件事：写下你做成功过的那件事，讲成 3 分钟的故事，先发一条朋友圈。先讲出你的故事，其他的后面再说。")

prs.save(OUT)
print("saved:", OUT)
print("slides:", len(prs.slides))
