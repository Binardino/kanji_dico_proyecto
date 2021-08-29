#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


#fetch Kanji Kangxi dictionary id_number (colonnne "No.")
df_radicals = pd.read_html('https://en.wikipedia.org/wiki/List_of_kanji_radicals_by_stroke_count')[0]

df_radicals


# In[3]:


#in this df_radicals, Meaning & Reading are concatenated into the same column "Meaning and reading"
#fetch other Kanji list, which lacks of need "No." column, but has tidy differentiated "meaning" & "reading" columns
# -> dfs to be merged
df_meaning_tidy = pd.read_html('https://en.wikipedia.org/wiki/List_of_kanji_radicals_by_frequency')[2]

df_meaning_tidy


# In[4]:


df_merged = df_radicals.merge(df_meaning_tidy,
                             how='left',
                             left_on="Radical (variants)",
                             right_on="Radical")

df_merged


# In[5]:


#merged 109 rows - remain 105 rows where merged failed - unmatched join key 
#- "Radical (variants)" has many concatenated radicals between parenthesis - to be wrangled
df_merged.loc[df_merged["Radical"].isnull()]


# In[6]:


df_meaning_tidy['Radical'].tail(50)


# In[7]:


df_meaning_tidy['Radical'] = df_meaning_tidy['Radical'].str.replace(' ', ',')

df_meaning_tidy['Radical_split'] = df_meaning_tidy['Radical'].str.split(",")


#df_meaning_tidy['Radical_split'] = df_meaning_tidy['Radical_split'].apply(lambda x : list(x))
#df_meaning_tidy['Radical_split'] = df_meaning_tidy['Radical_split'].

df_meaning_tidy.info()


# In[17]:


df_meaning_tidy.isnull().sum()


# In[8]:


df_meaning_tidy['Radical_split'].head(50)


# In[27]:


#spliting nested kanji tp keep only 1st kanji on each row
df_meaning_tidy['Radical'] = df_meaning_tidy['Radical'].str.replace(' ', ',')

df_meaning_tidy['Radical_split'] = df_meaning_tidy['Radical'].str.split(",").apply(lambda x : x[0])

df_meaning_tidy['Radical_split']


# In[31]:


df_radicals['Radical (variants)'] = df_radicals['Radical (variants)'].str.replace(' ', ',')

df_radicals['Radical (variants)_split'] = df_radicals['Radical (variants)'].str.split(",").apply(lambda x : x[0])

df_radicals['Radical (variants)_split']


# In[32]:


df_radicals['Radical (variants)_split'].tail(50)


# In[38]:


df_diff = df_radicals.loc[~(df_radicals["Radical (variants)_split"].isin(df_meaning_tidy["Radical_split"]))]
df_diff


# In[43]:


df_diff2 = df_meaning_tidy.loc[~(df_meaning_tidy["Radical_split"].isin(df_radicals["Radical (variants)_split"]))]
df_diff2


# In[44]:


df_diff2.shape


# In[ ]:


#there are differences of complicated symbols between 2 dfs i.e. difference between classical Chinese & Japanese Kanji

#need to fetch other Kanji radical df


# In[35]:


df_diff = df_radicals.merge(df_meaning_tidy,
                 how='outer',
                 left_on="Radical (variants)_split",
                 right_on="Radical_split")
df_diff


# In[ ]:





# In[33]:


df_meaning_tidy['Radical_split'].tail(50)


# In[9]:


df_radicals.columns

df_radicals['Radical (variants)'].fillna('', inplace=True)

df_radicals['Radical (variants)_split'] = df_radicals['Radical (variants)'].str.split(",", expand=True)


#df_meaning_tidy['Radical_split'] = df_meaning_tidy['Radical_split'].apply(lambda x : list(x))
#df_meaning_tidy['Radical_split'] = df_meaning_tidy['Radical_split'].

df_radicals.info()


# In[ ]:


#list of not official not recognized by Kangxi
df_unofficial = pd.read_html('https://en.wikipedia.org/wiki/List_of_kanji_radicals_by_stroke_count')[1]

df_unofficial

