"""Fig4_arch.png: Picture133.PNG with two labels corrected.

- per-window behavioural score written q_i (was tau, which denotes the
  revocation threshold in Chapter 4)
- second instantiation named "Fabric + Ethereum" (the undefined name
  "SynChain" removed), matching the text
Usage: python fig4_arch_patch.py <figures_dir>
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

FIG = sys.argv[1]
im = Image.open(os.path.join(FIG, "Picture133.PNG")).convert("RGB")
dr = ImageDraw.Draw(im)
INK = (20, 20, 20)
FONT = "C:/Windows/Fonts/seguisb.ttf"


def put(text, x, top, font):
    # place text so that its ink starts at (x, top)
    l, t, _, _ = font.getbbox(text)
    dr.text((x - l, top - t), text, font=font, fill=INK)


# 1. "trust scoring (tau)" -> "trust scoring (q_i)", centred on the old label
dr.rectangle((429, 189, 562, 214), fill=(238, 243, 248))
f = ImageFont.truetype(FONT, 18)
fs = ImageFont.truetype(FONT, 12)
head, q, sub, tail = "trust scoring (", "q", "i", ")"
w = f.getlength(head) + f.getlength(q) + fs.getlength(sub) + 1 + f.getlength(tail)
x = (433 + 556) / 2 - w / 2
top = 193
_, pt, _, _ = f.getbbox("(")
y = top - pt
dr.text((x, y), head, font=f, fill=INK); x += f.getlength(head)
dr.text((x, y), q, font=f, fill=INK); x += f.getlength(q)
dr.text((x, y + 9), sub, font=fs, fill=INK); x += fs.getlength(sub) + 1
dr.text((x, y), tail, font=f, fill=INK)

# 2. "II. SynChain / Fabric + / Ethereum / (enterprise / hybrid)" ->
#    "II. Fabric + / Ethereum / (enterprise / hybrid)"
dr.rectangle((1214, 400, 1337, 514), fill=(255, 255, 255))
g = ImageFont.truetype(FONT, 17)
put("Fabric +", 1221, 404, g)
put("Ethereum", 1217, 426, g)
put("(enterprise", 1217, 449, g)
put("hybrid)", 1217, 471, g)

im.save(os.path.join(FIG, "Fig4_arch.png"))
