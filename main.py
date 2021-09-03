import os

import imageio as imageio
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import matplotlib as mpl

mpl.rcParams['figure.max_open_warning'] = 200


def function1(xi):
    return 0.25 * xi ** 2 - 1


def function2(xi):
    return math.cos(xi / 2)


a = 1  # коэффициент температуропроводности
assert a != 0
var = 2

arrayy = []


def calculate(L, u0, ul, function):
    plt.style.use('seaborn-whitegrid')
    eps = 0.01
    tau = 0.001
    const = 200
    delta = L / 20
    n = int(L / delta)
    result = []
    X = []
    time_ = 0
    for x in range(0, n + 1):
        current_x = x * delta
        X.append(current_x)
        result.append(function(current_x))
    fig, xt = plt.subplots()
    plt.title("Моделирование распространени тепла в стержне после " + str(time_) + " сек")
    plt.xlabel("X")
    plt.ylabel("T")
    xt.xaxis.set_major_locator(ticker.MultipleLocator(L / 10))
    xt.yaxis.set_major_locator(ticker.MultipleLocator(abs(ul - u0) / 10))
    plt.grid(True)
    xt.plot(X, result)
    arrayy.append('{}.png'.format(0))
    plt.savefig('{}.png'.format(0))
    is_correct = False
    while not is_correct:
        time_ += tau * const
        for t in range(1, const + 1):
            is_correct = True
            if t % const == 0:
                fig, xt = plt.subplots()
            T = [u0]
            for x in range(1, n):
                tmp = tau * a * a / delta / delta * (result[x + 1] - 2 * result[x] + result[x - 1]) + result[x]
                T.append(tmp)
                if abs((result[x] - result[x - 1]) / delta - (ul - u0) / L) > eps:
                    is_correct = False
            T.append(ul)
            result = T
            if t % const == 0:
                plt.title("Моделирование распространени тепла в стержне после {:.2f} сек".format(time_))
                plt.xlabel("X")
                plt.ylabel("T")
                xt.xaxis.set_major_locator(ticker.MultipleLocator(L / 10))
                xt.yaxis.set_major_locator(ticker.MultipleLocator(abs(ul - u0) / 10))
                plt.grid(True)
                xt.plot(X[:n + 1], T[:n + 1])
                arrayy.append('{}.png'.format(time_))
                plt.savefig('{}.png'.format(time_))


if var == 1:
    calculate(L=4, u0=-1, ul=3,
              function=function1)  # Длина стержня, температура на одном конце, температура на другом конце, функция
if var == 2:
    calculate(L=10, u0=1, ul=0,
              function=function2)  # Длина стержня, температура на одном конце, температура на другом конце, функция

with imageio.get_writer('var{}.gif'.format(var), mode='I', duration=0.025) as writer:
    for filename in arrayy:
        image = imageio.imread(filename)
        writer.append_data(image)
    writer.close()

for filename in set(arrayy):
    os.remove(filename)
