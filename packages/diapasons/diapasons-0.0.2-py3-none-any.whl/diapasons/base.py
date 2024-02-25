from typing import List, Union, Optional

from pydantic import ValidationError

from .exceptions import PointNotNumberException, PointNotInDiapasonException, SplitByNotOverlapsDiapason
from .validators import DiapasonValidator


class Diapason:
    """
    class that represent diapason of numbers:
    Diapason([1, 2.9, 5])

    ----------_______________---------
    0         1     2.9      5     6
    """

    def __init__(self, points: List[Union[int, float]]):
        validate_points(points)
        self.points = [float(point) for point in points]
        self.points.sort()
        self.start_point = min(self.points)
        self.end_point = max(self.points)

    @property
    def is_point(self) -> bool:
        return self.start_point == self.end_point

    @property
    def length(self) -> float:
        return self.end_point - self.start_point

    def add_point(self, point: Union[int, float]) -> None:
        add_point(self, point)

    def add_points(self, points: list) -> None:
        add_points(self, points)

    def touch(self, other) -> bool:
        return touch(self, other)

    def intersects(self, other) -> bool:
        return intersects(self, other)

    def crosses(self, other) -> bool:
        return crosses(self, other)

    def overlaps(self, other) -> bool:
        return overlaps(self, other)

    def distance(self, other) -> float:
        return distance(self, other)

    def move(self, step: float) -> None:
        move(self, step)

    def split_by_point(self, point: float) -> tuple:
        return split_by_point(self, point)

    def split_by_diapason(self, other) -> tuple:
        return split_by_diapason(self, other)

    def common(self, other):
        return common(self, other)

    def different(self, other):
        return different(self, other)

    def __len__(self):
        return self.length

    def __str__(self):
        points = str(self.points[:5])
        if len(self.points) > 5:
            points = points[:-1] + '...]'
        return f'Diapason({points})'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.start_point == other.start_point and self.end_point == other.end_point

    def __add__(self, other):
        return Diapason(points=self.points + other.points)

    def __contains__(self, item):
        return contains(self, item)


def validate_points(points: list):
    try:
        DiapasonValidator(points=points)
    except ValidationError as ex:
        raise PointNotNumberException(
            f'Point must be valid integers or float, but got\n '
            f'"{ex.errors()[0]['input']}"'
        )


def touch(d_1: Diapason, d_2: Diapason) -> bool:
    """
    d_1 = Diapason([1, 2])
    d_2 = Diapason([2, 3])
    d_1.touch(d_2)
    True
    """

    if d_1.start_point <= d_2.start_point <= d_1.end_point:
        return True
    if d_1.start_point <= d_2.end_point <= d_1.end_point:
        return True
    return False


def intersects(d_1: Diapason, d_2: Diapason):
    """
    d_1 = Diapason([1, 3])
    d_2 = Diapason([2, 4])
    d_1.intersects(d_2)
    True
    """

    if d_1.start_point < d_2.start_point < d_1.end_point:
        return True
    if d_1.start_point < d_2.end_point < d_1.end_point:
        return True
    if d_2.start_point <= d_1.start_point and d_2.end_point >= d_1.end_point:
        return True
    return False


def crosses(d_1: Diapason, d_2: Diapason):
    """
    d_1 = Diapason([1, 3])
    d_2 = Diapason([3, 4])
    d_1.intersects(d_2)
    True
    """

    if d_1.start_point == d_2.end_point or d_1.end_point == d_2.start_point:
        return True
    return False


def contains(d_1: Diapason, d_2: Diapason) -> bool:
    """
    d_2 in d_1
    """
    if d_1.start_point <= d_2.start_point < d_1.end_point:
        if d_1.start_point < d_2.end_point <= d_1.end_point:
            return True
    return False


def distance(d_1: Diapason, d_2: Diapason):
    """
    Diapason([1, 2]).distance(Diapason([3, 4])) -> 1
    """
    if d_1.touch(d_2):
        return 0
    return min(
        abs(d_1.end_point - d_2.start_point),
        abs(d_1.start_point - d_2.end_point)
    )


def refresh(diapason: Diapason) -> None:
    diapason.points.sort()
    diapason.start_point = min(diapason.points)
    diapason.end_point = max(diapason.points)


def move(diapason: Diapason, step: float):
    for index, _ in enumerate(diapason.points):
        diapason.points[index] += step
    refresh(diapason)


def overlaps(d_1, d_2) -> bool:
    if d_1.start_point < d_2.start_point and d_1.end_point > d_2.end_point:
        return True
    return False


def split_by_point(diapason: Diapason, split_point: float) -> tuple[Diapason, Diapason]:
    if not Diapason([split_point]).intersects(diapason):
        raise PointNotInDiapasonException(
            f'Point {split_point} not in diapason {diapason}'
        )
    left_d = Diapason(
        [p for p in diapason.points if p < split_point] + [split_point]
    )
    right_d = Diapason(
        [split_point] + [p for p in diapason.points if p > split_point]
    )
    return left_d, right_d


def split_by_diapason(d_1: Diapason, d_2: Diapason) -> tuple[Diapason, Diapason]:
    if not d_1.overlaps(d_2):
        raise SplitByNotOverlapsDiapason(
            f'{d_1} not overlaps {d_2}, use "different()" method'
        )
    left_d = Diapason(
        [p for p in d_1.points if p < d_2.start_point] + [d_2.start_point]
    )
    right_d = Diapason(
        [d_2.end_point] + [p for p in d_1.points if p > d_2.end_point]
    )
    return left_d, right_d


def common(d_1: Diapason, d_2: Diapason) -> Optional[Diapason]:
    if not d_1.intersects(d_2):
        return None
    start_point = max(d_1.start_point, d_2.start_point)
    end_point = min(d_1.end_point, d_2.end_point)
    points = [p for p in d_1.points if start_point < p < end_point]
    points.extend([p for p in d_2.points if start_point < p < end_point])
    return Diapason(
        [start_point] + points + [end_point]
    )


def different(d_1: Diapason, d_2: Diapason) -> Optional[Union[tuple[Diapason, Diapason], Diapason]]:
    if d_1 == d_2:
        return None
    if not d_1.intersects(d_2):
        return d_1, d_2
    common_d = d_1.common(d_2)

    left_d = Diapason(
        [p for p in d_1.points if p < common_d.start_point] +
        [p for p in d_2.points if p < common_d.start_point] +
        [common_d.start_point]
    )
    right_d = Diapason(
        [common_d.end_point] +
        [p for p in d_1.points if p > common_d.end_point] +
        [p for p in d_2.points if p > common_d.end_point]
    )
    if left_d.is_point:
        return right_d
    if right_d.is_point:
        return left_d
    return left_d, right_d


def add_point(diapason: Diapason, point: Union[int, float]) -> None:
    validate_points([point])
    diapason.points.append(float(point))
    refresh(diapason)


def add_points(diapason: Diapason, points: list) -> None:
    validate_points(points)
    diapason.points.extend([float(point) for point in points])
    refresh(diapason)
