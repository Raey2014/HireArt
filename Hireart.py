# coding: utf-8
#! /usr/bin/env python
#python modules required
from __future__ import division
import pandas as pd
import sys
input_file = sys.argv[1] # input data
#input_out = sys.argv[2] # input data
df=pd.read_excel(input_file,index_col='Date of Contact')
df['Client Name'] = df['Client Name'].str.replace(' and ',', ')
df['number of contacts']=df["Client Name"].map(lambda x: len(str(x).split(',')))
df.index = df.index.to_period('M')

A = df.groupby(df.index)['number of contacts'].sum()
df1=pd.DataFrame(columns=['month','percentage of the highest month'],index=range(len(A.index.year.unique())))
for j in range(len(A.index.year.unique())):
	i=A.index.year.unique()[j]
	B=(A.loc[A.index.year==i]/A.loc[A.index.year==i].sum())*100.0
	df1.ix[j,'month']=B[B==B.max()].index[0]
	df1.ix[j,'percentage of the highest month']=B[B==B.max()][0]
B=df.groupby([df.index,df['Account manager']]).agg({"number of contacts" : "sum"})
B=B.reset_index()
B.rename(columns={'Date of Contact': 'month'}, inplace=True)
C = pd.merge(B,df1,how='inner',on='month')
C['percentage of the highest month']=C['percentage of the highest month'].astype(float).round(2)
C.to_csv('Account_manger_maximum_contacts.txt',sep=b'\t',index=None)


     