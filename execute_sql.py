#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-17 09:41:45
# @Author  : taoleilei (1214360171@qq.com)
# @Link    : ${link}
# @Version : $Id$

import os
import pymysql
from datetime import datetime
import uuid
import random
from DBUtils.PooledDB import PooledDB

CONN_CONFIG = {
    "host": "192.168.1.210",
    "port": 3306,
    "user": "root",
    "passwd": "iiecas",
    "db": "x",
    'charset': 'utf8',
}


class SQLPoll(object):

    # docstring for DbConnection

    __poll = None

    def __init__(self):
        self.pool = self.__get_db()
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    @classmethod
    def __get_db(cls):
        if cls.__poll is None:
            cls.__poll = PooledDB(
                creator=pymysql,
                mincached=10,
                maxconnections=100,
                **CONN_CONFIG)
        return cls.__poll

    def fetch_all(self, sql, args=None):
        if args is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def fetch_one(self, sql, args=None):
        if args is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def execute(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()
        result = self.cursor.lastrowid
        return result

    def __close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()


query_one = '''
    SELECT
        a.*, b.answer AS upload_answer,
        b.grade
    FROM
        (
            SELECT
                id,
                score,
                state,
                prize,
                title,
                one_blood,
                update_time
            FROM
                plot_problemflag
            WHERE
                problem_id = (
                    SELECT
                        id
                    FROM
                        plot_teamproblem
                    WHERE
                        team_id = (
                            SELECT
                                id
                            FROM
                                a_team
                            WHERE
                                `name` = %s
                        )
                    AND origin_id = %s
                )
        ) a
    LEFT JOIN a_team_game_grade b ON a.id = b.g_p_id
'''

sql_one = '''
    UPDATE sys_login
    SET `password` = MD5(%s)
    WHERE
        login_id IN (
            SELECT
                login_id
            FROM
                (
                    SELECT
                        login_id,
                        person_id
                    FROM
                        sys_login
                ) b
            WHERE
                b.person_id IN (
                    SELECT
                        person_id
                    FROM
                        a_team_person
                    WHERE
                        team_id = (
                            SELECT
                                id
                            FROM
                                a_team
                            WHERE
                                `name` = %s
                        )
                )
        )
'''


sql_two = '''
    UPDATE plot_teamproblem
    SET submit = %s
    WHERE
        id = (
            SELECT
                b.id
            FROM
                (
                    SELECT
                        id,
                        team_id,
                        origin_id
                    FROM
                        plot_teamproblem
                ) b
            WHERE
                b.team_id = (
                    SELECT
                        id
                    FROM
                        a_team
                    WHERE
                        `name` = %s
                )
            AND b.origin_id = %s
        )
'''

query_two = '''
    SELECT
        a.team_id,
        b.`name`
    FROM
        a_game_team a
    LEFT JOIN a_team b ON a.team_id = b.id
    WHERE
        a.game_id = %s
'''

sql_three = '''
    UPDATE sys_login
    SET `password` = MD5(%s)
    WHERE
        login_id IN (
            SELECT
                login_id
            FROM
                (
                    SELECT
                        login_id,
                        person_id
                    FROM
                        sys_login
                ) b
            WHERE
                b.person_id IN (
                    SELECT
                        person_id
                    FROM
                        a_team_person
                    WHERE
                        team_id = %s
                )
        )
'''


# 查询队伍得分详情
def check_grade(name, problem):
    result = []
    with SQLPoll() as db:
        result = db.fetch_all(query_one, (name, problem))
    print(result)


# 修改队伍账号密码
def alter_passwd_for_team(name, passwd):
    with SQLPoll() as db:
        db.execute(sql_one, (passwd, name))


# 修改某队的某道题目的提交次数
def alter_submit_for_team(name, problem, submit=0):
    with SQLPoll() as db:
        db.execute(sql_two, (submit, name, problem))


def random_passwd(length, simple):
    _letter_cases = "abcdefghjkmnpqrstuvwxy"
    _upper_cases = _letter_cases.upper()
    _numbers = ''.join(map(str, range(3, 10)))
    if simple:
        chars = _numbers
    else:
        chars = ''.join((_letter_cases, _upper_cases, _numbers * 4))
    return ''.join(random.sample(chars, length))


def alter_passwd_for_all(length=6, game_id=260, simple=True):
    passwd_info = {}
    with SQLPoll() as db:
        teams_info = db.fetch_all(query_two, (game_id,))
        for item in teams_info:
            team_id = item["team_id"]
            name = item["name"]
            passwd = random_passwd(length, simple)
            db.execute(sql_three, (passwd, team_id))
            passwd_info[name] = passwd
    print(passwd_info)
    # return passwd_info


if __name__ == '__main__':
    # check_grade(name="北京", problem=579)

    # alter_passwd_for_team(name="北京", passwd=123)

    alter_submit_for_team(name="吉林", problem=574, submit=8)

    # 简单数字8位以内
    # update sys_login set `password`=MD5(HE2L9v) where username='game'
    # update sys_login set `password`=MD5(Te83ds) where username='user'
    # alter_passwd_for_all(length=6, game_id=260, simple=False)
    # import datetime
    # start_time = "2019-11-15 09:30:00"
    # current_time = datetime.datetime.now()
    # start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    # current_time = current_time + datetime.timedelta(days=0.558)
    # print(current_time)
    # if current_time < start_time:
    #     print("ok")
    #     print(start_time)
    # src = "项目立项任务书V7.0.xml"
    # dest = "项目立项任务书V7.0"
    # import re
    # if re.search(dest, src, re.I):
    #     print("ok")
