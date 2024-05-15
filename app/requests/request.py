# Generate Requests
from flask import jsonify
import requests, logging;
import app.requests.game_extract as extract;
from concurrent.futures import ThreadPoolExecutor, as_completed;

api_key = "df5f51d5ba374f299bf346197b1527ca"
executor = ThreadPoolExecutor(max_workers = 5)
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
        
    futures = [executor.submit(fetch, url) for url in rawg_urls]
    results = [future.result() for future in as_completed(futures)]      
    return results
# ---------------------------------------------------------------------------------------------------- # 
def home_setup():
    urls = [
        f"https://api.rawg.io/api/genres?key={api_key}&page_size=50",
        f"https://api.rawg.io/api/tags?key={api_key}&page_size=50",
        f"https://api.rawg.io/api/platforms?key={api_key}&page_size=100"
    ]
    results = rawg_request(urls)
    data = []
    
    for result in results:
        if result is not None:
            logging.info("Success! Results Found")
            data.append({item["name"]: item["id"] for item in result["results"]})
        else:
            logging.error(no_response)
            data.append(None)
        
    return data
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
            return extract.game_data(result)
        else:
            logging.error(no_response)
            return None
# ---------------------------------------------------------------------------------------------------- # 