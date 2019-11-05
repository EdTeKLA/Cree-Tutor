from urllib.parse import urlparse

from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import TestCase
import django.test as test
from django.urls import reverse
from django.contrib.auth import authenticate
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from http import HTTPStatus
from selenium.webdriver.common.keys import Keys

from .models import AgeLevels, Gender, ModifiedUser


# Create your tests here.
class LoginTestCase(TestCase):
    def setUp(self):
        self.email = "test1@test.com"
        self.password = "secret"
        self.user = ModifiedUser.objects.create_user(email=self.email,
                                                     username=self.email,
                                                     password=self.password,
                                                     is_active=False)
        self.user.save()

    def test_modified_user_registeration(self):
        self.assertEqual(self.user.email, "test1@test.com")
        self.assertEqual(self.user.username, self.email)

    def test_user_login_unsuccessful_due_to_unauthenticated(self):
        c = test.Client()
        response = c.post('/signin/', {'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, 401)

    def test_user_login_unsuccessful_wrong_credentials(self):
        c = test.Client()
        response = c.post('/signin/', {'email': self.email, 'password': self.password + "1"})
        self.assertEqual(response.status_code, 401)

    def test_user_login_successful(self):
        self.user.is_active = True
        self.user.save()
        c = test.Client()
        response = c.post('/signin/', {'email': self.email, 'password': self.password})
        self.assertEqual(response.status_code, 200)


class SignUpTests(TestCase):
    def setUp(self):
        self.email = "test1@test.com"
        self.password = "secret"

    def test_user_registration_valid(self):
        c = test.Client()
        response = c.post('/signup/', {'email': self.email, 'password': self.password})
        body = response.json()
        if 'redirect' in body:
            self.assertEqual(body['redirect'], '/confirm_email')
        else:
            self.assertTrue(False)

    def test_user_registration_invalid(self):
        c = test.Client()
        self.__insert_user()
        response = c.post('/signup/', {'email': self.email, 'password': self.password})
        body = response.json()
        if 'error' in body.keys():
            self.assertEqual(body['error'], 'Account already exists')
        else:
            self.assertTrue(False)

    def __insert_user(self):
        self.email = "test1@test.com"
        self.password = "secret"
        self.user = ModifiedUser.objects.create_user(email=self.email,
                                                     username=self.email,
                                                     password=self.password,
                                                     is_active=True)
        self.user.save()

class SignupFunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    # TODO: selecting signup tab isn't switching nav view
    # def test_create_account(self):
    #     self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
    #     tab_xpath = "//*[@id=\"signup-form-tab\"]"
    #     tab = WebDriverWait(self.selenium, 20).until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))
    #     tab.click()
    #     username_input = self.selenium.find_element_by_id("email")
    #     username_input.send_keys('test1@test.com')
    #     password_input = self.selenium.find_element_by_id("password")
    #     password_input.send_keys('1234')
    #     password_input = self.selenium.find_element_by_id("confirm-password")
    #     password_input.send_keys('1234')
    #     self.selenium.find_element_by_id("signup-button").click()


class LoginFunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

        cls.user_email = "test1@test.com"
        cls.user_password = "1234"
        cls.user = ModifiedUser.objects.create(email=cls.user_email,
                                               username=cls.user_email,
                                               password=cls.user_password,
                                               is_active=False)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_not_authenticated(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_id("login-email")
        username_input.send_keys(self.user_email)
        password_input = self.selenium.find_element_by_id("login-password")
        password_input.send_keys(self.user_password)
        submit = self.selenium.find_element_by_name("submit")
        submit.click()
        url = urlparse(self.selenium.current_url).path
        self.assertEqual(url, reverse('login:index'))
        try:
            self.selenium.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/form[1]/div[3]/div/div")
        except NoSuchElementException:
            self.assertTrue(False)
