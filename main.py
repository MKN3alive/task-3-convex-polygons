from convex_polygons import ConvexPolygon
#import matplotlib.pyplot as plt
if __name__ == "__main__":


    poly1 = ConvexPolygon([(0,0), (4,0), (3,3),(2,4), (1,4), (0,3)])
    poly2 = ConvexPolygon([(5,4), (6,4), (6,5)])

    print("Полигон 1 вершины:", poly1.vertices)
    print("Полигон 2 вершины:", poly2.vertices)


    print("Периметр poly1:", poly1.perimeter())
    print("Площадь poly1:", poly1.area())


    inside_point = (2,1)
    outside_point = (5,1)
    print(f"Точка {inside_point} внутри poly1?", poly1.contains_point(inside_point))
    print(f"Точка {outside_point} внутри poly1?", poly1.contains_point(outside_point))


    triangles = poly1.triangulate()
    print(f"Poly1 разбит на {len(triangles)} треугольников:")
    for i, tri in enumerate(triangles, start=1):
        print(f"  Треугольник {i}: {tri.vertices}")
    if poly1.polygons_intersect(poly2):
        print("Многоугольники пересекаются")
    else:
        print("Многоугольники не пересекаются")

    # ===== ВИЗУАЛИЗАЦИЯ РАСКОММЕНТИРОВАТЬ import matplotlib.pyplot as plt=====
    '''
    plt.figure(figsize=(8,8))
    plt.axis("equal")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.title("Выпуклые многоугольники, триангуляция и пересечение")


    xs1, ys1 = zip(*(poly1.vertices + [poly1.vertices[0]]))
    plt.plot(xs1, ys1, 'b-', linewidth=2, label="Poly1")
    plt.fill(xs1, ys1, alpha=0.1, color='blue')


    for tri in triangles:
        tx, ty = zip(*(tri.vertices + [tri.vertices[0]]))
        plt.plot(tx, ty, 'g--', alpha=0.7)


    xs2, ys2 = zip(*(poly2.vertices + [poly2.vertices[0]]))
    plt.plot(xs2, ys2, 'r-', linewidth=2, label="Poly2")
    plt.fill(xs2, ys2, alpha=0.1, color='red')


    plt.scatter(*inside_point, color='green', s=80, label="Точка внутри Poly1")
    plt.scatter(*outside_point, color='orange', s=80, label="Точка вне Poly1")


    for i, (x, y) in enumerate(poly1.vertices):
        plt.text(x + 0.05, y + 0.05, f"V{i}", fontsize=10, color='blue')


    for i, (x, y) in enumerate(poly2.vertices):
        plt.text(x + 0.05, y + 0.05, f"W{i}", fontsize=10, color='red')

    plt.legend()
    plt.show()
'''
