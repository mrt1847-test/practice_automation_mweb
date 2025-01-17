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

with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

@pytest.fixture
def driver():
    # 디바이스 및 앱 정보 설정pip
    os_version = platform.platform()
    if 'Windows' in os_version:
        opts = selenium.webdriver.ChromeOptions()
        opts.add_argument("--start-maximized")
        driver = selenium.webdriver.Chrome(options=opts, executable_path="c:/webdriver/chromedriver.exe")
    elif 'mac' in os_version:
        opts = selenium.webdriver.ChromeOptions()
        opts.add_argument("--start-maximized")
        driver = selenium.webdriver.Chrome(
            options=opts, executable_path="/Users/" + username + "/webdriver/chromedriver")
    yield driver
    # 테스트 종료 후 Appium 서버와 연결 종료
    driver.quit()
