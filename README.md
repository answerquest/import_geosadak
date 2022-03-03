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
