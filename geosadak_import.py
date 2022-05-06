# geosadak_import.py
# by Nikhil VJ, nikhil.js@gmail.com

###########################

# flags - set to False to skip a section
CREATE_TABLES = True
HABITATION_FLAG = True
ROAD_FLAG = True
FACILITY_FLAG = True
PROPOSAL_FLAG = True
BLOCK_FLAG = True
batch = 100000

HABITATION_CLEAR = True
ROAD_CLEAR = True
FACILITY_CLEAR = True
PROPOSAL_CLEAR = True
BLOCK_CLEAR = True

from sqlalchemy import create_engine
import geopandas as gpd
import pandas as pd
import os, datetime, time, json, sys
import secrets

##########################

## FUNCTIONS
def makeUID(length=7):
    return secrets.token_urlsafe(length).upper()

def makeInt(x):
    if x:
        return str(int(x))
    elif x==0:
        return 'ZEROBLOCK'
    else:
        return None
def makeStr(x):
    if x:
        return str(x)
    else:
        return None

def logmessage( *content ):
    timestamp = '{:%Y-%m-%d %H:%M:%S} :'.format(datetime.datetime.utcnow() + datetime.timedelta(hours=5.5)) # from https://stackoverflow.com/a/26455617/4355695
    line = ' '.join(str(x) for x in list(content)) # from https://stackoverflow.com/a/3590168/4355695
    print(line) # print to screen also
    with open(os.path.join('import_log.txt'), 'a') as f:
        print(timestamp, line, file=f) # file=f argument at end writes to file. from https://stackoverflow.com/a/2918367/4355695


##########################
## INTIATE

creds = json.load(open('dbcreds_geosadak.json','r'))
engine = create_engine(f"postgresql://{creds['DB_USER']}:{creds['DB_PW']}@{creds['DB_SERVER']}:{creds['DB_PORT']}/{creds['DB_DBNAME']}")

root = os.path.dirname(__file__)
dataFolder = os.path.join(root,'pmgsy-geosadak','data')
folder_habitation = os.path.join(dataFolder,'Habitation')
folder_road = os.path.join(dataFolder,'Road_DRRP')
folder_facility = os.path.join(dataFolder,'Facilities')
folder_proposal = os.path.join(dataFolder,'Proposals')
folder_bound = os.path.join(dataFolder,'Bound_Block')

# setup DB - skip this if already done
if CREATE_TABLES:
    logmessage("#"*50)
    logmessage("Setting up DB")
    with open(os.path.join(root,'schema.sql'),'r') as f:
        schema = [' '.join(x.split()).strip() for x in f.read().split(';') if len(x)]
    c = engine.connect()
    for line in schema:
        if len(line):
            logmessage(line)
            res = c.execute(line)
    c.close()
    logmessage("DB setup done.")

###########

# habitations
if HABITATION_FLAG:
    logmessage("#"*50)
    start = time.time()
    filesList = [x for x in os.listdir(folder_habitation) if x.lower().endswith('.zip') ]
    logmessage(f"habitation: {filesList}")

    if HABITATION_CLEAR:
        d1 = "delete from habitation"
        c = engine.connect()
        res = c.execute(d1)
        logmessage(f"{res.rowcount} rows deleted in habitation table")
        c.close()

    for file1 in filesList:
        gdf1 = gpd.read_file(os.path.join(folder_habitation,file1)).fillna('')
        if len(gdf1):
            for col in ['HAB_ID', 'STATE_ID', 'DISTRICT_I', 'BLOCK_ID', 'TOT_POPULA']:
                gdf1[col] = gdf1[col].apply(makeInt)
            for col in ['HAB_NAME']:
                gdf1[col] = gdf1[col].apply(makeStr)
            gdf1['id'] = gdf1[col].apply(lambda x: makeUID())
            logmessage(f"{file1} {len(gdf1)} rows")
            gdf1.to_postgis('habitation',engine, if_exists='append', index=False, chunksize=batch)
    
    
    # Data-cleaning: there are cases where lat, lon are big negative numbers - invalid lat-longs in the data dumps. 
    # Have to remove those entries so they don't mess up other flows
    d2 = f"delete from habitation where ST_Y(geometry) < 0"
    c = engine.connect()
    res = c.execute(d2)
    logmessage(f"{res.rowcount} invalid lat-long rows deleted in habitation table")
    c.close()

    end = time.time()
    logmessage(f"Habitations imported in {round(end-start,1)} secs")

###########

# roads
if ROAD_FLAG:
    logmessage("#"*50)
    start = time.time()
    filesList = [x for x in os.listdir(folder_road) if x.lower().endswith('.zip') ]
    logmessage(f"road: {filesList}")

    if ROAD_CLEAR:
        d1 = "delete from road"
        c = engine.connect()
        res = c.execute(d1)
        logmessage(f"{res.rowcount} rows deleted in road table")
        c.close()

    for file1 in filesList:
        gdf1 = gpd.read_file(os.path.join(folder_road,file1)).fillna('')
        if len(gdf1):
            for col in ['ER_ID', 'STATE_ID', 'BLOCK_ID', 'DISTRICT_I']:
                gdf1[col] = gdf1[col].apply(makeInt)
            for col in ['DRRP_ROAD_', 'RoadCatego', 'RoadName', 'RoadOwner']:
                gdf1[col] = gdf1[col].apply(makeStr)
            gdf1['id'] = gdf1[col].apply(lambda x: makeUID())
            logmessage(f"{file1} {len(gdf1)} rows")
            gdf1.to_postgis('road',engine, if_exists='append', index=False, chunksize=batch)
    end = time.time()
    logmessage(f"Roads imported in {round(end-start,1)} secs")


