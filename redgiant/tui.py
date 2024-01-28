from statistics import mean
from itertools import cycle

from textual.app import App, ComposeResult
from textual.widgets import Sparkline, DataTable
from textual.coordinate import Coordinate
from textual.containers import Vertical

from redgiant import sensors

ROWS = [
    ("sensor", "now", "avg", "max", "min"),
    ("CPU", None, None, None, None)
]

cursors = cycle(["column", "row", "cell"])


class TUI(App[None]):
    DEFAULT_CSS = """
    Vertical {
       align: right middle;
    }

    Sparkline {
        height: 100;
    }
    """
    cpu_sparkline: Sparkline
    table: DataTable

    def update(self) -> None:
        now = sensors.get_cpu_temperature()
        self.cpu_sparkline.data.append(now)
        self.cpu_sparkline.refresh()
        data = self.cpu_sparkline.data
        temp_mean = mean(data)
        temp_max = max(data)
        temp_min = min(data)
        self.table.update_cell_at(Coordinate(row=0, column=1), now)
        self.table.update_cell_at(Coordinate(row=0, column=2), temp_mean)
        self.table.update_cell_at(Coordinate(row=0, column=3), temp_max)
        self.table.update_cell_at(Coordinate(row=0, column=4), temp_min)

    def init_table(self):
        self.table.cursor_type = next(cursors)
        self.table.zebra_stripes = True
        self.table.add_columns(*ROWS[0])
        self.table.add_rows(ROWS[1:])

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.init_table()
        self.update()
        self.set_interval(1 / 60, self.update)

    def compose(self) -> ComposeResult:
        self.cpu_sparkline = Sparkline(data=[])
        self.table = DataTable()
        yield Vertical(
            self.cpu_sparkline,
            self.table
        )
