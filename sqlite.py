import sqlite3
import math
import time
from tools import deserialization, serialization, addTransparency, cut_by_ratio

colorStorage = deserialization('color-mapping.pkl')
print('缓存存在:{}个图片'.format(len(colorStorage)))

conn = sqlite3.connect('example.db')


def sqrt(t):
    return math.sqrt(t)


c = conn.cursor()
conn.create_function("sqrt", 1, sqrt)
def square(i):
    return i**2
conn.create_function("square", 1, square)

# Create table 
# c.execute(
    # '''CREATE TABLE images (r INTEGER, g INTEGER, b INTEGER, path text, size text)''')


# for piece in colorStorage:  # 生成颜色匹配值列表
#     c.execute("INSERT INTO images VALUES ({0},{1},{2},'{3}',{4})"
#               .format(piece['color'][0],
#                       piece['color'][1],
#                       piece['color'][2],
#                       piece['path'],
#                       'null'))

# Save (commit) the changes
conn.commit()

for row in c.execute('SELECT count(r) FROM images'):
    print(row)


for row in c.execute("select sqrt(33.66), square(8)"):
    print(row)


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
