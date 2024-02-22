class _Screen:

    def __init__(self):
        self.port = None
        self._valid_fonts = [
            "MONO12",
            "MONO15",
            "MONO20",
            "MONO30",
            "MONO40",
            "MONO60",
            "PROP20",
            "PROP30",
            "PROP40",
            "PROP60"
            ]
        self._valid_colours = [
            "black",
            "white",
            "red",
            "green",
            "blue",
            "yellow",
            "orange",
            "purple",
            "cyan",
            "transparent"
        ]

    def send(self, command):
        if self.port is None:
            raise AttributeError("COM Port has not been bound.")

        self.port.write(f"{command}\r".encode())

    def print(self, string):
        self.send(f"brain.screen.print('{string}')")

    def set_cursor(self, row: int | float, column: int | float):
        self.send(f"brain.screen.set_cursor({row}, {column})")

    def clear_screen(self):
        self.send(f"brain.screen.clear_screen()")

    def clear_row(self, row: int | float):
        self.send(f"brain.screen.clear_row({row})")

    def set_font(self, font):
        if font not in self._valid_fonts:
            raise AttributeError("Font not found.")

        self.send(f"brain.screen.set_font(FontType.{font})")

    def set_pen_width(self, pen_width: int | float):
        self.send(f"brain.screen.set_pen_width({pen_width})")

    def set_pen_colour(self, colour: str):
        if colour.lower() not in self._valid_colours:
            raise AttributeError("Colour not found.")

        self.send(f"brain.screen.set_pen_color(Color.{colour.upper()})")

    def set_fill_colour(self, colour: str):
        if colour.lower() not in self._valid_colours:
            raise AttributeError("Colour not found.")

        self.send(f"brain.screen.set_fill_color(Color.{colour.upper})")


