# Generate Requests
from flask import jsonify
import requests, logging;
import app.requests.game_extract as extract;
from concurrent.futures import ThreadPoolExecutor, as_completed;

api_key = "df5f51d5ba374f299bf346197b1527ca"
no_response = "No Response Found! All Attempts Have Been Made | Quiting Process!"
# ---------------------------------------------------------------------------------------------------- # 
# Request via Lambda Function
def rawg_request(rawg_urls):
    [print(f"URL: [{url}]") for url in rawg_urls]
    
    def fetch(url):
        path = 'https://ngiwswbqrdqutlmyrr4auw56va0wdbua.lambda-url.us-east-1.on.aws/'
        response = requests.get(path, params = { "url": url })
        code = response.status_code
        
        if code == 200: return response.json()
        else:
            logging.error(f"Response Error: {response.text}")
            return None
        
    results = [None] * len(rawg_urls)  # Initialize a list to store results
    with ThreadPoolExecutor(max_workers = len(rawg_urls)) as executor:
        future_to_url = {executor.submit(fetch, url): idx for idx, url in enumerate(rawg_urls)}
        for future in as_completed(future_to_url):
            idx = future_to_url[future]
            try:
                result = future.result()
                results[idx] = result
            except Exception as e:
                logging.error(f"Exception occurred for URL index {idx}: {e}")

    return results
# ---------------------------------------------------------------------------------------------------- # 
def home_setup():
    urls = [
        f"https://api.rawg.io/api/genres?key={api_key}&page_size=50",
        f"https://api.rawg.io/api/tags?key={api_key}&page_size=50",
        f"https://api.rawg.io/api/platforms?key={api_key}&page_size=50"
    ]
    results = rawg_request(urls)
    
    if len(results) != 3:
        logging.error("Unexpected Number of Results for Genre, Tag, and Platform")
        return None, None, None
    
    genres_data, tags_data, platforms_data = results
    
    genres = {item["name"]: item["id"] for item in genres_data["results"]} if genres_data else None
    if genres is None: logging.error("Genres NOT Found")
    
    tags = {item["name"]: item["id"] for item in tags_data["results"]} if tags_data else None
    if tags is None: logging.error("Tags NOT Found")
    
    platforms = {item["name"]: item["id"] for item in platforms_data["results"]} if platforms_data else None
    if platforms is None: logging.error("Platforms NOT Found")

    return genres, tags, platforms
# ---------------------------------------------------------------------------------------------------- # 
def autocomplete_search(search_query):
    results = rawg_request([f"https://api.rawg.io/api/games?key={api_key}&search={search_query}"])
    
    for result in results:
        if result:
            game_names = [{'id': game['id'], 'value': game['name']} for game in result['results']]
            return jsonify(game_names)
        else: return None
# ---------------------------------------------------------------------------------------------------- # 
def search_by_id(game_ids, genre_name, genre_id, tag_name, tag_id, platform_name, platform_id):
    games = []
    combined_details = {
        'genres': {(genre_name, genre_id)}, 'tags': {(tag_name, tag_id)}, 'platforms': {(platform_name, platform_id)}
    }
    
    urls = [f"https://api.rawg.io/api/games/{game_id}?key={api_key}" for game_id in game_ids]
    results = rawg_request(urls)
    
    for result in results:
        if result:
            details = extract.extract_specifics(result)
            if details:
                games.append({"title": details["name"], "image": details["image"]})
                for key in ['genres', 'tags', 'platforms']:
                    if key in details: combined_details[key].update(details[key])
        
    result = {}
    for key in ['genres', 'tags', 'platforms']:
        names = ' | '.join(name for name, _ in combined_details[key])
        ids = ','.join(str(id) for _, id in combined_details[key])
        result[key + '_names'] = names
        result[key + '_ids'] = ids

    result['games'] = games
    return jsonify(result)
# ---------------------------------------------------------------------------------------------------- # 
def search_for_results(genres, tags, platforms, limit = 10):
    results = rawg_request(
        [f"https://api.rawg.io/api/games?key={api_key}&language=eng&genres={genres}&tags={tags}&platforms={platforms}&page_size={limit}"]
    )
    
    for result in results:
        if result:
            logging.info(f"Success! Up to {limit} Games found with filters: {genres} - {tags} - {platforms}")
            if 'results' in result and len(result['results']) > 0:
                game_ids = []
                for game in result["results"]: game_ids.append(game["id"])
                return "_".join(str(id) for id in game_ids)
        else:
            logging.error(no_response)
        
        return None
# ---------------------------------------------------------------------------------------------------- # 
def get_game_results(ids):
    if ids:
        game_ids = ids.split("_")
        all_games = []
        
        urls = [f"https://api.rawg.io/api/games/{game_id}?key={api_key}" for game_id in game_ids]
        results = rawg_request(urls)
        i = 1
        
        for i, result in enumerate(results, start = 1):
            if result:
                logging.info(f"Extracting Game: {i}")
                game_data = extract.extract_data(result)
                if game_data: 
                    all_games.append(game_data)
            else:
                logging.warning(f"Search Failed for Game: {i}")
                
        if all_games: return all_games
    else: 
        logging.warning("No IDs Provided")
        
    return None
# ---------------------------------------------------------------------------------------------------- # 