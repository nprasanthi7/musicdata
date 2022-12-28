from db_connection import DB_connection
import pandas as pd
import string
from fuzzywuzzy import fuzz
cnxn,cursor = DB_connection().get_connection()

query="SELECT * FROM [dbo].[GetDataMappingInfoByArtist] WHERE ArtistSlug='HJONES'"
cursor.execute(query)
db_table = cursor.fetchall()
table_rows=[]
for row in db_table:
    table_rows.append(list(row))
df=pd.DataFrame(table_rows,columns=['Type','ArtistSlug','Keyword','Description','Source'])
df['Keyword_cleaned']=df['Keyword'].apply(lambda x: ''.join([char for char in x if char not in string.punctuation ]))
df['Description_cleaned']=df['Description'].apply(lambda x: ''.join([char for char in x if char not in string.punctuation ]))
for index in range(len(df)):
    fuzz_similarity=fuzz.ratio(df['Keyword_cleaned'][index].lower(),df['Description_cleaned'][index].lower())
    df.loc[index,'Score']=fuzz_similarity
df=df.drop(['Keyword_cleaned','Description_cleaned'],axis=1)
df.to_csv('similar_artist.csv',index=None)