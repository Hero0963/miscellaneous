"""
AttendingExpectation will show to stimulate scatter diagram of
confirmed case, stay-at-home order and safe students in a class
"""

from dataclasses import dataclass
import random
import matplotlib.pyplot as plt
import time


@dataclass
class Constant:
    TOTAL_LOOP: int = 1
    HEADCOUNT: int = 36
    SICK_COUNT: int = 4
    SAFE: str = "o"
    DANGEROUS: str = "*"
    SICK: str = "x"
    PLOT: bool = True
    SAFE_COLOR: str = "blue"
    DANGEROUS_COLOR: str = "red"
    SICK_COLOR: str = "black"


@dataclass
class Student:
    x: int
    y: int


def get_numbered_students():
    students = []

    for i in range(Constant.HEADCOUNT):
        s = Student(i // 6 + 1, i % 6 + 1)
        students.append(s)

    return students


def get_sick_number():
    r = [x for x in range(Constant.HEADCOUNT)]
    sick_count = random.sample(r, Constant.SICK_COUNT)

    return sick_count


def get_sick_number_2():
    r = [x for x in range(Constant.HEADCOUNT)]
    random.shuffle(r)

    sick_count = r[:4]

    return sick_count


def get_sick_number_3():
    is_duplicate = True

    while is_duplicate:
        sick_count = [random.randint(0, Constant.HEADCOUNT - 1) for _ in range(Constant.SICK_COUNT)]
        if len(set(sick_count)) == Constant.SICK_COUNT:
            is_duplicate = False

    return sick_count


def simulation():
    stu = get_numbered_students()
    # for i in range(len(stu)):
    #     print(i, stu[i].x, stu[i].y)

    sick_count = get_sick_number()
    # print("sick_count= ", sick_count)

    plot_data = [-1] * Constant.HEADCOUNT

    attend = 0
    for idx, v in enumerate(stu):
        is_not_neighbor = True
        for _, m in enumerate(sick_count):
            # print("abs evaluation= ", v.x, v.y, stu[m].x, stu[m].y)
            distance_square = abs(v.x - stu[m].x) ** 2 + abs(v.y - stu[m].y) ** 2
            if distance_square <= 2:
                is_not_neighbor = False
                break
        # print("flag= ", is_not_neighbor)
        if is_not_neighbor:
            attend += 1
            plot_data[idx] = Constant.SAFE
        else:
            if idx in sick_count:
                plot_data[idx] = Constant.SICK
            else:
                plot_data[idx] = Constant.DANGEROUS

    plot(plot_data)

    # print("attend= ", attend)
    return attend


def plot(plot_data):
    if Constant.PLOT:
        # plt.xlabel("x")
        # plt.ylabel("y")
        plt.style.use('bmh')
        plt.axis([0, Constant.HEADCOUNT ** 0.5 + 1, 0, Constant.HEADCOUNT ** 0.5 + 1])

        for idx, val in enumerate(plot_data):
            x = idx // 6 + 1
            y = idx % 6 + 1
            # print("mark= ", val)
            status_color = convert_color(val)
            plt.plot(x, y, val, color=status_color)  # 定義x,y和圖的樣式

        # time_str = time.strftime("%Y%m%d-%H%M%S")
        # filename = time_str + '.png'
        # print(filename)

        # plt.savefig(filename)
        # plt.show()


def convert_color(status):
    if status == Constant.SAFE:
        color = Constant.SAFE_COLOR
    elif status == Constant.DANGEROUS:
        color = Constant.DANGEROUS_COLOR
    else:
        color = Constant.SICK_COLOR

    return color


def main():
    sum_att = 0

    for _ in range(Constant.TOTAL_LOOP):
        att = simulation()
        sum_att += att

    avg = sum_att / Constant.TOTAL_LOOP

    print("total_loop= ", Constant.TOTAL_LOOP, "average= ", avg)


if __name__ == "__main__":
    main()
