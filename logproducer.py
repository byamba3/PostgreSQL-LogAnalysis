#!/usr/bin/env python3

import psycopg2
from datetime import datetime

DBNAME = "news"
VIEWS_FILENAME = "create_views.sql"


def getTop3Articles(c):
    "Returns a list of tuples for the top 3 articles in the database"

    c.execute(
      """SELECT title, views from articleViews
         order by views desc limit 3""")
    return c.fetchall()


def getPopularAuthors(c):
    "Returns a list of tuples for the most popular authors in the database"

    c.execute(
        """SELECT name, TotalViews from authorViews join authors on
           authorViews.author = authors.id""")
    return c.fetchall()


def getMostRequestErrors(c):
    "Returns a list of tuples for days with most request errors"

    c.execute(
      """SELECT date, ErrorRate from errorCount where ErrorRate > 1
         order by ErrorRate desc""")
    return c.fetchall()


if __name__ == '__main__':

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # Creates the views from the VIEWS_FILENAME file
    c.execute(open(VIEWS_FILENAME, "r").read())

    topArticles = getTop3Articles(c)
    popularAuthors = getPopularAuthors(c)
    errorDays = getMostRequestErrors(c)

    db.close()

    # Prints out all the results to an output file

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
        text_file.write("\nDay(s) with most request errors: \n")
        for errorDay in errorDays:
            text_file.write(
                ' {0} - {1}% errors{2}'.format(
                  errorDay[0].strftime('%B %d, %Y'), errorDay[1], "\n"))
