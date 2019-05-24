import time

from django.utils.translation import ugettext_lazy
from optparse import make_option
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from django.core.management.base import BaseCommand, CommandError

from onadata.apps.fsforms.models import FieldSightXF

USER_NAME = ""
USER_PASSWORD = ""


# BASE_URL = "http://localhost:8001/"
BASE_URL = "https://app.fieldsight.org/"
# BASE_URL = "https://fieldsight.naxa.com.np/"
PROJECT_FORM_ID = 0
ID_STRING = ""


def run_enketo(project_form, instance):
    # display = Display(visible=0, size=(1024, 900))
    # display.start()
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    # firefox_capabilities['binary'] = '/home/awemulya/Downloads/geckodriver-v0.24.0-linux32'
    driver = webdriver.Firefox(capabilities=firefox_capabilities, executable_path='/geckodriver')
    driver.get(BASE_URL)
    driver.find_element_by_name('username').send_keys(USER_NAME)
    driver.find_element_by_name('password').send_keys(USER_PASSWORD + Keys.RETURN)
    # print(project_form)
    # project_fxf = FieldSightXF.objects.get(pk=project_form)
    # instances = project_fxf.project_form_instances.filter(instance__id__gt=instance).\
    #     values_list('instance', flat=True).order_by('pk')
    # ID_STRING = project_fxf.xf.id_string
    instances = []

    for ID_SUBMISSION in instances:
        enketo_url = "{}forms/edit/{}/{}".format(BASE_URL, ID_STRING, ID_SUBMISSION)
        driver.get(enketo_url)
        time.sleep(3)

        try:
            driver.execute_script("document.querySelectorAll('button#submit-form')[0].click()")
            time.sleep(2)
            print(ID_SUBMISSION)
        except TimeoutException:
            print "Loading took too much time!"
    driver.close()


class Command(BaseCommand):
    help = 'enketo auto edit'
    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--projectform",
            dest="f",
            help="specify project form",
            metavar="INT"
        ),
    )

    option_list = option_list + (
        make_option(
            "-i",
            "--instance",
            dest="i",
            help="Submission ID",
            metavar="INT"
        ),
    )

    def handle(self, *args, **options):
        project_form = options.get("f", 0)
        instance = options.get("i", 0)
        run_enketo(project_form, instance)


