CREATE SCHEMA IF NOT EXISTS @schema;

CREATE TABLE IF NOT EXISTS @schema.temp_dep_run (
    temp_dep_run_id                      uuid PRIMARY KEY,
    commit_hash                          varchar(50),
    temp_dep_run_dttm                    timestamp with time zone,
    run_input_data_start_date            date,
    run_input_data_end_date              date
);


CREATE OR REPLACE FUNCTION @schema.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = current_timestamp;
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TABLE @schema.test_table (
    test_id_1               integer not null,
    test_id_2               text not null,
    test_date               date not null,
    test_value              float not null,
    created_at              timestamptz not null default current_timestamp,
    updated_at              timestamptz not null default current_timestamp,
    readings                @schema.elec_reading[] not null,


    PRIMARY KEY (test_id_1, test_id_2, test_date)
);


CREATE TRIGGER update_test_table BEFORE UPDATE ON @schema.test_table
FOR EACH ROW EXECUTE PROCEDURE @schema.update_updated_at_column();

TRUNCATE @schema.test_table;
