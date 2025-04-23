from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))
    # Совпадает ли точка с другой?

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    def circle(z, s, a):  # пересечение ребра с 1-окружностью с центром a
        if z.x == s.x:  # если ребро паралельно оси 0Y
            if z.x >= a.x - 1 and z.x <= a.x + 1:
                y1, y2 = a.y + (1 - (z.x - a.x)**2)**0.5, a.y - \
                    (1 - (z.x - a.x)**2)**0.5
                t1 = R2Point(z.x, y1)
                t2 = R2Point(z.x, y2)
                return t1.is_inside(z, s) or t2.is_inside(z, s)
            return False
        else:
            k = (z.y - s.y) / (z.x - s.x)
            b = z.y - k * z.x
            d = (a.x - k * b + a.y)**2 - (k**2 + 1) * \
                (a.x**2 + b**2 - 2 * b * a.y + a.y**2 - 1)
            if d < 0:
                return False
            # if d == 0:
            #     x1 = (a.x - k*b + a.y)/(k**2 + 1)
            #     y1 = k*x1 + b
            #     t = R2Point(x1,y1)
            #     return t.is_inside(z, s)
            else:
                x1, x2 = (a.x - k * b + a.y) + \
                    d**0.5, (a.x - k * b + a.y) - d**0.5
                x1 /= (k**2 + 1)
                x2 /= (k**2 + 1)
                y1, y2 = k * x1 + b, k * x2 + b
                t1 = R2Point(x1, y1)
                t2 = R2Point(x2, y2)
                return t1.is_inside(z, s) or t2.is_inside(z, s)

    # пересечение ребра и прямоугольника = отрезок (a, b) с шириной 2 (вместо
    # 0)
    def straight(z, s, a, b):
        if a.x == b.x and z.x == s.x:
            if a.x < z.x + 1 and a.x > z.x - 1 and \
                (z.y <= max(a.y, b.y) + 1 and z.y >= min(a.y, b.y) - 1 \
                 or s.y <= max(a.y, b.y) + 1 and s.y >= min(a.y, b.y) -1):
                return True 
            return False
        elif z.x == s.x:
            y1 = z.x * (a.y - b.y) / (a.x - b.x) + a.y - (a.y - b.y) / (a.x - b.x) * a.x - 1
            return (y1 <= max(z.y, s.y) and y1 >= min(s.y, z.y) or y1 + 2 <= max(z.y, s.y) and y1 + 2 >= min(z.y, s.y))
        elif a.x == b.x:
            k = (z.y - s.y) / (z.x - s.x)
            y1 = k * (a.x + 1) + z.y - k * z.x
            y2 = k * (a.x - 1) + z.y - k * z.x
            return (y1 <= max(a.y, b.y) and y1 >= min(a.y, b.y) or y2 <= max(a.y, b.y) and y2 >= min(a.y, b.y))
        k0 = (a.y - b.y) / (a.x - b.x)
        k = (z.y - s.y) / (z.x - s.x)
        if k0 == k:
            return False
        b01 = a.y - k0 * a.x - 1
        b02 = b01 + 2
        bz = z.y - k * z.x
        x1 = (bz - b01) / (k0 - k)
        x2 = (bz - b01) / (k0 - k)
        y1, y2 = k * x1 + bz, k * x2 + bz
        # точки пересечения прямых, паралельных отрезку,
        # с окружностями вокруг концов отрезка
        a1x = (a.x - k0 * b01 + a.y) / (k0**2 + 1)
        a1y = k0 * a1x + b01
        a1 = R2Point(a1x, a1y)
        b1x = (b.x - k0 * b01 + b.y) / (k0**2 + 1)
        b1y = k0 * b1x + b01
        b1 = R2Point(b1x, b1y)
        a2x = (a.x - k0 * b02 + a.y) / (k0**2 + 1)
        a2y = k0 * a2x + b02
        a2 = R2Point(a2x, a2y)
        b2x = (b.x - k0 * b02 + b.y) / (k0**2 + 1)
        b2y = k0 * b2x + b02
        b2 = R2Point(b2x, b2y)
        t1 = R2Point(x1, y1)
        t2 = R2Point(x2, y2)
        # лежит ли 1ая точка пересечения внутри (a1, b1) и (z, s)
        in_edge_1 = t1.is_inside(z, s) and t1.is_inside(a1, b1)
        # лежит ли 2ая точка пересечения внутри (a2, b2) и (z, s)
        in_edge_2 = t2.is_inside(z, s) and t2.is_inside(a2, b2)
        return (in_edge_1 or in_edge_2)
