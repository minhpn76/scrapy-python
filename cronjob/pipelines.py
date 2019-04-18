# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymysql.cursors

class CronjobPipeline(object):


    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = pymysql.connect(
            host='localhost',
            port=8889,
            user='root',
            password='root',
            db='myscrapy',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def create_table(self):
        with self.conn.cursor() as cursor:
            delete_exitsing_table = "DROP TABLE IF EXISTS scrapy_tb"

            create_table_query = '''CREATE TABLE scrapy_tb(
                `id` int auto_increment primary key,
                `job_id` int not null,
                `job_title` varchar(255) not null,
                `area1` varchar(255) not null,
                `employment_type` varchar(255) not null,
                `job_category` varchar(255) not null,
                `salary_range` varchar(255),
                `posted_date` datetime not null,
                `age` text not null,
                `requirements` text not null,
                `salary` text not null,
                `period` text not null,
                `working_hour` text not null,
                `location` text not null,
                `desc` text not null,
                `company_name` varchar(255) not null,
                `company_website` varchar(255) not null,
                `representative` varchar(255) not null,
                `email` varchar(255) not null,
                `tel` varchar(255) not null,
                `fax` varchar(255) not null,
                `pr` text not null
            )'''
            # create_table_query = "CREATE TABLE scrapy_tb( `id` int auto_increment primary key, `job_id` int not null, `job_title` varchar(255) not null)"
            try:
                cursor.execute(delete_exitsing_table)
                cursor.execute(create_table_query)
            except Exception as e:
                print('====Exception create table=====', str(e))
                pass
        
    def close_connection(self):
        self.conn.close()
            
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        with self.conn.cursor() as cursor:
            try:
                check_exist_job_id = self.get_job_exist(item['job_id'])
                
                if check_exist_job_id is False:
                    insert_query = '''INSERT INTO `scrapy_tb` (`job_id`, 
                        `job_title`, `area1`, `employment_type`, `job_category`,
                        `salary_range`, `posted_date`, `age`, `requirements`,
                        `salary`, `period`, `working_hour`, `location`,
                        `desc`, `company_name`, `company_website`, `representative`,
                        `email`, `tel`, `fax`, `pr`) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

                    # insert_query = "INSERT INTO `scrapy_tb` (`job_id`, `job_title` )  VALUES(%s, %s)"

                    cursor.execute(insert_query, (
                        item['job_id'] if item['job_id'] is not  None else "", 
                        item['job_title'] if item['job_title'] is not  None else "", 
                        item['area1'] if item['area1'] is not  None else "", 
                        item['employment_type'] if item['employment_type'] is not  None else "",
                        item['job_category'] if item['job_category'] is not  None else "", 
                        item['salary_range'] if item['salary_range'] is not  None else "", 
                        item['posted_date'] if item['posted_date'] is not  None else "1900/01/01 00:00", 
                        item['age'] if item['age'] is not  None else "", 
                        item['requirements'] if item['requirements'] is not  None else "",
                        item['salary'] if item['salary'] is not  None else "", 
                        item['period'] if item['period'] is not  None else "", 
                        item['working_hour'] if item['working_hour'] is not  None else "", 
                        item['location'] if item['location'] is not  None else "",
                        item['desc'] if item['desc'] is not  None else "", 
                        item['company_name'] if item['company_name'] is not  None else "", 
                        item['company_website'] if item['company_website'] is not  None else "", 
                        item['representative'] if item['representative'] is not  None else "",
                        item['email'] if item['email'] is not  None else "", item['tel'] if item['tel'] is not  None else "", 
                        item['fax'] if item['fax'] is not  None else "", item['pr'] if item['pr'] is not  None else ""
                    ))
                    self.conn.commit()

                    print('====Success!=====')
            except Exception as e:
                print('====Exception store db=====', str(e))
                self.conn.rollback()

    def get_job_exist(self, job_id):
        with self.conn.cursor() as cursor:
            result = None
            try:
                get_row = "SELECT * FROM `scrapy_tb` WHERE `job_id`=%s"
                cursor.execute(get_row, (int(job_id)))
                result = cursor.fetchone()

            except Exception as e:
                pass

            if result:
                return True

            return False