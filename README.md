# Instagram Follow Tracker

Tkinter GUI + Selenium tool that finds accounts you follow who don't follow you back.

## Project layout

| File | Purpose |
|---|---|
| `main.py` | Tkinter GUI, entry point (`python main.py`) |
| `chrome_session.py` | Launches Chrome with a Selenium-attachable debug port |
| `instagram_scraper.py` | Scrapes follower/following lists via Selenium |
| `follow_actions.py` | Diffs the scraped lists and drives the unfollow flow |

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

1. Start the app:
   ```
   python main.py
   ```
2. Click **"If you are not logged in"** (or **"Open Session"** for a headless session) — this launches Chrome directly via `chrome_session.py` with a debug port open, using a Chrome profile stored in `chrome_profile/` (created on first run).
3. In that Chrome window, log into Instagram manually. This is a one-time step per profile — the session persists in `chrome_profile/` across runs.
4. Back in the app, click **"If you are logged in"** → **"Sync Data"**. Results are written to `synced_data/not_following_back.txt` and `synced_data/you_are_not_following_back.txt`.

## Known issues

- Selenium/Chrome must already be logged into Instagram before syncing — the app doesn't handle login itself.
- Instagram frequently changes its generated CSS class names. The selectors in `instagram_scraper.py` were captured at one point in time and may need updating if scraping starts failing/timing out.
- Instagram appears to rate-limit the followers/following pagination request after several scrapes in quick succession — if a sync stops short of the full count, wait a while before retrying (a console warning will say so).
