from typing import List, Tuple
import math

Point = Tuple[float, float]


class ConvexPolygon:
    def __init__(self, vertices: List[Point]):
        if len(vertices) < 3:
            raise ValueError("Многоугольник должен иметь хотя бы 3 вершины")
        self.vertices = vertices
        if not self._is_convex():
            raise ValueError("Многоугольник не является выпуклым")

    def _is_convex(self) -> bool:
        n = len(self.vertices)
        if n < 3:
            return False
        sign = None
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            x3, y3 = self.vertices[(i + 2) % n]
            cross = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
            if cross != 0:
                if sign is None:
                    sign = cross > 0
                elif (cross > 0) != sign:
                    return False
        return True

    def perimeter(self) -> float:
        p = 0
        for i in range(len(self.vertices)):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % len(self.vertices)]
            p += math.hypot(x2 - x1, y2 - y1)
        return p

    def contains_point(self, point: Point) -> bool:
        x, y = point
        n = len(self.vertices)
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
            if cross < 0:
                return False
        return True

    def area(self) -> float:
        n = len(self.vertices)
        s = 0
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            s += x1 * y2 - x2 * y1
        return abs(s) / 2

    def triangulate(self) -> List["ConvexPolygon"]: #Легкая триангуляция (Все треугольники содержат первую вершину)
        n = len(self.vertices)
        if n == 3:
            return [self]
        triangles = []
        v0 = self.vertices[0]
        for i in range(1, n - 1):
            tri_vertices = [v0, self.vertices[i], self.vertices[i + 1]]
            triangles.append(ConvexPolygon(tri_vertices))
        return triangles

    def triangulate_hard(self) -> List["ConvexPolygon"]: #Сложная триангуляция (Разные треугольники содержат разные вершины)
        triangles = []
        n = len(self.vertices)
        if n == 3:
            return [self]
        ind = 0
        v0=self.vertices[ind]
        c=1
        if n % 2 == 0:
            for i in range(0, n - 2):
                tri_vertices = [v0, self.vertices[(ind+c)%n], self.vertices[(ind+c*2)%n]]
                ind=(ind+c*2)%n
                v0=self.vertices[ind]
                if v0==self.vertices[0]:
                    c += 1
                triangles.append(ConvexPolygon(tri_vertices))
        else:
            for i in range(0, n - 2):
                if v0==self.vertices[n-1]:
                    c += 1
                    tri_vertices = [v0, self.vertices[(ind + c-1) % n], self.vertices[(ind + c * 2-1) % n]]
                    ind = (ind + c * 2-1) % n
                else:
                    tri_vertices = [v0, self.vertices[(ind+c)%n], self.vertices[(ind+c*2)%n]]
                    ind = (ind + c * 2) % n
                v0 = self.vertices[ind]
                triangles.append(ConvexPolygon(tri_vertices))

        return triangles

    def polygons_intersect(poly1: "ConvexPolygon", poly2: "ConvexPolygon") -> "ConvexPolygon | None":
        def inside(p, edge_start, edge_end):
            (x1, y1), (x2, y2) = edge_start, edge_end
            (px, py) = p
            return (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1) >= 0

        def intersection(p1, p2, e1, e2):
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = e1
            x4, y4 = e2

            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if denom == 0:
                return None
            px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
            py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
            return (px, py)

        output = poly1.vertices
        for i in range(len(poly2.vertices)):
            input_list = output
            output = []
            A = poly2.vertices[i]
            B = poly2.vertices[(i + 1) % len(poly2.vertices)]

            if not input_list:
                break

            S = input_list[-1]
            for E in input_list:
                if inside(E, A, B):
                    if not inside(S, A, B):
                        inter = intersection(S, E, A, B)
                        if inter:
                            output.append(inter)
                    output.append(E)
                elif inside(S, A, B):
                    inter = intersection(S, E, A, B)
                    if inter:
                        output.append(inter)
                S = E

        if len(output) < 3:
            return None

        return ConvexPolygon(output)
