# -*- coding: utf-8 -*-
"""Render console-window screenshots from the recorded sessions."""
import io, json, os
from PIL import Image, ImageDraw, ImageFont

WORK = r'D:\learning\C语言程序设计\实验4\_work'
SHOTS = os.path.join(WORK, 'shots')
os.makedirs(SHOTS, exist_ok=True)

data = json.load(io.open(os.path.join(WORK, 'sessions.json'), encoding='utf-8'))
displays = data['displays']

FONT_PATH = r'C:\Windows\Fonts\simsun.ttc'
SIZE = 21
LINE_H = 32
PAD = 26
TITLE_H = 38
BG = (12, 12, 12)
FG = (220, 220, 220)
CMD = (255, 255, 255)

font = ImageFont.truetype(FONT_PATH, SIZE, index=1)   # NSimSun
tfont = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 15, index=0)
print('console font:', font.getname(), 'title font:', tfont.getname())


def text_w(s, f):
    return f.getlength(s)


for n in sorted(displays, key=int):
    lines = displays[n]
    widths = [text_w(l, font) for l in lines] or [0]
    inner_w = int(max(widths)) + 2
    w = inner_w + PAD * 2
    h = TITLE_H + PAD * 2 + LINE_H * len(lines)

    img = Image.new('RGB', (w, h), BG)
    d = ImageDraw.Draw(img)
    # window frame + title bar
    d.rectangle([0, 0, w - 1, TITLE_H], fill=(243, 243, 243))
    d.rectangle([0, 0, w - 1, h - 1], outline=(160, 160, 160))
    d.text((12, (TITLE_H - 15) // 2 - 1), '命令提示符', font=tfont, fill=(40, 40, 40))
    # window buttons (minimise / maximise / close), each 46px wide
    cy = TITLE_H // 2
    cx_min = w - 3 * 46 + 23
    cx_max = w - 2 * 46 + 23
    cx_cls = w - 1 * 46 + 23
    d.line([(cx_min - 5, cy), (cx_min + 5, cy)], fill=(70, 70, 70), width=1)
    d.rectangle([cx_max - 5, cy - 5, cx_max + 5, cy + 5], outline=(70, 70, 70))
    d.line([(cx_cls - 5, cy - 5), (cx_cls + 5, cy + 5)], fill=(70, 70, 70), width=1)
    d.line([(cx_cls - 5, cy + 5), (cx_cls + 5, cy - 5)], fill=(70, 70, 70), width=1)

    y = TITLE_H + PAD - 4
    for line in lines:
        color = CMD if line.startswith('D:\\learning') else FG
        d.text((PAD, y), line, font=font, fill=color)
        y += LINE_H

    out = os.path.join(SHOTS, 'task%s.png' % n)
    img.save(out)
    print('saved', out, img.size)
print('DONE')
