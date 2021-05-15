import csv, os, time
import numpy as np
import pandas as pd
import pandasql as ps
import time

filename = os.path.realpath("../comparative_syntax_analogies.csv")

df = pd.read_csv(filename)

query = """
select *
from (select distinct 
    t1.a, t1.b, t2.a as c, t2.b as d, t2.category, "comparative|to-comp" as subcategory
from
    df t1
inner join df t2
    on t1.a != t2.a)
union
select *
from (select distinct
    t1.b as a, t1.a as b, t2.b as c, t2.a as d, t2.category, "comparative|from-comp" as subcategory
from
    df t1
inner join df t2
    on t1.b != t2.b)

"""
print("running query")

t1 = time.perf_counter()
result_df = ps.sqldf(query)
t2 = time.perf_counter()

result_df.to_csv("../processed_comparative_pairs.csv", index=False)