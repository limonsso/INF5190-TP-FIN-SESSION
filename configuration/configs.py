import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))


def get_configuration(config_file='./configuration/configuration.yaml'):
    smtp_configuration = {}
    email_configuration = {}
    with open(config_file) as file:
        documents = yaml.full_load(file)
        for item, doc in documents.items():
            if item == 'smtp_configuration':
                smtp_configuration = doc
            if item == 'email_configuration':
                email_configuration = doc
    return {'smtp_configuration': smtp_configuration, 'email_configuration': email_configuration}


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', b'_5#y2L"F4Q8z\n\xec]/')
    DEBUG = False
    FLASK_DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = False


config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY
