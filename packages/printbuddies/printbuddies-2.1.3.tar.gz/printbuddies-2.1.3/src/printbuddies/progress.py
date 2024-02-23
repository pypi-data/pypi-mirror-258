from datetime import timedelta

import rich
import rich.console
import rich.highlighter
import rich.progress
import rich.style
import rich.table
import rich.text
from noiftimer import Timer
from rich import filesize
from typing_extensions import Any, Callable, Iterable, Literal, Optional, Self, Sequence

from .gradient import Gradient


class BarColumn(rich.progress.BarColumn):
    def __init__(
        self,
        bar_width: int | None = 40,
        style: str | rich.style.Style = "sea_green1",
        complete_style: str | rich.style.Style = "deep_pink1",
        finished_style: str | rich.style.Style = "cornflower_blue",
        pulse_style: str | rich.style.Style = "deep_pink1",
        table_column: rich.table.Column | None = None,
    ) -> None:
        super().__init__(
            bar_width, style, complete_style, finished_style, pulse_style, table_column
        )


class TaskProgressColumn(rich.progress.TaskProgressColumn):
    def __init__(
        self,
        text_format: str = "{task.percentage:.2f}%",
        text_format_no_percentage: str = "",
        style: str | rich.style.Style = "light_coral",
        justify: Literal["default", "left", "center", "right", "full"] = "left",
        markup: bool = True,
        highlighter: rich.highlighter.Highlighter | None = None,
        table_column: rich.table.Column | None = None,
        show_speed: bool = True,
    ) -> None:
        super().__init__(
            text_format,
            text_format_no_percentage,
            style,
            justify,
            markup,
            highlighter,
            table_column,
            show_speed,
        )

    @classmethod
    def render_speed(cls, speed: Optional[float]) -> rich.text.Text:
        """Render the speed in iterations per second.

        Args:
            task (Task): A Task object.

        Returns:
            Text: Text object containing the task speed.
        """
        if speed is None:
            return rich.text.Text("", style="progress.percentage")
        unit, suffix = filesize.pick_unit_and_suffix(
            int(speed),
            ["", "×10³", "×10⁶", "×10⁹", "×10¹²"],
            1000,
        )
        data_speed = speed / unit
        return rich.text.Text(f"{data_speed:.1f}{suffix} it/s", style="deep_pink1")


class TimerColumn(rich.progress.TimeRemainingColumn):
    def __init__(self, elapsed_only: bool = False, *args: Any, **kwargs: Any):
        self.elapsed_only = elapsed_only
        super().__init__(*args, **kwargs)

    def get_time_remaining(self, task: rich.progress.Task) -> str:
        if self.elapsed_when_finished and task.finished:
            task_time = task.finished_time
        else:
            task_time = task.time_remaining
        if not task.total or not task_time:
            return ""
        time_remaining = Timer.format_time(task_time)
        if time_remaining == "<1s":
            time_remaining = "0s"
        return time_remaining

    def get_time_elapsed(self, task: rich.progress.Task) -> str:
        elapsed = task.finished_time if task.finished else task.elapsed
        if not elapsed:
            return ""
        delta = timedelta(seconds=max(0, int(elapsed)))
        time_elapsed = Timer.format_time(delta.total_seconds())
        if time_elapsed == "<1s":
            time_elapsed = "0s"
        return time_elapsed

    def render(self, task: rich.progress.Task) -> rich.text.Text:
        timing = self.get_time_elapsed(task)
        if not self.elapsed_only and (time_remaining := self.get_time_remaining(task)):
            timing += f" <-> {time_remaining}"
            return rich.text.Text().from_markup(Gradient().apply(timing))
        return rich.text.Text().from_markup(f"[pink1]{timing}")


