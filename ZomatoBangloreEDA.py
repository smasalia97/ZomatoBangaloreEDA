# %%
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

# %%
df = pd.read_csv(r'C:\Users\HP\Downloads\zomato.csv\zomato.csv')

# %%
df.head()

# %%
df.shape

# %%
df.columns

# %%
df.drop(['url', 'address','phone','menu_item','dish_liked','reviews_list'], axis=1, inplace=True)

# %%
df

# %%
df.info()

# %%
df.drop_duplicates(inplace = True)
df.shape

# %%
df['rate'].unique() 

# %%
def handlerate(value):
    if(value == 'NEW' or value == '-'):
        return np.nan
    else:
        value = str(value).split('/')
        value = value[0]
        return float(value)
    
df['rate'] = df['rate'].apply(handlerate)

# %%
df['rate'].head()

# %%
df.rate.isnull().sum()

# %%
df['rate'].fillna(df['rate'].mean(), inplace=True)

# %%
df.rate.isnull().sum()

# %%
df.dropna(inplace = True)

# %%
df.head()

# %%
df.rename(columns = {'approx_cost(for two people)' : 'Cost2plates', 'listed_in(type)' : 'Type'}, inplace = True)

# %%
df.head()

# %%
df.location.unique()

# %%
df['listed_in(city)'].unique()

# %%
df.drop(['listed_in(city)'], axis=1, inplace=True)

# %%
df.head()

# %%
df.Cost2plates.unique()

# %%
def handlecomma(value):
    value = str(value)
    if ',' in value:
        value = value.replace(',','')
        return float(value)
    else:
        return float(value)

df['Cost2plates'] = df['Cost2plates'].apply(handlecomma)
df.Cost2plates.unique()

# %%
df['Cost2plates'].head()

# %%
df['rest_type'].value_counts()

# %%
rest_types = df['rest_type'].value_counts(ascending = False)

# %%
rest_types

# %%
rest_type_lessthan1000 = rest_types[rest_types < 1000]

# %%
rest_type_lessthan1000

# %%
def handleresttype(value):
    if(value in rest_type_lessthan1000):
        return 'others'
    else:
        return value

df['rest_type'] = df['rest_type'].apply(handleresttype)
df.rest_type.value_counts()

# %%
df['location'].value_counts()

# %%
location = df['location'].value_counts(ascending = False)
location_lessthan300 = location[location < 300]

def handlelocation(value):
    if(value in location_lessthan300):
        return 'others'
    else:
        return value
    
df['location'] = df['location'].apply(handlelocation)
df['location'].value_counts()

# %%
df.cuisines.unique()

# %%
cuisines = df['cuisines'].value_counts(ascending = False)
cuisines_lessthan100 = cuisines[cuisines < 100]

def handlecuisines(value):
    if(value in cuisines_lessthan100):
        return 'others'
    else:
        return value
    
df['cuisines'] = df['cuisines'].apply(handlecuisines)
df['cuisines'].value_counts()

# %%
plt.figure(figsize = (16,10))
ax = sns.countplot(df['location'])
plt.xticks(rotation=90)
plt.show(); 

# %%
plt.figure(figsize=(6,6))
sns.countplot(df['book_table'], palette = 'rainbow')

# %%
plt.figure(figsize=(6,6))
sns.countplot(df['online_order'], palette = 'inferno')

# %%
plt.figure(figsize=(6,6))
sns.boxplot(x = 'online_order', y='rate', data=df)

# %%
plt.figure(figsize=(6,6))
sns.boxplot(x = 'book_table', y='rate', data=df)

# %%
df1 = df.groupby(['location', 'online_order'])['name'].count()
df1.to_csv('location_online.csv')

df1 = pd.read_csv('location_online.csv')
df1 = pd.pivot_table(df1, values=None, index=['location'], columns=['online_order'], fill_value=0, aggfunc=np.sum)
df1

# %%
df1.plot(kind='bar', figsize=(15,8))

# %%
df2 = df.groupby(['location', 'book_table'])['name'].count()
df2.to_csv('location_booktable.csv')

df2 = pd.read_csv('location_booktable.csv')
df2 = pd.pivot_table(df2, values=None, index=['location'], columns=['book_table'], fill_value=0, aggfunc=np.sum)
df2

# %%
df2.plot(kind='bar', figsize=(15,8))

# %%
plt.figure(figsize=(14,8))
sns.boxplot(x = 'Type', y='rate', data=df, palette = 'inferno')

# %%
df3 = df.groupby(['location', 'Type'])['name'].count()
df3.to_csv('location_Type.csv')

df3 = pd.read_csv('location_Type.csv')
df3 = pd.pivot_table(df3, values=None, index=['location'], columns=['Type'], fill_value=0, aggfunc=np.sum)
df3

# %%
df3.plot(kind='bar', figsize=(36,16))

# %%
df4 = df[['location','votes']]
df4.drop_duplicates()
df5 = df4.groupby(['location'])['votes'].sum()
df5 = df5.to_frame()
df5 = df5.sort_values('votes', ascending=False)
df5.head()

# %%
plt.figure(figsize=(15,8))
sns.barplot(df5.index, df5['votes'])
plt.xticks(rotation=90)

# %%
df6 = df[['cuisines','votes']]
df6.drop_duplicates()
df7 = df6.groupby(['cuisines'])['votes'].sum()
df7 = df7.to_frame()
df7 = df7.sort_values('votes', ascending=False)
df7.head()

# %%
df7 = df7.iloc[1:, :]
df7

# %%
plt.figure(figsize=(15,8))
sns.barplot(df7.index, df7['votes'])
plt.xticks(rotation=90)

# %%
