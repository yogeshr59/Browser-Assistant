from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something!")
        try:
            audio = r.listen(source, timeout=2.5, phrase_time_limit=2.5)
            text = r.recognize_google(audio)
            print("You said : ", text)
            return text
        except:
            return takecommand()


def scrolldown(driver):
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()


def scrollup(driver):
    ActionChains(driver).send_keys(Keys.PAGE_UP).perform()


"""
def nextab(browser):
    browser.switch_to.window(browser.window_handles[browser.window_handles.index(browser.current_window_handle) - 1])
    # ActionChains(browser).send_keys(Keys.CONTROL, Keys.TAB, Keys.CONTROL).perform()
"""


def nextab(driver):
    lst = driver.window_handles
    idx = lst.index(driver.current_window_handle)
    if idx >= len(lst) - 1:
        idx = -1
    driver.switch_to.window(lst[idx + 1])


""" 
def prevtab(driver):
    driver.switch_to.window(driver.window_handles[driver.window_handles.index(driver.current_window_handle) + 1])
"""


def prevtab(driver):
    lst = driver.window_handles
    idx = lst.index(driver.current_window_handle)
    if idx - 1 < 0:
        idx = len(lst)
    driver.switch_to.window(lst[idx - 1])


prev = 0

"""
def closetab(driver):
    global prev
    driver.close()
    # prev = prev - 1
    driver.switch_to.window(driver.window_handles[driver.current_window_handle])
"""


def closetab(driver):
    lst = driver.window_handles
    idx = lst.index(driver.current_window_handle)
    driver.close()
    if (idx == 0):
        driver.switch_to.window(lst[idx + 1])
    else:
        driver.switch_to.window(lst[idx - 1])
    del lst[idx]


def newtab(driver, url="https://www.google.com"):
    lst = driver.window_handles
    # idx = lst.index(driver.current_window_handle)
    idx = len(lst)
    prev = idx
    driver.execute_script("window.open('" + url + "', 'new_window" + str(prev) + "')")
    lst = driver.window_handles
    # idx = lst.index(driver.current_window_handle)
    idx = len(lst)
    prev = idx - 1
    driver.switch_to.window(lst[prev])


"""
def newtab(driver, url="https://www.google.com"):
    global prev
    driver.execute_script("window.open('" + url + "', 'new_window" + str(prev) + "')")
    prev = prev + 1
    driver.switch_to.window(driver.window_handles[driver.window_handles.index(driver.current_window_handle) + 1])
"""


def gnewtab(driver, url="https://www.google.com"):
    global prev
    driver.execute_script("window.open('" + url + "', 'new_window" + str(prev) + "')")
    prev = prev + 1


def goback(driver):
    driver.back()


def goforward(driver):
    driver.forward()


def refreshpage(driver):
    driver.refresh()


# def closetab(driver):
#    driver.close()


def ytdownload(driver):
    url = driver.current_url
    url = url.replace('https://www.', '')
    url = 'https://www.ss' + url
    driver.get(url)
    try:
        time.sleep(8)
        driver.find_element_by_css_selector("a.link.link-download.subname.ga_track_events.download-icon").click()
        nextab(driver)
        closetab(driver)
    except:
        time.sleep(7)
        driver.find_element_by_css_selector("a.h10__mq_btn").click()
        time.sleep(7)
        driver.find_element_by_class_name("a.link.link-download.subname.ga_track_events.download-icon").click()
        nextab(driver)
        closetab(driver)


def fvideo(driver):
    driver.find_element_by_css_selector('body').send_keys(Keys.ARROW_RIGHT)


def rvideo(driver):
    driver.find_element_by_css_selector('body').send_keys(Keys.ARROW_LEFT)


def checkcommand(comm, driver):
    if "down" in comm.lower():
        scrolldown(driver)
    if "up" in comm.lower():
        scrollup(driver)
    if "new tab" in comm.lower():
        newtab(driver)
    if "next" in comm.lower():
        nextab(driver)
    if "previous" in comm.lower():
        prevtab(driver)
    if "back" in comm.lower():
        goback(driver)
    if "forward" in comm.lower() and "go" in comm.lower():
        goforward(driver)
    if "open google" in comm.lower():
        opengoogle(driver)
    if "close tab" in comm.lower():
        closetab(driver)
    if "open youtube" in comm.lower():
        openyt(driver)
    if "play" in comm.lower() or "pause" in comm.lower():
        ytplaypause(driver)
    if "skip" in comm.lower() or "refresh" in comm.lower():
        refreshpage(driver)
    if "download" in comm.lower():
        ytdownload(driver)
    if "rewind video" in comm.lower():
        rvideo(driver)
    if "forward video" in comm.lower():
        fvideo(driver)
    if "facebook" in comm.lower():
        start(driver)
    if "my profile" in comm.lower():
        profile(driver)
    if "logout" in comm.lower():
        logout(driver)
    if "search profile" in comm.lower():
        print("What is the name?")
        text = takecommand()
        searchprofile(driver, text)
    if "set" in comm.lower():
        setfb()
        print("Credentials saved successfully")
    else:
        print("Sorry, Cannot Execute this command...")


