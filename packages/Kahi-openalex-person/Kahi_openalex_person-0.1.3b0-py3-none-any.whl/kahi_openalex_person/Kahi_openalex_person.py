from kahi.KahiBase import KahiBase
from pymongo import MongoClient, TEXT
from time import time
from joblib import Parallel, delayed
from kahi_impactu_utils.Utils import get_id_from_url


def process_one(oa_author, client, db_name, empty_person, max_tries=10):
    db = client[db_name]
    collection = db["person"]

    author = None
    for source, idx in oa_author["ids"].items():
        if source != "openalex":
            idx = get_id_from_url(idx)
        author = collection.find_one({"external_ids.id": idx})
    if author:
        already_updated = False
        for upd in author["updated"]:
            if upd["source"] == "openalex":
                already_updated = True
                break
        if already_updated:
            return None
        ext_sources = [ext["source"] for ext in author["external_ids"]]
        for key, val in oa_author["ids"].items():
            if key not in ext_sources:
                if key != "openalex":
                    val = get_id_from_url(val)
                if val:
                    rec = {"provenance": "openalex", "source": key, "id": val}
                    if rec not in author["external_ids"]:
                        author["external_ids"].append(rec)
        author["updated"].append({"source": "openalex", "time": int(time())})
        collection.update_one({"_id": author["_id"]}, {"$set": {
            "updated": author["updated"],
            "external_ids": author["external_ids"]
        }})
    else:
        entry = empty_person.copy()
        entry["updated"].append({"source": "openalex", "time": int(time())})

        entry["full_name"] = oa_author["display_name"]

        for name in oa_author["display_name_alternatives"]:
            if not name.lower() in entry["aliases"]:
                entry["aliases"].append(name.lower())
        for source, idx in oa_author["ids"].items():
            if source != "openalex":
                idx = get_id_from_url(idx)
            if idx:
                entry["external_ids"].append(
                    {"provenance": "openalex", "source": source, "id": idx})

        if "last_known_institution" in oa_author.keys():
            if oa_author["last_known_institution"]:
                aff_reg = None
                for source, idx in oa_author["last_known_institution"].items():
                    aff_reg = db["affiliations"].find_one(
                        {"external_ids.id": idx})
                    if aff_reg:
                        break
                if aff_reg:
                    name = aff_reg["names"][0]["name"]
                    for n in aff_reg["names"]:
                        if n["lang"] == "es":
                            name = n["name"]
                            break
                        elif n["lang"] == "en":
                            name = n["name"]
                    entry["affiliations"].append({
                        "id": aff_reg["_id"],
                        "name": name,
                        "types": aff_reg["types"],
                        "start_date": -1,
                        "end_date": -1
                    })

        collection.insert_one(entry)


class Kahi_openalex_person(KahiBase):

    config = {}

    def __init__(self, config):
        self.config = config

        self.mongodb_url = config["database_url"]

        self.client = MongoClient(self.mongodb_url)

        self.db = self.client[config["database_name"]]
        self.collection = self.db["person"]

        self.collection.create_index("external_ids.id")
        self.collection.create_index("affiliations.id")
        self.collection.create_index([("full_name", TEXT)])

        self.openalex_client = MongoClient(
            config["openalex_person"]["database_url"])
        if config["openalex_person"]["database_name"] not in self.openalex_client.list_database_names():
            raise Exception("Database {} not found in {}".format(
                config["openalex_person"]['database_name'], config["openalex_person"]["database_url"]))
        self.openalex_db = self.openalex_client[config["openalex_person"]
                                                ["database_name"]]
        if config["openalex_person"]["collection_name"] not in self.openalex_db.list_collection_names():
            raise Exception("Collection {}.{} not found in {}".format(config["openalex_person"]['database_name'],
                                                                      config["openalex_person"]['collection_name'], config["openalex_person"]["database_url"]))
        self.openalex_collection = self.openalex_db[config["openalex_person"]
                                                    ["collection_name"]]

        self.n_jobs = config["openalex_person"]["num_jobs"] if "num_jobs" in config["openalex_person"].keys(
        ) else 1
        self.verbose = config["openalex_person"]["verbose"] if "verbose" in config["openalex_person"].keys(
        ) else 0

        self.client.close()

    def process_openalex(self):
        author_cursor = self.openalex_collection.find(no_cursor_timeout=True)
        client = MongoClient(self.mongodb_url)
        Parallel(
            n_jobs=self.n_jobs,
            verbose=self.verbose,
            backend="threading")(
            delayed(process_one)(
                author,
                client,
                self.config["database_name"],
                self.empty_person()
            ) for author in author_cursor
        )
        client.close()

    def run(self):
        self.process_openalex()
        return 0
