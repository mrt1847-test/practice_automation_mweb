from typing import Tuple

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import os
import subprocess
import io
import re

import sys
import json
import time
import numpy 														# pip install numpy
import random
import requests
import datetime
from datetime import datetime, timedelta


# SELENIUM WEBDRIVER 제어 모듈 										# pip install selenium
from selenium import webdriver
from selenium.webdriver.remote.command import Command

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import *

# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from appium.webdriver.common.appiumby import AppiumBy
# from appium.webdriver.common.mobileby import MobileBy

from assertpy import assert_that
import assertpy


class BasePage:
    """The basis for all pages."""

    IMPLICIT_WAIT_TIME = 10
    TIMEOUT = 30

    def __init__(self, driver):
        """
        Base constructor.
        Sets driver, implicit wait, and timeout.
        """
        self.driver = driver
        self.driver.implicitly_wait(self.IMPLICIT_WAIT_TIME)
        self.timeout = self.TIMEOUT

    def click(self, by_locator: Tuple[str, str], timeout: int = 10):
        return (
            WebDriverWait(self.driver, timeout)
            .until(expected_conditions.visibility_of_element_located(by_locator))
            .click()
        )

    def get_element(self, by_locator: Tuple[str, str], timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(by_locator)
        )

    def send_keys(self, by_locator: Tuple[str, str], text: str):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(by_locator)
        ).send_keys(text)
