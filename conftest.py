import time
import subprocess
import pytest
import selenium.webdriver
from appium.options.android import UiAutomator2Options
import platform
import os
from appium import webdriver
import psutil
import json
import socket
import getpass

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

@pytest.fixture
def driver():
    username = getpass.getuser()
    # 디바이스 및 앱 정보 설정pip
    os_version = platform.platform()
    mobile_emulation = {
        "deviceName": "iPhone X"  # 사용하고 싶은 디바이스 이름
    }
    if 'Windows' in os_version:
        chrome_options = selenium.webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_argument("--start-maximized")
        driver = selenium.webdriver.Chrome(options=chrome_options, executable_path="c:/webdriver/chromedriver.exe")
    elif 'mac' in os_version:
        chrome_options = selenium.webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        driver = selenium.webdriver.Chrome(
            options=chrome_options, executable_path="/Users/" + username + "/webdriver/chromedriver")
    yield driver
    # 테스트 종료 후 Appium 서버와 연결 종료
    driver.quit()
