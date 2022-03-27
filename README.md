# import_geosadak

Importing pmgsy-geosadak data (https://github.com/datameet/pmgsy-geosadak) into a PostGreSQL database (with PostGIS extn enabled)

## Steps

1. Clone the data repo, keep under this folder
```
git clone https://github.com/datameet/pmgsy-geosadak
```
note: there's a split-up zip in the roads folder, extract to get original zip shapefile and delete off the split-up one

2. setup a PostGreSQL DB with PostGIS extension enabled, get a db user login for it. Put in the credentials json and remove the "sample_" in the filename.

3. setup tables in the DB with schema.sql

4. required python3 libs to run the program:
```
pip3 install pandas geopandas xlrd SQLAlchemy GeoAlchemy2
```

## DB setup related

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
States having BLOCK_ID values in boundaries shapefile which does not have matching Master data entry:  
TamilNadu - 3  
JammuAndKashmir - 3  
These blocks do have road data etc but no entry in master data excel: **8108, 8105, 8106, 8063, 8034, 8041**

States having BLOCK_ID=0 in their block boundary shapefile:  
Punjab - 1  
WestBengal - 3  
I've imported these boundaries with randomly assigned block ids. We'll need to match them to actual block id.


## DB setup in local machine using Docker

```
docker run -it --rm -p "5432:5432" \
-v /home/nikhil/Software/docker-postgres/data:/var/lib/postgresql \
-e DEFAULT_ENCODING="UTF8" \
-e DEFAULT_COLLATION="en_US.UTF-8" \
-e DEFAULT_CTYPE="en_US.UTF-8" \
-e PASSWORD_AUTHENTICATION="md5" \
-v /home/nikhil/Software/docker-postgres/pg_wal:/opt/postgres/pg_wal \
-e POSTGRES_INITDB_WALDIR=/opt/postgres/pg_wal \
-e POSTGRES_USER=YOUR_USER \
-e POSTGRES_PASS=YOUR_PW \
-e POSTGRES_MULTIPLE_EXTENSIONS=postgis \
-e ALLOW_IP_RANGE='0.0.0.0/0' \
-e POSTGRES_DBNAME=postgres,YOUR_DB \
kartoza/postgis:14-3.2
```

Notes:
- postgresql + postgis docker image taken from https://registry.hub.docker.com/r/kartoza/postgis , but there was one change as detailed at https://stackoverflow.com/a/64978644/4355695 to make the data persistence happen
- assuming admin user as "YOUR_USER" and password as "YOUR_PW" and DB name as "YOUR_DB", replace accordingly at your end
- using -v to mount the DB data on local folders, so that it's still there the next time you start this docker db
- below command is for command prompt Terminal on Linux/Ubuntu machines, assuming docker is properly installed and the logged in user has docker access. 
- On windows some syntax might vary; check and convert accordingly.
- the \ at the end is just to tell the OS that there's more on the next line (newline operator in shell script)


### Create DB tables
Once this is started, start PgAdmin DB management tool (https://www.pgadmin.org/) 
- connect to this DB (server: localhost, user:YOUR_USER, pw: YOUR_PW, rest all leave as-is ), 
- get on the "YOUR_DB" DB
- right-click, open query window
- run the contents of schema.sql

Note: PGAdmin is one way; you can also use other ways to connect to the DB and create the tables, like in a python program / notebook.
