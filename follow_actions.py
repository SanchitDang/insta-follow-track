from selenium import webdriver
from selenium.webdriver.common.by import By

import instagram_scraper
from chrome_session import DEBUG_PORT


def make_follow_following_data():
    instagram_scraper.get_acc_you_follow()
    instagram_scraper.human_delay(2, 5)
    instagram_scraper.get_acc_following_you()

    with open(r'synced_data/acc_following_you.txt', 'r') as f:
        followers_list = f.readlines()
    with open(r'synced_data/acc_you_follow.txt', 'r') as f:
        following_list = f.readlines()

    with open(r'synced_data/not_following_back.txt', 'w') as not_following_back:
        for following in following_list:
            if following not in followers_list:
                not_following_back.write(following)

    with open(r'synced_data/you_are_not_following_back.txt', 'w') as you_are_not_following_back:
        for followers in followers_list:
            if followers not in following_list:
                you_are_not_following_back.write(followers)


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", f"localhost:{DEBUG_PORT}")
    return webdriver.Chrome(options=options)


def unfollow_account(driver, user_name):
    """Unfollow a single account. Returns True if the unfollow succeeded.

    The "Following" button opens a dropdown menu (Mute/Restrict/Unfollow/...)
    rather than unfollowing directly - both clicks are needed.
    """
    try:
        driver.get('https://www.instagram.com/' + user_name)
        instagram_scraper.human_delay(1.5, 3.0)
        following_btn = driver.find_element(By.XPATH, '//div[text()="Following"]/ancestor::button[1]')
        driver.execute_script("arguments[0].click();", following_btn)
        instagram_scraper.human_delay(0.8, 1.8)
        unfollow_item = driver.find_element(By.XPATH, '//*[text()="Unfollow"]')
        driver.execute_script("arguments[0].click();", unfollow_item)
        instagram_scraper.human_delay(1.5, 3.0)
        return True
    except Exception:
        return False


def unfollow_one(user_name):
    """Unfollow a single account by username - used by the per-row Unfollow button."""
    driver = setup_driver()
    return unfollow_account(driver, user_name)


def unfollow_people():
    driver = setup_driver()

    with open(r'synced_data/not_following_back.txt', 'r') as not_following_back_data:
        usernames = [line.strip() for line in not_following_back_data.readlines()]

    for user_name in usernames:
        unfollow_account(driver, user_name)
