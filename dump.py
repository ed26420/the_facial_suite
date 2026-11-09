from django.test import Client
from django.db import connection, reset_queries

reset_queries()
client = Client()
client.get('/')

with open('queries.txt', 'w') as f:
    for i, q in enumerate(connection.queries, 1):
        f.write(f"--- QUERY {i} ---\n{q['sql']}\n\n")

print(f"Successfully logged {len(connection.queries)} queries to queries.txt!")