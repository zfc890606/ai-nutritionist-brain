# -*- coding: utf-8 -*-
"""
生成：大健康个人IP · 从0到1（整合版 · 砖红全屏）
整合来源：
  1) AI未来时代·个人IP三步-砖红版.pptx（总论：重要性 + 三部曲 + 商业定位）
  2) 精英班3打造IP与运营9.21版（赵旭）.pptx（小白：学习→实践→人设成立）
  3) 精英班3打造IP与运营-张飞7.20.pptx（运营：T型朋友圈 / 发圈 / 置顶）
版式：D直播工作台/直播课件版式规范-砖红双栏版（全屏版，无摄像头区）
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
                   "01-课程培训", "大健康个人IP·从0到1-整合版.pptx")

RED = RGBColor(0x8B, 0x10, 0x02)
BLACK = RGBColor(0x00, 0x00, 0x00)
GREY = RGBColor(0x66, 0x66, 0x66)
FONT = "苹方-简"

L = 1.204
W = 10.925

prs = Presentation(TEMPLATE)
base_slide = prs.slides[0]
bg_elems = [deepcopy(sh._element) for sh in list(base_slide.shapes)[:1]]

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
    for el in bg_elems:
        slide.shapes._spTree.append(deepcopy(el))
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


def chapter_line(slide, text):
    textbox(slide, L, 0.955, W, 0.6, [(text, 28, RED)])


def point_page(chapter, lead, conclusion, note):
    s = add_slide()
    chapter_line(s, chapter)
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


def three_col(chapter, cols, note):
    s = add_slide()
    chapter_line(s, chapter)
    for i, (num, label) in enumerate(cols):
        x = 1.204 + i * 3.85
        textbox(s, x, 2.35, 3.2, 1.35, [(num, 72, RED)])
        textbox(s, x, 3.75, 3.2, 1.15, [(label, 28, BLACK)])
    textbox(s, L, 6.55, W, 0.55, [(note, 28, BLACK)], align=PP_ALIGN.RIGHT)
    return s


slides = []

# 1 封面
s = add_slide()
textbox(s, L, 1.02, W, 0.6, [("张医生 · AI 营养师｜团队内部分享", 28, GREY)])
textbox(s, L, 2.42, W, 2.35, [("大健康个人 IP", 48, RED), ("从 0 到 1", 72, RED)])
textbox(s, L, 5.05, W, 0.6, [("定位 → 起步 → 运营", 28, BLACK)])
textbox(s, L, 6.85, W, 0.4, [("2026.11 · 内部认知分享，不构成收入承诺", 18, GREY)])
notes(s, "开场：今天不讲空理论，讲一条从0到1的路——先想明白，再起步，最后用朋友圈把IP运营起来。")

# 2 目录
s = add_slide()
textbox(s, L, 1.02, W, 0.6, [("目录", 28, RED)])
textbox(s, L, 2.4, W, 3.4,
        [("01  总论：为什么做", 48, RED),
         ("02  小白：90 天起步", 48, RED),
         ("03  运营：朋友圈体系", 48, RED)])
textbox(s, L, 5.9, W, 0.55, [("先想明白，再动手", 28, BLACK)])
notes(s, "三部分：总论、90天起步、朋友圈运营。听完就能开始发第一条。")

# 3 章节 01
slides.append(chapter_page("01", "总论", "先想明白", "定位不对，努力白费"))
notes(slides[-1], "第一部分总论。先想明白为什么做、IP是什么、定位怎么定。")

# 4 经营自己
slides.append(point_page("01 · 总论", "经营自己", "是最大的杠杆", "打工卖时间，做自己卖价值"))
notes(slides[-1], "打工是把时间卖一次，经营自己是把价值重复卖很多次。个人IP就是你的杠杆。")

# 5 技能 vs 经历
slides.append(point_page("01 · 总论", "技能被 AI 抹平", "经历不会", "你是一个观点的容器 · Dan Koe"))
notes(slides[-1], "AI把技能变得便宜，把你的经历、判断、走过的路变得稀缺。这就是普通人的机会。")

# 6 三部曲总览
slides.append(three_col("01 · 总论", [("01", "找到自己是谁"), ("02", "被更多人看见"), ("03", "变成产品")],
                        "一个闭环，顺序不能反"))
notes(slides[-1], "三部曲：找到自己是谁、被更多人看见、把过程变成产品。顺序不能反。")

# 7 定位
slides.append(point_page("01 · 总论", "定位不在外面", "在你身上", "你真实走过的，就是商业定位"))
notes(slides[-1], "定位不在外面，不在热门赛道，在你真实走过的路里。")

# 8 定位三问
s = add_slide()
chapter_line(s, "01 · 商业定位")
textbox(s, L, 2.45, W, 3.2,
        [("我真实是谁？", 48, RED),
         ("我走过什么？", 48, RED),
         ("我正在变成什么？", 48, RED)])
textbox(s, L, 6.707, W, 0.55, [("讲清楚这三件事，定位自然清晰", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "三个问题：我真实是谁？我走过什么？我正在变成什么？写下来，定位就有了雏形。")

# 9 商业校准
slides.append(point_page("01 · 商业定位", "不是每个价值点", "都要放大", "结合你当下的商业来选"))
notes(slides[-1], "不是每个价值点都要放大。结合你当下的商业来选——能帮人健康，或能带人创业。")

# 10 三个定位案例
s = add_slide()
chapter_line(s, "01 · 定位案例")
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
notes(s, "三个例子：董博士减重40斤做脂肪，阿娟调理痘痘做痘痘，我创业亏40万做创业。共同点是真实走过。")

# 11 章节 02
slides.append(chapter_page("02", "小白起步", "90 天", "从学到做，人设自然长出来"))
notes(slides[-1], "第二部分：小白怎么起步。不用等专业，90天就能长出初步人设。")

# 12 三阶段
slides.append(three_col("02 · 90 天路径", [("01", "学习"), ("02", "实践"), ("03", "人设成立")],
                        "顺序不能跳，人设是结果"))
notes(slides[-1], "三个阶段：先学一个点，再真做一遍，人设自然成立。人设是结果，不是包装。")

# 13 学一个点
slides.append(point_page("02 · 第一阶段 学习", "先学一个点", "学透", "「假饥饿」、少食多餐、营养早餐，选一个"))
notes(slides[-1], "第一阶段学习。不要什么都学，选一个具体的点：假饥饿信号、少食多餐、营养早餐，任选一个学透。")

# 14 讲一次
slides.append(point_page("02 · 第一阶段 学习", "用自己的话", "讲一次", "最好的输入，就是输出"))
notes(slides[-1], "学习的标准不是看完，是能用自己的话讲一次。最好的输入就是输出。")

# 15 真做一遍
slides.append(point_page("02 · 第二阶段 实践", "真做一遍", "做出来", "不是讲道理，是拿出结果"))
notes(slides[-1], "第二阶段实践。真做一遍，拿到自己的结果，不是转述别人的道理。")

# 16 整个旅程
slides.append(point_page("02 · 第二阶段 实践", "最让人信服的", "是整个旅程", "不是最终的结果"))
notes(slides[-1], "最让人信服的不是最终结果，是整个旅程。把每天的变化记录下来。")

# 17 人设
slides.append(point_page("02 · 第三阶段 人设", "人设不是包装", "是长出来的", "水到渠成，画龙点睛"))
notes(slides[-1], "第三阶段人设。人设不是包装出来的，是成长到位之后水到渠成、画龙点睛。")

# 18 90天节奏
s = add_slide()
chapter_line(s, "02 · 90 天节奏")
for i, (period, task) in enumerate([
    ("第 1 个月", "学：选一个点，学透、讲出来"),
    ("第 2 个月", "做：真实践，记录全过程"),
    ("第 3 个月", "立：持续输出，人设成型"),
]):
    y = 2.45 + i * 1.15
    textbox(s, L, y, 3.0, 0.8, [(period, 48, RED)], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 4.4, y, 7.6, 0.8, [(task, 28, BLACK)], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, L, 6.707, W, 0.55, [("不用等完美，先开始", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "90天节奏：第一个月学，第二个月做，第三个月立。不用等完美。")

# 19 现在就发
slides.append(point_page("02 · 落地", "不用等准备好", "现在就发", "先有变化，才有内容"))
notes(slides[-1], "今天就开始发圈。先有变化，才有内容；先有路，才有话讲。")

# 20 章节 03
slides.append(chapter_page("03", "IP 运营", "朋友圈", "让更多人看见你、记住你、信任你"))
notes(slides[-1], "第三部分：IP成立之后，怎么运营、怎么表达、怎么让更多人看见。")

# 21 第一阵地
slides.append(point_page("03 · 朋友圈", "朋友圈不是日记", "是第一阵地", "谁获取注意力，谁就有生产力"))
notes(slides[-1], "朋友圈不是日记，是你的第一阵地。谁获取注意力，谁就有生产力。")

# 22 T型朋友圈
s = add_slide()
chapter_line(s, "03 · T 型朋友圈")
textbox(s, L, 2.35, 1.0, 1.2, [("横", 72, RED)])
textbox(s, 2.6, 2.5, 3.6, 0.8, [("大杂家", 48, RED)])
textbox(s, 2.6, 3.45, 3.6, 1.4, [("生活、学习、朋友\n展示真实的美好", 28, BLACK)])
textbox(s, 7.1, 2.35, 1.0, 1.2, [("竖", 72, RED)])
textbox(s, 8.0, 2.5, 4.1, 0.8, [("小专家", 48, RED)])
textbox(s, 8.0, 3.45, 4.1, 1.4, [("一个领域，持续深耕\n帮人解决问题", 28, BLACK)])
textbox(s, L, 6.707, W, 0.55, [("横是广度，竖是深度", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "T型朋友圈：横是广度，做有血有肉的大杂家；竖是深度，做一个小领域的小专家。")

# 23 大杂家三瓣
s = add_slide()
chapter_line(s, "03 · 横：大杂家")
textbox(s, L, 2.35, W, 3.2,
        [("我的生活", 48, RED),
         ("我的学习", 48, RED),
         ("我的朋友", 48, RED)])
textbox(s, L, 6.707, W, 0.55, [("有血有肉，真性情", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "大杂家三瓣：我的生活、我的学习、我的朋友。让人看到你真实、立体、有能量。")

# 24 小专家公式
s = add_slide()
chapter_line(s, "03 · 竖：小专家")
textbox(s, L, 2.35, W, 3.2,
        [("立 Flag", 48, RED),
         ("过程感悟", 48, RED),
         ("过程监督", 48, RED)])
textbox(s, L, 6.707, W, 0.55, [("每一个小改变，都能吸引同频的人", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "小专家公式：立Flag、过程感悟、过程监督。每一个小改变都能吸引同频的人。")

# 25 标签
s = add_slide()
chapter_line(s, "03 · 发圈标签")
textbox(s, L, 2.35, W, 3.2,
        [("#营养早餐第X天", 48, RED),
         ("#美好生活天天见", 48, RED),
         ("#改变故事", 48, RED)])
textbox(s, L, 6.707, W, 0.55, [("标签让内容被看见、被记住", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "每条内容带标签：营养早餐第X天、美好生活天天见、改变故事。标签让内容被看见、被记住。")

# 26 借力
slides.append(point_page("03 · 内容", "公司内容打底", "加一点自己", "自拍、感受、真实场景"))
notes(slides[-1], "内容不用全部原创：公司内容打底，加一点自己——自拍、感受、真实场景。")

# 27 文案
slides.append(point_page("03 · 文案", "90% 模仿", "10% 创新", "用 AI 找文案，再改成自己的话"))
notes(slides[-1], "文案公式：90%模仿，10%创新。用AI找文案，再改成自己的话。")

# 28 置顶五件套
s = add_slide()
chapter_line(s, "03 · 置顶朋友圈")
rows = [
    ("①", "高光时刻：荣誉、成绩、上台"),
    ("②", "梦想与心路：我为什么出发"),
    ("③", "我能帮你什么：价值与方案"),
    ("④", "高质量圈子：我和谁在一起"),
    ("⑤", "真实生活：有血有肉的你"),
]
for i, (num, text) in enumerate(rows):
    y = 2.2 + i * 0.78
    textbox(s, L, y, 0.6, 0.6, [(num, 28, RED)])
    textbox(s, 1.85, y, 10.2, 0.6, [(text, 28, BLACK)])
textbox(s, L, 6.707, W, 0.55, [("置顶不是炫耀，是让人三秒看懂你", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "置顶五件套：高光时刻、梦想与心路、我能帮你什么、高质量圈子、真实生活。五条置顶，三秒看懂你。")

# 29 置顶作用
slides.append(point_page("03 · 置顶朋友圈", "别人点开你", "三秒就懂你", "先看置顶，再看你发什么"))
notes(slides[-1], "别人点开你，先看置顶。置顶不是炫耀，是让对方快速知道你是谁、能帮他什么。")

# 30 发圈配比
s = add_slide()
chapter_line(s, "03 · 发圈节奏")
textbox(s, L, 1.95, 2.2, 0.5, [("内容", 28, BLACK)])
textbox(s, 3.6, 1.95, 2.0, 0.5, [("每周", 28, BLACK)])
textbox(s, 5.9, 1.95, 6.0, 0.5, [("目的", 28, BLACK)])
for i, (kind, count, purpose) in enumerate([
    ("生活", "2 条", "让人觉得你真实"),
    ("学习", "2 条", "让人觉得你在成长"),
    ("专业", "2 条", "让人觉得你专业"),
    ("改变", "1 条", "让人觉得你真的变了"),
    ("互动", "每天", "让关系热起来"),
]):
    y = 2.6 + i * 0.82
    textbox(s, L, y, 2.2, 0.6, [(kind, 28, RED)])
    textbox(s, 3.6, y, 2.0, 0.6, [(count, 28, BLACK)])
    textbox(s, 5.9, y, 6.0, 0.6, [(purpose, 28, BLACK)])
textbox(s, L, 6.707, W, 0.55, [("少量多次，长期稳定", 28, BLACK)], align=PP_ALIGN.RIGHT)
notes(s, "一周发圈配比：生活2、学习2、专业2、改变1，互动每天。少量多次，长期稳定。")

# 31 收口
slides.append(point_page("03 · 收口", "技巧遍地都是", "真实才是壁垒", "IP 不是包装出来的，是活出来的"))
notes(slides[-1], "收口：技巧遍地都是，真实才是壁垒。IP不是包装出来的，是活出来的。")

# 32 结尾
s = add_slide()
textbox(s, L, 1.02, W, 0.6, [("下一步", 28, GREY)])
textbox(s, L, 2.45, W, 1.3, [("先发第一条", 72, RED)])
textbox(s, L, 5.55, W, 1.0, [("今天写 3 分钟，配一张真实照片", 28, BLACK)])
textbox(s, L, 6.85, W, 0.4, [("张医生｜AI 营养师 · 2026.11", 18, GREY)])
notes(s, "下一步：今天先发第一条。写3分钟，配一张真实照片，不用等准备好。")

prs.save(OUT)
print("saved:", OUT)
print("slides:", len(prs.slides))
