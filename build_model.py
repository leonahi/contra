import sqlite3 as lite
import numpy
import Pycluster as cluster
from get_clusterid import *

import matplotlib.pyplot as plt 

def build_model(dbName):
  """ """
  clusterIdtoSPND = get_clusterid(v_co_dbName = dbName)
  #print(clusterIdtoSPND)
  
  con = lite.connect(dbName)
  
  with con:
    cur = con.cursor()

    for clusterNo in clusterIdtoSPND:
      column = ", ".join(clusterIdtoSPND[clusterNo])
      cur.execute("SELECT {0} FROM sensor".format(column))
      data = cur.fetchall()
      #data_c = meanc(numpy.matrix(data)) #-----------All points
      data_c = meanc(numpy.matrix(data[0:6999])) #-----------First 7000 points
      #covMatrix = numpy.cov(data_c,rowvar=0)

      print("cluster No. {} : {}".format(clusterNo, column))
      
#---------------------------------------Calculate SVD--------------------------------------------------      
      U, S, V = numpy.linalg.svd(numpy.transpose(data_c))
      #columnmean, coordinates, components, eigenvalues = cluster.pca(numpy.transpose(data_c))
      #S, U = numpy.linalg.eigh(covMatrix)      
      #print(eigenvalues)
      #print(numpy.around(components,3))
      #print(numpy.around(U, 4))
      print(U) 
      print(S)
      plot_eigen(S, clusterNo, column)
#------------------------------------------------------------------------------------------------------


#--------------------------------------Calculate Residual----------------------------------------------
      #res = calc_residual(U, data_c)      
      #plot_residual(res, clusterNo, column)
      #print(res.shape)
      #res_covMat = numpy.cov(res, rowvar=0)
      #res_inv = numpy.linalg.inv(res_covMat)
      #print(numpy.round(res_inv,4))
#------------------------------------------------------------------------------------------------------      
      
      
      



  
def calc_residual(U, data_c):    # Calculate Residual
  A = U[:,1:]
  return numpy.dot(data_c, A)


def meanc(data):
  return (data - numpy.mean(data, axis=0))      # Converting data to zero mean


def plot_eigen(S, clusterNo, column):      # Plot Eigen Values
  plt.title("Cluster: {} , Column: {}".format(clusterNo, column))
  plt.plot(S, marker='o', linestyle='--', color='r', label='Square')
  plt.ylabel("Eigen Value")
  plt.show()

def plot_residual(res, clusterNo, column):     # Plot Residual
  color = ('#FFFF00', '#FF0000', '#FF00FF', '#0000FF', '#0B0B3B', '#FAAC58', '#0B3B39', '#2E64FE')
  for col in range(0,5):
    plt.plot(res[:,col], color=color[col])
  plt.ylim([-5,5])
  plt.title("Cluster_{} : {}".format(clusterNo, column))
  #plt.legend(loc='best')
  plt.show()



if __name__ == "__main__":
  build_model("SPND_Database/Cobalt/10SPND1-42.db")
  #SPND_Database/Vanadium/10F29-130.db
  #SPND_Database/Cobalt/10SPND1-42.db

   
    #clusters = ["Cluster_{}".format(item) for item in list(clusterIdtoSPND.keys())]
    #clusterList = " BLOB, ".join(clusters)
    #clusterList += " BLOB"
    #clusters = ", ".join(clusters)
    #ques = ", ".join(['?']*len(clusters))
    #print(clusters)
    #print(clusterList)
    #cur_models.execute("CREATE TABLE IF NOT EXISTS models(Id INTEGER PRIMARY KEY, Timestamp DATETIME CURRENT_TIMESTAMP, {})".format(clusterList))

  
  
    #column = ", ".join(clusterIdtoSPND[0])
    #cur.execute("SELECT {0} FROM sensor".format(column))
    #data = cur.fetchall()
    #data_c = meanc(numpy.array(data))
    #covMatrix = numpy.cov(data_c,rowvar=0)
    #U, S, V = numpy.linalg.svd(covMatrix)
    #print(numpy.around(U, 6))
    #print(S)

    
    #columnmean, coordinates, components, eigenvalues = cluster.pca(data) 
    #covMatrix = numpy.corrcoef(data_c,rowvar=0)
    
    #print(eigenvalues)
    #print(components)
    #print(columnmean)
    
    #print(U)
    #print(V)
    
    #data_c.dump(open('arr_dump.npy', 'wb'))
    
  
    #cur_models.execute("INSERT INTO models(Timestamp, {0}) VALUES (DateTime('now'), {1})".format(clusters, ques), tuple(models))
    #print(models)  
  