#from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver


class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.wd.implicitly_wait(5)
        self.base_url = base_url

    def logout(self):
        wd = self.wd
        wd.find_element_by_xpath("//i[2]").click()
        wd.find_element_by_link_text(u"Выход").click()
        #wd.find_element_by_link_text("administrator").click()

    def input_value(self, field_name, text):
        wd = self.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def login(self, userName, password):
        wd = self.wd
        wd.get(self.base_url)
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(userName)
        wd.find_element_by_name("username").click()
        wd.find_element_by_css_selector("input[type='%s']" % "submit").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_name("password").click()
        wd.find_element_by_css_selector("input[type='%s']" % "submit").click()

    def is_valid(self):
        wd = self.wd
        try:
            self.wd.current_url
            return True
        except:
            return False

    def ensure_logout(self):
        wd = self.wd
        if self.is_loged_in():
            self.logout()

    def is_loged_in(self):
        wd = self.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, userName):
        wd = self.wd
        return wd.find_element_by_xpath("//li/span").text ==  userName

    def ensure_login(self, userName, password):
        wd = self.wd
        if self.is_loged_in():
            if self.is_logged_in_as(userName):
                return
            else:
                self.logout()
        self.login(userName, password)


    def destroy(self):
        wd = self.wd
        self.wd.quit()