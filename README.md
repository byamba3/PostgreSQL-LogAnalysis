# Log Analysis by byamba3
This is a python program that makes PostgreSQL queries from a news database to generate a log
that displays the names and views of the top 3 articles, names and views of the most popular authors, and the days with most request errors. 
The program should preferrably run inside a Linux Virtual Machine that supports Python, psycopg2, and PostgreSQL.

## How to run:
- Install VirtualBox from [here](https://www.virtualbox.org/wiki/Downloads) which will run your VM. Download Install the platform package for your operating system.
- Install a VM environment that supports Python3, PostgreSQL, and psycopg2. Vagrant is what I'll be using, and the **Vagrantfile** is included.
- Clone the files in the repository in a folder called **vagrant** and extract the newsdata.zip file to the same directory.
- Open up a terminal within the **vagrant** folder, and enter `vagrant up` then once finished, enter `vagrant ssh`.
- Enter `cd /vagrant` to acess the shared folder
- From there, if you want to run the Python progarm to produce the logs, enter `python3 logproducer.py` and you'll find a file called **Output.txt** within the **vagrant** folder on your local machine.
- To access the database directly, type `psql news` and from there on you can see the tables with with `\dt` and use `SELECT` statemens.

## Views used:

All the created views are found within the **create_views.sql** file. You can open this file in your favorite text editor.

```CREATE VIEW pathviews as 
    SELECT replace(path, '/article/', '') as path, count(*) as views from log 
    where status = '200 OK' and length(path) > 1 group by path;

CREATE VIEW articleViews as 
    SELECT author, articles.title as title, views from articles join pathviews 
    on articles.slug = pathviews.path;

CREATE VIEW authorViews as 
    SELECT author, sum(views) as TotalViews from articleViews 
    group by author order by TotalViews desc;

CREATE VIEW TOTALcount as 
    SELECT date(time) as date, count(*) as views from log 
    group by date;

CREATE VIEW FAILcount as 
    SELECT date(time) as date, count(*) as views from log 
    where status = '404 NOT FOUND' group by date;

CREATE VIEW errorCount as 
    SELECT TOTALcount.date, round(((FAILcount.views * 100.0) / 
    TOTALcount.views), 2) as ErrorRate from TOTALcount left join FAILcount
    on FAILcount.date = TOTALcount.date;
```

## License

Copyright (c) 2017 Byambasuren Ulziisaikhan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
