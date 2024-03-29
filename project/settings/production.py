from .base import * # base에서 전체 상속
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['bamsam.pr73cnh8mn.ap-northeast-2.elasticbeanstalk.com']