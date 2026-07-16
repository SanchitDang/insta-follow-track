"""Launches a Chrome instance with a remote-debugging port so Selenium can
attach to it. Replaces the old zDevChrome.bat / zOpenDevChrome.vbs pair -
running Chrome via subprocess directly needs no admin elevation, unlike the
old vbs launcher's "runas" verb, which silently hung on the UAC prompt.
"""
import os
import subprocess

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEBUG_PORT = 9222
# Chrome silently exits if --user-data-dir is relative, so this is resolved
# to an absolute path up front.
PROFILE_DIR = os.path.abspath("chrome_profile")


def launch_chrome(headless=False):
    """Open Chrome pointed at Instagram with the debug port enabled.

    Log into Instagram manually in the window that opens; the debug port
    lets Selenium (see instagram_scraper.py) attach to this same session.
    """
    args = [
        CHROME_PATH,
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={PROFILE_DIR}",
    ]
    if headless:
        args += ["--headless", "--disable-gpu"]
    else:
        args += ["--app=https://www.instagram.com"]
    subprocess.Popen(args)
