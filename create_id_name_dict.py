import urllib2
import json
import psycopg2

# Get item-name dictionary
r = urllib2.urlopen("https://dl.dropboxusercontent.com/u/75481541/gw2/item_names.json")

# Save as dictionary
data = json.load(r)

# Change to tuples

data_tuple = data.items()

if __name__ == '__main__':
	print len(data_tuple)


# Insert into db

conn = psycopg2.connect("dbname=gw2_db user=postgres")

cur = conn.cursor()

cur.execute("CREATE TABLE id_names (id serial PRIMARY KEY, item_id integer, item_name varchar);")

query = "INSERT INTO id_names (item_id, item_name) VALUES (%s, %s)"

cur.executemany(query, data_tuple)

cur.execute("CREATE INDEX id_names_id1 on id_names (item_name) WITH (fillfactor = 100);")

# Commit and close

conn.commit()

cur.close()

conn.close()






