import os
import shutil
import time
import random
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions

MAXWAIT = 60.

def format_string(string):
    return string.replace(' ', '-')
def check_string(string):
    return string.replace(' ', '-').replace('-', '').isnumeric()

def wait_check(condition, maxWait = None):
    waited = 0.
    while not condition():
        waitTime = random.random()
        time.sleep(waitTime)
        waited += waitTime
        if not maxWait is None:
            if waited > maxWait:
                raise Exception("Wait time exceeded!")

def download_all(linksDict, tempDir, outDir, outExt, keys = None, notkeys = set(), maxWait = MAXWAIT):
    print("Downloading all...")
    if keys is None:
        keys = linksDict.keys()
    keys = sorted([key for key in keys if key not in notkeys])
    for key in keys:
        newFilename = key + outExt
        if newFilename in os.listdir(outDir):
            print("File already exists - skipping.")
        else:
            link = linksDict[key]
            link.click()
            wait_check(lambda: len(os.listdir(tempDir)), maxWait)
            oldFilename = os.listdir(tempDir)[0]
            oldFilepath = os.path.join(tempDir, oldFilename)
            newFilepath = os.path.join(outDir, newFilename)
            os.rename(oldFilepath, newFilepath)
            wait_check(lambda: not len(os.listdir(tempDir)), maxWait)
            print("Downloaded:", newFilename)
    print("Downloaded all.")

class Driver:
    def __init__(self, options, profile, tempDir = None):
        if tempDir is None:
            tempDir = os.path.join(os.path.getcwd(), '_temp')
        self.options, self.profile, self.tempDir = \
            options, profile, tempDir
    def __enter__(self):
        self.driver = webdriver.Firefox(
            options = self.options,
            firefox_profile = self.profile
            )
        if not os.path.isdir(self.tempDir):
            os.makedirs(self.tempDir, exist_ok = False)
        return self.driver
    def __exit__(self, *args):
        self.driver.quit()
        if os.path.isdir(self.tempDir):
            shutil.rmtree(self.tempDir)
        if os.path.isfile('geckodriver.log'):
            os.remove('geckodriver.log')

def pull_datas(dataURL, loginName, loginPass, outDir, dataMime, outExt, **kwargs):

    parsed = urlparse(dataURL)
    loginURL = '://'.join(parsed[:2])

    outDir = os.path.abspath(outDir)
    if not os.path.isdir(outDir):
        os.makedirs(outDir, exist_ok = True)
    tempDir = os.path.join(outDir, '_temp')

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", tempDir)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", dataMime)
    options = Options()
    options.add_argument("--headless")

    with Driver(options, profile, tempDir) as driver:

        print("Navigating to login page...")
        try:
            driver.get(loginURL)
        except exceptions.WebDriverException:
            raise ValueError("No login page found!")
        print("Navigated to login page.")

        print("Logging in...")
        username = driver.find_element_by_id("email")
        password = driver.find_element_by_id("pass")
        submit   = driver.find_element_by_id("loginbutton")
        username.send_keys(loginName)
        password.send_keys(loginPass)
        submit.click()
        try:
            loginForm = driver.find_element_by_id("login_form")
            raise ValueError("Bad login credentials!")
        except exceptions.NoSuchElementException:
            pass
        print("Logged in.")

        print("Navigating to data page...")
        try:
            driver.get(dataURL)
        except exceptions.WebDriverException:
            raise ValueError("Bad data URL!")
        print("Navigated to data page.")

        print("Finding data...")
        linksDict = {
            format_string(elem.text): elem \
                for elem in driver.find_elements_by_xpath("//a[@href]") \
                    if check_string(elem.text)
            }
        if len(linksDict) > 0:
            print("Data found.")
            download_all(linksDict, tempDir, outDir, outExt, **kwargs)
        else:
            print("No data found at that URL. Aborting.")
