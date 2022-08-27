"""
This program use Monte Carlo method to find specific area
"""

import datetime
import numpy as np
import random
import time
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Triangle:
    vtx_a: Point
    vtx_b: Point
    vtx_c: Point


@dataclass
class Circle:
    center: Point
    radius: float


@dataclass
class Constant:
    TOTAL_LOOP: int = 50
    TOTAL_POINTS: int = 100 * 100
    DOMAIN_X: float = 10
    DOMAIN_Y: float = 10
    TRIANGLE: Triangle = Triangle(Point(0, 0), Point(6, 0), Point(6, 3))
    CIRCLE: Circle = Circle(Point(4, 2), 2)
    DRAW: bool = False
    DRAW_RANGE: float = 10
    DRAW_SAVE: bool = False


def monte_carlo():
    points = get_points()
    plot_data = []

    count_points_in_triangle = 0
    count_points_in_goal = 0

    for point in points:
        if is_in_triangle(point):
            count_points_in_triangle += 1
            if is_in_goal_region(point):
                count_points_in_goal += 1
                plot_data.append(point)

    # print("count_points_in_triangle= ", count_points_in_triangle)
    # print("count_points_in_goal= ", count_points_in_goal)

    if Constant.DRAW:
        plot(plot_data)

    return count_points_in_triangle, count_points_in_goal


def get_points():
    points = []
    for i in range(Constant.TOTAL_POINTS):
        x = round(random.uniform(0, Constant.DOMAIN_X), 2)
        y = round(random.uniform(0, Constant.DOMAIN_Y), 2)
        p = Point(x, y)
        points.append(p)

    return points


def is_in_goal_region(point: Point) -> bool:
    if is_in_triangle(point) and not is_in_circle(point):
        return True

    return False


def is_in_triangle(p: Point) -> bool:
    t = Constant.TRIANGLE
    vector_ab = [t.vtx_b.x - t.vtx_a.x, t.vtx_b.y - t.vtx_a.y]
    vector_ac = [t.vtx_c.x - t.vtx_a.x, t.vtx_c.y - t.vtx_a.y]
    vector_ap = [p.x - t.vtx_a.x, p.y - t.vtx_a.y]

    matrix_a = np.array([[vector_ab[0], vector_ac[0]], [vector_ab[1], vector_ac[1]]])
    b = np.array([[vector_ap[0]], [vector_ap[1]]])

    if np.linalg.det(matrix_a) == 0:
        return False

    x = np.linalg.solve(matrix_a, b)
    alpha, beta = x[0], x[1]

    if alpha > 0 and beta > 0 and 0 < alpha + beta < 1:
        return True
    else:
        return False


def is_in_circle(point: Point) -> bool:
    circle = Constant.CIRCLE
    if square_distance_between_points(circle.center, point) < circle.radius ** 2:
        return True
    return False


def square_distance_between_points(p: Point, q: Point) -> float:
    return (p.x - q.x) ** 2 + (p.y - q.y) ** 2


def distance_between_points(p: Point, q: Point) -> float:
    return ((p.x - q.x) ** 2 + (p.y - q.y) ** 2) ** 0.5


def plot(plot_data):
    figure, axes = plt.subplots()
    c = Constant.CIRCLE
    cx = c.center.x
    cy = c.center.y
    r = c.radius

    t = Constant.TRIANGLE
    # my_tri = Polygon([t.vtx_a, t.vtx_b, t.vtx_c, ])

    draw_circle = plt.Circle((cx, cy), r, fill=False)

    axes.add_collection(PolyCollection([
        [[t.vtx_a.x, t.vtx_a.y], [t.vtx_b.x, t.vtx_b.y], [t.vtx_c.x, t.vtx_c.y],
         ]
    ], facecolors="white", edgecolor="black"))

    axes.add_artist(draw_circle)

    plt.xlim(0, Constant.DOMAIN_X)
    plt.ylim(0, Constant.DOMAIN_Y)
    plt.title("View")

    for data in plot_data:
        x = data.x
        y = data.y
        plt.plot(x, y, "x", color="red")

    if Constant.DRAW_SAVE:
        time_str = time.strftime("%Y%m%d-%H%M%S")
        filename = time_str + '.png'
        plt.savefig(filename)

    plt.show()


def main():
    print("This program use Monte Carlo method to find specific area,")
    print("the parameters are set in the Constant class,")
    print("please check it.")

    print("It will simulate ", Constant.TOTAL_LOOP, "times. ")
    print("The simulation points for each time is  ", Constant.TOTAL_POINTS, ".")

    start = datetime.datetime.now()
    print("start_time: ", start)

    sum_of_points_in_triangle = 0
    sum_of_points_in_goal = 0

    for _ in range(Constant.TOTAL_LOOP):
        t, g = monte_carlo()
        sum_of_points_in_triangle += t
        sum_of_points_in_goal += g

    ave_t = sum_of_points_in_triangle / Constant.TOTAL_LOOP
    ave_g = sum_of_points_in_goal / Constant.TOTAL_LOOP

    theo_val_of_t = Constant.TOTAL_POINTS * ((6 * 3 * 0.5) / (Constant.DOMAIN_X * Constant.DOMAIN_Y))
    theo_val_of_g = Constant.TOTAL_POINTS * (
            (0.5 * 6 * 3 - 0.5 * np.pi * Constant.CIRCLE.radius ** 2) / (Constant.DOMAIN_X * Constant.DOMAIN_Y))

    print("theoretical value= ", theo_val_of_t, theo_val_of_g)
    print("simulation result= ", ave_t, ave_g)

    end = datetime.datetime.now()
    print("end_time: ", end)
    print("elapsed_time: ", end - start)


if __name__ == "__main__":
    main()

# Ref= https://www.youtube.com/watch?v=VHvMMtyvOgI
