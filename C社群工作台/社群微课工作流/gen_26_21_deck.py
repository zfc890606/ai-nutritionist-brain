#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周五微课堂 26-21期《全营养轻断食·执行要点》— Yellow × Black Editorial
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


def footer(s, txt, fill=BLACK, color=YELLOW, size=16, top=Inches(6.05)):
    rect(s, M, top, CW, Inches(0.8), fill=fill)
    text(s, M + Inches(0.24), top, CW - Inches(0.48), Inches(0.8),
         [[(txt, size, True, color, SANS)]], anchor=MSO_ANCHOR.MIDDLE)


# ══════════════ 1 · 封面 ══════════════
s = slide()
rect(s, 0, 0, W, Inches(0.42), fill=BLACK)
text(s, M, Inches(0.02), CW, Inches(0.4), [[("每周五健康共修微课堂", 12, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, W - M - Inches(3.0), Inches(0.02), Inches(3.0), Inches(0.4),
     [[("26-21 期", 12, True, YELLOW, SANS)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

text(s, M, Inches(1.42), CW, Inches(0.6), [[("5+2 · 全营养支持的减脂模式", 15, True, GRAY, SANS)]])
text(s, M, Inches(2.02), Inches(11.6), Inches(1.9),
     [[("全营养轻断食", 76, True, BLACK, SERIF)], [("执行要点", 52, True, BLACK, SERIF)]], spacing=1.05)
rect(s, M, Inches(4.42), Inches(2.6), Pt(7), fill=BLACK)
text(s, M, Inches(4.78), Inches(10.6), Inches(0.7),
     [[("怎么控卡，怎么补营养——一周挑两天就够了", 22, False, INK, SANS)]])
rect(s, M, Inches(5.58), Inches(4.6), Inches(0.62), fill=BLACK)
text(s, M + Inches(0.22), Inches(5.58), Inches(4.4), Inches(0.62),
     [[("主讲 · 本群主理人 张医生", 16, True, YELLOW, SANS)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(6.5), CW, Inches(0.4), [[("今晚 19:30 · 社群开讲", 13, False, GRAY, SANS)]])

# ══════════════ 2 · 目录 ══════════════
s = slide()
eyebrow(s, "目 录", "02")
title(s, "今天讲五件事")
items = [("01", "什么叫「全营养轻断食」"),
         ("02", "执行要点一：控卡（5+2 · 600/500千卡）"),
         ("03", "执行要点二：保营养（全营养）"),
         ("04", "饿了怎么扛 · 额外的价值"),
         ("05", "方案 + 真实见证")]
y = Inches(2.72)
for num, txt in items:
    rect(s, M, y, Inches(0.62), Inches(0.62), fill=BLACK)
    text(s, M, y, Inches(0.62), Inches(0.62), [[(num, 20, True, YELLOW, LATIN)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + Inches(0.95), y, Inches(10.4), Inches(0.62), [[(txt, 23, True, INK, SERIF)]],
         anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.78)

# ══════════════ 3 · 民间偏方到科学殿堂 ══════════════
s = slide()
eyebrow(s, "第一部分 · 来历", "03")
title(s, "从民间偏方，到科学殿堂", size=36)
bullets(s, [
    ("七千年历史  ", "——斋月 · 辟谷，古人早就在做，只是没这个名字"),
    ("2016 · 诺贝尔奖  ", "——大隅良典发现「细胞自噬」机制"),
    ("2021 · 中国官方指南  ", "——首次把轻断食写进医学指南"),
    ("2024 · 卫健委  ", "——《肥胖症诊疗指南》，推动全民「体重管理年」"),
], top=Inches(2.75), size=20, gap=0.72)

# ══════════════ 4 · 细胞自噬 ══════════════
s = slide()
eyebrow(s, "第一部分 · 原理", "04")
title(s, "身体自带一场「大扫除」", size=36)
text(s, M, Inches(2.5), CW, Inches(0.8),
     [[("细胞自噬 = 身体「自己吃自己」。", 28, True, BLACK, SANS)]], spacing=1.0)
bullets(s, [
    ("饿的时候  ", "——身体优先吃掉衰老、破损、癌变的细胞，拿来供能"),
    ("轻断食  ", "——正好能启动这个机制"),
    ("所以  ", "——它能抗衰，让身体更「新」"),
], top=Inches(3.5), size=20, gap=0.72)

# ══════════════ 5 · 局限性空白 ══════════════
s = slide()
eyebrow(s, "第一部分 · 安全", "05")
title(s, "官方方案里，它的「副作用」一栏几乎是空白", size=30)
bullets(s, [
    ("国家认可的减重方案都列出来了  ", "——限制能量、低能量……里面就有轻断食"),
    ("别的方案  ", "——底下要写一堆注意事项、禁忌人群"),
    ("轻断食  ", "——这一栏干干净净，北京协和等大医院都在做"),
], top=Inches(2.85), size=19, gap=0.8)
footer(s, "科学认了、官方认了——我们就放心做。", size=17, top=Inches(6.2))

# ══════════════ 6 · 核心一句话 ══════════════
s = slide()
eyebrow(s, "第一部分 · 核心", "06")
title(s, "记住这六个字", size=36)
text(s, M, Inches(2.6), CW, Inches(1.8),
     [[("控卡 + 保营养", 46, True, BLACK, SERIF)]], spacing=1.1)
rect(s, M, Inches(3.95), CW, Inches(0.05), fill=BLACK)
bullets(s, [
    ("一周挑两天，把量压下来  ", "——让身体去烧它自己存的脂肪"),
    ("但不能光饿  ", "——得把营养喂够"),
    ("全营养支持的轻断食减脂模式  ", "——就这两个动作"),
], top=Inches(4.4), size=20, gap=0.72)

# ══════════════ 7 · 5+2怎么排 ══════════════
s = slide()
eyebrow(s, "要点一 · 5+2", "07")
title(s, "5+2：一周挑两天，就够了", size=36)
bullets(s, [
    ("一周 7 天  ", "——5 天正常吃，2 天做「轻断食日」"),
    ("这两天的规矩  ", "——不连着（周一+周四 / 周二+周五）"),
    ("灵活  ", "——哪天有应酬、要喝酒，就顺延一天，你自己说了算"),
    ("不用  ", "——天天吃沙拉、天天泡健身房那种苦日子"),
], top=Inches(2.75), size=19, gap=0.72)

# ══════════════ 8 · 控卡硬标准 ══════════════
s = slide()
eyebrow(s, "要点一 · 控卡", "08")
title(s, "控卡有个硬标准", size=34)
stat(s, M, Inches(2.55), Inches(5.6), "600", "轻断食日 · 男性（千卡）", big_size=58)
rect(s, M + Inches(5.9), Inches(2.5), Pt(3), Inches(2.3), fill=BLACK)
stat(s, M + Inches(6.3), Inches(2.55), Inches(5.6), "500", "轻断食日 · 女性（千卡）", big_size=58)
rect(s, M, Inches(5.2), CW, Inches(0.95), fill=BLACK)
text(s, M + Inches(0.24), Inches(5.2), CW - Inches(0.48), Inches(0.95),
     [[("正常一天：男性 2300 / 女性 1800 千卡——不够就对了，身体去烧脂肪。", 19, True, YELLOW, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)

# ══════════════ 9 · 不掉肌肉 ══════════════
s = slide()
eyebrow(s, "要点一 · 为什么有效", "09")
title(s, "为什么它不掉肌肉，专减内脏脂肪", size=30)
bullets(s, [
    ("身体先用脂肪、后用蛋白质  ", "——蛋白质是最后才动用的"),
    ("脂肪一烧  ", "——内脏脂肪下来 · 血管脂肪下来 · 肚子下来"),
    ("减内脏脂肪  ", "——这是最直接的一套"),
], top=Inches(2.85), size=20, gap=0.85)
footer(s, "你现在要的是健康——那盯的就是内脏脂肪。", size=17, top=Inches(6.2))

# ══════════════ 10 · 光控卡不行 ══════════════
s = slide()
eyebrow(s, "要点一 · 别踩坑", "10")
title(s, "光控卡行不行？——不行", size=36)
bullets(s, [
    ("靠鸡蛋+玉米+粥凑 600 千卡  ", "——能做到，也确实能减脂"),
    ("但长期这样  ", "——营养跟不上，是「拿健康换体重」"),
    ("要不要？  ", "——不要。所以要配上第二个动作"),
], top=Inches(2.85), size=20, gap=0.85)
footer(s, "控卡只解决「量」，营养还得单独解决。", size=17, top=Inches(6.2))

# ══════════════ 11 · 全营养 ══════════════
s = slide()
eyebrow(s, "要点二 · 保营养", "11")
title(s, "把七大营养素，一样不缺地补齐", size=32)
bullets(s, [
    ("蛋白质 · 维生素 · 矿物质 · 好脂肪 · 水……  ", "——每一样都在给机能打底"),
    ("做法  ", "——控卡不变，用营养素工具按营养师比例配齐"),
    ("量  ", "——男性三餐约 546 千卡 · 女性 500 以内"),
], top=Inches(2.75), size=19, gap=0.78)
footer(s, "量控住，营养喂够——既减得下来，又不伤身。", size=17, top=Inches(6.2))

# ══════════════ 12 · 饿了怎么扛 ══════════════
s = slide()
eyebrow(s, "执行技巧", "12")
title(s, "饿了，怎么扛过去？", size=36)
bullets(s, [
    ("先定性  ", "——饥饿感是「条件反射」，不是身体真缺能量"),
    ("扛 1–1.5 小时  ", "——肝糖原上场 → 脂肪供能 → 就不饿了"),
    ("转移注意力  ", "——喝水 · 无糖饮料 · 咖啡 · 打游戏 · 做课件 · 睡觉"),
    ("越做越轻松  ", "——身体适应后，饥饿感越来越轻"),
], top=Inches(2.75), size=19, gap=0.72)

# ══════════════ 13 · 额外好处 ══════════════
s = slide()
eyebrow(s, "额外价值", "13")
title(s, "它额外给你的三样", size=36)
cards = [("01", "改善胰岛素敏感性", "对血糖管理有实实在在的帮助"),
         ("02", "让大脑更清醒", "促进神经营养因子，帮助维持认知"),
         ("03", "延缓衰老", "细胞自噬，清理衰老、破损的细胞")]
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

# ══════════════ 14 · 九个字 ══════════════
s = slide()
eyebrow(s, "记住它", "14")
text(s, M, Inches(1.9), CW, Inches(0.5), [[("九个字，记住就好", 15, True, GRAY, SANS)]])
text(s, M, Inches(2.7), Inches(12.0), Inches(2.4),
     [[("调体质 · 保健康 · 延寿命", 54, True, BLACK, SERIF)]], spacing=1.2)
rect(s, M, Inches(4.6), Inches(2.6), Pt(7), fill=BLACK)
text(s, M, Inches(4.95), CW, Inches(0.8),
     [[("这就是轻断食的意义——不只是瘦，是把整个人的状态调回去。", 19, False, INK, SANS)]])

# ══════════════ 15 · 方案 + 见证 ══════════════
s = slide()
eyebrow(s, "方案收口", "15")
title(s, "全营养轻断食 = 控卡 + 保营养", size=32)
bullets(s, [
    ("轻断食日（每周两天，不连）  ", "——营养素餐配齐，男性约546 / 女性500以内"),
    ("其余五天  ", "——正常吃饭，鱼肉蛋奶照吃，不节食、不硬撑"),
    ("常态化  ", "——应酬完、出差回来，挑一天，把状态快速拉回来"),
    ("真实见证  ", "——学员、董博士、龚教授：外行都学得会，普通人做得到"),
], top=Inches(2.72), size=18, gap=0.66)

# ══════════════ 16 · 行动号召 ══════════════
s = slide()
rect(s, 0, 0, W, H, fill=BLACK)
rect(s, 0, Inches(2.3), W, Inches(0.09), fill=YELLOW)
text(s, M, Inches(0.9), CW, Inches(0.5), [[("行动号召", 14, True, YELLOW, SANS)]])
text(s, M, Inches(1.18), Inches(11.6), Inches(1.0),
     [[("控卡 + 保营养", 40, True, YELLOW, SERIF)]], spacing=1.0)
text(s, M, Inches(2.72), Inches(11.8), Inches(1.6),
     [[("挑两天压住度（男600 / 女500千卡），把七大营养补齐——", 21, False, WHITE, SANS)],
      [("饿了扛一两个小时就过去，把它变成生活里的一个习惯。", 21, False, WHITE, SANS)]], spacing=1.35)
rect(s, M, Inches(4.68), Inches(8.4), Inches(0.68), fill=YELLOW)
text(s, M + Inches(0.22), Inches(4.68), Inches(8.1), Inches(0.68),
     [[("想要一份属于你的「5+2轻断食执行方案」 → 私信张医生", 15, True, BLACK, SANS)]],
     anchor=MSO_ANCHOR.MIDDLE)
text(s, M, Inches(5.75), CW, Inches(0.5),
     [[("调体质 · 保健康 · 延寿命　|　下周五，健康微课堂，不见不散！", 15, False, YELLOW, SANS)]])
text(s, M, Inches(6.6), CW, Inches(0.4),
     [[("以上为健康科普分享，不构成诊疗建议，个体情况请咨询专业医师。", 11, False, GRAY, SANS)]])

# ───────────── Save ─────────────
out = "/Users/mac/Documents/zfc最强大脑/C社群工作台/社群微课工作流/全营养轻断食执行要点-26-21期.pptx"
prs.save(out)
print("Saved:", out, "| slides:", len(prs.slides._sldIdLst))
