# Generate Requests
from flask import jsonify
import requests, time, logging;
import app.requests.game_extract as extract;

api_key = "df5f51d5ba374f299bf346197b1527ca"
no_response = "No Response Found! All Attempts Have Been Made | Quiting Process!"
# ---------------------------------------------------------------------------------------------------- # 
# Request via Lambda Function
def rawg_request(rawg_url):
    url = 'https://ngiwswbqrdqutlmyrr4auw56va0wdbua.lambda-url.us-east-1.on.aws/'
    params = { "url": rawg_url }
    response = requests.get(url, params=params)
    code = response.status_code
    
    if code == 200: return response.json()
    else:
        logging.error(f"Response Error: [{response.text}]")
        print(f"Response Error: [{response.text}]")
        return None
# ---------------------------------------------------------------------------------------------------- # 
def home_setup():
    genres = rawg_request(f"https://api.rawg.io/api/genres?key={api_key}")
    tags = rawg_request(f"https://api.rawg.io/api/tags?key={api_key}")
    platforms = rawg_request(f"https://api.rawg.io/api/platforms?key={api_key}")
    data = []
    
    if genres:
        logging.info("Success! Genres have been found")
        data.append({item["name"]: item["id"] for item in genres["results"]})
    else: 
        logging.error(no_response)
        data.append(None)
        
    if tags:
        logging.info("Success! Tags have been found")
        data.append({item["name"]: item["id"] for item in tags["results"]})
    else: 
        logging.error(no_response)
        data.append(None)
        
    if platforms:
        logging.info("Success! Platforms have been found")
        data.append({item["name"]: item["id"] for item in platforms["results"]})
    else: 
        logging.error(no_response)
        data.append(None)
        
    return data
# ---------------------------------------------------------------------------------------------------- # 
def autocomplete_search(search_query):
    response = rawg_request(f"https://api.rawg.io/api/games?key={api_key}&search={search_query}")
    if response:
        game_names = [{'id': game['id'], 'value': game['name']} for game in response['results']]
        return jsonify(game_names)
    else: return None
# ---------------------------------------------------------------------------------------------------- # 
def search_by_id(game_ids, genreName, genreID, tagName, tagID, platformName, platformID):
    games = []
    combined_details = {
        'genres': {(genreName, genreID)}, 'tags': {(tagName, tagID)}, 'platforms': {(platformName, platformID)}
    }
    
    for game_id in game_ids:
        data = rawg_request(f"https://api.rawg.io/api/games/{game_id}?key={api_key}")
        if data:
            details = extract.extract_specifics(data)
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
    data = rawg_request(f"https://api.rawg.io/api/games?key={api_key}&language=eng&genres={genres}&tags={tags}&platforms={platforms}&page_size={limit}")
    
    if data:
        logging.info(f"Success! Up to {limit} Games found with filters: {genres} - {tags} - {platforms}")
        return extract.game_data(data)
    else:
        logging.error(no_response)
        return None
# ---------------------------------------------------------------------------------------------------- # 