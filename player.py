import requests
import queue
from bs4 import BeautifulSoup
import sqlite3

q=queue.Queue()
conn=sqlite3.connect('player.sqlite')
cur=conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Player;

CREATE TABLE IF NOT EXISTS Player (
	id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	player	TEXT NOT NULL ,
	position TEXT,
	GP	REAL,
	GS	REAL,
	MIN	REAL,
	PPG	REAL,
	OFFR	REAL,
	DEFR	REAL,
	RPG	REAL,
	APG	REAL,
	SPG	REAL,
	BPG	REAL,
	TPG	REAL,
	FPG	REAL,
	ATO	REAL,
	PER	REAL
)
''')

url='http://www.espn.com/nba/team/stats/_/name/bos'
ropen=requests.get(url)
soup=BeautifulSoup(ropen.content)
tag=soup('option')
team=set()
count=0
for i in tag:
    value=i.get('value')
    if count==30:
        break
    if(len(value)>0):
        q.put(value);
        #print(value)
    count+=1;

while q.empty() is False:
    url=q.get()
    print(url)
    ropen=requests.get('http:'+url)
    soup = BeautifulSoup(ropen.content)
    rows=soup.find('table',{"class":'tablehead'})
    for row in rows.find_all('tr'):
        result=list()
        result.append([data.text for data in row.find_all('td')])
        for a in result:
            if(a[0]=='GAME STATISTICS' or a[0]=='PLAYER' or a[0]=='Totals'):
                print('Not do this line.')
                continue
            if(len(a)==14):
                a.append('0')
            print('Do this line')
            player1=a[0].split(',')
            name=player1[0]
            print(name)
            posi=player1[1].strip()
            print(posi)
                #cur.execute('''INSERT INTO Player(player,position)
                #VALUES(?,?)''',(name,posi))
                #print('success name')
            cur.execute('''
            INSERT  INTO Player(player,position,GP,GS,MIN,PPG,OFFR,DEFR,RPG,APG,SPG,BPG,TPG,FPG,ATO,PER)                
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(name,posi,a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12],a[13],a[14]))
            print('success data')
    conn.commit()




