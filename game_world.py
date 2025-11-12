# world[0] : 가장 낮은 계층 layer
# world[1] : 그 다음 계층 layer
# world[2] : 가장 높은 계층 layer
world = [[], [], []]

def add_object(o, depth=0):
    world[depth].append(o)

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    print("삭제할 월드가 없습니다")

def clear():
    for layer in world:
        layer.clear()