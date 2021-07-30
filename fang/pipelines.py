# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sqlite3
import time

import requests


class FangPipeline(object):
    def __init__(self, sqlite_file, sqlite_table):
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table
        self.conn = None
        self.cur = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file=crawler.settings.get('SQLITE_FILE'),  # 从 settings.py 提取
            sqlite_table=crawler.settings.get('SQLITE_TABLE')
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()
        create_sql = '''CREATE TABLE IF NOT EXISTS {0} (
                            id TEXT PRIMARY KEY,
                            link TEXT,
                            title TEXT,
                            xiaoqu TEXT,
                            region TEXT,
                            rooms TEXT,
                            area TEXT,
                            toward TEXT,
                            floor TEXT,
                            `year` TEXT,
                            price INTEGER,
                            unit INTEGER,
                            tag TEXT
                        );'''.format(self.sqlite_table)
        print create_sql
        try:
            self.cur.execute(create_sql)
        except sqlite3.Error as e:
            print(e)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cur.execute("SELECT * FROM {0}  WHERE id=?".format(self.sqlite_table), (item["id"],))
        rows = self.cur.fetchall()
        if len(rows) == 0:
            url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d62ddc01-d117-44f1-90b0-4b0aed82a918"
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "content": '''# [**{0}**]({1})\n
                               > <font color="comment">{2} - {3}</font>      <font color="warning">**{4}万**</font>
                               > <font color="comment">{5}</font>       <font color="comment">单价{6}元/平米</font>
                               > <font color="comment">{7}</font>
                               '''.format(item["title"].encode('utf-8'), item["link"].encode('utf-8'), item["xiaoqu"].encode('utf-8'), item["region"].encode('utf-8'), item["price"],
                                          " | ".join([item["rooms"].encode('utf-8'), item["area"].encode('utf-8'), item["toward"].encode('utf-8'), item["floor"].encode('utf-8'), item["year"].encode('utf-8')]),
                                          item["unit"], item["tag"].encode('utf-8'))
                }
            }
            requests.post(url, data=json.dumps(payload))
            time.sleep(3)
        insert_sql = "REPLACE INTO {0}({1}) values ({2})".format(self.sqlite_table,
                                                                 ', '.join(item.keys()),
                                                                 ', '.join(['?'] * len(item.keys())))
        values = [item[k] for k in item.keys()]
        self.cur.execute(insert_sql, values)
        self.conn.commit()

        return item
