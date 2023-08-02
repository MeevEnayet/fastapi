from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post,user, auth, vote


#this line is the command that told sql alchemy to run the create statement so that it generated all the tables when it started up
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["https://www.google.com"]

app.add_middleware(
    CORSMiddleware, #middleware is basically a function that runs before every request, if someone sends a request to our app, before it goes throught he routers it goes through the middleware and our middleware can perform some sort of operation 
    allow_origins= origins, #specify what domains should be able to talk to our api
    allow_credentials=True,
    allow_methods=["*"], #we can allow specific http methods, not allowing post requests for example 
    allow_headers=["*"] #allow specific headers only 
)

app.include_router(post.router)
app.include_router(user.router) #get the router object from the user file, imports all of the specific routes
app.include_router(auth.router)
app.include_router(vote.router)

#below code is called a path operation or route
#in this case the web browser is generating an http request
#postman helps us in giving an http request
@app.get("/")
def root():
    return {"message" : "Welcome to my api!!!!"}