CREATE TABLE IF NOT EXISTS ds_election_provinces (
    id int NOT NULL AUTO_INCREMENT,
    province_id int NOT NULL,
    name_np varchar(100) NOT NULL,
    name_en varchar(100) NOT NULL,
    color varchar(10),
    created_at timestamp default now(), 
    updated_at timestamp default now() on update now(),
    PRIMARY KEY (id),
    UNIQUE(province_id)
);

CREATE TABLE IF NOT EXISTS ds_election_districts (
    id int NOT NULL AUTO_INCREMENT,
    district_id varchar(50) NOT NULL,
    province_id int NOT NULL,
    name_np varchar(100) NOT NULL,
    name_en varchar(100) NOT NULL,
    total_fregions int NOT NULL,
    total_pregions int NOT NULL,
    created_at timestamp default now(), 
    updated_at timestamp default now() on update now(),
    PRIMARY KEY (id),
    UNIQUE(district_id)
    -- FOREIGN KEY (province_id) REFERENCES ds_election_provinces(province_id)
);

CREATE TABLE IF NOT EXISTS ds_election_regions (
    id int NOT NULL AUTO_INCREMENT,
    region_id float NOT NULL,
    district_id varchar(50) NOT NULL,
    province_id int NOT NULL,
    rtype ENUM ('federal','provincial') NOT NULL default "federal",
    name_np varchar(100) NOT NULL,
    name_en varchar(100) NOT NULL,
    created_at timestamp default now(), 
    updated_at timestamp default now() on update now(),
    PRIMARY KEY (id),
    UNIQUE(district_id, region_id)
    -- FOREIGN KEY (province_id) REFERENCES ds_election_provinces(province_id)
);

CREATE TABLE IF NOT EXISTS ds_election_fresults (
    id bigint NOT NULL AUTO_INCREMENT,
    province_id int NOT NULL,
    district_id varchar(50) NOT NULL,
    region_id float NOT NULL,
    rtype ENUM ('federal','provincial') NOT NULL default "federal",
    declared boolean DEFAULT false,
    result JSON,
    elected JSON,
    created_at timestamp default now(), 
    updated_at timestamp default now() on update now(),
    PRIMARY KEY (id)
    -- FOREIGN KEY (province_id) REFERENCES ds_election_provinces(province_id),
    -- FOREIGN KEY (district_id) REFERENCES ds_election_districts(district_id)
);

CREATE TABLE IF NOT EXISTS ds_election_presults (
    id bigint NOT NULL AUTO_INCREMENT,
    province_id int NOT NULL,
    district_id varchar(50) NOT NULL,
    region_id float NOT NULL,
    rtype ENUM ('federal','provincial') NOT NULL default "federal",
    declared boolean DEFAULT false,
    result JSON,
    elected JSON,
    created_at timestamp default now(), 
    updated_at timestamp default now() on update now(),
    PRIMARY KEY (id)
    -- FOREIGN KEY (province_id) REFERENCES ds_election_provinces(province_id),
    -- FOREIGN KEY (district_id) REFERENCES ds_election_districts(district_id)
);

CREATE TABLE IF NOT EXISTS ds_election_parties (
    id int NOT NULL AUTO_INCREMENT,
    party_id int NOT NULL,
    code varchar(20) NOT NULL,
    name_np varchar(100) NOT NULL,
    name_en varchar(100) NOT NULL,
    short_name_np varchar(100),
    short_name_en varchar(100),
    color varchar(10),
    symbol varchar(100),
    created_at timestamp default now(), 
    updated_at timestamp default now() on update now(),
    PRIMARY KEY (id),
    UNIQUE(code)
);

DROP VIEW IF EXISTS ds_v_df_results;
DROP VIEW IF EXISTS ds_v_pf_results;
DROP VIEW IF EXISTS ds_v_federal_results;

CREATE VIEW ds_v_df_results AS SELECT province_id,  district_id, json_object('id', ROUND(region_id,  0), 'declared', declared, 'result',result,'elected', elected) AS regions FROM ds_election_fresults;
CREATE VIEW ds_v_pf_results AS SELECT province_id, json_object('id', district_id, 'regions', JSON_ARRAYAGG(regions)) AS districts from ds_v_df_results GROUP by province_id, district_id;
CREATE VIEW ds_v_federal_results AS SELECT JSON_ARRAYAGG(districts) AS provinces from ds_v_pf_results GROUP by province_id;


DROP VIEW IF EXISTS ds_v_dp_results;
DROP VIEW IF EXISTS ds_v_pp_results;
DROP VIEW IF EXISTS ds_v_provincial_results;
CREATE VIEW ds_v_dp_results AS SELECT province_id,  district_id, json_object('id', ROUND(region_id, 1), 'declared', declared, 'result',result,'elected', elected) AS regions FROM ds_election_presults;
CREATE VIEW ds_v_pp_results AS SELECT province_id, json_object('id', district_id, 'regions', JSON_ARRAYAGG(regions)) AS districts from ds_v_dp_results GROUP by province_id, district_id;
CREATE VIEW ds_v_provincial_results AS SELECT JSON_ARRAYAGG(districts) AS provinces from ds_v_pp_results GROUP by province_id;


DROP VIEW IF EXISTS ds_v_district_regions;
DROP VIEW IF EXISTS ds_v_province_district_regions;

CREATE view ds_v_district_regions AS SELECT d.province_id, d.district_id, d.name_np, d.name_en, d.total_fregions, d.total_pregions, JSON_ARRAYAGG(JSON_OBJECT("id", r.region_id, "rtype", r.rtype, "name_np", r.name_np, "name_en", r.name_en)) AS "regions" FROM ds_election_districts d, ds_election_regions r WHERE r.district_id = d.district_id GROUP BY d.district_id ORDER by d.id;
CREATE VIEW ds_v_province_district_regions AS SELECT p.province_id, p.name_np, p.name_en, p.color, JSON_ARRAYAGG(JSON_OBJECT("id", dr.district_id, "name_np", dr.name_np, "name_en", dr.name_en, "total_fregion", dr.total_fregions, "total_pregion", dr.total_pregions, "regions", dr.regions)) AS "districts" FROM ds_election_provinces p, ds_v_district_regions dr WHERE p.province_id = dr.province_id GROUP BY p.province_id;