def gsearch(comm, driver):
    driver.find_element_by_name("q").send_keys(comm)
    driver.find_element_by_name("q").send_keys(Keys.RETURN)

    links = driver.find_elements_by_class_name("r")
    cnt: int = 0
    for i in links:
        gnewtab(driver, i.find_element_by_css_selector('a').get_attribute('href'))
        cnt = cnt + 1
        if (cnt == 3):
            break
    lst = driver.window_handles
    idx = lst.index(driver.current_window_handle)
    driver.switch_to.window(lst[idx + 1])


def opengoogle(driver):
    driver.get("https://www.google.com")
    print("What do you want to search for?")
    text = takecommand()
    gsearch(text, driver)


def openyt(driver):
    driver.get("https://www.youtube.com")
    print("What do you want to search?")
    text = takecommand()
    driver.find_element_by_id("search").send_keys(text)
    driver.find_element_by_id("search").send_keys(Keys.RETURN)
    links = driver.find_elements_by_css_selector("a#video-title.yt-simple-endpoint.style-scope.ytd-video-renderer")

    cnt = 0
    for i in links:
        gnewtab(driver, i.get_attribute("href"))
        cnt = cnt + 1
        if (cnt == 3):
            break
    lst = driver.window_handles
    idx = lst.index(driver.current_window_handle)
    driver.switch_to.window(lst[idx + 1])


def ytplaypause(driver):
    driver.find_element_by_css_selector("body").send_keys(Keys.SPACE)


username = "8140189833"
password = "testaccount123"


def start(driver):
    driver.get("https://www.facebook.com")
    obj = driver.find_element_by_name("email")
    # obj.clear()'
    file = open("username.txt",'r')
    user = file.read()
    file.close()
    obj.send_keys(user)
    time.sleep(1)
    obj = driver.find_element_by_name("pass")
    file = open("password.txt",'r')
    pasw = file.read()
    file.close()
    obj.send_keys(pasw)
    obj.send_keys(Keys.RETURN)
    time.sleep(1)
    """
    try:
        driver.find_element_by_css_selector("button._42ft._4jy0._6lth._4jy6._4jy1. selected._51sy").click()
    except:
        driver.find_element_by_id('loginbutton').click()
    """
    time.sleep(1)


def logout(driver):
    # self.driver.close()
    driver.find_element_by_id('userNavigationLabel').click()
    time.sleep(2)
    driver.find_element_by_xpath("//span[text()='Log Out']").click()


def profile(driver):
    driver.find_element_by_class_name("_1vp5").click()


def message(driver):
    driver.find_element_by_xpath('//*[@id="u_0_e"]/a').click()


def searchprofile(driver, text):
    for _ in range(25):
        driver.find_element_by_css_selector("input._1frb").send_keys(Keys.BACKSPACE)
    driver.find_element_by_css_selector("input._1frb").send_keys(text)
    driver.find_element_by_css_selector("input._1frb").send_keys(Keys.RETURN)

def setfb():
    print("Type Username")
    un = input()
    print("Type Password")
    pw = input()
    file = open("username.txt",'w')
    file.write(un)
    file.close()
    file = open("password.txt",'w')
    file.write(pw)
    file.close()

if __name__ == "__main__":
    print("This might take some...")
    #option = Options()
    #option.add_argument("disable-infobars")
    #option.add_argument("--disable-extensions")

    #option.add_experimental_option("prefs",{"profile.default_content_setting_values.notifications": 1})
    browser = webdriver.Chrome(executable_path=r"C:\Users\Yogesh\PycharmProjects\trial1\chromedriver.exe")
    browser.maximize_window()
    while True:
        command1 = takecommand()
        if command1.lower() == "stop":
            break
        checkcommand(command1, browser)