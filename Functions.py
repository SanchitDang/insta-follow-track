import InstaDataSyncer
from selenium import webdriver
from time import sleep

# Functions
def make_follow_following_data():

    InstaDataSyncer.get_acc_you_follow()
    InstaDataSyncer.human_delay(2, 5)
    InstaDataSyncer.get_acc_following_you()

    acc_following_you = open(r'synced_data/acc_following_you.txt', 'r')
    acc_you_follow = open(r'synced_data/acc_you_follow.txt', 'r')
    not_following_back = open(r'synced_data/not_following_back.txt', 'w')
    you_are_not_following_back = open(r'synced_data/you_are_not_following_back.txt', 'w')

    followers_list = acc_following_you.readlines()
    following_list = acc_you_follow.readlines()

    for following in following_list:
        if following not in followers_list:
            not_following_back.write(following)

    for followers in followers_list:
        if followers not in following_list:
            you_are_not_following_back.write(followers)

def unfollow_people():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:9222")

    driver = webdriver.Chrome(options=options)

    # Unfollow multiple
    with open(r'synced_data\not_following_back.txt', 'r') as not_following_back_data:
        total_user_names = len(not_following_back_data.readlines())
        not_following_back_data.seek(0)
        for i in range(total_user_names):
            user_name = not_following_back_data.readline()
            user_name_without_newline = user_name[:-1]
            driver.get('https://www.instagram.com/' + user_name_without_newline)
            try:
                sleep(2)
                driver.find_element_by_xpath('//span[@aria-label="Following"]').click()
                sleep(1)
                driver.find_element_by_xpath('//button[text()="Unfollow"]').click()
                sleep(2)
            except:
                pass
