import sqlite3
from pypika import Query, Table

db_path = "auctions.db"

con = sqlite3.connect(db_path, isolation_level=None)

cur = con.cursor()

try:
    cur.execute(
        """CREATE TABLE auctions(
            _id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT,
            image_url TEXT,
            close_date TEXT,
            current_bid REAL,
            unit_size TEXT,
            unit_content TEXT
        )"""
    )
except:
    print("ERROR: auction table maybe exist")
    pass


def insert_data(auction):
    cur.execute(
        "INSERT INTO auctions VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
        (
            auction["_id"],
            auction["name"],
            auction["location"],
            ','.join(map(str, auction["image_url"])),
            auction["close_date"],
            auction["current_bid"],
            auction["unit_size"],
            auction["unit_content"],
        ),
    )
    

def update_data(auction):
    cur.execute(
"""
UPDATE auctions
SET name = ?,
    location = ?,
    image_url = ?,
    close_date = ?,
    current_bid = ?,
    unit_size = ?,
    unit_content = ?
WHERE
    _id = ?
""",
        (
            auction["name"],
            auction["location"],
            ','.join(map(str, auction["image_url"])),
            auction["close_date"],
            auction["current_bid"],
            auction["unit_size"],
            auction["unit_content"],
            auction["_id"],
        ),
    )

def count_table():
    res = cur.execute(
"""
SELECT COUNT(*)
FROM auctions
"""
    )
    return res.fetchone()[0]

def get_specific_auction(auction):
    auctions = Table("auctions")
    q = str(Query.from_("auctions").select(auctions._id).where(auctions._id == auction["_id"]))
    res = cur.execute(q)
    return res.fetchone()