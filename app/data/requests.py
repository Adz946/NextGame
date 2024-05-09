import requests, time;
api_key = "b876dc8875674725a3d822a2d8dc79d2"
# ---------------------------------------------------------------------------------------------------- #
def extract_game_data(json_data):
    if 'results' in json_data:
        games = json_data['results']  # Multiple games
    else:
        games = [json_data]  # Single game
    
    games_info = []  # List to hold all games' information

    for game in games:
        game_details = {
            'id': game['id'],
            'name': game['name'],
            'slug': game['slug'],
            'release_date': game['released'],
            'rating': game['rating'],
            'metacritic': game.get('metacritic', 'N/A'),  # Using get for optional fields
            'background_image': game['background_image'],
            'platforms': [
                {
                    'platform_name': platform['platform']['name'],
                    'released_at': platform['released_at'],
                    'requirements_en': platform.get('requirements_en')  # Optional field
                } for platform in game['platforms']
            ],
            'genres': [genre['name'] for genre in game['genres']],
            'stores': [
                {
                    'store_name': store['store']['name'],
                    'domain': store['store']['domain']
                } for store in game['stores']
            ],
            'tags': [tag['name'] for tag in game['tags']],
            'esrb_rating': game['esrb_rating']['name'] if game.get('esrb_rating') else 'Not Rated'
        }
        games_info.append(game_details)

    return games_info
  # ---------------------------------------------------------------------------------------------------- #  
def search_dataset(url = f"https://api.rawg.io/api/games?key={api_key}&page=1", retries = 5, delay = 3):
    for attempt in range(retries):
        response = requests.get(url)
        code = response.status_code
        
        if code != 200:
            print("Failure!")
            if code == 401: print("Unauthorized Error")
            elif code == 429: print("Too Many Requests")
            elif code == 500: print("Internal Server Error")
            elif code == 502: print(f"Bad Gateway! Attempt: {attempt}")
            else: print(f"Unknown Issue: Code {code}")
            time.sleep(delay)
        else: 
            try: return extract_game_data(response.json())
            except requests.exceptions.JSONDecodeError as jd: print(f"JSON Decode Error: [ {jd} ]")
    print("Error! All Attempts Exceeded!")
    return None
# ---------------------------------------------------------------------------------------------------- #
def get_genres():
    url = f"https://api.rawg.io/api/genres?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json()
        return {genre['name']: genre['id'] for genre in genres['results']}
    else:
        print("Failed to fetch genres")
        return None
    
def get_tags():
    url = f"https://api.rawg.io/api/tags?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        tags = response.json()
        return {tag['name']: tag['id'] for tag in tags['results']}
    else:
        print("Failed to fetch tags")
        return None
    
def get_platforms():
    url = f"https://api.rawg.io/api/platforms?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        platforms = response.json()
        return {platform['name']: platform['id'] for platform in platforms['results']}
    else:
        print("Failed to fetch platforms")
        return None
# ---------------------------------------------------------------------------------------------------- #
def get_all_games(limit = 5):
    for page in range(1, limit + 1):
        url = f"https://api.rawg.io/api/games?key={api_key}&page={page}"
        data = search_dataset(url)
        
        for num, game in enumerate(data, start = 1):
            print(f"Game {num}: ID == [{game["id"]}] | Title == [{game["name"]}] | Slug == [{game["slug"]}] | Rating == [{game["rating"]}]")
        
def get_game_by_id(id = 3498):
    url = f"https://api.rawg.io/api/games/{id}?key={api_key}"
    data = search_dataset(url)
    
    for num, game in enumerate(data, start = 1):
        print(f"Game {num}: ID == [{game["id"]}] | Title == [{game["name"]}] | Slug == [{game["slug"]}] | Rating == [{game["rating"]}]")   
        for genres in game["genres"]:
                print(f"Genre: {genres}")
# ---------------------------------------------------------------------------------------------------- #