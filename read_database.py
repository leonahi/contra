import sqlite3 as lite
from Pycluster import *
from numpy import *

def read_database(databaseName):
  ''' Read databaseName and return data array in the format as required by Pycluster module'''
  
  con = lite.connect(databaseName)
  con.row_factory = lite.Row
  
  con_new = lite.connect(databaseName)
  
  with con, con_new:
    cur = con.cursor()
    cur_new = con_new.cursor()
    
    cur.execute("SELECT * FROM sensor")
    
    columnNames = cur.fetchone()
    columnNames = columnNames.keys()
    
    cur_new.execute("SELECT * FROM sensor")
    rows = cur_new.fetchall()
    
    ROW = [row[3:] for row in rows]
    
    Data = matrix(ROW)
    
    rc = Data.shape
    mask = ones((rc[0], rc[1]))    
    mask = matrix(mask)
    
    counter = 0
    for i in range(Data.shape[0]):
      for j in range(Data.shape[1]):
        if Data[i,j] < 0:
          counter += 1
          #print(Data[i,j])
          mask[i,j] = 0
    
    counter += 40;
    print("Total number of missing data points : {}".format(counter))
    print("Total number of missing observation : {}".format( int(counter/rc[1])))
    print("Total number of observation : {}".format(rc[0]))
    missingObservation = int(counter/rc[1])
    print("Percentage of missing observation : {}".format((missingObservation*100)/rc[0]))
    
    #mask = mask.transpose()
    
    '''    
    clusterid, error, nfound = kcluster(data=Data, nclusters=7, 
                                        mask=mask, weight=None,
                                        transpose=1, npass=1,
                                        method='a', dist='c', initialid=None)
                                        
    print(clusterid)
    print(nfound)
    print(error)
    
    #SPNDtoClusterId = {col:cid for col, cid in zip(columnNames[3:], clusterid)}
    
    clusterIdtoSPND = {}
    lst = []
    for cid in clusterid:
      clusterIdtoSPND[cid] = lst

    for cid, col in zip(clusterid, columnNames[3:]):
      clusterIdtoSPND[cid].append(col)
    
    #clusterIdtoSPND = { for col, cid in zip(columnNames[3:], clusterid)}
    
    
    #SPNDtoClusterId = {print("{} : {}".format(col,cid)) for col, cid in zip(columnNames[3:], clusterid)}
    #print(clusterid.shape)    
    
    #print(zeros(9).reshape(3,3))
    
    #print(columnNames)
    #print(Data[0,0])
    #print(Data.shape)
    #print(mask)
    '''
if __name__ == '__main__':
  read_database("SPND_Database/F29-130_SPND1-42.db")