from selenium import webdriver

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--disable-gpu')
chrome_opt.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})     