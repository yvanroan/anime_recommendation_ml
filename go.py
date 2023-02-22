from start import preprocess, vector, add_keyword,recommend, get_ratings
import pandas as pd



def run():

    anime_name = input("Enter the name of the anime(in lowercase):\n")
    print("Cleaning the database...")
    df_ani= preprocess('assets/animes.xlsx')
    
 
    print("Checking for the anime in the database...")
    ans = (df_ani['title'].eq(anime_name)).any()
    if not ans:
        print("Unfortunately the anime is not in our database at the moment\n T T \n _")
        return 
    
    print("Anime found in the database...")
    print("Finding keywords...")
    df_ani = add_keyword(df_ani)
    print("Creating a vector...")
    vector_keyword = vector(df_ani)
    print("Recommending the perfect animes in the database...")
    result = recommend(anime_name, vector_keyword, df_ani)

    print(result)


if __name__== "__main__":
    run()
