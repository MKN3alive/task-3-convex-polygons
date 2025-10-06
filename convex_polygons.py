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

    """
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
    """
    def polygons_intersect(poly1: "ConvexPolygon", poly2: "ConvexPolygon") -> bool:
        def get_axes(vertices):
            axes = []
            n = len(vertices)
            for i in range(n):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % n]
                dx, dy = x2 - x1, y2 - y1
                axes.append((-dy, dx))
            return axes
        def project(vertices, axis):
            ax, ay = axis
            projections = [x * ax + y * ay for (x, y) in vertices]
            return min(projections), max(projections)
        for vertices in (poly1.vertices, poly2.vertices):
            for axis in get_axes(vertices):
                min1, max1 = project(poly1.vertices, axis)
                min2, max2 = project(poly2.vertices, axis)
                if max1 < min2 or max2 < min1:
                    return False
        return True