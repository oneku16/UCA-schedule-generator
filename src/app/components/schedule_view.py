from typing import Iterable

from flet import (
    Page,
    Container,
    Column,
    Row,
    Draggable,
    DragTarget,
    Text,
    Stack,
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
from flet.core.types import MainAxisAlignment, CrossAxisAlignment

from consts import DAYS, QUARTERS


class DraggableObject:
    def __init__(self, source: Draggable):
        self.source = source
        self.target = None


class AdminScheduleView(Container):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.bgcolor = Colors.YELLOW_50
        self.alignment = Alignment(0, 0)
        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=self.__build_schedule(
                        'prep', 'fresh', 'soph',
                    )
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=self.__build_schedule(
                        'jun', 'sen',
                    ),

                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text(value='edit'),
                        Text(value='publish'),
                        Text(value='generate'),
                        Text(value='select'),
                    ],
                )
            ],
            alignment='top_center',
        )
        self.page.update()

    def __build_schedule(self, *cohort_names: Iterable[str]) -> list[Container]:
        containers = list()
        for cohort_name in cohort_names:
            container = Container(
                content=Stack(
                    controls=[
                        Container(
                            content=Text(
                                value=cohort_name,
                            ),
                            alignment=center,
                            width=600,
                            height=30,
                            bgcolor=Colors.GREEN_50,
                            top=0,
                        ),
                        Stack(
                            controls=[
                                Container(
                                    content=self.__get_table(),
                                    alignment=center,
                                    width=600,
                                    height=370,
                                    bgcolor=Colors.ORANGE_100
                                ),
                            ],
                            top=30,
                        ),

                    ],
                ),
                width=600,
                height=400,
                bgcolor=Colors.GREY,
                alignment=center,
            )
            containers.append(container)
        return containers

    @staticmethod
    def __get_table() -> Column:
        def get_days():
            return [
                Container(
                    # alignment=MainAxisAlignment.SPACE_BETWEEN,
                    content=Text(value=day),
                    bgcolor=Colors.BROWN_50,
                    height=75,
                    width=100,
                    alignment=center,
                ) for day in DAYS
            ]
        def get_quarters():
            return [
                Container(
                    content=Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=get_days(),
                    )
                ) for _ in QUARTERS
            ]
        return Column(
            alignment=MainAxisAlignment.CENTER,
            controls=get_quarters()
        )


