"""
Django settings for deal_crm project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0=f5b9k)5s_ukd!rj)%paoj2(museij=_*2h8o(%7n+or($&_l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'web.apps.WebConfig',
]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.md.AuthMiddleware'
]

ROOT_URLCONF = 'deal_crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                # 'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deal_crm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'deal_crm',
        'USER':'root',
        'PASSWORD':'root',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# caches 配置
CACHES = {
    # default 是缓存名，可以配置多个缓存
    "default": {
        # 应用 django-redis 库的 RedisCache 缓存类
        "BACKEND": "django_redis.cache.RedisCache",
        # 配置正确的 ip和port
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            # redis客户端类
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # redis连接池的关键字参数
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100
            },
            # 如果 redis 设置了密码，那么这里需要设置对应的密码，如果redis没有设置密码，那么这里也不设置
            # "PASSWORD": "root",
        }
    }
}


# session 配置

# 存储session数据默认使用的模块
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
# Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
SESSION_COOKIE_NAME = 'sessionid'
# Session的cookie失效日期（2周）（默认）
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# Session的cookie保存的域名（默认）
SESSION_COOKIE_DOMAIN = None
# 是否Https传输cookie（默认）
SESSION_COOKIE_SECURE = False
# Session的cookie保存的路径（默认）
SESSION_COOKIE_PATH = '/'
# 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_HTTPONLY = True
# 是否每次请求都保存Session，默认修改之后才保存
SESSION_SAVE_EVERY_REQUEST = True
# 是否关闭浏览器使得Session过期（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# session数据的序列化类
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


# 自定义配置
LOGIN_HOME = '/home/'
NB_WHITE_URL = ['/login/', '/sms/login/']

NB_MENU = {
    'ADMIN': [
        {
            'text': "用户信息",
            'icon': "fa-bed",
            'children': [
                {'text': "级别列表", 'url': "/level/list", 'name': "level_list"},
                {'text': "客户列表", 'url': "/customer/list", 'name': "customer_list"},

            ]
        },
        {
            'text': "其他",
            'icon': "fa-bed",
            'children': [
                {'text': "价格策略", 'url': "/policy/list", 'name': "policy_list"},
            ]
        },

    ],
    'CUSTOMER': [
        {
            'text': "用户信息",
            'icon': "fa-bed",
            'children': [
            ]
        },
    ],
}

NB_PERMISSION_PUBLIC = {
    "home": {"text": "主页", 'parent': None},
    "logout": {"text": "注销", 'parent': None},
}

NB_PERMISSION = {
    "ADMIN": {
        'level_list': {"text": "级别列表", 'parent': None},
        'level_add': {"text": "新建级别", 'parent': 'level_list'},
        'level_edit': {"text": "编辑级别", 'parent': 'level_list'},
        'level_delete': {"text": "删除级别", 'parent': 'level_list'},

        'customer_list': {"text": "客户列表", 'parent': None},
        'customer_add': {"text": "新建客户", 'parent': 'customer_list'},
        'customer_edit': {"text": "编辑客户", 'parent': 'customer_list'},
        'customer_delete': {"text": "编辑客户", 'parent': 'customer_list'},

        'policy_list': {"text": "价格策略", 'parent': None},
        'policy_add': {"text": "价格策略", 'parent': 'policy_list'},
        'policy_edit': {"text": "编辑策略", 'parent': 'policy_list'},
        'policy_delete': {"text": "删除策略", 'parent': 'policy_list'},
    },
    "CUSTOMER": {
    }
}


try:
    from local_settings import *
except Exception:
    pass