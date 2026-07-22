import sqlite3
import os
import node

class DataBase:
    def __init__(self, db_path='monitor.db'):  # Один параметр, одно имя
        self.db_path = db_path  # Один атрибут

    def create_tables(self):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.executescript('''
                   PRAGMA foreign_keys = ON;
                   PRAGMA journal_mode = WAL;
                   PRAGMA synchronous = NORMAL;
                   PRAGMA temp_store = MEMORY;
                   PRAGMA cache_size = -64000;
                   PRAGMA busy_timeout = 5000;


                   CREATE TABLE locations (
                       building TEXT NOT NULL,
                       cabinet INTEGER,
                       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
                   );


                   CREATE TABLE parameters_for_connection_S7 (
                       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       ip TEXT NOT NULL,
                       port INTEGER DEFAULT 102 NOT NULL
                   );


                   CREATE TABLE parameters_for_connection_SNMP (
                       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       ip TEXT NOT NULL,
                       port INTEGER DEFAULT 161 NOT NULL,
                       version_snmp INTEGER DEFAULT 2 NOT NULL,
                       community_string TEXT DEFAULT 'public' NOT NULL,
                       availability INTEGER DEFAULT 0 NOT NULL
                   );


                   CREATE TABLE availability_devices (
                       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       yes_or_no INTEGER NOT NULL
                   );


                   CREATE TABLE list_devices (
                       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       fk_location_id INTEGER NOT NULL,
                       fk_parameters_for_connection_S7 INTEGER,
                       fk_availability_id INTEGER,
                       fk_parameters_for_connection_SNMP INTEGER,

                       CONSTRAINT list_devices_availability_devices_FK
                           FOREIGN KEY (fk_availability_id)
                           REFERENCES availability_devices(id),

                       CONSTRAINT list_devices_locations_FK
                           FOREIGN KEY (fk_location_id)
                           REFERENCES locations(id),

                       CONSTRAINT list_devices_parameters_for_connection_S7_FK
                           FOREIGN KEY (fk_parameters_for_connection_S7)
                           REFERENCES parameters_for_connection_S7(id),

                       CONSTRAINT list_devices_parameters_for_connection_SNMP_FK
                           FOREIGN KEY (fk_parameters_for_connection_SNMP)
                           REFERENCES parameters_for_connection_SNMP(id)
                   );


                   CREATE TABLE viewed_parameters_snmp (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name_parameter TEXT NOT NULL,
                       oid TEXT NOT NULL UNIQUE,
                       unit TEXT
                   );


                   CREATE TABLE status_list (
                       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       status INTEGER NOT NULL
                   );


                   CREATE TABLE history_parameters_SNMP (
                       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,

                       fk_list_devices_id INTEGER NOT NULL,
                       fk_viewed_parameters_snmp_id INTEGER NOT NULL,

                       data_time INTEGER,
                       value TEXT NOT NULL,

                       fk_status_list_id INTEGER NOT NULL,

                       CONSTRAINT history_parameters_SNMP_list_devices_FK
                           FOREIGN KEY (fk_list_devices_id)
                           REFERENCES list_devices(id),

                       CONSTRAINT history_parameters_SNMP_viewed_parameters_snmp_FK
                           FOREIGN KEY (fk_viewed_parameters_snmp_id)
                           REFERENCES viewed_parameters_snmp(id),

                       CONSTRAINT history_parameters_SNMP_status_list_FK
                           FOREIGN KEY (fk_status_list_id)
                           REFERENCES status_list(id)
                   );


                   CREATE TABLE present_parameters_snmp (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,

                       fk_list_devices_id INTEGER NOT NULL,
                       fk_viewed_parameter_snmp_id INTEGER NOT NULL,

                       catch_value TEXT NOT NULL,

                       fk_status_list_id INTEGER NOT NULL,

                       CONSTRAINT present_parameters_snmp_status_list_FK
                           FOREIGN KEY (fk_status_list_id)
                           REFERENCES status_list(id),

                       CONSTRAINT present_parameters_snmp_list_devices_FK
                           FOREIGN KEY (fk_list_devices_id)
                           REFERENCES list_devices(id),

                       CONSTRAINT present_parameters_snmp_viewed_parameters_snmp_FK
                           FOREIGN KEY (fk_viewed_parameter_snmp_id)
                           REFERENCES viewed_parameters_snmp(id)
                   );



                   CREATE INDEX idx_locations_building
                   ON locations(building);


                   CREATE INDEX idx_s7_ip
                   ON parameters_for_connection_S7(ip);


                   CREATE INDEX idx_snmp_ip
                   ON parameters_for_connection_SNMP(ip);


                   CREATE INDEX idx_list_devices_location
                   ON list_devices(fk_location_id);


                   CREATE INDEX idx_list_devices_s7
                   ON list_devices(fk_parameters_for_connection_S7);


                   CREATE INDEX idx_list_devices_snmp
                   ON list_devices(fk_parameters_for_connection_SNMP);


                   CREATE INDEX idx_list_devices_availability
                   ON list_devices(fk_availability_id);


                   CREATE INDEX idx_history_device
                   ON history_parameters_SNMP(fk_list_devices_id);


                   CREATE INDEX idx_history_parameter
                   ON history_parameters_SNMP(fk_viewed_parameters_snmp_id);


                   CREATE INDEX idx_history_device_parameter_time
                   ON history_parameters_SNMP(
                       fk_list_devices_id,
                       fk_viewed_parameters_snmp_id,
                       data_time
                   );


                   CREATE INDEX idx_present_device
                   ON present_parameters_snmp(fk_list_devices_id);


                   CREATE INDEX idx_present_parameter
                   ON present_parameters_snmp(fk_viewed_parameter_snmp_id);

               ''')

    def convert_nodes_to_tables(self, nodes: list):
        pass

    def insert_nodes_in_db(self, nodes:list):
        names_device_snmp = [node.name for node in nodes]

        with sqlite3.connect(self.db_path) as connection:
            pass
            



db = DataBase("C:/MyPythonProgramm/SNMP_simple/data/monitor.db")
db.create_tables()