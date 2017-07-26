# Log Analysis by byamba3
Program that produces a comprehensive log on popular articles, top authors and days with most errors from a news database using PSQL

## Requirements
- Vagrant
- Linux VM
- Python3

## How to run:
- Run the Linux VM
- Place the **logproducer.py** inside the **/vagrant** folder
- Change directory to **/vagrant** on your VM
- Run logproducer.py from the directory

## Views used:

1. Top 3 Articles: 

- create view pathviews as select path, count(*) as views from log where status = '200 OK' and length(path) > 1 group by path order by views desc

- create view u_pathviews as select replace(path, '/article/', '') as updatedPaths, views from pathviews

2. Popular authors:

- create view pathviews as select path, count(*) as views from log where status = '200 OK' and length(path) > 1 group by path order by views desc

- create view u_pathviews as select replace(path, '/article/', '') as updatedPaths, views from pathviews

- create view articleViews as select author, articles.title, views from articles join u_pathviews on articles.slug = u_pathviews.updatedPaths

- create view authorViews as select author, sum(views) as TotalViews from articleViews group by author order by TotalViews desc

3. Most request errors:

- create view OKcount as select date(time) as date, count(*) as views from log where status = '200 OK' and length(path) > 1 group by date order by date desc

- create view FAILcount as select date(time) as date, count(*) as views from log where status = '404 NOT FOUND' and length(path) > 1 group by date order by date desc

- create view joinedCount as select OKcount.date as date, OKcount.views as OKViews, FAILcount.views as FAILViews, (COALESCE(OKcount.views,0) + COALESCE(FAILcount.views,0)) as total from OKcount left join FAILcount on OKcount.date = FAILcount.date

- create view errorCount as select date, round(((FAILViews * 100.0) / total), 2) as ErrorRate from joinedCount3. 

## License
MIT License

Copyright (c) [2017] [Byambasuren Ulziisaikhan]

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
