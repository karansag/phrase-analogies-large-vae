import csv, os, time
import numpy as np
import pandas as pd
import pandasql as ps
import time

filename = os.path.realpath("../comparative_sent_pairs.csv")

df = pd.read_csv(filename)

query = """
select distinct 
    t1.a, t1.b, t2.a as c, t2.b as d
from
    df t1
inner join df t2
    on t1.a != t2.a;
"""
print("running query")

t1 = time.perf_counter()
result_df = ps.sqldf(query)
t2 = time.perf_counter()

result_df.to_csv("../processed_comparative_pairs.csv", index=False)