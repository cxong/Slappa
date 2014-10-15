from sprite import *


def overlap(group1, group2, func):
    if isinstance(group1, Sprite) and isinstance(group2, Sprite):
        overlap_sprites(group1, group2, func)
    elif isinstance(group1, Sprite) and not isinstance(group2, Sprite):
        for b in group2:
            overlap_sprites(group1, b, func)
    elif not isinstance(group1, Sprite) and isinstance(group2, Sprite):
        for a in group1:
            overlap_sprites(a, group2, func)
    else:
        for a in group1:
            for b in group2:
                overlap_sprites(a, b, func)


def overlap_sprites(a, b, func):
    a_p = Point(a.x + a.body.x, a.y + a.body.y)
    b_p = Point(b.x + b.body.x, b.y + b.body.y)
    width = a.body.width + b.body.width
    height = a.body.height + b.body.height
    if (a_p.x + width / 2 > b_p.x and a_p.x < b_p.x + width / 2 and
            a_p.y + height / 2 > b_p.y and a_p.y < b_p.y + height / 2):
        func(a, b)