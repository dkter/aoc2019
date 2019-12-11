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

rendered_layer = []
for index, px in enumerate(layers[0]):
    layer = 0
    while px == '2':
        layer += 1
        px = layers[layer][index]
    rendered_layer.append(px)


layer_iter = iter(rendered_layer)
for y in range(height):
    for x in range(width):
        ch = next(layer_iter)
        if ch == '1':
            print('█', end='')
        elif ch == '0':
            print(' ', end='')
    print()
