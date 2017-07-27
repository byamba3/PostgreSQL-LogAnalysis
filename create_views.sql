
CREATE TABLE posts ( content TEXT,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );

CREATE VIEW pathviews as 
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