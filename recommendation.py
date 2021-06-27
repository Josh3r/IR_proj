"""
Some notes:
1. Input would be 3 games of your desire
2. Output would be a recommended game, in my case, it would be based entirely on the genre
########
Columns:
url,types,name,desc_snippet,recent_reviews,all_reviews,release_date,developer,publisher,popular_tags,game_details,languages,achievements,genre,game_description,mature_content,minimum_requirements,recommended_requirements,original_price,discount_price
Important/relevant columns:
recent_reviews, all_reviews, genre, name
"""
from collections import Counter, defaultdict
import pandas
df = pandas.read_csv('./steam_games.csv', usecols = ['name', 'recent_reviews', 'all_reviews', 'genre', 'popular_tags'])


def get_genre(games):
    # Input = list of 3 games
    # We have to iterate over this list, and for each game, find it's genre and place it in the genre_count
    genre_count = defaultdict(int)
    for game in games:
        game_row = df.loc[df['name'] == game]
        genre = game_row["genre"].to_string(index=False)
        print("Genre for this game is:",genre)
        try:
            genre_list = genre.split(",")
            for genre in genre_list:
                genre_count[genre] += 1
        except:
            genre_count[genre] += 1
    # now return max
    max_genre = max(genre_count.values())
    for genre in genre_count:
        if genre_count[genre] == max_genre:
            return genre
    return -1 # Error


# This function recieves a genre as input and returns an orderd list of the games under this genre, orderd by their all_reviews
def get_genre_ordered_list(genre):
    ordered_list = [] # Each element in this ordred list is a tuple in the form of: (game_name, overall_reviws)
    games = df.loc[df['genre'] == genre]
    for index, row in games.iterrows():
        try:
            game_name, score = row["name"], int(row["all_reviews"].split("%")[0][-2:])
            ordered_list.append((game_name, score))
        except:
            # This means there are no reviews or not enough reviews to have a score, hence we pass this
            pass
        #print(score)
    ordered_list.sort(key = lambda x:x[1]) # Sort by the overall score
    return ordered_list

# The recommend function accepts 3 games of choice from the players and will return a game based on the genres of these 3 games
# The curated list should be ordered by score, after which the top scoring game in this curated list (based on genre) will be returned as the result
def recommend(interests):
    # 1st task: parse the 3 games from interests input and get the core genre
    genre_of_interest = get_genre(interests)
    print(genre_of_interest)
    # 2nd task: parse the CSV for a game from this genre, and return an ordered list, orderd by overall_score
    recommendations = get_genre_ordered_list(genre_of_interest)
    # 3rd task: return the top of this ordered list
    return recommendations.pop()


######### Driver test code
inp_game = ["DOOM", "PLAYERUNKNOWN'S BATTLEGROUNDS", "BATTLETECH"]
print(recommend(inp_game))