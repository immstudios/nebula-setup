#!/usr/bin/env python3

import os
import sys
import time
import json

import rex

from nxtools import *
from defaults import *

if os.path.exists("template"):
    from template import *

try:
    import psycopg2
except ImportError:
    log_traceback("Import error")
    critical_error("Unable to import psycopg2")

#
# Settings
#

config = {}
try:
    config.update(json.load(open("settings.json")))
except Exception:
    log_traceback("Configuration error")
    critical_error("Unable to open settings file")


def cs_download():
    if not os.path.exists("cs"):
        os.mkdir("cs")
    try:
        import requests
    except ImportError:
        logging.warning("python-requests library is not installed")
        return

    try:
        csdata = json.loads(requests.get("https://cs.nbla.xyz/dump").text)
    except:
        log_traceback("Unable to load classification schemes")
        return
    for csdato in csdata:
        with open("cs/{}.json".format(slugify(csdato["cs"])), "w") as f:
            json.dump(csdato, f)

cs_download()

#
# Database connection
#

class DB(object):
    def __init__(self, **kwargs):
        self.pmap = {
                "host" : "db_host",
                "user" : "db_user",
                "password" : "db_pass",
                "database" : "db_name",
            }

        self.settings = {
                key : kwargs.get(self.pmap[key], config[self.pmap[key]]) for key in self.pmap
            }

        self.conn = psycopg2.connect(**self.settings)
        self.cur = self.conn.cursor()

    def lastid(self):
        self.query("SELECT LASTVAL()")
        return self.fetchall()[0][0]

    def query(self, query, *args):
        self.cur.execute(query, *args)

    def fetchone(self):
        return self.cur.fetchone()

    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()

    def __len__(self):
        return True

#
# Template installers
#

def install_settings():
    logging.info("Installing site settings")
    db = DB()
    db.query("DELETE FROM settings")
    for key in data["settings"]:
        value = json.dumps(data["settings"][key])
        db.query("INSERT INTO settings (key, value) VALUES (%s, %s)", [key, value])
    db.commit()


def install_storages():
    logging.info("Installing storages")
    db = DB()
    db.query("DELETE FROM storages")
    for key in data["storages"]:
        value = json.dumps(data["storages"][key])
        db.query("INSERT INTO storages (id, settings) VALUES (%s, %s)", [key, value])
    db.commit()
    db.query("SELECT setval(pg_get_serial_sequence('storages', 'id'), coalesce(max(id),0) + 1, false) FROM storages;")
    db.commit()


def install_channels():
    logging.info("Installing channels")
    db = DB()
    db.query("DELETE FROM channels")
    for id in data["channels"]:
        channel_type, settings = data["channels"][id]
        db.query(
                "INSERT INTO channels (id, channel_type, settings) VALUES (%s, %s, %s)",
                [id, channel_type, json.dumps(settings)]
            )
    db.query("SELECT setval(pg_get_serial_sequence('channels', 'id'), coalesce(max(id),0) + 1, false) FROM channels;")
    db.commit()


def install_services():
    logging.info("Installing services")
    db = DB()
    db.query("DELETE FROM services")
    for id in data["services"]:
        stype, host, title, settings, autostart, loop_delay = data["services"][id]
        if not settings:
            settings = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<service/>"
        else:
            settings = open(settings).read()
        db.query(
            "INSERT INTO services (id, service_type, host, title, settings, autostart, loop_delay) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            [id, stype, host, title, settings, autostart, loop_delay])
    db.commit()
    db.query("SELECT setval(pg_get_serial_sequence('services', 'id'), coalesce(max(id),0) + 1, false) FROM services;")
    db.commit()


def install_actions():
    logging.info("Installing actions")
    db = DB()
    db.query("DELETE FROM actions")
    for id in data["actions"]:
        title, service_type, settings_path = data["actions"][id]
        settings = open(settings_path).read()
        db.query(
                "INSERT INTO actions (id, service_type, title, settings) VALUES (%s, %s, %s, %s)",
                [id, service_type, title, settings]
            )
    db.query("SELECT setval(pg_get_serial_sequence('actions', 'id'), coalesce(max(id),0) + 1, false) FROM actions;")
    db.commit()


def install_folders():
    logging.info("Installing asset folders")
    db = DB()
    db.query("DELETE FROM folders")
    for id in data["folders"]:
        settings = data["folders"][id]
        db.query(
                "INSERT INTO folders (id, settings) VALUES (%s, %s)",
                [id, json.dumps(settings)]
            )
    db.query("SELECT setval(pg_get_serial_sequence('folders', 'id'), coalesce(max(id),0) + 1, false) FROM folders;")
    db.commit()


def install_meta_types():
    logging.info("Installing metadata set")
    db = DB()
    languages = ["en", "cs"]

    aliases = {}
    for lang in languages:
        aliases[lang] = {}
        trans_table_fname = os.path.join("aliases", "meta-aliases-{}.json".format(lang))
        l = json.load(open(trans_table_fname))
        for key, alias, header, description in l:
            if header is None:
                header = alias
            aliases[lang][key] = [alias, header, description]

    db.query("DELETE FROM meta_types")
    for key in data["meta_types"]:
        ns, e, index, ft, cls, settings = data["meta_types"][key]
        meta_type_data = {
                "ns" : ns,
                "class" : cls,
                "fulltext" : ft,
                "editable" : e,
                "aliases" : {}
            }
        if settings:
            meta_type_data.update(settings)

        for lang in languages:
            meta_type_data["aliases"][lang] = aliases[lang][key]

        db.query(
                "INSERT INTO meta_types (key, settings) VALUES (%s, %s)",
                [key, json.dumps(meta_type_data)]
            )
        if index:
            idx_name = "idx_" + key.replace("/", "_")
            db.query(
                    "CREATE INDEX IF NOT EXISTS {} ON assets((meta->>%s))".format(idx_name),
                    [key]
                )
    db.commit()


def install_cs():
    logging.info("Installing classification schemes")
    db = DB()
    for csfile in get_files("cs"):
        try:
            data = json.load(csfile.open())
        except:
            log_traceback("Unable to load classification schema {}".format(csfile))
            continue
        name = data["cs"]
        db.query("DELETE FROM cs WHERE cs=%s", [name])
        db.commit()
        for value in data["data"]:
            settings = data["data"][value]
            db.query("INSERT INTO cs (cs, value, settings) VALUES (%s, %s, %s)", [name, value, json.dumps(settings)])
        db.commit()




def install_views():
    logging.info("Installing asset views")
    db = DB()
    db.query("DELETE FROM views")
    for id in data["views"]:
        settings = data["views"][id]
        db.query(
                "INSERT INTO views (id, settings) VALUES (%s, %s)",
                [id, json.dumps(settings)]
            )
    db.query("SELECT setval(pg_get_serial_sequence('views', 'id'), coalesce(max(id),0) + 1, false) FROM views;")
    db.commit()


#
# Run
#

if __name__ == "__main__":
    start_time = time.time()

    install_settings()
    install_storages()
    install_channels()
    install_services()
    install_actions()
    install_folders()
    install_meta_types()
    install_cs()
    install_views()

    logging.goodnews("Nebula settings migration completed in {:03f} seconds".format(time.time() - start_time))
