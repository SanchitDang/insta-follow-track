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


def unfollow_people():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", f"localhost:{DEBUG_PORT}")

    driver = webdriver.Chrome(options=options)

    with open(r'synced_data/not_following_back.txt', 'r') as not_following_back_data:
        usernames = [line.strip() for line in not_following_back_data.readlines()]

    for user_name in usernames:
        driver.get('https://www.instagram.com/' + user_name)
        try:
            instagram_scraper.human_delay(1.5, 3.0)
            driver.find_element(By.XPATH, '//span[@aria-label="Following"]').click()
            instagram_scraper.human_delay(0.8, 1.8)
            driver.find_element(By.XPATH, '//button[text()="Unfollow"]').click()
            instagram_scraper.human_delay(1.5, 3.0)
        except Exception:
            pass
