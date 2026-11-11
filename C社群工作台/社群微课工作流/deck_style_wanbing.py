#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社群微课 PPT 固定风格引擎 —— 万病寻源版（2026-10-30 定）

用法：
    from deck_style_wanbing import *
    new_deck()
    s = slide()
    head(s, "第一部分 · 标题区小标签", "这一页的大标题", 3)
    ...
    save("主题-YYYY-MM-DD-期号.pptx")

规范文档：C社群工作台/社群微课工作流/PPT风格规范-万病寻源版.md
样板成品：AI大健康赛道副业怎么做-万病寻源版-26-23期.pptx（19 页完整示例）
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

# ───────────── 固定配色（改这里等于改全套风格） ─────────────
PAPER  = RGBColor(0xF5, 0xF0, 0xE8)   # 米白纸感底
CREAM  = RGBColor(0xFA, 0xF6, 0xEF)   # 隔行浅米
CARD   = RGBColor(0xFF, 0xFD, 0xF7)   # 卡片白
PINK   = RGBColor(0xFF, 0x3A, 0x8D)   # 主强调
YELLOW = RGBColor(0xFF, 0xD4, 0x00)   # 次强调
CYAN   = RGBColor(0x00, 0xD4, 0xE6)   # 第三色
GREEN  = RGBColor(0x16, 0xA3, 0x4A)   # 正向
RED    = RGBColor(0xDC, 0x26, 0x26)   # 负向/警示
BLACK  = RGBColor(0x12, 0x12, 0x12)   # 反色页底
INK    = RGBColor(0x1A, 0x1A, 0x1A)   # 正文
GRAY   = RGBColor(0x6B, 0x6B, 0x6B)   # 辅助文字
LGRAY  = RGBColor(0xA8, 0xA0, 0x94)   # 页码/浅符号
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
HAIR   = RGBColor(0xE5, 0xDE, 0xD2)   # 卡片描边

BODY = "PingFang SC"       # 正文/标题：现代黑体
NUM  = "Helvetica Neue"    # 大数字

W = Inches(13.333)
H = Inches(7.5)
M = Inches(0.6)            # 左右留白
CW = W - 2 * M             # 内容宽
TOTAL = 19                 # 页数基数（不够就改）

prs = None


def _set_ea(run, typeface):
    rPr = run._r.get_or_add_rPr()
    for tag in ('a:ea', 'a:cs'):
        el = rPr.find(qn(tag))
        if el is None:
            el = parse_xml('<%s xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="%s"/>' % (tag, typeface))
            rPr.append(el)
        else:
            el.set('typeface', typeface)


def new_deck():
    """新建一份 16:9 空白演示文稿，全部页面米白底。"""
    global prs
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    return prs


def slide(bg=PAPER):
    """新建一页。反色页传 slide(BLACK) / slide(PINK)。"""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    f = s.background.fill
    f.solid()
    f.fore_color.rgb = bg
    return s


def rect(s, l, t, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE):
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
    """paras = [[(文本, 字号, 粗体, 颜色, 字体), ...], ...]；缺省后两项自动补。"""
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


def pageno(s, page, color=LGRAY):
    """右下角页码 x / TOTAL（每页必加）。"""
    text(s, Inches(11.9), Inches(7.02), Inches(1.3), Inches(0.3),
         [[("%d / %d" % (page, TOTAL), 10, False, color, BODY)]], align=PP_ALIGN.RIGHT)


def head(s, label, ttl, page, tsize=38, label_color=PINK, tcolor=INK):
    """标准页头：左上小标签 + 大标题 + 右下页码。除封面/反色页外每页都用。"""
    text(s, M, Inches(0.30), Inches(4.6), Inches(0.34),
         [[(label, 13, True, label_color, BODY)]], spacing=1.0)
    text(s, M, Inches(0.72), CW, Inches(0.95), [[(ttl, tsize, True, tcolor, BODY)]], spacing=1.06)
    pageno(s, page)


def note(s, txt, top=Inches(6.62), color=GRAY, size=11):
    """页脚小字：数据出处 / 备注。数据页必填。"""
    text(s, M, top, CW, Inches(0.32), [[(txt, size, False, color, BODY)]])


def band(s, txt, top, h=0.72, fill=BLACK, color=WHITE, size=20, left=None, width=None):
    """整幅结论条：一句话结论压底。"""
    left = M if left is None else left
    width = CW if width is None else width
    rect(s, left, top, width, h, fill=fill)
    text(s, left + Inches(0.26), top, width - Inches(0.52), h,
         [[(txt, size, True, color, BODY)]], anchor=MSO_ANCHOR.MIDDLE)


def save(path):
    prs.save(path)
    print("saved:", path)
