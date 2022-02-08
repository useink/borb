import random
import typing
from decimal import Decimal


class RectangularMazeFactory:
    @staticmethod
    def rectangular_maze(grid_width: int = 10, grid_height: int = 10):

        # determine lines
        cells: typing.List[typing.List[typing.Tuple[bool, bool, bool, bool]]] = [
            [(True, True, True, True) for _ in range(0, grid_width)]
            for _ in range(0, grid_height)
        ]

        cells_stk: typing.List[typing.Tuple[int, int]] = [
            (
                random.randint(0, grid_width - 1),
                random.randint(0, grid_height - 1),
            )
        ]
        while sum([sum([1 for t in row if all(t)]) for row in cells]) > 0:
            # check last element
            x, y = cells_stk[-1]

            # find intact neighbours
            nbs: typing.List[typing.Tuple[int, int]] = []
            if x != 0 and all(cells[x - 1][y]):
                nbs.append((x - 1, y))
            if x != (grid_width - 1) and all(cells[x + 1][y]):
                nbs.append((x + 1, y))
            if y != 0 and all(cells[x][y - 1]):
                nbs.append((x, y - 1))
            if y != (grid_height - 1) and all(cells[x][y + 1]):
                nbs.append((x, y + 1))
            # pop
            if len(nbs) == 0:
                cells_stk.pop(-1)
                continue
            # go to unvisited nb
            nb: typing.Tuple[int, int] = random.choice(nbs)
            cells_stk.append(nb)

            # tear down the walls
            # new cell is WEST
            if x == nb[0] + 1 and y == nb[1]:
                cells[x - 1][y] = (
                    cells[x - 1][y][0],
                    False,
                    cells[x - 1][y][2],
                    cells[x - 1][y][3],
                )
                cells[x][y] = (cells[x][y][0], cells[x][y][1], cells[x][y][2], False)
            # new cell is EAST
            if x == nb[0] - 1 and y == nb[1]:
                cells[x + 1][y] = (
                    cells[x + 1][y][0],
                    cells[x + 1][y][1],
                    cells[x + 1][y][2],
                    False,
                )
                cells[x][y] = (cells[x][y][0], False, cells[x][y][2], cells[x][y][3])
            # new cell is NORTH
            if x == nb[0] and y == nb[1] + 1:
                cells[x][y - 1] = (
                    cells[x][y - 1][0],
                    cells[x][y - 1][0],
                    False,
                    cells[x][y - 1][3],
                )
                cells[x][y] = (False, cells[x][y][1], cells[x][y][2], cells[x][y][3])
            # new cell is SOUTH
            if x == nb[0] and y == nb[1] - 1:
                cells[x][y + 1] = (
                    False,
                    cells[x][y + 1][1],
                    cells[x][y + 1][2],
                    cells[x][y + 1][3],
                )
                cells[x][y] = (cells[x][y][0], cells[x][y][1], False, cells[x][y][3])
        lines: typing.List[
            typing.Tuple[typing.Tuple[Decimal, Decimal], typing.Tuple[Decimal, Decimal]]
        ] = []
        for i in range(0, grid_width):
            for j in range(0, grid_height):
                # NORTH
                if cells[i][j][0]:
                    lines.append(((i * 10, j * 10), ((i + 1) * 10, j * 10)))
                # EAST
                if cells[i][j][1]:
                    lines.append((((i + 1) * 10, j * 10), ((i + 1) * 10, (j + 1) * 10)))
                # SOUTH
                if cells[i][j][2]:
                    lines.append((((i + 1) * 10, (j + 1) * 10), (i * 10, (j + 1) * 10)))
                # WEST
                if cells[i][j][3]:
                    lines.append(((i * 10, (j + 1) * 10), (i * 10, j * 10)))

        # return
        return lines
