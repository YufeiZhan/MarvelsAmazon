import pandas as pd
import numpy as np

if __name__=="__main__":
    order = pd.read_csv("Orders.csv",header=None)
    orderitems = pd.read_csv("OrderItems.csv",header=None)
    # print(order.iloc[0,0])
    oid = order.iloc[:,0]
    oid_in_oi = orderitems.iloc[:, 1].unique()
    keep = np.intersect1d(oid_in_oi, oid)
    print(len(keep))
    order = order[order[0].isin(keep)]
    order.to_csv("Orders.csv",index=False,header=False)