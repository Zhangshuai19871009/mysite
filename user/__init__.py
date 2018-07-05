import os
from django.apps import AppConfig

default_app_config = 'user.PrimaryUserConfig'

VERBOSE_APP_NAME = '用户拓展管理'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class PrimaryUserConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME