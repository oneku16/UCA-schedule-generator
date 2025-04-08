import flet as ft

from flet import Draggable, DragTarget, DragTargetEvent, Page


import flet
from flet import (
    Column,
    Container,
    Draggable,
    DragTarget,
    DragTargetEvent,
    Page,
    Row,
    border,
    Colors,
)


class DraggableObject(Draggable):
    def __init__(self, content, page: Page, source: DragTarget, on_drag_start):
        super().__init__(content=content, on_drag_start=on_drag_start)
        self.source = source
        self.page = page
        self.target = None
        self.width = 50
        self.height=50

    def swap(self):
        self.page.update()


def main(page: Page):
    drag_controls = [
        DragTarget(
            content=Container(
                content=flet.Text(),
                # bgcolor=Colors.GREEN,
            )
        ) for num in range(1, 3)
    ]

    page.title = "Drag and Drop example"

    def drag_will_accept(e):
        e.control.content.border = border.all(
            2, Colors.BLACK45 if e.data == "true" else Colors.RED
        )
        e.control.update()

    def drag_accept(e: DragTargetEvent):
        print(type(e))
        print(e.control.content.content.value)
        print(e.control.content)
        print(400)
        src = page.get_control(e.src_id)
        e.control.content.bgcolor = src.content.bgcolor
        print(src.content.content.value)
        print(e.control.content.content.content.content.value)
        e.control.content.content.content.content.value, src.content.content.value = src.content.content.value, e.control.content.content.content.content.value
        # e.control.content.content.value = src.content.content.value
        e.control.content.border = None
        e.control.update()

    def drag_leave(e):
        e.control.content.border = None
        e.control.update()

    def f(e):
        src = e.control
        print(src.content.content.value)
        print(src.source.content.content.value)

        # src.source.content.content.value, src.content.content.value = src.content.content.value, src.content.content.content.value
        page.update()
    from random import randint
    real_controls = [
        DraggableObject(
            content=Container(
                content=flet.Text(
                    value=f'{randint(1, 100)}'
                ),
                bgcolor=Colors.GREEN,
                width=50,
                height=50,
            ),
            page=page,
            source=drag_control,
            on_drag_start=f,
        ) for drag_control in drag_controls
    ]
    for a, b in zip(drag_controls, real_controls):
        a.content.content = flet.Text(value=b.content.content.value)

    page.add(
        Row(
            controls=real_controls,
            # [
                # Column(
                #     [
                #         Draggable(
                #             group="color",
                #             content=Container(
                #                 content=flet.Text(value='Yes'),
                #                 width=50,
                #                 height=50,
                #                 bgcolor=Colors.CYAN,
                #                 border_radius=5,
                #             ),
                #             content_feedback=Container(
                #                 content=flet.Text(value='Fuck u'),
                #                 width=20,
                #                 height=20,
                #                 bgcolor=Colors.CYAN,
                #                 border_radius=3,
                #             ),
                #         ),
                #         Draggable(
                #             group="color",
                #             content=Container(
                #                 content=flet.Text(value="orange"),
                #                 width=50,
                #                 height=50,
                #                 bgcolor=Colors.ORANGE_100,
                #                 border_radius=5,
                #             ),
                #         ),
                #         Draggable(
                #             group="color",
                #             content=Container(
                #                 content=flet.Text(value="QWER"),
                #                 width=50,
                #                 height=50,
                #                 bgcolor=Colors.GREEN,
                #                 border_radius=5,
                #             ),
                #         ),
                #     ]
                # ),
                # Container(width=100, bgcolor='red'),
                # DragTarget(
                #     group="color",
                #     content=Container(
                #         content=Draggable(
                #             content=Container(
                #                 content=flet.Text(value="A"),
                #                 bgcolor=Colors.GREY,
                #             ),
                #             on_drag_start=drag_accept
                #
                #         ),
                #         width=50,
                #         height=50,
                #         bgcolor=Colors.BLUE_GREY_100,
                #         border_radius=5,
                #     ),
                #     on_will_accept=drag_will_accept,
                #     on_accept=drag_accept,
                #     on_leave=drag_leave,
                # ),
                # DragTarget(
                #     group="color",
                #     content=Container(
                #         content=Draggable(
                #             content=Container(
                #                 content=flet.Text(value="B"),
                #                 bgcolor=Colors.GREY,
                #             )
                #
                #         ),
                #         width=50,
                #         height=50,
                #         bgcolor=Colors.BLUE_GREY_100,
                #         border_radius=5,
                #     ),
                #     on_will_accept=drag_will_accept,
                #     on_accept=drag_accept,
                #     on_leave=drag_leave,
                # ),
            # ]
        )
    )


flet.app(main)