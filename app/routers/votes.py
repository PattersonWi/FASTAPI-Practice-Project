from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(

    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)

def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.post_id == vote.post_id)
    already_voted = vote_query.first()

    # If user wants to vote
    if vote.dir == 1:
        if already_voted:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail= f"User {current_user.id} has already voted on post {vote.post_id}")
        
        # If it has not voted already
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully added vote"}

    # If user wants to delete vote
    else:
        if not already_voted:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Vote does not exist")
        
        # deletes vote
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Message": "Successfully deleted vote"}