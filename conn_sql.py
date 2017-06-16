#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymssql

conn =pymssql.connect(host='172.16.89.171',user='multiverse',password='multiverse',database='multiverse')
'''
如果和本机数据库交互，只需修改链接字符串
conn=pymssql.connect(host='.',database='Michael')
'''
cur = conn.cursor()
#cur = conn.cursor(as_dict=True)
if not cur:  
    raise Exception('连接数据库失败')
sSQL = 'select top 5 LocalAssetUID,Name from [dbo].[Asset]'
cur.execute(sSQL)

#-----------------fetchall()----------------------
result = cur.fetchall()

#如果update/delete/insert记得要conn.commit()
#否则数据库事务无法提交

#1.result是list，而其中的每个元素是 tuple  
print type(result),type(result[0])

#2. cur.rowcount 返回最后操作影响的行数 
print '\n\n总行数：'+ str(cur.rowcount)

#3.通过enumerate返回行号
for i,(LocalAssetUID,name) in  enumerate(result):
    print '第 '+str(i+1)+'行>>'+ name
#-----------cur = conn.cursor(as_dict=True)-----------------------------
#for row in  enumerate(result):
#    print '第 '+str(row[0]+1)+'行>>'+ row[1]['Name']
    
print cur.rownumber
#-----------------fetchone()--------------------    
#4.一次取一条数据,cur.rowcount为-1  
r = cur.fetchone()

print('\n')

while r:

    LocalAssetUID,name =r #r是一个元祖  
    print LocalAssetUID+' 的节目名称:'+ name
    r=cur.fetchone()
#-------------------------------------------    
    
cur.close()
conn.close()