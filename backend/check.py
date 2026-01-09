import sqlite3, json

conn = sqlite3.connect(
    r"C:/Users/hp/AIBookDiscoveryProject/instance/users.db"
)
cursor = conn.cursor()

cursor.execute("SELECT email, search_history FROM user")
for email, history in cursor.fetchall():
    print(email, json.loads(history))

conn.close()