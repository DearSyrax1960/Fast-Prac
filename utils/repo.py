from sqlalchemy.orm import Session

from models.users_model import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def save_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
