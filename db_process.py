import traceback
import time
import json

import mysql.connector
import traceback


"""
Project: Federated Search Version2
Objective: To scrape content from various search engines
Owner: Innefu Labs Pvt. Ltd.
Description: This script have database utilities.
Dependencies:  mysql.connector
Script: support script
"""

# Import dependencies

import requests, os, json, time, ast
import traceback
import mysql.connector
from utils import up_mariadb
from logs import *


gdelt_data_logger = Logger(job="Fb_Mysql")


local_machine_ip = '192.168.0.0'


class FbDatabase(object):
    """
    Database services
    """

    def __init__(self, logger=gdelt_data_logger):
        """
        Initialization
        :param logger: object
                logger object
        """
        # self.machine_ip = requests.get('http://ipinfo.io/json').json()['ip']
        self.machine_ip = local_machine_ip
        self.connection = self.db_connection()
        self.cursor = self.connection.cursor(buffered=True)
        self.logger = logger
        self.gdelt_url_table = "fbUrls"

        self.create_gdelt_url_table()

    def db_config(self):
        """
        Default database configuration
        :return: dict
        """
        conf={
            'host': '127.0.0.1',
            'port': '3306',
            'user': 'root',
            'passwd': '', # your password
            'database': '' # your database
        }
        return conf

    def create_gdelt_url_table(self):
        up_mariadb(self.connection)
        if not self.connection.is_connected():
            self.connection = self.db_connection()
        print('CREATE TABLE IF NOT EXISTS')
        self.cursor = self.connection.cursor(buffered=True)
        try:
            query = """CREATE TABLE IF NOT EXISTS {}.{} (
                            id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            url varchar(500) NOT NULL UNIQUE)
                    """.format(self.db_config()['database'], self.gdelt_url_table)

            self.cursor.execute(query)
            self.connection.commit()
            print('Table created successfully')
        except Exception as e:
            gdelt_data_logger.log_obj.error(traceback.print_exc(), "CREATE TABLE ERROR", exc_info=True)

    def db_connection(self):
        """
        Create connection with database
        :return: object
            Connected db connection object
        """
        config = self.db_config()
        try:
            mydb=mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                passwd=config['passwd'],
                database=config['database']
            )
            return mydb
        except Exception as e:
            gdelt_data_logger.log_obj.error(traceback.print_exc(), "DB CONNECTION ERROR", exc_info=True)

    def gdelt_url_insert(self,  url):
        """
        Insert values to the db table
        :param json_data: dict
                    data to store
        :param types: str
                profile, keyword etc.
        :return: dict
                data
        """
        up_mariadb(self.connection)
        if not self.connection.is_connected():
            self.connection = self.db_connection()
        self.cursor=self.connection.cursor(buffered=True)
        try:
            sql="INSERT IGNORE INTO {} (url) VALUES (%s)".format(self.gdelt_url_table)
            arg=(url, )
            self.cursor.execute(sql, arg)
            ids=self.cursor.lastrowid
            self.connection.commit()
            if ids > 0:
                return True
        except Exception as e:
            gdelt_data_logger.log_obj.error(traceback.print_exc(), exc_info=True)
            pass
        return False
