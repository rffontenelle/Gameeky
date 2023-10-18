import math

from typing import Dict, Tuple, List

from ...common.utils import clamp
from ...common.entity import Entity, Vector
from ...common.direction import Direction


class SpatialPartition:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._entity_by_position: Dict[Tuple[int, int], List[Entity]] = {}

    def add(self, entity: Entity) -> None:
        position = (
            math.floor(entity.position.x),
            math.floor(entity.position.y),
        )

        if position not in self._entity_by_position:
            self._entity_by_position[position] = []

        self._entity_by_position[position].append(entity)

    def remove(self, entity: Entity) -> None:
        position = (
            math.floor(entity.position.x),
            math.floor(entity.position.y),
        )

        self._entity_by_position[position].remove(entity)

        if len(self._entity_by_position[position]) == 0:
            del self._entity_by_position[position]

    def get_position_for_direction(
        self,
        x: float,
        y: float,
        z: float,
        direction: Direction,
    ) -> Vector:
        position = Vector(x=x, y=y, z=z)

        if direction == Direction.RIGHT:
            position.x += 1
        if direction == Direction.DOWN:
            position.y += 1
        if direction == Direction.LEFT:
            position.x -= 1
        if direction == Direction.UP:
            position.y -= 1

        # Don't go outside'of the scene
        position.x = clamp(self.width - 1, 0, position.x)
        position.y = clamp(self.height - 1, 0, position.y)

        return position

    def find_by_position(self, position: Vector) -> List[Entity]:
        x = math.floor(position.x)
        y = math.floor(position.y)

        return self._entity_by_position.get((x, y), [])

    def find_by_direction(self, entity: Entity) -> List[Entity]:
        x = math.floor(entity.position.x)
        y = math.floor(entity.position.y)

        if entity.direction == Direction.RIGHT:
            x += 1
        elif entity.direction == Direction.UP:
            y -= 1
        elif entity.direction == Direction.LEFT:
            x -= 1
        elif entity.direction == Direction.DOWN:
            y += 1

        return self._entity_by_position.get((x, y), [])

    def find_by_distance(
        self,
        target: Entity,
        distance_x: int,
        distance_y: int,
    ) -> List[Entity]:
        entities = []

        from_range_x = math.floor(max(target.position.x - distance_x, 0))
        to_range_x = math.floor(min(target.position.x + distance_x, self.width))

        from_range_y = math.floor(max(target.position.y - distance_y, 0))
        to_range_y = math.floor(min(target.position.y + distance_y, self.height))

        for y in range(from_range_y, to_range_y):
            for x in range(from_range_x, to_range_x):
                entities += self._entity_by_position.get((x, y), [])

        return entities
