from pystray import MenuItem, Menu
import pystray, sys, os
from PIL import Image
import time
from multiprocessing import Process, freeze_support, Queue
import justpy as jp

q = Queue()

fig_name = "leaf.png"

if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
    except NameError:
        application_path = os.getcwd()

fig_full_path = os.path.join(application_path, fig_name)


def action():
    print("action")


def exit_action(icon):
    icon.visible = False
    icon.stop()


def setup(icon):
    icon.visible = True

    i = 0
    while icon.visible:
        # Some payload code
        print(i)
        i += 1

        time.sleep(5)


def run_gui(start_server):
    freeze_support()
    server = Process(target=start_server, args=(q,))
    # server.daemon = True
    server.start()

    icon = pystray.Icon("mon")
    icon.menu = Menu(
        MenuItem("Open", lambda: action),
        MenuItem("Exit", lambda: exit_action(icon)),
    )
    icon.icon = Image.open(fig_full_path)
    icon.title = "tooltip"

    icon.run(setup)
    server.terminate()
    server.join(timeout=1.0)


wp = jp.WebPage(delete_flag=False)


def start_server(iq):
    wp.q = iq
    wp.add(jp.Hello())
    jp.justpy(lambda: wp)


def main():
    run_gui(start_server)


if __name__ == "__main__":
    main()