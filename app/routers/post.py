from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional
from sqlalchemy import func


router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#while True:
#    try:
#        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='mailmeev@3000', cursor_factory=RealDictCursor)
#        cursor =conn.cursor()
#        print("database connection was successful")
#        break 
#    except Exception as error:
#        print("Connecting to db failed")
#        print(f"The error was {error}")
#        time.sleep(2)


#my_posts = [{"title": "title of post 1", "content": "Content of post 1", "id" :1},{"title": "favourite foods", "content" : "i like pizza", "id" :2}]
#save in memory as db is not ready yet

#def find_post(id):
#    for p in my_posts:
#        if p['id'] == id:
#            return p
#
#def find_index_post(id):
#    for i,p in enumerate(my_posts):
#        if p['id'] == id:
#            return i 



#@router.get("/posts")
#def get_posts():
#    cursor.execute("""SELECT * FROM posts""")
#    posts=cursor.fetchall()
#    #print(posts)
#    return {"data" : posts}

#@router.get("/", response_model=List[schemas.Post])
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit: int = 10, skip: int =0, search: Optional[str]=""):
#    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).all()
#    post_list = []
#    for post, votes in results:
#        post_dict = {
#            "post_id": post.id,
#            "title": post.title,
#            "content": post.content,
#            "votes": votes,
#        }
#        post_list.append(post_dict)
#
    return results
    


#@router.post("/createposts")
#def create_posts(payLoad: dict=Body(...)):
#    #payLoad stores the body data, it will be of the type
#    print(payLoad)
#    return {"post" : f"title {payLoad['title']} content: {payLoad['content']}"}
##title str, content str, category, Bool publish


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int =Depends(oauth2.get_current_user)):
    print (current_user.id)
    #new_post=models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    return new_post





#@router.post("/posts", status_code= status.HTTP_201_CREATED)
#def create_posts(post: Post):
#    #gets type validated data from post class
#    #data is already assigned to post variable
#    #data is extracted and stored into post, it is stored as a pydantic model 
#    #post_dict = post.dict()
#    #post_dict['id']=randrange(0,10000000)
#    #my_posts.routerend(post_dict)
#    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
#    #this way of %s sanitizes the input 
#    new_post = cursor.fetchall()
#    conn.commit()
#    #saves it into the db
#    return {"data": "created post"}

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)
    #post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':f"post with id {id} was not found"}
    return post


#
#@router.get("/posts/{id}")
#def get_post(id: int, response: Response):
#    cursor.execute("""SELECT * FROM posts where id = %s """,(str(id)))
#    post=cursor.fetchone()
#    #post=find_post(id)
#    if not post:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail = f"post with id {id} was not found")
#        #response.status_code = status.HTTP_404_NOT_FOUND
#        #return {'message':f"post with id {id} was not found"}
#    return {"post_detail": post}
#

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    delete_query=db.query(models.Post).filter(models.Post.id==id)
    delete_post_find=delete_query.first()
    if delete_post_find==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #my_posts.pop(index)
    if delete_post_find.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail ="Not authorized to perform requested action")

    delete_post=delete_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id:int, post: schemas.PostCreate, db: Session = Depends(get_db),user_id:int =Depends(oauth2.get_current_user)):
    update_query=db.query(models.Post).filter(models.Post.id==id)
    update_post_find=update_query.first()
    if update_post_find==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    #post=find_post(id)
    post_dict = post.dict() #convert the post to a dictionary
    update_query.update(post_dict,synchronize_session=False)
    db.commit()
    return update_query.first()


#@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
#def delete_post(id: int):
#    cursor.execute("""DELETE FROM posts where id=%s RETURNING *""",(str(id)))
#    index=cursor.fetchone()
#    conn.commit()
#    #index=find_index_post(id)
#    if index==None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#    #my_posts.pop(index)
#    return Response(status_code=status.HTTP_204_NO_CONTENT)
#
#
#@router.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
#def update_post(id:int, post: Post):
#    index=find_index_post(id)
#    if index==None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#    #post=find_post(id)
#    post_dict = post.dict() #convert the post to a dictionary
#    post_dict['id']=id
#    my_posts[index]=post_dict
#    print(post)
#    return {"data" : post_dict}