from contextlib import contextmanager
import types
from dataclasses import dataclass
import justpy as jp
import atexit


# @contextmanager
# def _(w):
#     # to nest gui building
#     yield w


@dataclass
class Menu:
    icon: str
    label: str
    separator: bool
    page: object


def new__init__(self, *args, **kw):
    print("new init")
    self.__parent__ = kw.get("a")
    self.__init__(*args, **kw)


@contextmanager
def _(widget, *args, **kw):
    def __webpage__(self):
        a = self.a
        while True:
            if isinstance(a, jp.QuasarPage) or a is None:
                return a
            a = a.a

    widget.__webpage__ = __webpage__
    try:
        yield widget
    finally:
        if kw.get("_finally"):
            kw["_finally"]()


class DefaultLayout(jp.QuasarPage):
    def __init__(self, **kwargs):
        atexit.register(self.close)
        super().__init__(**kwargs)
        layout = jp.QLayout(view="hHh Lpr lff", classes="q-pa-md", style="height:300px", a=self)

        async def toggle_menu(comp, msg):
            print("button clicked")
            await drawer.run_method("toggle()", msg.websocket)

        with _(jp.QHeader(elevated=True, classes="bg-black", a=layout)) as header:
            with _(jp.QToolbar(a=header)) as toolbar:
                toolbar += jp.QBtn(flat=True, round=True, dense=True, icon="menu", click=toggle_menu)
                toolbar += jp.QToolbarTitle(text="Header!!")

        with _(
            jp.QDrawer(
                v_model="drawer",
                show_if_above=True,
                width=200,
                breakpoint=500,
                bordered=True,
                content_class="bg-grey-3",
                a=layout,
            )
        ) as drawer:
            with _(jp.QScrollArea(classes="fit", a=drawer)) as scrollarea:
                with _(jp.QList(a=scrollarea)) as qlist:
                    with _(jp.Div(a=qlist)) as menu:
                        self.menu = menu
        page_container = jp.QPageContainer(a=layout)
        self.content = jp.QPage(padding=True, a=page_container)

    def close(self):
        print("close", self)


def main():
    """ Usage """

    def create_wp():
        """Create separate websession

        Otherwise, it's a shared session which of course can be cool.
        """
        wp = DefaultLayout()  # delete_flag=False)
        return wp

    def foo(self, msg):
        msg.page.content.delete_components()
        jp.QBtn(text="back to main", click=index, a=msg.page.content)
        for n in range(0, 155):
            msg.page.content.add(
                jp.P(
                    text="Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugit nihil praesentium molestias a adipisci, dolore vitae odit, quidem consequatur optio voluptates asperiores pariatur eos numquam rerum delectus commodi perferendis voluptate?"
                )
            )

    def index(self, msg):
        msg.page.content.delete_components()
        jp.QBtn(text="foo", click=foo, a=msg.page.content)

    def create_menu(menu_list, wp3):
        wp3.menu.delete_components()
        for i, menu in enumerate(menu_list):
            qitem = jp.QItem(clickable=True, v_ripple=True, a=wp3.menu, click=menu.page)
            qs1 = jp.QItemSection(avatar=True, a=qitem)
            qs1 += jp.QIcon(name=menu.icon)
            qitem += jp.QItemSection(text=menu.label)
            if menu.separator:
                wp3.menu += jp.QSeparator(key="sep" + str(i))

    def app():
        menu_list = [
            Menu("inbox", "Inbox", True, foo),
            Menu("send", "Outbox", False, index),
            Menu("delete", "Trash", False, foo),
            Menu("error", "Spam", True, index),
            Menu("settings", "Settings", True, foo),
            Menu("feedback", "Send Feedback", True, foo),
            Menu("help", "Help", True, foo),
        ]

        wp = create_wp()  # if you want separate web sessions
        create_menu(menu_list, wp)

        class msg(object):  # a weird bit since we're avoiding use of requests
            page = wp

        index(None, msg)
        import pdb

        # pdb.set_trace()
        return wp

    jp.justpy(app)


if __name__ == "__main__":
    main()