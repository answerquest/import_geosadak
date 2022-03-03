

DROP TABLE IF EXISTS habitation;
CREATE TABLE habitation (
	id VARCHAR(10) NOT NULL PRIMARY KEY,
	"HAB_ID" VARCHAR(10) NULL,
	"STATE_ID" VARCHAR(10) NULL,
	"DISTRICT_I" VARCHAR(10) NULL,
	"BLOCK_ID" VARCHAR(10) NULL, 
	"HAB_NAME" VARCHAR(100) NULL,
	"TOT_POPULA" VARCHAR(10) NULL,
	geometry GEOMETRY(POINT,4326) NULL
);

DROP TABLE IF EXISTS road;
CREATE TABLE road (
	id VARCHAR(10) NOT NULL PRIMARY KEY,
	"ER_ID" VARCHAR(10) NULL,
	"STATE_ID" VARCHAR(3) NULL,
	"BLOCK_ID" VARCHAR(5) NULL,
	"DISTRICT_I" VARCHAR(5) NULL,
	"DRRP_ROAD_" VARCHAR(50) NULL,
	"RoadCatego" VARCHAR(20) NULL,
	"RoadName" VARCHAR(200) NULL,
	"RoadOwner" VARCHAR(10) NULL,
	geometry GEOMETRY(LINESTRING,4326) NULL
);


DROP TABLE IF EXISTS facility;
CREATE TABLE facility (
	id VARCHAR(10) NOT NULL PRIMARY KEY,
	"STATE_ID" VARCHAR(5) NULL,
	"DISTRICT_I" VARCHAR(5) NULL,
	"BLOCK_ID" VARCHAR(5) NULL,
	"HAB_ID" VARCHAR(10) NULL,
	"FACILITY_I" VARCHAR(10) NULL,
	"FAC_DESC" VARCHAR(200) NULL,
	"FAC_CATEGO" VARCHAR(50) NULL,
	geometry GEOMETRY(POINT,4326) NULL
);


DROP TABLE IF EXISTS proposal;
CREATE TABLE proposal (
	id VARCHAR(10) NOT NULL PRIMARY KEY,
	"MRL_ID" VARCHAR(6) NULL,
	"STATE_ID" VARCHAR(2) NULL,
	"DISTRICT_I" VARCHAR(3) NULL,
	"BLOCK_ID" VARCHAR(4) NULL,
	"CN_CODE" VARCHAR(6) NULL,
	"PROPOSED_L" DECIMAL(5,2) NULL,
	"WORK_NAME" VARCHAR(255) NULL,
	"IMS_YEAR" INT NULL,
	"IMS_BATCH" VARCHAR(10) NULL,
	geometry GEOMETRY(GEOMETRY, 4326) NULL
);


DROP TABLE IF EXISTS block;
CREATE TABLE block (
	"BLOCK_ID" VARCHAR(5) NOT NULL PRIMARY KEY,
	"BLOCK_NAME" VARCHAR(50) NULL,
	"DISTRICT_ID" VARCHAR(5) NULL,
	"DISTRICT_NAME" VARCHAR(50) NULL,
	"STATE_ID" VARCHAR(5) NULL,
	"STATE_NAME" VARCHAR(50) NULL,
	geometry GEOMETRY (GEOMETRY, 4326) NULL
);
