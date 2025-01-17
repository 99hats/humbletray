from humbletray import layout, systray, chromeapp
import justpy as jp

wp = jp.WebPage(delete_flag=False)
app = None


def serve(q):
    print("serve")
    jp.Div(text="Success", a=wp)
    jp.Hello(a=wp)
    jp.justpy(lambda: wp)


def main_v1():
    global app
    if app is None:
        app = chromeapp.ChromeApp("http://localhost:8000", "humbletray", (800, 600), lockPort=None, chromeargs=[])
    systray.run_gui(serve)
    print("closing")
    app.exit()
    try:
        app.wait()  # block
    except KeyboardInterrupt:
        print("-Process stopped")
    app.exit()


if __name__ == "__main__":
    main_v1()