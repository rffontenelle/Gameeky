import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw

from .global_settings import GlobalSettings
from .entity_settings import EntitySettings

from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "window.ui"))
class Window(Adw.ApplicationWindow):
    __gtype_name__ = "Window"

    game_box = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._global_settings = GlobalSettings()
        self._entity_settings = EntitySettings()

        self.game_box.append(self._global_settings)
        self.game_box.append(self._entity_settings)

    @property
    def description(self) -> Description:
        description = self._global_settings.description
        description.game.default = self._entity_settings.description

        return description

    @description.setter
    def description(self, description: Description) -> None:
        self._global_settings.description = description
        self._entity_settings.description = description.game.default
