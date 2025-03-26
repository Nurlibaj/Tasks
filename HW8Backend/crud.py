from sqlalchemy.orm import Session
import models.sql_models as models
import schemas

# User operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email_and_password(db: Session, email: str, password: str):
    return db.query(models.User).filter(
        models.User.email == email, 
        models.User.password == password
    ).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate, avatar_path: str = None):
    db_user = models.User(
        email=user.email,
        password=user.password,
        name=user.name,
        avatar=avatar_path
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_flower(db: Session, flower_id: int):
    return db.query(models.Flower).filter(models.Flower.id == flower_id).first()

def get_flowers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flower).offset(skip).limit(limit).all()

def create_flower(db: Session, flower: schemas.FlowerCreate):
    db_flower = models.Flower(
        name=flower.name,
        count=flower.count,
        price=flower.price
    )
    db.add(db_flower)
    db.commit()
    db.refresh(db_flower)
    return db_flower

def update_flower(db: Session, flower_id: int, flower_update: schemas.FlowerUpdate):
    db_flower = get_flower(db, flower_id)
    if db_flower:
        update_data = flower_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_flower, key, value)
        db.commit()
        db.refresh(db_flower)
    return db_flower

def delete_flower(db: Session, flower_id: int):
    db_flower = get_flower(db, flower_id)
    if db_flower:
        db.delete(db_flower)
        db.commit()
        return True
    return False


def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    db_purchase = models.Purchase(
        user_id=purchase.user_id,
        flower_id=purchase.flower_id
    )
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

def get_user_purchases(db: Session, user_id: int):
    return db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()

def get_purchased_flowers(db: Session, user_id: int):
    purchases = db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()
    flowers = []
    for purchase in purchases:
        flower = db.query(models.Flower).filter(models.Flower.id == purchase.flower_id).first()
        if flower:
            flowers.append(flower)
    return flowers 