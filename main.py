#!/usr/bin/env python3

from importlib import import_module
from sys import argv
from math import sqrt
from functools import partial


def find_char(field, char):
    for n, line in enumerate(field):
        try:
            return n, line.index(char)
        except ValueError:
            pass
    return None


def print_path(Point, field, path):
    if type(path) is list:
        print('-' * (len(field[0]) + 2))
        for y in range(len(field)):
            print('|', end='')
            for x in range(len(field[0])):
                if field[y][x] in 'se':
                    print(field[y][x], end='')                
                elif Point(y, x) in path:
                    print('*', end='')
                else:
                    print(field[y][x], end='')
            print('|')
        print('-' * (len(field[0]) + 2))
    else:
        print("No path")

def main():
    try:
        module = import_module(argv[1])
    except IndexError:
        exit("No module specified")

    field = (
            's.           ',
            '      .      ',
            '...... ..... ',
            ' .   ..      ',
            ' ...         ',
            'e     .      ',
            )

    start = module.Point(*find_char(field, 's'))
    end = module.Point(*find_char(field, 'e'))
    block = '.'
    cost = partial(lambda a, b: sqrt((a.y - b.y)**2 + (a.x - b.x)**2), end)
    adjacent = lambda p: {module.Point(y,x) \
            for y in range(p.y - 1, p.y + 2) for x in range(p.x - 1, p.x + 2)
            if 0 <= y < len(field) and 0 <= x < len(field[0])
            }

    path = module.find_path(field, start, end, block, cost, adjacent)
    print_path(module.Point, field, path)


if __name__ == '__main__':
    main()
