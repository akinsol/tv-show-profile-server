from typing import List
from config import CLIENT_ID
import requests
import schema


headers = {
    "Content-type": "application/json",
    "trakt-api-key": CLIENT_ID,
    "trakt-api-version": '2'
}


def get_search(search: str):
    results = (requests.get(f'https://api.trakt.tv/search/show?query={search}', headers=headers)).json()
    show_list = []
    for result in results:
        show = result['show']
        show_list.append(schema.Search(show['ids']['trakt'], show['title']))
    return show_list


def get_show(show_id: int):
    show = (requests.get(f'https://api.trakt.tv/shows/{show_id}?extended=full', headers=headers)).json()
    return schema.Show(
        show_id,
        show['title'],
        show['overview'],
        show['rating'],
        get_season_list(show_id),
    )


def get_season_list(show_id):
    seasons = (requests.get(f'https://api.trakt.tv/shows/{show_id}/seasons?extended=full', headers=headers)).json()
    season_list = []
    for season in seasons:
        if season['number'] != 0:
            season_list.append(schema.BasicSeason(
                season['number'],
                season['rating']
            ))
    return season_list


def get_season(show_id: int, season_number: int):
    results = (requests.get(f'https://api.trakt.tv/shows/{show_id}/seasons?extended=full', headers=headers)).json()
    for result in results:
        if result['number'] == season_number:
            episodes = get_episodes(show_id, season_number, result['episode_count'])
            season = schema.Season(
                season_number,
                result['overview'],
                result['rating'],
                episodes,
            )
            return season


def get_episodes(show_id, season_number, episode_count):
    episode_list = []
    episode_number = 1
    while episode_count >= episode_number:
        episode = (requests.get(
            f'https://api.trakt.tv/shows/{show_id}/seasons/{season_number}/episodes/{episode_number}?extended=full',
            headers=headers)
        ).json()
        episode_list.append(schema.Episode(
            episode['title'],
            episode['number'],
            episode['overview'],
            episode['rating']
        ))
        episode_number += 1
    return episode_list


def get_appearances(show_id, season, search):
    results = (requests.get(f'https://api.trakt.tv/shows/{show_id}/seasons/{season}/people',
                            headers=headers)).json()
    cast = results['cast']
    for actor in cast:
        characters = actor['characters']
        for character in characters:
            if character == search:
                return 1
    return 0


def get_cast(show_id: int, seasons: List[str]):
    results = (
        requests.get(f'https://api.trakt.tv/shows/{show_id}/people', headers=headers)).json()
    cast = results['cast']
    character_list = []
    for actor in cast:
        characters = actor['characters']
        for character in characters:
            appearances = 0
            for season in seasons:
                appearances = appearances + get_appearances(show_id, season, character)
            character_list.append(schema.Character(character, actor['person']['name'], appearances))
    return character_list