class Progress(rich.progress.Progress):
    """Renders an auto-updating progress bar(s).

    Args:
        console (Console, optional): Optional Console instance. Default will an internal Console instance writing to stdout.
        auto_refresh (bool, optional): Enable auto refresh. If disabled, you will need to call `refresh()`.
        refresh_per_second (Optional[float], optional): Number of times per second to refresh the progress information or None to use default (10). Defaults to None.
        speed_estimate_period: (float, optional): Period (in seconds) used to calculate the speed estimate. Defaults to 30.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        redirect_stdout: (bool, optional): Enable redirection of stdout, so ``print`` may be used. Defaults to True.
        redirect_stderr: (bool, optional): Enable redirection of stderr. Defaults to True.
        get_time: (Callable, optional): A callable that gets the current time, or None to use Console.get_time. Defaults to None.
        disable (bool, optional): Disable progress display. Defaults to False
        expand (bool, optional): Expand tasks table to fit width. Defaults to False.

        description_last (bool, optional): When using the default columns, the description column will be after the bar instead of before.
    """

    def __enter__(self) -> Self:
        self.start()
        return self

    @classmethod
    def get_default_columns(cls) -> tuple[rich.progress.ProgressColumn, ...]:
        return (
            rich.progress.TextColumn("[pink1]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimerColumn(),
            rich.progress.TextColumn("[pink1]{task.fields[suffix]}"),
        )

    def add_task(
        self,
        description: str = "",
        start: bool = True,
        total: float | None = 100,
        completed: int = 0,
        visible: bool = True,
        suffix: str = "",
        **fields: Any,
    ) -> rich.progress.TaskID:
        fields |= {"suffix": suffix}
        return super().add_task(description, start, total, completed, visible, **fields)


def track(
    sequence: (
        Sequence[rich.progress.ProgressType] | Iterable[rich.progress.ProgressType]
    ),
    description: str = "Yeehaw...",
    total: Optional[float] = None,
    auto_refresh: bool = True,
    console: Optional[rich.console.Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: rich.style.StyleType = "sea_green1",
    complete_style: rich.style.StyleType = "deep_pink1",
    finished_style: rich.style.StyleType = "cornflower_blue",
    pulse_style: rich.style.StyleType = "deep_pink1",
    update_period: float = 0.1,
    disable: bool = False,
    show_speed: bool = True,
) -> Iterable[rich.progress.ProgressType]:
    """Track progress by iterating over a sequence.

    Args:
        sequence (Iterable[ProgressType]): A sequence (must support "len") you wish to iterate over.
        description (str, optional): Description of task show next to progress bar. Defaults to "Yeehaw...".
        total: (float, optional): Total number of steps. Default is len(sequence).
        auto_refresh (bool, optional): Automatic refresh, disable to force a refresh after each iteration. Default is True.
        transient: (bool, optional): Clear the progress on exit. Defaults to False.
        console (Console, optional): Console to write to. Default creates internal Console instance.
        refresh_per_second (float): Number of times per second to refresh the progress information. Defaults to 10.
        style (StyleType, optional): Style for the bar background. Defaults to "bar.back".
        complete_style (StyleType, optional): Style for the completed bar. Defaults to "bar.complete".
        finished_style (StyleType, optional): Style for a finished bar. Defaults to "bar.finished".
        pulse_style (StyleType, optional): Style for pulsing bars. Defaults to "bar.pulse".
        update_period (float, optional): Minimum time (in seconds) between calls to update(). Defaults to 0.1.
        disable (bool, optional): Disable display of progress.
        show_speed (bool, optional): Show speed if total isn't known. Defaults to True.
    Returns:
        Iterable[ProgressType]: An iterable of the values in the sequence.

    """

    columns = list(Progress.get_default_columns())
    progress = Progress(
        *columns,
        auto_refresh=auto_refresh,
        console=console,
        transient=transient,
        get_time=get_time,
        refresh_per_second=refresh_per_second or 10,
        disable=disable,
    )

    with progress:
        yield from progress.track(
            sequence, total=total, description=description, update_period=update_period
        )
