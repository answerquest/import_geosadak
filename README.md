# import_geosadak

Importing pmgsy-geosadak data (https://github.com/datameet/pmgsy-geosadak) into a PostGreSQL database (with PostGIS extn enabled)

## Steps

1. Clone the data repo, keep under this folder
```
git clone https://github.com/datameet/pmgsy-geosadak
```
note: there's a split-up zip in the roads folder, extract to get original zip shapefile and delete off the split-up one

2. setup a PostGreSQL DB with PostGIS extension enabled, get a db user login for it. Put in the credentials json and remove the "sample_" in the filename. Alternative: use a Dockerised postgresql with data stored on a mounted folder. See instructions for both below.

3. In the program geosadak_import.py, keep `CREATE_TABLES = True` to do tables setup alongwith the program. In case you're running it again and don't need to setup tables again, change this to False. You can also see the DB schema in schemal.sql and create the tables yourself through pgadmin.

4. required python3 libs to run the program:
```
pip3 install pandas geopandas xlrd SQLAlchemy GeoAlchemy2
```

5. Run the program
```
python3 geosadak_import.py
```
It should take about half an hour.



## DB setup in local machine using Docker

```
docker run -it --rm -p "5432:5432" \
-e POSTGRES_USER=user1 \
-e POSTGRES_PASS=password1 \
-e POSTGRES_DBNAME=postgres,geosadak \
-v /home/nikhil/Software/docker-postgres/data:/var/lib/postgresql \
-e DEFAULT_ENCODING="UTF8" \
-e DEFAULT_COLLATION="en_US.UTF-8" \
-e DEFAULT_CTYPE="en_US.UTF-8" \
-e PASSWORD_AUTHENTICATION="md5" \
-v /home/nikhil/Software/docker-postgres/pg_wal:/opt/postgres/pg_wal \
-e POSTGRES_INITDB_WALDIR=/opt/postgres/pg_wal \
-e POSTGRES_MULTIPLE_EXTENSIONS=postgis \
-e ALLOW_IP_RANGE='0.0.0.0/0' \
kartoza/postgis:14-3.2
```

Notes:
- postgresql + postgis docker image taken from https://registry.hub.docker.com/r/kartoza/postgis , but there was one change as detailed at https://stackoverflow.com/a/64978644/4355695 to make the data persistence happen
- `-p 5432:5432` : in case the 5432 port num on your system is occupied, change the left side number here to map another free port to the dockerized DB. Don't change the right side number.
- assuming admin user as "user1" and password as "password1" and DB name as "geosadak", replace accordingly at your end
- using -v to mount the DB data on local folders, so that it's still there the next time you start this docker db
- below command is for command prompt Terminal on Linux/Ubuntu machines, assuming docker is properly installed and the logged in user has docker access. 
- On windows some syntax might vary; check and convert accordingly.
- the \ at the end is just to tell the OS that there's more on the next line (newline operator in shell script)


## DB setup, without docker

This is if you have installed PostGreSQL in a ubuntu machine, or a ubuntu webserver in EC2, DigitalOcean, Hetzner, SSDnodes etc.

Get into the psql shell:
```
su - postgres
psql
```

Creating a master user
```
createuser --interactive --pwprompt;
```

will get following prompts
```
Enter name of role to add: geosadak_admin
Enter password for new role: 
Enter it again: 
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) y
```

Creating new db "geosadak":
```
createdb -O geosadak_admin geosadak;
```

Enable postgis extension in the DB: https://postgis.net/install/
```
\connect geosadak;
CREATE EXTENSION postgis;
```

Ok all set, get out of the psql shell and postgresql user account and back to your regular user
```
exit
exit
```

## Some data inconsistencies found:
1. States having BLOCK_ID values in boundaries shapefile which does not have matching Master data entry:  
TamilNadu - 3  
JammuAndKashmir - 3  
These blocks do have road data etc but no entry in master data excel: **8108, 8105, 8106, 8063, 8034, 8041**

2. States having BLOCK_ID=0 in their block boundary shapefile:  
Punjab - 1  
WestBengal - 3  
I've imported these boundaries with randomly assigned block ids. We'll need to match them to actual block id.

3. Following 8 habitation ids have null district id, zero block id and don't seem to have proper lat-longs. They are all under state Maharashtra (21):  
"1229800", "1229524", "1229611", "1229553", "1229557", "1229780", "1240063", "1240589", "1229803"  
Query:   
```select id, "STATE_ID", "DISTRICT_I", "HAB_ID", ST_AsText(geometry) from habitation where "BLOCK_ID" = 'ZEROBLOCK'
```

4. 4230 Habitation entries have null district id, across 21 states.
Queries:  
```
select id, "STATE_ID", "DISTRICT_I", "HAB_ID", ST_AsText(geometry) from habitation where "DISTRICT_I" is null;
select "STATE_ID", count(*) as count from habitation where "DISTRICT_I" is null group by  "STATE_ID" order by count desc
```

### Using PGAdmin tool to manage the DB
Once this is started, start PgAdmin DB management tool (https://www.pgadmin.org/) 
- connect to this DB (server: localhost, user:user1, pw: password1, rest all leave as-is ), 
- get on the "geosadak" DB
- right-click, open query window
- Run queries like: `select * from road where "BLOCK_ID" = '2571'`
- On the geometry column, you'll see an eye button at end. Click it to see the query results in map view.

Note: PGAdmin is one way; you can also use other ways to connect to the DB and query the tables, like in a python program / notebook.
