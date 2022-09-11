CREATE TABLE IF NOT EXISTS ds_election_provinces (
    id int NOT NULL AUTO_INCREMENT,
    province_id int NOT NULL,
    name_np varchar(100) NOT NULL,
    name_en varchar(100) NOT NULL,
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
    created_at timestamp default now(), 
    updated_at timestamp default now() on update now(),
    PRIMARY KEY (id),
    UNIQUE(district_id)
    -- FOREIGN KEY (province_id) REFERENCES ds_election_provinces(province_id)
);

CREATE TABLE IF NOT EXISTS ds_election_fresults (
    id bigint NOT NULL AUTO_INCREMENT,
    province_id int NOT NULL,
    district_id varchar(50) NOT NULL,
    type ENUM ('federal','provincial') NOT NULL default "federal",
    region_id float NOT NULL,
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
    type ENUM ('federal','provincial') NOT NULL default "federal",
    region_id float NOT NULL,
    declared boolean DEFAULT false,
    result JSON,
    elected JSON,
    created_at timestamp default now(), 
    updated_at timestamp default now() on update now(),
    PRIMARY KEY (id)
    -- FOREIGN KEY (province_id) REFERENCES ds_election_provinces(province_id),
    -- FOREIGN KEY (district_id) REFERENCES ds_election_districts(district_id)
);

DROP VIEW if EXISTS ds_v_df_results;
DROP VIEW if EXISTS ds_v_pf_results;
DROP VIEW if EXISTS ds_v_federal_results;

CREATE VIEW ds_v_df_results as SELECT province_id,  district_id, json_object('id', ROUND(region_id,  0), 'declared', declared, 'result',result,'elected', elected) as regions FROM ds_election_fresults;
CREATE VIEW ds_v_pf_results as SELECT province_id, json_object('id', district_id, 'regions', JSON_ARRAYAGG(regions)) as districts from ds_v_df_results GROUP by province_id, district_id;
CREATE VIEW ds_v_federal_results as SELECT JSON_ARRAYAGG(districts) as provinces from ds_v_pf_results GROUP by province_id;


DROP VIEW if EXISTS ds_v_dp_results;
DROP VIEW if EXISTS ds_v_pp_results;
DROP VIEW if EXISTS ds_v_provincial_results;
CREATE VIEW ds_v_dp_results as SELECT province_id,  district_id, json_object('id', ROUND(region_id, 1), 'declared', declared, 'result',result,'elected', elected) as regions FROM ds_election_presults;
CREATE VIEW ds_v_pp_results as SELECT province_id, json_object('id', district_id, 'regions', JSON_ARRAYAGG(regions)) as districts from ds_v_dp_results GROUP by province_id, district_id;
CREATE VIEW ds_v_provincial_results as SELECT JSON_ARRAYAGG(districts) as provinces from ds_v_pp_results GROUP by province_id;
