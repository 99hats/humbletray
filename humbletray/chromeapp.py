import sys, os, webbrowser
from typing import Text
import shutil, logging
import tempfile, subprocess
from loguru import logger


class FULLSCREEN:
    pass


CHROMECACHE = ".cache"
size = (800, 600)

# from Guy
class ChromeApp:
    def __init__(self, url, appname="driver", size=None, lockPort=None, chromeargs=[]):
        def find_chrome_win():
            import winreg  # TODO: pip3 install winreg

            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
            for install_type in winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE:
                try:
                    with winreg.OpenKey(install_type, reg_path, 0, winreg.KEY_READ) as reg_key:
                        return winreg.QueryValue(reg_key, None)
                except WindowsError:
                    pass

        def find_chrome_mac():
            default_dir = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            if os.path.exists(default_dir):
                return default_dir

        if sys.platform[:3] == "win":
            exe = find_chrome_win()
        elif sys.platform == "darwin":
            exe = find_chrome_mac()
        else:
            for i in ["chromium-browser", "chromium", "google-chrome", "chrome"]:
                try:
                    exe = webbrowser.get(i).name
                    break
                except webbrowser.Error:
                    exe = None

        if not exe:
            raise Exception("no chrome browser, no app-mode !")
        else:
            args = [  # https://peter.sh/experiments/chromium-command-line-switches/
                exe,
                "--app=" + url,  # need to be a real http page !
                "--app-id=%s" % (appname),
                "--app-auto-launched",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-notifications",
                "--disable-features=TranslateUI",
                # ~ "--no-proxy-server",
            ] + chromeargs
            if size:
                if size == FULLSCREEN:
                    args.append("--start-fullscreen")
                else:
                    args.append("--window-size=%s,%s" % (size[0], size[1]))

            if lockPort:  # enable reusable cache folder (coz only one instance can be runned)
                self.cacheFolderToRemove = None
                args.append("--remote-debugging-port=%s" % lockPort)
                args.append("--disk-cache-dir=%s" % CHROMECACHE)
                args.append("--user-data-dir=%s/%s" % (CHROMECACHE, appname))
            else:
                self.cacheFolderToRemove = os.path.join(tempfile.gettempdir(), appname + "_" + str(os.getpid()))
                args.append("--user-data-dir=" + self.cacheFolderToRemove)
                args.append("--aggressive-cache-discard")
                args.append("--disable-cache")
                args.append("--disable-application-cache")
                args.append("--disable-offline-load-stale-cache")
                args.append("--disk-cache-size=0")

            logger.debug("CHROME APP-MODE: %s", " ".join(args))
            self._p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def wait(self):
        self._p.wait()

    def __del__(self):  # really important !
        print("deleting")
        self._p.kill()
        if self.cacheFolderToRemove:
            shutil.rmtree(self.cacheFolderToRemove, ignore_errors=True)

    def exit(self):
        print("exiting")
        # ~ self._com(dict(method="Browser.close"))
        self._p.kill()
        sys.exit()


def open_browser():
    """Returns ChromeApp instance
    or None if Chrome is not installed
    in which case the system browser is used.
    """
    try:
        # we need to keep an instance handle on this or it will immediately self-destruct
        return ChromeApp("http://localhost:8000", "humbletray", (800, 600), lockPort=None, chromeargs=[])
    except:
        # returns None because it is external process
        import webbrowser, time

        webbrowser.open("http://localhost:8000")
        return None


if __name__ == "__main__":
    import justpy as jp
    from multiprocessing import Process

    wp = jp.WebPage()
    jp.Div(text="Success", a=wp)

    def start_server():
        jp.justpy(lambda: wp)

    browser = open_browser()

    jp.justpy(lambda: wp)