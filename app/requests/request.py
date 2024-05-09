# Generate Request
import requests, time, logging;
from app.requests.game_extract import game_data, extract_data;

api_key = "b876dc8875674725a3d822a2d8dc79d2"
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
def search_dataset(url_end, page = 1):
    url = f"https://api.rawg.io/api/{url_end}?key={api_key}"
    if url_end == "games": url += f"&page={page}" 
    data = make_request(url)
            
    if data:
        logging.info(f"Success! {url_end} Data Will Be Extracted")
        if url_end == "games": return game_data(data)
        elif url_end in ["genres", "tags", "platforms"]: return {item["name"]: item["id"] for item in data["results"]}
        else: logging.error("Unsupported Endpoint?!")
    else: 
        logging.error("No Response Found! All Attempts Have Been Made | Quiting Process!")
        return None
# ---------------------------------------------------------------------------------------------------- # 
def search_by_id(id = 3498):
    url = f"https://api.rawg.io/api/games/{id}?key={api_key}"
    data = make_request(url)
    
    if data:
        logging.info(f"Success! Game [{id}] Will Be Extracted")
        return extract_data(data)
    else: 
        logging.error("No Response Found! All Attempts Have Been Made | Quiting Process!")
        return None
    
def search_by_title(title):
    url = f"https://api.rawg.io/api/games?key={api_key}&search={title}"
    data = make_request(url)
    
    if data:
        logging.info(f"Success! Game [{id}] Will Be Extracted")
        return extract_data(data)
    else: 
        logging.error("No Response Found! All Attempts Have Been Made | Quiting Process!")
        return None
# ---------------------------------------------------------------------------------------------------- # 