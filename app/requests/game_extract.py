import logging;
# ---------------------------------------------------------------------------------------------------- # 
def extract_data(game):
    if isinstance(game, dict):
        try:
            return {
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
        except KeyError as e: logging.error(f"Missing Key in Data: [{e}]")
        except Exception as e: logging.error(f"Data Error: [{e}]")
    else: 
        logging.warning("Data NOT A Dict")
        return None
# ---------------------------------------------------------------------------------------------------- #   
def game_data(json_data):
    if json_data: return [extract_data(game) for game in json_data.get('results', [json_data])]
    else: 
        logging.info("No Data To Extract")
        return []
# ---------------------------------------------------------------------------------------------------- # 