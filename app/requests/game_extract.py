import logging;
# ---------------------------------------------------------------------------------------------------- # 
def extract_specifics(game):
    if isinstance(game, dict):
        try:
            return {
                "name": game["name"],
                "image": game["background_image"],
                "genres": 
                    [(genre["name"], genre["id"]) for genre in game.get("genres", [])], 
                "tags": 
                    [(tag["name"], tag["id"]) for tag in game.get("tags", [])], 
                "platforms": 
                    [(platform['platform']['name'], platform['platform']["id"]) for platform in game.get("platforms", [])] 
            }
        except KeyError as e: logging.error(f"Missing Key in Data: [{e}]")
        except Exception as e: logging.error(f"Data Error: [{e}]")
    else: 
        logging.warning("Data NOT A Dict")
        return None
# ---------------------------------------------------------------------------------------------------- # 
def extract_data(game):
    if isinstance(game, dict):
        try:
            return {
                'id': game['id'],
                'name': game['name'],
                'rating': game['rating'],
                'released': game['released'],
                'image': game['background_image'],
                'esrb_rating': game['esrb_rating']['name'] if game.get('esrb_rating') else 'Not Rated',
                
                'tags': 
                    [tag['name'] for tag in game.get('tags', []) if 'name' in tag],
                'genres': 
                    [genre['name'] for genre in game.get('genres', []) if 'name' in genre],
                'stores': 
                    [store['store']['name'] for store in game.get('stores', []) if 'store' in store and 'name' in store['store']],
                'platforms': 
                    [platform['platform']['name'] for platform in game.get('platforms', []) if 'platform' in platform and 'name' in platform['platform']]          
            }
        except KeyError as e: logging.error(f"Missing Key in Data: [{e}]")
        except Exception as e: logging.error(f"Data Error: [{e}]")
    else:
        logging.warning("Data NOT A Dict")
        return None
# ---------------------------------------------------------------------------------------------------- #   
def game_data(json_data):
    games = []
    
    if 'results' in json_data and len(json_data['results']) > 0:
        for game in json_data['results']: games.append(extract_data(game))
        return games
    else:
        logging.info("Nothing to extract :(")
        return None
# ---------------------------------------------------------------------------------------------------- # 