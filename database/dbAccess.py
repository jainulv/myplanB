import couchdb
import json

couch = couchdb.Server("http://admin:NRbzj75z@localhost:5984")
db = couch['course_catlog']

with open("courses.json", "r") as jsonfile:
    db_entry = json.load(jsonfile)
    db.save(db_entry)
