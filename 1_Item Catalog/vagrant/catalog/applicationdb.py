#!/usr/bin/env python
import psycopg2
import datetime
import uuid

DBNAME = "forum"


def get_categories():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select * from Category order by name desc"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return datas


def get_categorytoComboBox():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select * from Category order by name desc"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return datas


def get_products():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select * from Product"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return datas


def get_category_products(id):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select * from Product where category_id = '" + id + "';"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return datas


def get_category_from_id(id):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select * from Category where id = '" + id + "';"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return datas


def get_product_details(id):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select * from Product where id = '" + id + "';"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return datas


def get_category_details(id):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select * from Category where id = '" + id + "';"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return datas


def delete_product(id):
    rows_deleted = 0
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(database=DBNAME)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute("DELETE FROM Product WHERE id= %s", (id,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def get_last_products():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select * from Product order by id desc limit 3"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return datas


def get_last_productId():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select id from Product order by id desc limit 1"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return datas


def add_products(title, description, category):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    idd = get_last_productId()
    newid = int(str(idd[0][0])) + 1

    try:

        sql_insert_query = """insert into product """
        sql_insert_query = """(id,title,description,category_id) """
        sql_insert_query = """values (%s,%s,%s,%s)"""
        sql_record_query = (newid, title, description, category)
        c.execute(sql_insert_query, sql_record_query)
        db.commit()
        count = c.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        if(db):
            print("Failed to insert record into mobile table", error)
    finally:
        if(db):
            c.close()
            db.close()
            print("PostgreSQL db is closed")


def update_products_object(productObject):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    print("ID :" + productObject.id)
    id = int(productObject.id)

    try:

        sql_insert_query = """update product set title = %s,"""
        sql_insert_query += """description=%s,category_id = %s where id = %s"""
        sql_record_query = (
            productObject.title,
            productObject.description,
            productObject.category_id,
            id)
        c.execute(sql_insert_query, sql_record_query)
        db.commit()
        count = c.rowcount
        print(count, "Record updated successfully")

    except (Exception, psycopg2.Error) as error:
        if(db):
            print("Failed to update record into mobile table", error)
    finally:
        if(db):
            c.close()
            db.close()
            print("PostgreSQL db is closed")


def add_products_object(productObject):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    idd = get_last_productId()
    newid = int(str(idd[0][0])) + 1

    try:

        sql_insert_query = """insert into product """
        sql_insert_query += """(id,title,description,category_id) """
        sql_insert_query += """values (%s,%s,%s,%s)"""
        sql_record_query = (
            newid,
            productObject.title,
            productObject.description,
            productObject.category_id)
        c.execute(sql_insert_query, sql_record_query)
        db.commit()
        count = c.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        if(db):
            print("Failed to insert record into mobile table", error)
    finally:
        # closing database connection.
        if(db):
            c.close()
            db.close()
            print("PostgreSQL db is closed")


def add_user_object(userObject):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    newid = str(uuid.uuid4().int & (1 << 16)-1)
    userObject.email = "asd@asd.com"

    try:
        sql_insert_query = """insert into users (id,name,email,password)"""
        sql_insert_query += """ values (%s,%s,%s,%s)"""
        sql_record_query = (
            newid, userObject.name, userObject.email, userObject.password)
        print(sql_record_query)
        c.execute(sql_insert_query, sql_record_query)
        db.commit()
        count = c.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        if(db):
            print("Failed to insert record into table", error)
    finally:
        # closing database connection.
        if(db):
            c.close()
            db.close()
            print("PostgreSQL db is closed")


def get_user_details(user):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    try:
        sql_insert_query = """select * from users where """
        sql_insert_query += """name = %s and password = %s;"""
        sql_record_query = (
            user.name, user.password)
        c.execute(sql_insert_query, sql_record_query)
        datas = c.fetchall()

    except (Exception, psycopg2.Error) as error:
        if(db):
            print("Failed to insert record into table", error)
    finally:
        # closing database connection.
        if(db):
            c.close()
            db.close()
        return datas
