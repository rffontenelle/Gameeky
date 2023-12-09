from .base import Handler as BaseHandler

from ....common.definitions import Action, State


class Handler(BaseHandler):
    def prepare(self, value: float) -> bool:
        self._entity.action = Action.IDLE

        return super().prepare(value)

    def tick(self) -> None:
        self._entity.state = State.IDLING

        self.finish()