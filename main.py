from fastapi import FastAPI
from schema import Query
import strawberry
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter


origins = [
    "http://127.0.0.1:8000"
]

gql_schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(gql_schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
