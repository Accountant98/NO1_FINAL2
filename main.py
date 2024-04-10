from cadic_test import create_cadics_new
from create_cadics import create_cadics_old

df1 = create_cadics_new(case="CASE1", market="JPN", powertrain="EV", car="WZ1J", list_group=["ALL"])
df2 = create_cadics_old(case="CASE1", market="JPN", powertrain="EV", car="WZ1J", list_group=["ALL"])
print(df1)
print(df2)
df1.to_excel("cadic_new.xlsx",index=None, header=None)
df2.to_excel("cadic_old.xlsx",index=None, header=None)
if df1.equals(df2):
    print("DataFrame df1 và df2 giống nhau.")
else:
    print("DataFrame df1 và df2 không giống nhau.")
print("******************************************")