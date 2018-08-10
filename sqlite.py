import sqlite3
import math
import time
from tools import deserialization, serialization, addTransparency, cut_by_ratio
from db import createDB

colorStorage = deserialization('color-mapping.pkl')
print('缓存存在:{}个图片'.format(len(colorStorage)))

(conn,c) = createDB()

for row in c.execute('SELECT count(r) FROM images'):
    print(row)


for row in c.execute("select sqrt(33.66), square(8)"):
    print(row)


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
