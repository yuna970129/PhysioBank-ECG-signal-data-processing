import wfdb 
import pandas as pd
import numpy as np
import glob

dat_files=glob.glob('*.dat') 
df=pd.DataFrame(data=dat_files)
df.to_csv("files_list.csv",index=False,header=None) 
files=pd.read_csv("files_list.csv",header=None)
​
for i in range(0,len(files)):
    recordname=str(files.iloc[[i]])
    print(recordname[:-4])
    recordname_new=recordname[-7:-4] 
    record = wfdb.rdsamp(recordname_new) 
    record=np.asarray(record[0])
    path=recordname_new+".csv"
    np.savetxt(path,record,delimiter=",") #
    
    csv = pd.read_csv(recordname_new + ".csv", header=None)
#    csv=csv.apply(lambda x : 200*x + 1024)
    
#    csv=csv.astype(int)
    csv.to_csv('C:/Users/CSD/Desktop/CPR_project/mitdb_mV/'+recordname_new+'.csv', index = True, header=True)
    
#    f = open('C:/Users/Nayu/Desktop/mitdb/'+recordname_new+'annotations.txt', "w")
#    f.close()
    
    print("Files done: %s/%s"% (i,len(files)))
​
print("\nAll files done!")