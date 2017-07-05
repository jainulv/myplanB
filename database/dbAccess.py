import couchdb
import json
# ask admin for username and password
couch = couchdb.Server("http://username:password@localhost:5984")
db = couch['course_catlog']

with open("courses.json", "r") as jsonfile:
    db_entry = json.load(jsonfile)
    db.save(db_entry)
