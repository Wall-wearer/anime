from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from datetime import datetime, time
from selenium.webdriver.support.ui import Select
from threading import Thread
from time import sleep
import random
import os
import pytz

# put the URLs of the anime here
urls = [
    # 'https://www.olevod.tv/details/4/50671',    # 家里蹲吸血姬的苦闷
    # 'https://www.olevod.tv/details/4/48575',    # 黑暗集会
    'https://www.olevod.tv/details/4/50657',    # 不死不幸
    'https://www.olevod.tv/details/4/50435',    # 葬送的芙莉莲
    # 'https://www.olevod.tv/details/4/50631',    # 哥布林杀手 第二季
    # 'https://www.olevod.tv/details/4/50589',    # 16bit的感动
    # 'https://www.olevod.tv/details/4/51243',    # 关于我转生变成史莱姆这档事 彩叶草之梦
    # 'https://www.olevod.tv/details/4/48561',    # 僵尸100～变成僵尸之前想做的100件事
    # 'https://www.olevod.tv/details/4/50701',    # 超超超超超喜歡你的 100 個女朋友
    'https://www.olevod.tv/details/4/50492',    # 香格里拉·开拓异境～粪作猎手挑战神作
    'https://www.olevod.tv/details/4/50485',    # 狩龙人拉格纳
    # 'https://www.olevod.tv/details/4/50697',    # 间谍过家家 第二季
    'https://www.olevod.tv/details/4/52816',    # 不是真正的伙伴被赶出勇者队伍 第二季
    'https://www.olevod.tv/details/4/52687',    # 实力至上主义的教室 第三季
    'https://www.olevod.tv/details/4/53009',    # 开除坦克异世界
    'https://www.olevod.tv/details/4/52792',    # 我独自升级
    'https://www.olevod.tv/details/1/52709',    # 梦想成为魔法少女
    'https://www.olevod.tv/details/4/52880',    # 恶役千金LV99
    'https://www.olevod.tv/details/4/52794',    # 轮回七次的恶役千金
    'https://www.olevod.tv/details/4/52850',    # 公主大人，接下来是“拷问”时间
    'https://www.olevod.tv/details/4/52715',    # 魔都精兵的奴隶
    'https://www.olevod.tv/details/4/52851',    # 愚蠢天使与恶魔共舞
    'https://www.olevod.tv/details/4/51020',    # 药屋少女的呢喃
    'https://www.olevod.tv/details/4/52926'     # 勇气爆发
]

# Define the time interval (45 minutes in seconds)
gap = 3 * 10 * 60  # 45 minutes


def time_check():
    # Get the current time in the desired time zone
    # time_zone = pytz.timezone('Your_Time_Zone_Here')
    current_time = datetime.now().time()

    # Define the time range
    start_time = datetime.strptime('22:00', '%H:%M').time()
    end_time = datetime.strptime('03:00', '%H:%M').time()

    if start_time <= current_time or current_time <= end_time:
        return True
    else:
        return False


# Coooool thing
# create a reminder on reminder app
def create_reminder(title, body, url, list_name):
    # this is a script
    script = f'''
        tell application "Reminders"
            set theList to list "{list_name}"
            set newReminder to make new reminder at end of reminders of theList
            set name of newReminder to "{title}"
            set body of newReminder to "{body}, {url}, {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
        end tell
    '''
    os.system(f"osascript -e '{script}'")


def notify(title, filename):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(filename, title))


def start(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.headless = True

    # Create an undetected Chrome driver
    driver = uc.Chrome(options=chrome_options)
    # Navigate to the webpage
    driver.get(url)
    return driver


# used to get the name of the anime
def get_anime_name(soup):
    # get the title
    get_title = soup.find('div', class_='pc-details-bg')  # find only return the first thing it found
    title_index = get_title.find('div', class_='title')
    title = title_index.text
    # print(f"番名：{title}")
    return title


# Function to save updated episodes to the file
def save_updated_episodes(episodes, filename):
    with open(filename, 'w') as file:
        for episode in episodes:
            file.write(episode + "\n")


# Function to create and initialize a file to store previous titles
def initialize_previous_titles_file(filename):
    with open(filename, 'w') as file:
        # Write an initial placeholder value or an empty list
        # For example, you can write an empty list as the initial value
        file.write('[]')


def load_previous_episodes(filename):
    try:
        with open(filename, 'r') as file:
            previous_episodes = file.read().splitlines()  # splitlines: split the string into a list of lines
            '''
            把几行内容中的东西拆分：
            line 1
            line 2
            line 3
            =>
            [line 1, line 2, line 3]
            去掉其中的\n
            '''
        return previous_episodes
    except FileNotFoundError:
        return []


def check_for_new_episodes(url, driver, filename):
    # Load the previous episodes
    previous_episodes = load_previous_episodes(filename)  # 返回了一个呈数组的东西

    # Find the parent element that contains the titles of episodes
    episode_count = driver.find_element(By.CLASS_NAME, 'el-row.item')
    # here, the episode element contained in 'el-row.item'

    # Here, if the url is available
    if episode_count:  # if the episode is located
        # Find all episodes within the parent element
        episode_elements = episode_count.find_elements(By.CLASS_NAME, 'list-content')

        # Extract the episodes and store them in a list
        # extract episodes from 'episode_elements' and store them into 'current_episodes'
        current_episodes = [current.text for current in episode_elements]
        '''
        current.text: find the elements text attribute
        从当前的episode_elements中获取元素以.text存入数列
        '''

        # Compare the current episodes with the previous episodes
        new_episodes = [episode for episode in current_episodes if episode not in previous_episodes]
        '''
        这里，episode是用来占位置的，即将数组current_episodes中的每个元素作为episode存储在'new_episodes'中
        （条件：在'current_episodes'中存在但是不在'previous_episodes'中）
        此处创建一个新数组，来存放后面发现的东西，如果没有发现新的数据则将会返回一个空数组。
        '''

        if new_episodes:  # if 'new_episodes' is not empty, return True.
            print("New episodes found for", url, filename, datetime.now())
            for episode in new_episodes:
                print("New episode:", episode)

                # add to reminder
                create_reminder(filename, episode, url, "Anime")
                notify("Found", filename)

                # Save the current episodes as the new previous episodes
                save_updated_episodes(current_episodes, filename)
        else:
            print("No new episodes found for", url, filename)
    else:
        print("Error: Can't locate the episodes for", url, filename)


# main
def process(url):
    # initial part, to find out the basic information of the anime
    driver = start(url)
    # waiting for refresh
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'list-content')))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')  # 完全读取整个html

    title = get_anime_name(soup)  # get the information of the anime
    filename = f'{title}.txt'  # Construct the filename

    # use to list the all episodes it has.
    # episode_elements = soup.find_all('div', class_="list-content")  # find out all the episodes and return its number
    # print(f"Number of Episode: {len(episode_elements)}")

    # check the new episode
    check_for_new_episodes(url, driver, filename)


# main
#while True:
#if time_check():
print("Checking...")
for url in urls:
    process(url)  # Main process to check for new episodes

print(f"finished at: {datetime.now().time()}")

print(f"Finished one loop, restart {gap/3600} hour later...")
# print(f"..{}..") ables print variables inside the {} to terminal

# notice me checking finished.
# Sleep for one hour (3600 seconds)
#sleep(gap)
#else:
#    print("Waiting for 22:00 to start...")
    #notify("Finished", "There is no new episodes")
#    sleep(gap)
