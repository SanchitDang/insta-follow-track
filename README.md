# Instagram Follow Tracker

Tkinter GUI + Selenium tool that finds accounts you follow who don't follow you back.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set your Instagram username in `.env`:
   ```
   IG_USERNAME=your_instagram_username
   ```

## Running

1. **Open a debuggable Chrome session** — launches Chrome on `--remote-debugging-port=9222` so Selenium can attach to it:
   ```
   zDevChrome.bat
   ```
   (The app's "If you are not logged in" button tries to do this via `zOpenDevChrome.vbs`, but that script requests admin elevation and may silently hang on the UAC prompt — running the `.bat` directly is the reliable path.)
2. In that Chrome window, log into Instagram manually.
3. Start the app:
   ```
   python main.py
   ```
4. Click **"If you are logged in"** → **"Sync Data"**. Results are written to `synced_data/not_following_back.txt` and `synced_data/you_are_not_following_back.txt`.

## Known issues

- Selenium/Chrome must already be logged into Instagram before syncing — the app doesn't handle login itself.
- Instagram frequently changes its generated CSS class names. The selectors in `InstaDataSyncer.py` were captured at one point in time and may need updating if scraping starts failing/timing out.
- `Functions.py`'s `unfollow_people()` uses the deprecated `find_element_by_xpath` Selenium API and will need updating to `find_element(By.XPATH, ...)` before it will run on current Selenium versions.
