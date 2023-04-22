from bs4 import BeautifulSoup as BSoup
import cssutils
import logging
from matplotlib import colors
import re

def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)

def hex2col(c):
    if '#' in c:
        h = c.lstrip('#')
        if len(h) == 6:
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            c = (r, g, b)
        elif len(h) == 3:
            r = int(h[0], 16) / 15 * 255
            g = int(h[1], 16) / 15 * 255
            b = int(h[2], 16) / 15 * 255
            c = (r, g, b)
    else:
        c=colors.to_rgb(c)
        c= tuple(255*k for k in c)
    return c;
cssutils.log.setLevel(logging.CRITICAL)

selectors = {}
with open("C:\\Users\\20182653\\Desktop\\TESLAN\\2023-Beun-LANCo\\Logo\SVG2ILD\\content\\SVG SEQUENCE TEST\\stupid_animation_test0001.svg") as webpage:
    html = webpage.read()
    soup = BSoup(html,features="xml")
for styles in soup.select('style'):
    css = styles.encode_contents()
    css = cssutils.parseString(css)
    for rule in css:
        if rule.type == rule.STYLE_RULE:
            style = rule.selectorText
            selectors[style] = {}
            for item in rule.style:
                propertyname = item.name
                value = item.value
                selectors[style][propertyname] = value

color={}
color['0']=(0,0,0)
for i in selectors:
    if 'stroke' in selectors[i].keys():
        c=selectors[i]['stroke']
        hex2col(c)
        color[i] =c
stroke_ind=[m.start() for m in re.finditer('stroke=', str(soup))]
stroke_ind+=[m.start() for m in re.finditer('stroke =', str(soup))]
l=[]
for i in stroke_ind:
    l.append(re.split('\"|\'',str(soup)[i:i+16])[1])
l=set(l)
for i in l:
    color[i]=hex2col(i)
print(color)
#print(list(color.keys()).index('.cls-2'))
#color=[]
#if selectors['.cls-1']['stroke'].find("#")==-1):
#    color.append(selectors['.cls-1']['stroke'])
