from fastapi import FastAPI

from app.routers.vote import vote

from . import models
from .config import settings 
from .database import engine
from .routers import post, user, auth, vote


app = FastAPI()

# models.Base.metadata.create_all(bind=engine)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {'message': 'Hello Worldddd'}









# my_posts = [{'id': 1, 'title': 'title post 1', 'content': 'content post 1'},
#             {'id': 2, 'title': 'title post 2', 'content': 'content post 2'}]

# def find_post(post_id):
#     for p in my_posts:
#         if p['id'] == post_id:
#             return p

# def find_post_index(post_id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == post_id:
#             return i