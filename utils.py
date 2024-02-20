import time, os
from newspaper import Article
import json, random, string
from datetime import datetime
from dateutil import tz


def up_mariadb(db_conn):
    if db_conn is None:
        os.system("systemctl restart mariadb")
    return None


class ArticleData(object):

    def __init__(self, url):
        self.article = Article(url)
        self.article.download()
        self.article.parse()
        self.article.nlp()

    def get_title(self):
        return self.article.title

    def get_authors(self):
        return self.article.authors

    def get_content(self):
        return self.article.text

    def top_image(self):
        return self.article.top_image

    def movie(self):
        return self.article.movies

    def summery(self):
        return self.article.summary


def indian_datetime():
    from_zone=tz.gettz('UTC')
    to_zone=tz.gettz('Asia/Kolkata')
    dt=datetime.now()
    utc=datetime.strptime(dt.strftime('%Y-%m-%d %H:%M:%S.f'), '%Y-%m-%d %H:%M:%S.f')
    utc1=utc.replace(tzinfo=from_zone)
    return utc1.strftime('%Y-%m-%d %H-%M-%S.%f')


def save_json(records, job, additional_dir=None):
    """
    Save your output records in json file
    :param records: dict
    dat you send
    :param job: str
    job name i.e. web, federated
    :return:None
    """
    try:
        if additional_dir is None:
            path = 'data_json'
        else:
            path=additional_dir
        if not os.path.exists(path):
            os.makedirs(path)
            print('Dir Created')
        file_name = os.path.join(path, indian_datetime() + '_'+job+'.json')
        with open(file_name, 'w') as outfile:
            json.dump(records, outfile)
        print('File save')
        outfile.close()
    except:
        pass
    return None


def save_record_json(records, job, additional_dir=None):
    """
    Save your output records in json file
    :param records: dict
    dat you send
    :param job: str
    job name i.e. web, federated
    :return:None
    """
    try:
        if additional_dir is None:
            path = 'record_data_json'
        else:
            path=additional_dir
        if not os.path.exists(path):
            os.makedirs(path)
            print('Dir Created')
        chars="".join(random.choices(string.ascii_letters+string.digits, k=7))
        file_name = os.path.join(path, f"{chars}_{indian_datetime()}_{job}.json")
        with open(file_name, 'w') as outfile:
            json.dump(records, outfile)
        print('File save')
        outfile.close()
    except Exception as e:
        print("Save File Exception:", e)
        pass
    return None