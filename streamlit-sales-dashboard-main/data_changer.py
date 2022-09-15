from dataclasses import replace
import pandas as pd

PLACES=['Thrissur','Ernamkulam','Kozhikode','Trivandrum','Triprayar','Kannur','Chennai','Mumbai','Banglore','Delhi']

df=pd.read_excel('D:\prgrming\git\DS_project\supermarkt_sales.xlsx',skiprows=3)
i=0
list=[]
for i in range(1000):
    list.append(PLACES[i%10])
# print(df.tail)

df['City']=list
# for place in df['City']:
#     place=PLACES[i%10]
#     df.
    # print(place)
    # df.replace(df['City'].place,PLACES[i%10])
    # i+=1

# for place in df['City']:
#     print(place)

print("success")

df.to_excel('sales.xlsx',sheet_name='Sales')
