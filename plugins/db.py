import sqlite3
import json

#con = sqlite3.connect(".././data/menus.sdb")

q = "{\"file\":\".././data/menus.sdb\",\"sql\":\"select * from menus\"}"
u = "{\"file\":\".././data/menus.sdb\",\"sql\":\"INSERT INTO menus VALUES (16,22, ,0,6)\"}"

def dict_factory(cursor, row):  
    d = {}  
    for idx, col in enumerate(cursor.description):  
        d[col[0]] = row[idx]  
    return d

def query(param):
    j = json.loads(param)
    con = sqlite3.connect(j["file"])
    con.row_factory = dict_factory
    cu=con.cursor()
    cu.execute(j["sql"])
    rows= cu.fetchall()
    #for row in rows:  
    #    print row
    cu.close()
    con.close()
    return json.dumps(rows)
def execute(param):
    j = json.loads(param)
    con = sqlite3.connect(j["file"])
    con.row_factory = dict_factory
    cu=con.cursor()
    cu.execute(j["sql"])
    con.commit()
    rows= cu.fetchall()
    #for row in rows:  
    #    print row
    cu.close()
    con.close()
    return json.dumps(rows)
    
    
    
