# -*- coding: utf-8 -*-

"""
Django settings for test1 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1l6o8x$%k@j#9p(j2@@jcn!e^&gm5=5^^l28dy=owktm*1u!mv'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'product.UserProperty'
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 'django-filters',
    'product',
    'djcelery',
    'djkombu',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'test1.urls'

WSGI_APPLICATION = 'test1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "test",
        'USER': 'root',
        # 'PASSWORD': "123456",
        'HOST': "127.0.0.1",
        'PORT': "3306",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
       # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ) ,
    # 'DEFAULT_PERMISSION_CLASSES': (
    #    'rest_framework.permissions.AllowAny',
    # ),
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

}

import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=300),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

AUTHENTICATION_BACKENDS = (
    'product.views.CustomBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "product.context_processors.admin_media",
            ],
        },
    },
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Celery 设置
import djcelery
djcelery.setup_loader()  # 去每一个应用目录下找 tasks.py 文件，到文件中去执行 celery 任务函数
CELERY_IMPORTS = ('product.tasks',)
CELERY_BROKER_URL = 'redis://localhost:6379/0' # celery中间队列
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Asia/Shanghai'

'''发送邮件配置'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smtp服务器地址
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱地址
EMAIL_HOST_USER = 'f1643076443@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'femn2018'
# 收件人看到的发件人
EMAIL_FROM = 'leipengkai<f1643076443@163.com>'

# BROKER_URL = 'amqp://guest:guest@localhost:5672/'  # connect RabbitMQ
BROKER_URL = 'django://' # and add this app:

INSTALLED_APPS += ('kombu.transport.django', )
