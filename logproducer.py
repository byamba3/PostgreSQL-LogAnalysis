#!/usr/bin/python3

import psycopg2
from datetime import datetime

DBNAME = "news"


def getTop3Articles(c):

    c.execute(
      "create view pathviews as select path, count(*) as views from "
      "log where status = '200 OK' and length(path) > 1 group by path order "
      "by views desc")
    c.execute(
      "create view u_pathviews as select replace(path, '/article/', '') as"
      " updatedPaths, views from pathviews")
    c.execute(
      "select articles.title, views from articles join u_pathviews on "
      "articles.slug = u_pathviews.updatedPaths limit 3")
    return c.fetchall()


def getPopularAuthors(c):

    c.execute(
      "create view pathviews as select path, count(*) as views "
      "from log where status = '200 OK' and length(path) > 1 group by path "
      "order by views desc")
    c.execute(
        "create view u_pathviews as select replace(path, '/article/', '')"
        " as updatedPaths, views from pathviews")
    c.execute(
      "create view articleViews as select author, articles.title, "
      "views from articles join u_pathviews on "
      "articles.slug = u_pathviews.updatedPaths")
    c.execute(
      "create view authorViews as select author, sum(views) as "
      "TotalViews from articleViews group by author order by TotalViews desc")
    c.execute(
        "select name, TotalViews from authorViews join authors on "
        "authorViews.author = authors.id")
    return c.fetchall()


def getMostRequestErrors(c):
    c.execute(
      "create view OKcount as select date(time) as date, count(*) "
      "as views from log where status = '200 OK' and length(path) > 1 "
      "group by date order by date desc")
    c.execute(
      "create view FAILcount as select date(time) as date, "
      "count(*) as views from log where status = '404 NOT FOUND' and "
      "length(path) > 1 group by date order by date desc")
    c.execute(
      "create view joinedCount as select OKcount.date as date, "
      "OKcount.views as OKViews, FAILcount.views as FAILViews, "
      "(COALESCE(OKcount.views,0) + COALESCE(FAILcount.views,0)) as total "
      "from OKcount left join FAILcount on OKcount.date = FAILcount.date")
    c.execute(
      "create view errorCount as select date, round(((FAILViews * "
      "100.0) / total), 2) as ErrorRate from joinedCount")
    c.execute(
      "select date, ErrorRate from errorCount where ErrorRate > 1 "
      "order by ErrorRate desc")
    return c.fetchall()


if __name__ == '__main__':
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    topArticles = getTop3Articles(c)
    db.close()

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    popularAuthors = getPopularAuthors(c)
    db.close()

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    errorDays = getMostRequestErrors(c)
    db.close()

    with open("Output.txt", "w") as text_file:
        text_file.write("Top articles: \n")
        for post in topArticles:
            text_file.write(
                ' "{0}" - {1} views{2}'.format(post[0], post[1], "\n"))

    with open("Output.txt", "a") as text_file:
        text_file.write("\nMost popular authors: \n")
        for author in popularAuthors:
            text_file.write(
                ' {0} - {1} views{2}'.format(author[0], author[1], "\n"))

    with open("Output.txt", "a") as text_file:
        text_file.write("\nDays with most request errors: \n")
        for errorDay in errorDays:
            text_file.write(
                ' {0} - {1}% errors{2}'.format(
                  errorDay[0].strftime('%B %d, %Y'), errorDay[1], "\n"))
