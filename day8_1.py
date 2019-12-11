with open("day8_in.txt") as f:
    data = f.read()

width = 25
height = 6

area = width * height

layers = []
tmp = []
for index, px in enumerate(data):
    tmp.append(px)
    if (index + 1) % area == 0:
        layers.append(tmp)
        tmp = []

target_layer = None
for layer in layers:
    if target_layer is None or layer.count('0') < target_layer.count('0'):
        target_layer = layer

print(target_layer.count('1') * target_layer.count('2'))
