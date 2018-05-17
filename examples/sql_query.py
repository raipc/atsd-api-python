from atsd_client import connect_url
from atsd_client.services import SQLService

conn = connect_url('https://atsd_hostname:8443', 'user', 'passwd')

# Single-line SQL query
# query = 'SELECT datetime, time, entity, value FROM jvm_memory_free LIMIT 3';

# Multi-line SQL query, use triple quotes (single or double)
query = """
SELECT datetime, time, entity, value
  FROM "jvm_memory_free"
ORDER BY datetime DESC
  LIMIT 3
"""

svc = SQLService(conn)
df = svc.query(query)

print(df)