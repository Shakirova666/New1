from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def __init__(self, a, b):
        self.count = 0
        self.a = a
        self.b = b

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p, self.a, self.b)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b
        self.count = 0

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, self.a, self.b)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, a, b):
        self.p, self.q = p, q
        self.a, self.b = a, b
        in_edge = R2Point.circle(
            p,
            q,
            self.a) or R2Point.circle(
            p,
            q,
            self.b) or R2Point.straight(
            p,
            q,
            self.a,
            self.b)
        self.count = 1 - 1 * int(in_edge)

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.a, self.b)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q, self.a, self.b)
        else:
            return Segment(self.p, r, self.a, self.b)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, p, q):
        self.points = Deq()
        self.points.push_first(b)
        self.a, self.b = p, q
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))

        in_edge_ab = R2Point.circle(
            a,
            b,
            self.a) or R2Point.circle(
            a,
            b,
            self.b) or R2Point.straight(
            a,
            b,
            self.a,
            self.b)
        self.count = 1 - 1 * int(in_edge_ab)

        in_edge_ac = R2Point.circle(
            a,
            c,
            self.a) or R2Point.circle(
            a,
            c,
            self.b) or R2Point.straight(
            a,
            c,
            self.a,
            self.b)
        self.count = self.count + 1 - 1 * int(in_edge_ac)

        in_edge_cb = R2Point.circle(
            c,
            b,
            self.a) or R2Point.circle(
            c,
            b,
            self.b) or R2Point.straight(
            c,
            b,
            self.a,
            self.b)
        self.count = self.count + 1 - 1 * int(in_edge_cb)

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            in_edge = R2Point.circle(
                self.points.last(), self.points.first(), self.a)
            in_edge = in_edge or R2Point.circle(
                self.points.last(), self.points.first(), self.b)
            in_edge = in_edge or R2Point.straight(
                self.points.last(), self.points.first(), self.a, self.b)
            self.count = self.count - 1 + 1 * int(in_edge)

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                q = self.points.first()
                self._perimeter -= p.dist(q)
                self._area += abs(R2Point.area(t, p, q))
                in_edge = R2Point.circle(q, p, self.a)
                in_edge = in_edge or R2Point.circle(q, p, self.b)
                in_edge = in_edge or R2Point.straight(q, p, self.a, self.b)
                self.count = self.count - 1 + 1 * int(in_edge)
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                q = self.points.last()
                self._perimeter -= p.dist(q)
                self._area += abs(R2Point.area(t, p, q))
                in_edge = R2Point.circle(q, p, self.a)
                in_edge = in_edge or R2Point.circle(q, p, self.b)
                in_edge = in_edge or R2Point.straight(q, p, self.a, self.b)
                self.count = self.count - 1 + 1 * int(in_edge)
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())

            in_edge = R2Point.circle(self.points.first(), t, self.a)
            in_edge = in_edge or R2Point.circle(self.points.first(), t, self.b)
            in_edge = in_edge or R2Point.straight(
                self.points.first(), t, self.a, self.b)
            self.count = self.count + 1 - 1 * int(in_edge)

            in_edge = R2Point.circle(self.points.last(), t, self.a)
            in_edge = in_edge or R2Point.circle(self.points.last(), t, self.b)
            in_edge = in_edge or R2Point.straight(
                self.points.last(), t, self.a, self.b)
            self.count = self.count + 1 - 1 * int(in_edge)

            self.points.push_first(t)
        return self