###########

# facilities
if FACILITY_FLAG:
    logmessage("#"*50)
    start = time.time()
    filesList = [x for x in os.listdir(folder_facility) if x.lower().endswith('.zip') ]
    logmessage(f"facility: {filesList}")

    if FACILITY_CLEAR:
        d1 = "delete from facility"
        c = engine.connect()
        res = c.execute(d1)
        logmessage(f"{res.rowcount} rows deleted in facility table")
        c.close()

    for file1 in filesList:
        gdf1 = gpd.read_file(os.path.join(folder_facility,file1)).fillna('')
        if len(gdf1):
            for col in ['STATE_ID', 'DISTRICT_I', 'BLOCK_ID', 'HAB_ID', 'FACILITY_I']:
                gdf1[col] = gdf1[col].apply(makeInt)
            for col in  ['FAC_DESC', 'FAC_CATEGO']:
                gdf1[col] = gdf1[col].apply(makeStr)
            gdf1['id'] = gdf1[col].apply(lambda x: makeUID())
            logmessage(f"{file1} {len(gdf1)} rows")
            gdf1.to_postgis('facility',engine, if_exists='append', index=False, chunksize=batch)
    end = time.time()
    logmessage(f"Facilities imported in {round(end-start,1)} secs")


###########

# proposals
if PROPOSAL_FLAG:
    logmessage("#"*50)
    start = time.time()
    filesList = [x for x in os.listdir(folder_proposal) if x.lower().endswith('.zip') ]
    logmessage(f"proposal: {filesList}")

    if PROPOSAL_CLEAR:
        d1 = "delete from proposal"
        c = engine.connect()
        res = c.execute(d1)
        logmessage(f"{res.rowcount} rows deleted in proposal table")
        c.close()


    for file1 in filesList:
        gdf1 = gpd.read_file(os.path.join(folder_proposal,file1)).fillna('')
        if len(gdf1):
            for col in ['MRL_ID','STATE_ID', 'DISTRICT_I', 'BLOCK_ID', 'CN_CODE', 'IMS_BATCH']:
                gdf1[col] = gdf1[col].apply(makeInt)
            for col in ['WORK_NAME']:
                gdf1[col] = gdf1[col].apply(makeStr)
            gdf1['id'] = gdf1[col].apply(lambda x: makeUID())
            logmessage(f"{file1} {len(gdf1)} rows")
            gdf1.to_postgis('proposal',engine, if_exists='append', index=False, chunksize=batch)

    end = time.time()
    logmessage(f"Proposals imported in {round(end-start,1)} secs")


###########
# Blocks master and block shapes
if BLOCK_FLAG:
    logmessage("#"*50)
    logmessage("Blocks master and boundaries")
    start = time.time()

    if BLOCK_CLEAR:
        d1 = "delete from block"
        c = engine.connect()
        res = c.execute(d1)
        logmessage(f"{res.rowcount} rows deleted in block table")

    file1 = 'MasterData.xls'
    df1 = pd.read_excel(os.path.join(dataFolder,file1), dtype=str)

    for col in ['BLOCK_ID', 'DISTRICT_ID', 'STATE_ID']:
        df1[col] = df1[col].apply(makeInt)
    for col in ['BLOCK_NAME', 'DISTRICT_NAME', 'STATE_NAME']:
        df1[col] = df1[col].apply(makeStr)
    df1.to_sql('block',engine, if_exists='append', index=False, chunksize=batch)
    logmessage(f"Loaded masterdata excel {len(df1)} rows to block table")

    # Block boundaries
    filesList = [x for x in os.listdir(folder_bound) if x.lower().endswith('.zip') ]
    logmessage(f"block_bound: {filesList}")


    for file1 in filesList:
        gdf1 = gpd.read_file(os.path.join(folder_bound,file1)).fillna('')
        if len(gdf1):
            logmessage(f"{file1} {len(gdf1)} rows")
            gdf1['BLOCK_ID'] = gdf1['BLOCK_ID'].apply(makeInt)
            for N,row in gdf1.iterrows():
                shape = str(row['geometry'])
                
                if row['BLOCK_ID'] != 'ZEROBLOCK':
                    # https://postgis.net/docs/ST_GeomFromText.html
                    u1 = f"""update block set geometry = ST_GeomFromText('{shape}',4326) 
                    where "BLOCK_ID"='{row['BLOCK_ID']}'
                    """
                    # print(u1)
                    res = c.execute(u1)
                    if not res.rowcount:
                        logmessage(f"No block? {row['BLOCK_ID']} making one.")
                        i1 = f"""insert into block("BLOCK_ID","DISTRICT_ID","STATE_ID",geometry) values 
                        ('{row['BLOCK_ID']}','{makeInt(row['DISTRICT_I'])}','{makeInt(row['STATE_ID'])}', 
                        ST_GeomFromText('{shape}',4326) ) """
                        logmessage(' '.join(i1.split())[:100])
                        res2 = c.execute(i1)

                else:
                    # handling edge cases where zero block_id encountered in shapefile
                    BLOCK_ID = makeUID()
                    i2 = f"""insert into block ("BLOCK_ID","DISTRICT_ID","STATE_ID",geometry) values
                    ('{BLOCK_ID}','{makeInt(row['DISTRICT_I'])}','{makeInt(row['STATE_ID'])}', 
                    ST_GeomFromText('{shape}',4326) ) """
                    logmessage(' '.join(i2.split())[:100])
                    res3 = c.execute(i2)
                    logmessage(f"uploaded boundary with BLOCK_ID = {BLOCK_ID}")
    c.close()
    end = time.time()
    logmessage(f"Blocks master and boundaries imported in {round(end-start,1)} secs")
