import logging, traceback, os, datetime
from logging.handlers import TimedRotatingFileHandler


class Logger(object):

    def __init__(self, job):
        self.job = job
        self.log_obj = logging.getLogger(self.job)
        self.log_obj.setLevel(logging.DEBUG)
        if not os.path.exists("./logs"):
            os.makedirs("./logs")
        self.handler = TimedRotatingFileHandler(filename='./logs/{}.log'.format(self.job),
                                                when='D', interval=1, backupCount=90,
                                                encoding='utf-8', delay=False)
        self.handler.setLevel(logging.ERROR)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.log_obj.addHandler(self.handler)

    @staticmethod
    def write_logs(log_file, err_txt, additional_dir=None):
        try:
            log_dir = 'logs'
            if additional_dir:
                log_dir = additional_dir
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            fl = open(os.path.join(log_dir, log_file), "a+")
            fl.write(f"{str(datetime.datetime.now())} | {err_txt}")
            fl.close()
        except:
            pass
        return None
