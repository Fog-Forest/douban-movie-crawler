#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import mysql.connector

host = "localhost"  # 数据库主机地址
user = "root"  # 数据库用户名
passwd = "root"  # 数据库密码
database = "movie"  # 数据库名


# 创建数据库
def create_db():
    db = mysql.connector.connect(host=host, user=user, passwd=passwd)  # 打开数据库连接
    cursor = db.cursor()  # 创建游标对象
    try:
        cursor.execute("CREATE DATABASE `movie`")  # 执行MYSQL语句
        print("数据库创建成功！")
    except Exception:
        print("【movie】数据库已存在，跳过创建！")
    db.close()  # 关闭数据库连接


# 创建数据表
def create_table():
    db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
    cursor = db.cursor()
    try:
        cursor.execute("CREATE TABLE `movie` ( `id` INT NOT NULL AUTO_INCREMENT,\
         `db_id` INT(20) NOT NULL, `title` VARCHAR(100) NOT NULL , `rate` FLOAT NOT NULL , `img` VARCHAR(100) NOT NULL ,\
          `data` TINYTEXT NOT NULL , `description` TEXT NOT NULL , `director` TEXT NOT NULL ,\
           `author` TEXT NOT NULL , `actor` TEXT NOT NULL , `genre` VARCHAR(255) NOT NULL ,\
            PRIMARY KEY (`id`)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci")
        print("表创建成功！")
    except Exception:
        print("表已存在，跳过创建！")
    db.close()  # 关闭数据库连接


# 插入电影数据 ID、标题、评分、图链
def insert_data(id, db_id, title, rate, img):
    db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
    cursor = db.cursor()
    insert = "INSERT INTO `movie` (`id`, `db_id`, `title`, `rate`, `img`, `data`, `description`,\
     `director`, `author`, `actor`, `genre`) VALUES ('" + id + "', '" + db_id + "', '" + title + "', '" + rate +\
             "', '" + img + "', '', '', '', '', '', '')"
    # print(insert)  # 查看数据库插入语句
    cursor.execute(insert)
    db.commit()  # 提交任务，数据才会写入数据库
    db.close()  # 关闭数据库连接


# 插入电影详情 日期、简介、导演、作者、演员、类型
def insert_info(id, data, description, director, author, actor, genre):
    db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
    cursor = db.cursor()
    insert = "UPDATE `movie` SET `data` = '" + data + "', `description` = '" + description + "', `director` = '"\
             + director + "', `author` = '" + author + "', `actor` = '" + actor + "', `genre` = '"\
             + genre + "' WHERE `movie`.`id` = " + id + ";"
    print(insert)  # 查看数据库插入语句
    cursor.execute(insert)
    db.commit()  # 提交任务，数据才会写入数据库
    db.close()  # 关闭数据库连接


if __name__ == '__main__':
    create_db()
    create_table()