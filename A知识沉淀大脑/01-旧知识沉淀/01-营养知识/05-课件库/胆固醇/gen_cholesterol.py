# -*- coding: utf-8 -*-
"""
胆固醇 · 逻辑拆解课件生成脚本
House style：奶油底 + 粉/黄/青强调色（对齐 gen_diabetes.py）
输出：胆固醇·逻辑拆解.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
import os

# ---------- 配色 ----------
C = {
    'CREAM':      RGBColor(0xFA, 0xF3, 0xE0),
    'CREAM_LT':   RGBColor(0xFF, 0xF8, 0xEC),
    'PINK':       RGBColor(0xFF, 0x00, 0x66),
    'YELLOW':     RGBColor(0xFF, 0xD7, 0x00),
    'CYAN':       RGBColor(0x00, 0xBF, 0xFF),
    'BLACK':      RGBColor(0x22, 0x22, 0x22),
    'DARK':       RGBColor(0x44, 0x44, 0x44),
    'MED':        RGBColor(0x8A, 0x80, 0x78),
    'WHITE':      RGBColor(0xFF, 0xFF, 0xFF),
    'CARD':       RGBColor(0xFF, 0xFD, 0xF7),
    'GREEN':      RGBColor(0x2E, 0xA0, 0x43),
    'RED':        RGBColor(0xD1, 0x3A, 0x3A),
}
FONT = 'PingFang SC'

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = prs.slide_width, prs.slide_height

# ---------- helpers ----------
def add_slide(bgcolor=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    f = s.background.fill
    f.solid()
    f.fore_color.rgb = bgcolor or C['CREAM']
    return s

def tb(slide, l, t, w, h, txt, sz=18, clr=None, bold=False,
       align=PP_ALIGN.LEFT, font=FONT, anchor=MSO_ANCHOR.TOP, line=None, italic=False):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    try:
        tf.vertical_anchor = anchor
    except Exception:
        pass
    lines = txt.split('\n') if isinstance(txt, str) else txt
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line:
            p.line_spacing = line
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(sz)
        r.font.bold = bold
        r.font.italic = italic
        r.font.name = font
        r.font.color.rgb = clr or C['BLACK']
    return box

def rect(slide, l, t, w, h, fill, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08):
    sh = slide.shapes.add_shape(shape, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(1.5)
    sh.shadow.inherit = False
    try:
        sh.adjustments[0] = radius
    except Exception:
        pass
    return sh

def kicker(slide, txt, clr=None):
    rect(slide, Inches(0.6), Inches(0.5), Inches(0.16), Inches(0.42), clr or C['PINK'])
    tb(slide, Inches(0.9), Inches(0.45), Inches(11.5), Inches(0.5),
       txt, sz=15, clr=clr or C['PINK'], bold=True)

def headline(slide, txt, sz=34, clr=None, t=1.15):
    tb(slide, Inches(0.6), Inches(t), Inches(12.1), Inches(1.0),
       txt, sz=sz, clr=clr or C['BLACK'], bold=True)

def card(slide, l, t, w, h, title, body, accent=C['PINK'], tsz=18, bsz=13):
    rect(slide, l, t, w, h, C['CARD'], line=accent, radius=0.06)
    rect(slide, l, t, Inches(0.12), h, accent, radius=0.5)
    tb(slide, l + Inches(0.28), t + Inches(0.14), w - Inches(0.45), Inches(0.5),
       title, sz=tsz, clr=accent, bold=True)
    tb(slide, l + Inches(0.28), t + Inches(0.62), w - Inches(0.45), h - Inches(0.72),
       body, sz=bsz, clr=C['DARK'], line=1.25)

def footer(slide, n):
    tb(slide, Inches(0.6), Inches(7.02), Inches(9), Inches(0.35),
       '胆固醇 · 逻辑拆解手册    |    张医生 · AI营养师', sz=10, clr=C['MED'])
    tb(slide, Inches(12.2), Inches(7.02), Inches(0.7), Inches(0.35),
       str(n), sz=11, clr=C['MED'], align=PP_ALIGN.RIGHT)

# ============================================================
# S1 · 封面
# ============================================================
s = add_slide(C['BLACK'])
rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.28), C['PINK'])
rect(s, Inches(0), Inches(7.22), Inches(13.333), Inches(0.28), C['YELLOW'])
tb(s, Inches(0.9), Inches(1.6), Inches(11.5), Inches(0.6),
   'HDL / LDL / 内源合成', sz=18, clr=C['CYAN'], bold=True)
tb(s, Inches(0.9), Inches(2.35), Inches(11.8), Inches(2.2),
   '胆固醇高，\n不是吃出来的', sz=62, clr=C['WHITE'], bold=True, line=1.05)
tb(s, Inches(0.95), Inches(4.9), Inches(11.5), Inches(0.9),
   '内源合成逻辑拆解  ＋  三管齐下解决方案', sz=24, clr=C['YELLOW'], bold=True)
tb(s, Inches(0.95), Inches(5.9), Inches(11.5), Inches(0.6),
   '人体 70%–80% 的胆固醇是肝脏自己造的，只有 20%–30% 来自饮食', sz=15, clr=C['CREAM'])
tb(s, Inches(0.95), Inches(6.5), Inches(11.5), Inches(0.5),
   '张医生 · AI营养师', sz=14, clr=C['MED'])

# ============================================================
# S2 · 认知纠偏 2:8
# ============================================================
s = add_slide()
kicker(s, '认知纠偏')
headline(s, '血里的胆固醇，到底从哪来？')
# 两个大块
rect(s, Inches(0.9), Inches(2.5), Inches(5.5), Inches(3.6), C['CARD'], line=C['CYAN'], radius=0.05)
tb(s, Inches(1.2), Inches(2.75), Inches(5.0), Inches(0.6), '外源 · 吃进来', sz=20, clr=C['CYAN'], bold=True)
tb(s, Inches(1.2), Inches(3.5), Inches(5.0), Inches(1.4), '20% – 30%', sz=52, clr=C['CYAN'], bold=True)
tb(s, Inches(1.2), Inches(4.7), Inches(5.0), Inches(1.2),
   '只来自动物性食物\n蛋黄 · 内脏 · 脑髓 · 肥肉', sz=14, clr=C['DARK'], line=1.3)
rect(s, Inches(6.9), Inches(2.5), Inches(5.5), Inches(3.6), C['CARD'], line=C['PINK'], radius=0.05)
tb(s, Inches(7.2), Inches(2.75), Inches(5.0), Inches(0.6), '内源 · 肝脏自己造', sz=20, clr=C['PINK'], bold=True)
tb(s, Inches(7.2), Inches(3.5), Inches(5.0), Inches(1.4), '70% – 80%', sz=52, clr=C['PINK'], bold=True)
tb(s, Inches(7.2), Inches(4.7), Inches(5.0), Inches(1.2),
   '肝脏合成一半以上\n小肠 · 皮肤 · 肾上腺补其余', sz=14, clr=C['DARK'], line=1.3)
tb(s, Inches(0.9), Inches(6.3), Inches(11.6), Inches(0.5),
   '结论：胆固醇高，重点不是"少吃蛋黄"，而是肝脏为什么造太多、身体为什么清不掉。',
   sz=15, clr=C['BLACK'], bold=True)
footer(s, 2)

# ============================================================
# S3 · 核心公式
# ============================================================
s = add_slide()
kicker(s, '逻辑核心', C['CYAN'])
headline(s, '一个公式看懂高胆固醇')
rect(s, Inches(1.2), Inches(2.7), Inches(10.9), Inches(1.7), C['BLACK'], radius=0.08)
tb(s, Inches(1.2), Inches(2.95), Inches(10.9), Inches(1.2),
   '血胆固醇  ＝  生成  −  清除', sz=40, clr=C['WHITE'], bold=True, align=PP_ALIGN.CENTER)
card(s, Inches(0.9), Inches(4.75), Inches(5.4), Inches(1.55),
     '生成端 ↑', '肝脏内源合成（HMGCR 油门）\n胆汁酸回收后肝脏"加班补货"',
     accent=C['PINK'], bsz=13)
card(s, Inches(7.0), Inches(4.75), Inches(5.4), Inches(1.55),
     '清除端 ↓', 'LDL 受体把坏胆固醇回收进肝\n胆汁酸→粪便 排出通道',
     accent=C['GREEN'], bsz=13)
footer(s, 3)

# ============================================================
# S4 · 肝脏三件套
# ============================================================
s = add_slide()
kicker(s, '机制')
headline(s, '肝脏里的"三件套"')
card(s, Inches(0.9), Inches(2.5), Inches(3.75), Inches(3.8), '① HMGCR',
     '胆固醇合成的\n总闸门 / 限速酶。\n\n它快，\n胆固醇就多。', accent=C['PINK'], bsz=15)
card(s, Inches(4.85), Inches(2.5), Inches(3.75), Inches(3.8), '② SREBP-2',
     '细胞里的\n胆固醇传感器。\n\n肝里胆固醇低，\n它就开足马力\n催合成。', accent=C['YELLOW'], bsz=15)
card(s, Inches(8.8), Inches(2.5), Inches(3.75), Inches(3.8), '③ LDL 受体',
     '把血里 LDL\n回收进肝的抓手。\n\n抓手少，\n血胆固醇高。', accent=C['CYAN'], bsz=15)
tb(s, Inches(0.9), Inches(6.5), Inches(11.6), Inches(0.5),
   '这三个名字，决定了胆固醇"造多少"和"清多快"。', sz=14, clr=C['BLACK'], bold=True)
footer(s, 4)

# ============================================================
# S5 · 恒温器
# ============================================================
s = add_slide()
kicker(s, '稳态')
headline(s, '一套"恒温器"，失灵就出事')
rect(s, Inches(0.9), Inches(2.45), Inches(11.6), Inches(0.9), C['CARD'], line=C['GREEN'], radius=0.08)
tb(s, Inches(1.15), Inches(2.6), Inches(11.1), Inches(0.6),
   '肝里胆固醇低  →  SREBP-2 激活  →  HMGCR↑ 多造  ＋  LDL受体↑ 多回收', sz=15, clr=C['DARK'])
rect(s, Inches(0.9), Inches(3.5), Inches(11.6), Inches(0.9), C['CARD'], line=C['CYAN'], radius=0.08)
tb(s, Inches(1.15), Inches(3.65), Inches(11.1), Inches(0.6),
   '肝里胆固醇高  →  HMGCR 被抑制  →  合成下降（正常刹车）', sz=15, clr=C['DARK'])
rect(s, Inches(0.9), Inches(4.9), Inches(11.6), Inches(1.55), C['PINK'], radius=0.06)
tb(s, Inches(0.9), Inches(5.05), Inches(11.6), Inches(1.2),
   '胆固醇高 ＝ 恒温器失灵', sz=26, clr=C['WHITE'], bold=True, align=PP_ALIGN.CENTER)
tb(s, Inches(0.9), Inches(5.75), Inches(11.6), Inches(0.6),
   '要么油门卡死（合成过多），要么刹车不灵（回收 / 排泄受阻）',
   sz=14, clr=C['CREAM'], align=PP_ALIGN.CENTER)
footer(s, 5)

# ============================================================
# S6 · 六成因总览
# ============================================================
s = add_slide()
kicker(s, '核心章节 · 内源合成过多')
headline(s, '肝脏为什么会造太多？6 大成因')
items = [
    ('① 遗传', 'LDL受体缺陷\n家族性高胆固醇'),
    ('② 胰岛素抵抗', '代谢综合征\nVLDL→小而密LDL'),
    ('③ 肥胖', '肝 HMGCR 活性\n比常人高约 60%'),
    ('④ 饮食', '饱和脂肪\n精制糖 / 果糖'),
    ('⑤ 纤维不足', '胆汁酸循环受阻\n排污管堵死'),
    ('⑥ 甲减 / 停药', '清除变慢\n他汀反跳'),
]
l0, t0, cw, ch, gx, gy = Inches(0.9), Inches(2.45), Inches(3.72), Inches(1.75), Inches(0.22), Inches(0.28)
for i, (t, b) in enumerate(items):
    r, c = divmod(i, 3)
    x = l0 + (cw + gx) * c
    y = t0 + (ch + gy) * r
    acc = [C['PINK'], C['CYAN'], C['YELLOW']][i % 3]
    card(s, x, y, cw, ch, t, b, accent=acc, tsz=16, bsz=12)
footer(s, 6)

# ============================================================
# S7 · 成因① 遗传
# ============================================================
s = add_slide()
kicker(s, '成因 ① · 最硬的成因', C['PINK'])
headline(s, 'LDL 受体缺陷 / 家族性高胆固醇')
tb(s, Inches(0.9), Inches(2.4), Inches(11.6), Inches(2.0),
   'LDL 受体基因（LDLR）突变 → 肝细胞"抓手"变少 → 血里 LDL 清不掉；\n'
   '同时肝内胆固醇不足，SREBP-2 反向激活 HMGCR → 合成更多。\n'
   '清除变差 ＋ 合成变多，双重叠加。', sz=16, clr=C['DARK'], line=1.35)
card(s, Inches(0.9), Inches(4.5), Inches(5.4), Inches(1.7), '关键数据',
     '约 85%–90% 的家族性高胆固醇变异在 LDLR 基因\n'
     '杂合子 LDL-C ≈ 常人 2 倍；纯合子可达 400–1000 mg/dL',
     accent=C['PINK'], bsz=13)
card(s, Inches(7.0), Inches(4.5), Inches(5.4), Inches(1.7), '识别线索',
     'LDL-C ≥ 4.9 mmol/L\n父母/兄弟姐妹同样高、年轻就心梗、跟腱黄色瘤',
     accent=C['CYAN'], bsz=13)
tb(s, Inches(0.9), Inches(6.4), Inches(11.6), Inches(0.5),
   '要点：这类"主因压过饮食"，必须就医 + 基因筛查 + 家族级联筛查。', sz=14, clr=C['RED'], bold=True)
footer(s, 7)

# ============================================================
# S8 · 成因② 胰岛素抵抗
# ============================================================
s = add_slide()
kicker(s, '成因 ② · 现代人最常见', C['CYAN'])
headline(s, '胰岛素抵抗 / 代谢综合征')
rect(s, Inches(0.9), Inches(2.45), Inches(11.6), Inches(1.0), C['CARD'], line=C['CYAN'], radius=0.08)
tb(s, Inches(1.15), Inches(2.62), Inches(11.1), Inches(0.7),
   '胰岛素抵抗 → 肝脏大量分泌富含甘油三酯的 VLDL\n'
   '→ 经 CETP / 肝脂酶交换 → 生成"小而密 LDL（sdLDL）"', sz=15, clr=C['DARK'], line=1.2)
card(s, Inches(0.9), Inches(3.7), Inches(5.4), Inches(2.3), '为什么更坏',
     'sdLDL 更易钻进血管壁，更易致动脉粥样硬化；\n'
     '但它的胆固醇含量低——所以常规 LDL-C 可能看着"正常"，\n'
     '实际颗粒数已在升高，风险被低估。',
     accent=C['PINK'], bsz=13)
card(s, Inches(7.0), Inches(3.7), Inches(5.4), Inches(2.3), '识别线索',
     '腰围大 · 甘油三酯高 · HDL 低\n空腹血糖偏高 · 脂肪肝\n\n'
     '这条链常早于糖尿病出现。',
     accent=C['CYAN'], bsz=13)
tb(s, Inches(0.9), Inches(6.25), Inches(11.6), Inches(0.55),
   '断链关键：减精制糖、减内脏脂肪、增肌运动，改善胰岛素敏感性。', sz=14, clr=C['BLACK'], bold=True)
footer(s, 8)

# ============================================================
# S9 · 成因③ 肥胖
# ============================================================
s = add_slide()
kicker(s, '成因 ③', C['YELLOW'])
headline(s, '肥胖：肝脏在超额值班')
rect(s, Inches(2.2), Inches(2.7), Inches(8.9), Inches(2.1), C['BLACK'], radius=0.08)
tb(s, Inches(2.2), Inches(2.95), Inches(8.9), Inches(0.7),
   '肥胖者肝 HMG-CoA 还原酶活性', sz=20, clr=C['CREAM'], align=PP_ALIGN.CENTER)
tb(s, Inches(2.2), Inches(3.5), Inches(8.9), Inches(1.1),
   '比正常体重者高约 60%', sz=38, clr=C['YELLOW'], bold=True, align=PP_ALIGN.CENTER)
card(s, Inches(0.9), Inches(5.05), Inches(5.4), Inches(1.5), '机制',
     '肥胖常伴随全身胆固醇合成增加，\n肝脏是胆固醇产量上升的主要贡献者。',
     accent=C['PINK'], bsz=13)
card(s, Inches(7.0), Inches(5.05), Inches(5.4), Inches(1.5), '最划算的一步',
     '减重 5%–10%，\nLDL 与整体血脂谱同步改善。',
     accent=C['GREEN'], bsz=13)
footer(s, 9)

# ============================================================
# S10 · 成因④ 饮食
# ============================================================
s = add_slide()
kicker(s, '成因 ④ · 怎么"喂"出内源合成过多', C['PINK'])
headline(s, '真正在喂养高胆固醇的，是这几样')
card(s, Inches(0.9), Inches(2.45), Inches(3.75), Inches(4.0), '饱和脂肪',
     '肥肉 · 黄油 · 奶油\n\n直接促进胆固醇吸收\n＋ 促进肝脏合成\n\n催合成 ↑',
     accent=C['PINK'], bsz=13)
card(s, Inches(4.85), Inches(2.45), Inches(3.75), Inches(4.0), '精制糖 / 果糖',
     '白米白面 · 甜点\n含糖饮料 · 果汁\n\n血糖飙升→胰岛素→\n肝脏把糖变甘油三酯\n→ VLDL → sdLDL\n\n催 VLDL ↑',
     accent=C['YELLOW'], bsz=13)
card(s, Inches(8.8), Inches(2.45), Inches(3.75), Inches(4.0), '反式脂肪',
     '植脂末 · 部分氢化油\n\n升 LDL、降 HDL\n最坏的一类脂肪\n\n双向恶化 ↑↑',
     accent=C['RED'], bsz=13)
tb(s, Inches(0.9), Inches(6.6), Inches(11.6), Inches(0.5),
   '一句话：喂养高胆固醇的是"饱和脂肪 + 精制糖/果糖 + 纤维不足"的组合，而不是鸡蛋本身。',
   sz=14, clr=C['BLACK'], bold=True)
footer(s, 10)

# ============================================================
# S11 · 成因⑤ 胆汁酸循环
# ============================================================
s = add_slide()
kicker(s, '成因 ⑤ · 被忽视的排出口', C['CYAN'])
headline(s, '纤维吃太少，等于把排污管堵了')
tb(s, Inches(0.9), Inches(2.4), Inches(11.6), Inches(1.9),
   '胆固醇的最大出口，是在肝里变成胆汁酸 → 排进肠道 → 随粪便排出。\n'
   '正常情况下，约 95% 的胆汁酸会被肠道回收送回肝脏（肠肝循环）。\n'
   '如果纤维不足、胆汁酸被截留排掉 → 肝脏回收到手的胆汁酸变少 → 以为"缺货" → 加班合成胆固醇来补。',
   sz=15, clr=C['DARK'], line=1.35)
card(s, Inches(0.9), Inches(4.5), Inches(5.4), Inches(1.7), '可溶性纤维',
     '燕麦β-葡聚糖 · 车前子 · 果胶 · 瓜尔胶\n'
     '结合胆汁酸 → 重吸收↓ → 肝脏把更多胆固醇转成胆汁酸排出。',
     accent=C['GREEN'], bsz=13)
card(s, Inches(7.0), Inches(4.5), Inches(5.4), Inches(1.7), '肠道菌群',
     '发酵纤维产短链脂肪酸(SCFA)，丙酸增多可抑制内源胆固醇合成；\n'
     '改变 FXR/FGF15 信号，调节胆固醇吸收与排泄。',
     accent=C['CYAN'], bsz=13)
tb(s, Inches(0.9), Inches(6.4), Inches(11.6), Inches(0.5),
   '这就是"吃得很素，血脂还是高"的机制解释。', sz=15, clr=C['RED'], bold=True)
footer(s, 11)

# ============================================================
# S12 · 成因⑥ 甲减/药物反跳
# ============================================================
s = add_slide()
kicker(s, '成因 ⑥')
headline(s, '两个常被忽略的幕后推手')
card(s, Inches(0.9), Inches(2.5), Inches(5.4), Inches(3.7), '甲状腺功能减退',
     '甲减会下调 LDL 受体、\n减慢 LDL 清除 → 血胆固醇升高。\n\n'
     '血脂顽固不降，\n要查甲功。',
     accent=C['CYAN'], bsz=15)
card(s, Inches(7.0), Inches(2.5), Inches(5.4), Inches(3.7), '药物反跳 / 核受体激活',
     '他汀抑制 HMGCR 后，肝会代偿性上调合成；\n'
     '突然停药，肝脏合成可骤增约 5 倍。\n\n'
     '某些药物（如利福平）经 PXR 诱导 HMGCR。\n\n'
     '降脂药不能自行骤停。',
     accent=C['PINK'], bsz=14)
footer(s, 12)

# ============================================================
# S13 · 解决方案总览
# ============================================================
s = add_slide(C['BLACK'])
tb(s, Inches(0.9), Inches(0.9), Inches(11.6), Inches(0.5), '解决方案', sz=16, clr=C['CYAN'], bold=True)
tb(s, Inches(0.9), Inches(1.35), Inches(11.6), Inches(0.9),
   '不是少吃胆固醇，而是三管齐下', sz=34, clr=C['WHITE'], bold=True)
cols = [
    ('① 减合成', '砍饱和脂肪\n戒反式脂肪\n控精制糖 / 果糖', C['PINK']),
    ('② 增清除', '每周运动 150 分钟\n减重 5%–10%\n查甲功', C['CYAN']),
    ('③ 促排泄', '可溶性纤维 5–10g/天\n植物甾醇约 2g/天', C['YELLOW']),
]
for i, (t, b, acc) in enumerate(cols):
    x = Inches(0.9) + Inches(3.95) * i
    rect(s, x, Inches(2.6), Inches(3.6), Inches(3.6), C['CARD'], line=acc, radius=0.05)
    tb(s, x + Inches(0.3), Inches(2.85), Inches(3.0), Inches(0.6), t, sz=22, clr=acc, bold=True)
    tb(s, x + Inches(0.3), Inches(3.7), Inches(3.0), Inches(2.3), b, sz=15, clr=C['DARK'], line=1.35)
tb(s, Inches(0.9), Inches(6.5), Inches(11.6), Inches(0.5),
   '总思路：肝脏造多少 − 身体清多快 − 肠道排多少，三条线一起改。', sz=14, clr=C['CREAM'])
footer(s, 13)

# ============================================================
# S14 · 膳食 + 生活方式
# ============================================================
s = add_slide()
kicker(s, '第一层 · 膳食重塑')
headline(s, '先改餐桌，再谈补剂')
card(s, Inches(0.9), Inches(2.45), Inches(5.4), Inches(4.05), '脂肪换质 + 纤维吃够',
     '• 饱和脂肪→不饱和脂肪\n（橄榄油 · 菜籽油 · 坚果 · 深海鱼）\n'
     '• 彻底避开反式脂肪\n（植脂末 · 部分氢化油）\n'
     '• 可溶性纤维 5–10 g/天\n（燕麦 · 豆类 · 苹果 · 车前子）\n'
     '• 植物甾醇约 2 g/天（LDL↓5–15%）',
     accent=C['GREEN'], bsz=13)
card(s, Inches(7.0), Inches(2.45), Inches(5.4), Inches(4.05), '第二层 · 生活方式',
     '• 运动：每周 ≥150 分钟中等强度有氧\n　＋ 每周 2 次力量训练\n'
     '• 减重 5%–10%\n'
     '• 戒烟 + 限酒\n'
     '• 睡眠与压力管理\n'
     '• 复查：4–6 周见效，12 周评估\n　之后每 6–12 周复测',
     accent=C['CYAN'], bsz=13)
tb(s, Inches(0.9), Inches(6.6), Inches(11.6), Inches(0.5),
   '砍精制糖与果糖、主食一半换全谷粗粮——这是断"VLDL→小而密LDL"链的关键。', sz=13, clr=C['BLACK'], bold=True)
footer(s, 14)

# ============================================================
# S15 · 营养素 + 医疗边界 + LDL目标
# ============================================================
s = add_slide()
kicker(s, '第三 / 四层 · 支持与边界', C['PINK'])
headline(s, '营养素支持  与  就医边界')
card(s, Inches(0.9), Inches(2.45), Inches(5.4), Inches(2.2), '营养素支持方向',
     '阻断胆固醇吸收：植物甾醇\n促胆汁酸排泄：可溶性纤维 · 益生元\n'
     '降甘油三酯：ω-3 鱼油\n护血管内皮：茶多酚 · 维C/E · 辅酶Q10',
     accent=C['GREEN'], bsz=12)
card(s, Inches(7.0), Inches(2.45), Inches(5.4), Inches(2.2), '必须就医的情形',
     'LDL-C ≥ 4.9 mmol/L 或强家族史\n→ 疑似家族性高胆固醇\n\n'
     '他汀不可自行骤停（反跳）\n生活方式不能替代药物（极高危）',
     accent=C['RED'], bsz=12)
rect(s, Inches(0.9), Inches(4.85), Inches(11.6), Inches(1.7), C['CARD'], line=C['PINK'], radius=0.05)
tb(s, Inches(1.15), Inches(4.98), Inches(11.1), Inches(0.5),
   'LDL-C 目标（《中国血脂管理指南 2023》）', sz=15, clr=C['PINK'], bold=True)
tb(s, Inches(1.15), Inches(5.5), Inches(11.1), Inches(0.95),
   '普通健康者  < 3.4 mmol/L\n'
   '40 岁以上糖尿病等高危  < 2.6 mmol/L\n'
   '极高危（已心梗/脑梗等）  < 1.8 mmol/L，且较基线降幅 > 50%',
   sz=13, clr=C['DARK'], line=1.3)
footer(s, 15)

# ============================================================
# S16 · 收尾
# ============================================================
s = add_slide(C['BLACK'])
rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.28), C['PINK'])
rect(s, Inches(0), Inches(7.22), Inches(13.333), Inches(0.28), C['YELLOW'])
tb(s, Inches(0.9), Inches(1.5), Inches(11.6), Inches(0.5),
   '记住这一句', sz=16, clr=C['CYAN'], bold=True)
tb(s, Inches(0.9), Inches(2.2), Inches(11.8), Inches(2.4),
   '胆固醇高 ＝\n合成太多 ＋ 清不掉 ＋ 排不出', sz=40, clr=C['WHITE'], bold=True, line=1.15)
tb(s, Inches(0.95), Inches(4.9), Inches(11.6), Inches(0.6),
   '别只盯着蛋黄——那是两成的账；真正要翻的，是肝上那八成的账。',
   sz=18, clr=C['YELLOW'], bold=True)
tb(s, Inches(0.95), Inches(6.3), Inches(11.6), Inches(0.6),
   '免责声明：本课件为营养健康科普分享，不构成诊疗建议，个体情况请咨询专业医师。',
   sz=11, clr=C['MED'])

# ---------- save ----------
out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, '胆固醇·逻辑拆解.pptx')
prs.save(out_path)
print('OK ->', out_path)
