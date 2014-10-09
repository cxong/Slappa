from point import *


def overlap(group1, group2, func):
    for a in group1:
        for b in group2:
            a_p = Point(a.x + a.body.x, a.y + a.body.y)
            b_p = Point(b.x + b.body.x, b.y + b.body.y)
            width = a.body.width + b.body.width
            height = a.body.height + b.body.height
            if (a_p.x + width / 2 > b_p.x and a_p.x < b_p.x + width / 2 and
                    a_p.y + height / 2 > b_p.y and a_p.y < b_p.y + height / 2):
                func(a, b)