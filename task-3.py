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

    # def intersection

    # def area

    # def triangulate
