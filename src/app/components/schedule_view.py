from typing import Iterable

from flet import (
    Page,
    Container,
    Column,
    Row,
    Draggable,
    DragTarget,
    Text,
)
from flet.core.colors import Colors
from flet.core.alignment import (
    bottom_center ,
    bottom_left ,
    bottom_right,
    center,
    center_left,
    center_right,
    top_center,
    top_left,
    top_right,
    Alignment,
)


class AdminScheduleView(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.content = Column(
            controls=[
                Column(
                    controls=[
                        Container(
                            content=Row(
                                alignment='center',
                                controls=self.build_schedule_containers(
                                    'prep', 'fresh', 'soph',
                                )
                            ),
                        ),
                        Container(
                            content=Row(
                                alignment='center',
                                controls=self.build_schedule_containers(
                                    'jun', 'sen',
                                ),
                            ),
                        ),
                    ]
                ),
            ],
        )
        self.bgcolor = Colors.YELLOW_50
        self.width = 1800
        self.height = 900
        self.page.update()

    @staticmethod
    def build_schedule_containers(*cohort_names: Iterable[str]) -> list[Container]:
        containers = list()
        for cohort_name in cohort_names:
            container = Container(
                content=Text(
                    value=cohort_name
                ),
                width=575,
                height=400,
                bgcolor=Colors.GREY,
            )
            containers.append(container)
        return containers
