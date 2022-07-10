import itertools
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By


# TODO : WIP - Need to implement test cases for integration testing
import asyncio

# driver = webdriver.Chrome(executable_path="~/chromedriver")


# async def test_multi_user(username, password):
#     driver = webdriver.Chrome(executable_path="/home/manimoha/Downloads/chromedriver")
#     driver.get("http://127.0.0.1:8000/client/")
#     print(driver.title)
#     search_bar = driver.find_element("id", "chat-message-input")
#     search_bar.send_keys(f"register {username} {password}")
#     search_bar.send_keys(Keys.RETURN)
#     await asyncio.sleep(0.1)
#     search_bar.send_keys(f"connect {username} {password}")
#     search_bar.send_keys(Keys.RETURN)
#     await asyncio.sleep(0.1)
#     search_bar.send_keys("look")
#     search_bar.send_keys(Keys.RETURN)
#     await asyncio.sleep(200)


# async def test():
#     for permutation in itertools.permutations("def"):
#         username = "".join(permutation)
#         await test_multi_user(username, username)


# loop = asyncio.get_event_loop()
# tasks = []
# for permutation in itertools.permutations("bcd"):
#     username = "".join(permutation)
#     pasword = username
#     tasks.append(loop.create_task(test_multi_user(username, pasword)))

# loop.run_until_complete(asyncio.wait(tasks))
