from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import  Session # this will allow you to declare the type of the db parameters and have better type checks and completion in your functions.
from typing import List, Optional
from sqlalchemy import func


from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)


# before sqlalchemy join: @router.get("/", response_model=List[schemas.Post])
# after sqlalchemy join: @router.get("/", response_model=List[schemas.PostOut])
@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # # Execute a query
    # cur.execute('SELECT * FROM "Posts"')

    # # Retrieve query results
    # records = cur.fetchall()

    # before sqlalchemy join:
    # records = db.query(models.Post).filter(models.Post.name.contains(search)).limit(limit).offset(skip).all()

    # after sqlalchemy join:
    records = db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.name.contains(search)).limit(limit).offset(skip).all()
    return records

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no SQL injections!)
    # cur.execute('INSERT INTO "Posts" ("Name", "Age", "Height", "Gender") VALUES (%s, %s, %s, %s) RETURNING *', 
    # (post.name, post.age, post.height, post.gender))
    # new_post = cur.fetchone()
    
    # # Make the changes to the database persistent
    # conn.commit()

    # This code does the exact same thing that the code above
    # only that this time we use sqlalchemy instead 
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model= schemas.PostOut)
def get_post_id(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cur.execute('SELECT * FROM "Posts" WHERE "ID" = %s', (id,))
    # post = cur.fetchone()

    # This code does the exact same thing that the code above
    # only that this time we use sqlalchemy instead 
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post =  db.query(models.Post, func.count(models.Votes.post_id).label("Votes")).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "ERROR 404: Not Found")
    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session =Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cur.execute('DELETE FROM "Posts" WHERE "ID" = %s RETURNING *', (id,))
    # post_to_delete = cur.fetchone()
    # conn.commit()
    
    post_to_delete = db.query(models.Post).filter(models.Post.id == id)

    if post_to_delete.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The post with id: {id} does not exist")

    if post_to_delete.first().user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action!")

    post_to_delete.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cur.execute('UPDATE "Posts" SET "Name" = %s, "Age" = %s, "Height" = %s, "Gender" = %s WHERE "ID" = %s RETURNING *', 
    # (post.name, post.age, post.height, post.gender, id))
    # post_to_update = cur.fetchone()

    # conn.commit()

    post_to_update = db.query(models.Post).filter(models.Post.id == id)

    if post_to_update.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The post with id: {id} does not exist")

    if post_to_update.first().user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action!")

    post_to_update.update(post.dict(), synchronize_session = False)  
    db.commit()  
    return post_to_update.first()