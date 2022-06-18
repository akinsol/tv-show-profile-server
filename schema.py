import resolver
import strawberry
from typing import List, Optional


@strawberry.type
class Character:
    name: Optional[str]
    actor: Optional[str]
    appearances: Optional[int]


@strawberry.type
class Episode:
    title: Optional[str]
    number: Optional[int]
    summary: Optional[str]
    rating: Optional[float]


@strawberry.type
class Season:
    number: Optional[int]
    summary: Optional[str]
    rating: Optional[float]
    episodes: Optional[List[Episode]]


@strawberry.type
class BasicSeason:
    number: Optional[int]
    rating: Optional[float]


@strawberry.type
class Show:
    trakt_id: Optional[int]
    title: Optional[str]
    summary: Optional[str]
    rating: Optional[float]
    seasons: Optional[List[BasicSeason]]


@strawberry.type
class Search:
    trakt_id: int
    title: str


@strawberry.type
class Query:
    results: List[Search] = strawberry.field(resolver=resolver.get_search)
    show: Show = strawberry.field(resolver=resolver.get_show)
    season: Season = strawberry.field(resolver=resolver.get_season)
    cast: List[Character] = strawberry.field(resolver=resolver.get_cast)
