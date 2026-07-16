# Instagram Follow Tracker

Tkinter (ttkbootstrap) GUI + Selenium tool that finds accounts you follow who don't follow you back, and unfollows them.

## Project layout

| File | Purpose |
|---|---|
| `main.py` | GUI, entry point (`python main.py`) |
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
2. On the first page, click **"Open Chrome"** (or **"Open Chrome (Headless)"**) — this launches Chrome directly via `chrome_session.py` with a debug port open, using a Chrome profile stored in `chrome_profile/` (created on first run).
3. In that Chrome window, log into Instagram manually. This is a one-time step per profile — the session persists in `chrome_profile/` across runs.
4. Back in the app, click **"Continue to Dashboard"**, then **"Sync Data"**. Results are written to `synced_data/not_following_back.txt` and `synced_data/you_are_not_following_back.txt`.
5. From the dashboard, **"View Accounts Not Following Back"** opens a list with a per-account Unfollow button, or **"Unfollow All That Don't Follow Back"** does the whole list at once (with a confirmation prompt first — this performs real, hard-to-undo actions on Instagram).

## Known issues

- Selenium/Chrome must already be logged into Instagram before syncing — the app doesn't handle login itself.
- Instagram frequently changes its generated CSS class names. The selectors in `instagram_scraper.py` and `follow_actions.py` were captured at one point in time and may need updating if scraping/unfollowing starts failing/timing out.
- Instagram appears to rate-limit the followers/following pagination request after several scrapes in quick succession — if a sync stops short of the full count, wait a while before retrying (a console warning will say so).
