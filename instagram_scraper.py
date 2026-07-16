import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

from chrome_session import DEBUG_PORT

load_dotenv()


def human_delay(min_seconds, max_seconds):
    """Randomized pause so scraping activity doesn't have a fixed, bot-like cadence."""
    time.sleep(random.uniform(min_seconds, max_seconds))


# Global configuration
IG_BASE_URL = 'https://www.instagram.com/'
username = os.environ["IG_USERNAME"]

# Instagram regenerates its atomic CSS class names frequently, so the modal's
# scroll container is located at runtime via computed style instead of a
# hardcoded selector.
FIND_SCROLL_CONTAINER_JS = '''
    const dialog = arguments[0];
    const all = dialog.querySelectorAll("div");
    for (const el of all) {
        const cs = getComputedStyle(el);
        if ((cs.overflowY === "auto" || cs.overflowY === "scroll") && el.scrollHeight > el.clientHeight) {
            return el;
        }
    }
    return null;
'''

# Initialize file paths
acc_you_follow_file = r'synced_data/acc_you_follow.txt'
acc_following_you_file = r'synced_data/acc_following_you.txt'


def setup_driver():
    """Set up the WebDriver, attaching to the Chrome session opened via chrome_session.launch_chrome()."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", f"localhost:{DEBUG_PORT}")
    return webdriver.Chrome(options=options)


def extract_usernames(dialog):
    """Read the usernames currently rendered in the followers/following dialog,
    parsed from each row's profile link rather than a hardcoded text class."""
    names = []
    for link in dialog.find_elements(By.CSS_SELECTOR, 'a[role="link"]'):
        href = link.get_attribute('href') or ''
        path = href.replace(IG_BASE_URL, '').strip('/')
        if path and '/' not in path and path not in names:
            names.append(path)
    return names


def collect_usernames(driver, num, file):
    """Scroll the followers/following dialog, writing newly seen usernames
    until num accounts have been collected."""
    dialog = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]'))
    )
    scroller = driver.execute_script(FIND_SCROLL_CONTAINER_JS, dialog)

    seen = []
    stagnant_rounds = 0
    while len(seen) < num and stagnant_rounds < 5:
        for name in extract_usernames(dialog):
            if name not in seen:
                seen.append(name)
                file.write(name + '\n')
                if len(seen) >= num:
                    break

        before = len(seen)
        if scroller:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroller)
        human_delay(0.8, 1.8)
        stagnant_rounds = stagnant_rounds + 1 if len(seen) == before else 0

    if len(seen) < num:
        print(f"WARNING: only collected {len(seen)}/{num} accounts - scrolling stopped "
              f"loading new results (likely Instagram throttling this session). "
              f"Wait a while before syncing again.")


def get_stat_link_and_count(driver, keyword):
    """Find the profile-header stat block (e.g. 'following' or 'followers') and
    return its clickable link element plus the parsed count."""
    count_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{keyword}")]'))
    )
    count = int(count_el.text.split()[0].replace(",", ""))
    link_el = count_el.find_element(By.XPATH, './ancestor::a[1]')
    return link_el, count


def get_acc_you_follow():
    """Collect accounts that the user is following."""
    driver = setup_driver()
    driver.get(IG_BASE_URL + username + '/')
    human_delay(1.5, 3.0)

    link_el, following_count = get_stat_link_and_count(driver, 'following')
    # A native Selenium click lands on the wrong nested element here and is a
    # no-op; dispatching the click via JS reliably triggers Instagram's handler.
    driver.execute_script("arguments[0].click();", link_el)
    human_delay(1.5, 3.0)

    with open(acc_you_follow_file, 'w') as file:
        collect_usernames(driver, following_count, file)


def get_acc_following_you():
    """Collect accounts that follow the user."""
    driver = setup_driver()
    driver.get(IG_BASE_URL + username + '/')
    human_delay(1.5, 3.0)

    link_el, followers_count = get_stat_link_and_count(driver, 'followers')
    driver.execute_script("arguments[0].click();", link_el)
    human_delay(1.5, 3.0)

    with open(acc_following_you_file, 'w') as file:
        collect_usernames(driver, followers_count, file)
