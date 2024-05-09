# Generate Request
from flask import jsonify
import requests, time, logging;
import app.requests.game_extract as extract;

api_key = "b876dc8875674725a3d822a2d8dc79d2"
no_response = "No Response Found! All Attempts Have Been Made | Quiting Process!"
# ---------------------------------------------------------------------------------------------------- # 
def make_request(url, retries = 5):
    delay = 3
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.warning(f"HTTP error on attempt {attempt + 1}: {e}")
            time.sleep(delay)  # Increase delay exponentially if needed
            delay *= 2
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            break  # Non-retryable error
    return None
# ---------------------------------------------------------------------------------------------------- # 
def home_setup():
    genres = make_request(f"https://api.rawg.io/api/genres?key={api_key}")
    tags = make_request(f"https://api.rawg.io/api/tags?key={api_key}")
    platforms = make_request(f"https://api.rawg.io/api/platforms?key={api_key}")
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
    response = requests.get(f"https://api.rawg.io/api/games?key={api_key}&search={search_query}")
    game_names = [{'id': game['id'], 'value': game['name']} for game in response.json()['results']]
    return jsonify(game_names)
# ---------------------------------------------------------------------------------------------------- # 
def search_by_id(game_ids):
    common_details = {}
    all_details = []

    for game_id in game_ids:
        url = f"https://api.rawg.io/api/games/{game_id}?key={api_key}"
        data = make_request(url)
        if data:
            details = {
                'genres': set(genre['name'] for genre in data.get('genres', [])),
                'tags': set(tag['name'] for tag in data.get('tags', [])),
                'platforms': set(platform['platform']['name'] for platform in data.get('platforms', []))
            }
            all_details.append(details)

    if all_details:
        # Initialize common details with the first game's details
        common_details = all_details[0]
        for details in all_details[1:]:
            # Intersect the sets to find common genres, tags, platforms
            common_details['genres'] &= details['genres']
            common_details['tags'] &= details['tags']
            common_details['platforms'] &= details['platforms']
            
        # Convert sets to comma-separated strings
        common_details = {key: ','.join(values) for key, values in common_details.items()}
        return jsonify(common_details)
    else:
        return jsonify({"error": "Failed to fetch game details for provided IDs"}), 500
# ---------------------------------------------------------------------------------------------------- # 
def search_for_results(genre, tag, platform):
    url = f"https://api.rawg.io/api/games?key={api_key}&genres={genre}&tags={tag}&platforms={platform}&page_size=10"
    data = make_request(url)
    
    if data:
        logging.info(f"Success! Up to 10 Games found with filters: {genre} - {tag} - {platform}")
        return extract.game_data(data)
    else:
        logging.error(no_response)
        return None
# ---------------------------------------------------------------------------------------------------- # 