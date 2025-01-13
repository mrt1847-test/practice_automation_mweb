import time
import subprocess
import pytest
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
    if 'Windows' in os_version:  # windows인 경우
        app_path = os.path.abspath(config["win"]["app_path"])
        chrome_path = os.path.abspath(config["win"]["chrome_path"])
    elif 'mac' in os_version:
        app_path = os.path.abspath(config["mac"]["app_path"])
        chrome_path = os.path.abspath(config["mac"]["chrome_path"])
    options = UiAutomator2Options()
    options.platformName = "Android"
    options.deviceName = "AOS14"  # 에뮬레이터 또는 실제 장치의 이름
    options.app = app_path  # 앱의 APK 파일 경로
    options.appPackage = "com.ebay.kr.gmarket"  # 앱 패키지 이름
    options.appActivity = "com.ebay.kr.gmarket.eBayKoreaGmarketActivity"  # 시작 액티비티 이름
    options.adbExecTimeout = 60000
    options.noReset = False
    options.set_capability("goog:chromeOptions", {
        "androidPackage": "com.ebay.kr.gmarket",  # 앱 패키지
        "androidProcess": "com.ebay.kr.gmarket"  # 앱 프로세스 (필요한 경우 설정)
    })
    # options.set_capability("chromedriverExecutable", chrome_path)
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("acceptInsecureCerts",True)
    # options.set_capability("chromedriverPort", 9515)
    # options.set_capability("goog:loggingPrefs", {
    #     "browser": "ALL"
    # })
    # options.set_capability("autoWebview", True)

    # adb shell dumpsys package com.android.chrome | findstr versionName
    # adb shell dumpsys package com.android.chrome | grep versionName

    # desired_capabilities = {
    #     "platformName": "Android",
    #     "deviceName": "",
    #     "automationName": "UiAutomator2",
    #     "app": app_path,
    #     "newCommandTimeout": 900,
    #     "appPackage": "com.ebay.kr.gmarket",
    #     "appActivity": "com.ebay.kr.gmarket.eBayKoreaGmarketActivity",
    #     "acceptInsecureCerts": True,
    #     "noReset": False,
    #     "chromedriverExecutable": chrome_path,
    #     "appium:chrome_options": {
    #         "androidPackage": "com.ebay.kr.gmarket"
    #     }
    # }

    # Appium 서버와 연결
    driver = None
    try:
        # driver = webdriver.Remote("http://localhost:4723", desired_capabilities=desired_capabilities)
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        print("Driver initialized successfully!")
    except Exception as e:
        print(f"Driver initialization failed: {e}")
        raise
    while driver == None:
        time.sleep(1)
        print("드라이버 생성 대기중")

    driver.start_activity("com.ebay.kr.gmarket","com.ebay.kr.gmarket.eBayKoreaGmarketActivity")
    yield driver
    # 테스트 종료 후 Appium 서버와 연결 종료
    driver.quit()

def is_appium_server_running(host="localhost", port=4723):
    """Appium 서버가 실행 중인지 확인"""
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (ConnectionRefusedError, socket.timeout):
        return False

@pytest.fixture(scope="session", autouse=True)
def manage_appium_server():
    print("appium 실행")
    try:
        os_version = platform.platform()
        # 운영 체제에 따라 명령어 설정
        if 'mac' in os_version:  # 맥 OS인 경우
            process = subprocess.Popen("appium --allow-insecure chromedriver_autodownload", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time.sleep(5)
        elif 'Windows' in os_version:  # windows인 경우
            process = subprocess.run('start cmd /K "appium --allow-insecure chromedriver_autodownload"', shell=True)
            time.sleep(5)

    except FileNotFoundError:
        print("Appium이 시스템 경로에 설치되어 있는지 확인하세요.")

    except Exception as e:
        print("오류 발생:", e)

    for _ in range(10):  # 최대 10초 대기
        if is_appium_server_running():
            print("Appium 서버가 실행되었습니다.")
            break
        time.sleep(1)
    else:
        raise RuntimeError("Appium 서버 시작 실패")

    yield process
    # 테스트 종료 후 Appium 서버 종료
    print("테스트 종료 후 정리 작업 시작...")
    try:
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            try:
                # cmdline 속성의 유효성을 확인합니다.
                if proc.info['cmdline'] and 'appium' in ' '.join(proc.info['cmdline']):
                    # 프로세스를 종료합니다.
                    psutil.Process(proc.info['pid']).terminate()
                    print(f"Appium process with PID {proc.info['pid']} terminated.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, IndexError):
                pass
    except Exception as e:
        print("Appium 종료 중 오류 발생:", e)