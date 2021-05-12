import csv, os, time
import numpy as np
import pandas as pd
import pandasql as ps
import time

filename = os.path.realpath("../plural_sent_pairs.csv")

df = pd.read_csv(filename)

query = """
select * 
from (select distinct 
    t1.b as a, t1.a as b, t2.b as c, t2.a as d, t1.category, 'plural|from-single' as subcategory
from
    df t1
inner join df t2
    on t1.b != t2.b
    and t1.category == t2.category
limit 3000000)
union
select *
from (select distinct
    t1.a, t1.b, t2.a as c, t2.b as d, t1.category, 'plural|to-' || t1.subcategory as subcategory
from
    df t1
inner join df t2
    on t1.a != t2.a
    and t1.category == t2.category
    and t1.subcategory == t2.subcategory
limit 3000000);
"""
print("running query")

t1 = time.perf_counter()
result_df = ps.sqldf(query)
t2 = time.perf_counter()

result_df.to_csv("../processed_plural_to_singular_pairs.csv", index=False)