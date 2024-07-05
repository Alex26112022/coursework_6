import os
from configparser import ConfigParser
from dotenv import load_dotenv

load_dotenv()

yandex_user = os.getenv('YANDEX_USER')
yandex_password = os.getenv('YANDEX_PASSWORD')

ROOT_DIR = os.path.dirname(__file__)
database_params = os.path.join(ROOT_DIR, 'database.ini')


def config(filename=database_params, section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0].upper()] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section,
                                                               filename))
    return db
