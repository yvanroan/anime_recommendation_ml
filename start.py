import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer


# from sqlalchemy import create_engine

def preprocess(animes):# we'll add profile and reviews later and add more functionalities
    '''
    cleaning the excel files for data analysis
    '''

    df_ani = pd.read_excel(animes)
    # df_rev = pd.read_excel(reviews)
    
    df_ani.sort_values(by=['uid'])
    df_ani['score'].replace('', np.nan, inplace=True)
    #cleaning
    df_ani = df_ani[['uid','title', 'synopsis', 'genre', 'score']]
    # aniscore_df = df_ani[['title', 'score']]
    # aniscore_df.set_index('title')
    df_ani['title']= df_ani['title'].str.lower()
    df_ani['synopsis']= df_ani['synopsis'].fillna(' ')
    #turn genre into a sentence for the nlp
    df_ani['genre']= df_ani['genre'].str.replace(" ", "")

    

    #changing uid to anime_uid to make both table match column name
    df_ani.replace({'uid': 'anime_uid'}, inplace=True)
    # df_rev = df_rev[['uid', 'anime_uid', 'score']]

    return df_ani

def find_keywords(synopsis: str):

    # create a rake object 
    rake = Rake()
    keywords = []
    for plot in synopsis:
        rake.extract_keywords_from_text(plot)
        keywords_i = rake.get_ranked_phrases()
        keywords_i_string = ""
        for keyword in keywords_i:
            keywords_i_string = keywords_i_string + " " + keyword
        keywords.append(keywords_i_string)
              
    return keywords

def get_ratings(df_ani):

    tfidf = TfidfVectorizer()
    print("start")
    tfidf_matrix =  tfidf.fit_transform(df_ani['genre'])
    
    
    df = df_ani.dropna(subset=['score'])
    genre_df = pd.DataFrame(tfidf_matrix.toarray())
    genre_df.columns = ['genre' + "|" + i for i in tfidf.get_feature_names()]
    rating_df = genre_df.mul(df['score'], axis=0)

    rating_df['anime'] = df['title']
    rating_df = rating_df.reset_index(drop = True)
    # get a list of the columns
    col = list(rating_df.columns)
    a, b = col.index("anime"), col.index("genre|action")
    col[b], col[a] = col[a], col[b]
    rating_df = rating_df[col]
    
    # genre_df.to_excel('assets/genres.xlsx')
    rating_df.to_excel('assets/rating.xlsx')

def get_genre(list_genre):

    result=""
    for i in list_genre:
        result += i + " "
    
    return result

def add_keyword(df_ani):

    df_ani['synopsis'] = find_keywords(df_ani['synopsis'])
    df_ani['synopsis'].to_excel('assets/synopsis.xlsx')
    print('work done')
    df_ani['genre'] = df_ani['genre'].apply(lambda x: get_genre(x))
    print("")
    df_ani['keywords'] = df_ani['synopsis'] +  df_ani['genre']

    return df_ani

def vector(df_ani):
    
    vectorizer = CountVectorizer()
    vectorized_keywords = vectorizer.fit_transform(df_ani['keywords'])
    vectorized_keywords = vectorized_keywords.toarray()

    return vectorized_keywords


def recommend(anime_name,keyword_vector,df_ani):
        
    similarity_matrix = cosine_similarity(keyword_vector, keyword_vector[list(np.where(df_ani["title"] == anime_name)[0]), :])
    similarity_dataframe = pd.DataFrame(similarity_matrix)
    similarity_dataframe.index = df_ani['title'] 
    similarity_dataframe =  similarity_dataframe.iloc[:,0]
    similarity_dataframe = similarity_dataframe.sort_values(ascending = False)
    similarity_dataframe = similarity_dataframe.drop_duplicates()

    return list(similarity_dataframe.index)[1:6]



# Create a connection to a SQLite database
# engine = create_engine('sqlite:///my_database.db', echo=False)

# Write the DataFrame to a table in the database
# df.to_sql('my_table', con=engine)

# Query the data using SQL commands
# query = '''
#     SELECT *
#     FROM my_table
#     WHERE column1 = 'value1'
# '''
# result = pd.read_sql(query, con=engine)