import os
import re
from PIL import Image

map_folder = r'/home/sdtd/instances/dogfort/Random Gen/Donkeyteeth/map/'
map_output = '/var/www/sdtd/map.png'

x_pixel_scale = 256
y_pixel_scale = 256

zoom = 1

scope = re.compile("^.*map\/[{}]\/(-?[\d])".format(zoom))

root_dirs = [(root, files) for root, dirs, files in os.walk(map_folder)]

scoped_dirs = []
for d, f in root_dirs:
    if re.match(scope, d):
        scoped_dirs.append((d, f))

images = []
for d in scoped_dirs:
    for img in d[1]:
        r1 = re.search("(-?[\d]).png", img)
        r2 = re.search("^.*map\/(-?[\d])\/(-?[\d])", d[0])
        y = int(r1.group(1))
        x = int(r2.group(2))
        with open("{}/{}".format(d[0], img),'rb') as f:
            im = Image.open(f)
            images.append(((x,y), im.copy()))

def bounds(x_coords, y_coords):
    return (
            x_pixel_scale*(max(x_coords) - min(x_coords) + 1), 
            y_pixel_scale*(max(y_coords) - min(y_coords) + 1)
           )

x_coords = [c[0] for c,im in images]
y_coords = [c[1] for c,im in images]
canvas_size = bounds(x_coords, y_coords)

def new_canvas():
    return Image.new("RGB", canvas_size)

canvas = new_canvas()
for c,im in images:
    scaled = im.resize((x_pixel_scale,y_pixel_scale), Image.ANTIALIAS)
    canvas.paste(scaled,
        (
         x_pixel_scale*(c[0] - min(x_coords)),
         y_pixel_scale*(max(y_coords) - c[1])
        )
    )

canvas.save(map_output)
