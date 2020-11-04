from humbletray.systray import run_gui
import justpy as jp
from humbletray import systray
from pystray import MenuItem, Menu
from loguru import logger

logger.add("humble.log")
wp = jp.WebPage(delete_flag=False)


def start_server(iq):
    wp.q = iq
    wp.add(jp.Hello())
    jp.justpy(lambda: wp)


def open():
    print("open")
    logger.info("open")


def main():

    # menu = [
    #     MenuItem("Open", lambda: open()),
    # ]
    # systray.run_gui(start_server, menu)
    # systray.run_gui_v2(start_server)
    systray.run_gui_v3(start_server)


if __name__ == "__main__":
    main()