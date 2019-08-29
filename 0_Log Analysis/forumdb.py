#!/usr/bin/env python
import psycopg2

DBNAME = "forum"


def get_firstQuestion():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select a.title, mp.views from articles a, ("
    sqlQuery += "select l.path,count(l.path) as views from log l "
    sqlQuery += "where length(l.path)>5 and l.method = 'GET' and "
    sqlQuery += "status='200 OK' group by l.path order by views desc limit 3"
    sqlQuery += ") mp where right(mp.path,-9)=a.slug"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return reversed(datas)


def get_secondQuestion():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select au.name, count(au.name) as views from authors au,"
    sqlQuery += " articles ar,log l where au.id = ar.author and "
    sqlQuery += "right(l.path,-9)=ar.slug and l.method = 'GET' and"
    sqlQuery += " l.status='200 OK' group by au.name order by views desc"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return reversed(datas)


def get_thirdQuestion():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    sqlQuery = "select datenf as datum, "
    sqlQuery += "CAST(countNok AS float)*100/CAST(countOk AS float)"
    sqlQuery += " as errorPercent from (select dateNf,count(dateNf)"
    sqlQuery += " as countNok from"
    sqlQuery += " (select TO_CHAR(time :: DATE, 'dd/mm/yyyy')"
    sqlQuery += " as dateNf from log where status='404 NOT FOUND')"
    sqlQuery += " as nfTable group by dateNf) as tableNok,"
    sqlQuery += "(select dateOk,count(dateOk) as countOk from "
    sqlQuery += "(select TO_CHAR(time :: DATE, 'dd/mm/yyyy') "
    sqlQuery += "as dateOk from log) as okTable group by dateOk)"
    sqlQuery += " as tableOk where tableOk.dateOk=tableNok.datenf"
    sqlQuery += " and countNok*100>countOk"
    c.execute(sqlQuery)
    datas = c.fetchall()
    db.close()
    return reversed(datas)
