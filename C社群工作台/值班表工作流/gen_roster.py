#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公益群 / 共修群 月度运营值班表生成器
=====================================
用法：
    python3 gen_roster.py templates/2026-11.json
    python3 gen_roster.py templates/2026-11.json --out "../公益群:共修群运营值班表-2026-11.xlsx"

输入 JSON 结构见 templates/2026-11.json。
输出：一个 .xlsx，两个 sheet（健康公益群 / 健康共修群），版式与 2026-10 原表一致。
"""

import json
import os
import sys
from copy import copy

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------- 设计常量
FONT_NAME = "微软雅黑"

COLUMNS = [
    ("A", "周次", 9),
    ("B", "日期", 13),
    ("C", "主理人", 10),
    ("D", "主持人", 12),
    ("E", "海报推广", 12),
    ("F", "工作一\n早晚营养餐打卡", 20),
    ("G", "工作二\n周二KOC故事分享会", 34),
    ("H", "工作三\n周五微课堂（主题）", 36),
    ("I", "微课堂讲师", 10),
]

THEMES = {
    "green": {
        "title_color": "1B5E20",
        "head_fill": "2E7D32",
        "accent_fill": "1565C0",   # 海报推广列的表头（蓝）
        "zebra": "F7FBF7",
    },
    "blue": {
        "title_color": "0D47A1",
        "head_fill": "1565C0",
        "accent_fill": None,
        "zebra": "F5F9FF",
    },
}

THIN = Side(style="thin", color="000000")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
COURSE_RED = "C62828"
TEXT_DARK = "212121"


def fill(color):
    return PatternFill("solid", fgColor=color)


def style_cell(cell, *, bold=False, size=10.5, color=TEXT_DARK,
               bg=None, align="center", wrap=True, border=True):
    cell.font = Font(name=FONT_NAME, size=size, bold=bold, color=color)
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=wrap)
    if bg:
        cell.fill = fill(bg)
    if border:
        cell.border = BORDER


def build_sheet(wb, sheet_name, display_name, period, theme_key, weeks, fixed_checkin,
                f_header=None):
    theme = THEMES[theme_key]
    ws = wb.create_sheet(title=sheet_name)

    # 标题行
    ws.merge_cells("A1:I1")
    ws["A1"] = f"《{display_name}》运营值班表（{period}）"
    style_cell(ws["A1"], bold=True, size=15, color=theme["title_color"], border=False)
    ws.row_dimensions[1].height = 36

    # 表头
    for col, title, width in COLUMNS:
        ws.column_dimensions[col].width = width
        c = ws[f"{col}2"]
        c.value = f_header if (col == "F" and f_header) else title
        bg = theme["head_fill"]
        if col == "E" and theme["accent_fill"]:
            bg = theme["accent_fill"]
        style_cell(c, bold=True, size=11, color="FFFFFF", bg=bg)
    ws.row_dimensions[2].height = 44

    # 周数据
    for i, w in enumerate(weeks):
        r = 3 + i
        zebra = theme["zebra"] if i % 2 == 1 else None
        ws.row_dimensions[r].height = 58

        values = {
            "A": w.get("week", f"第{'一二三四五六七八九十'[i]}周"),
            "B": w.get("date", ""),
            "C": w.get("host", ""),
            "D": w.get("mc", ""),
            "E": w.get("poster", w.get("host", "")),
            "F": w.get("checkin", fixed_checkin),
            "G": w.get("koc", ""),
            "H": w.get("course", ""),
            "I": w.get("lecturer", ""),
        }
        aligns = {"A": "center", "B": "center", "C": "center", "D": "center",
                  "E": "center", "F": "center", "G": "left", "H": "left", "I": "center"}

        for col, _, _ in COLUMNS:
            c = ws[f"{col}{r}"]
            c.value = values[col]
            if col == "H":
                style_cell(c, bold=True, size=10.5, color=COURSE_RED,
                           bg=zebra, align="left")
            else:
                style_cell(c, size=10.5, color=TEXT_DARK, bg=zebra, align=aligns[col])

    ws.freeze_panes = "A3"
    return ws


def main():
    if len(sys.argv) < 2:
        print("用法: python3 gen_roster.py <input.json> [--out <output.xlsx>]")
        sys.exit(1)

    src = sys.argv[1]
    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)

    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    else:
        out = data.get("output") or (
            os.path.splitext(os.path.basename(src))[0] + ".xlsx"
        )

    wb = Workbook()
    wb.remove(wb.active)

    pub = data["groups"]["公益群"]
    prac = data["groups"]["共修群"]

    build_sheet(
        wb, pub.get("sheet", "健康公益群"), "健康公益群",
        data["period"], pub.get("theme", "green"), pub["weeks"],
        pub.get("checkin", "每日早晚营养餐打卡，日常活群"),
        pub.get("f_header"),
    )
    build_sheet(
        wb, prac.get("sheet", "健康共修群"), "健康共修群",
        data["period"], prac.get("theme", "blue"), prac["weeks"],
        prac.get("checkin", "每日早晚营养餐打卡"),
        prac.get("f_header"),
    )

    wb.save(out)
    print(f"已生成: {os.path.abspath(out)}")


if __name__ == "__main__":
    main()
