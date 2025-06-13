from sqlalchemy.orm import Session

from core.database.models import User, Subscription, SubscriptionType


def get_or_create_user(db: Session, telegram_id: int):
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_subscription_type(db: Session, code: str):
    return db.query(SubscriptionType).filter_by(code=code).first()


def add_subscription(
        db: Session,
        telegram_id: int,
        city: str,
        info_type_code: str,
        time: str
):
    city = city.strip().lower()
    user = get_or_create_user(db, telegram_id)
    sub_type = get_subscription_type(db, info_type_code)
    if not sub_type:
        raise ValueError("Unknown subscription type")
    sub = db.query(Subscription).filter_by(
        user_id=user.id,
        city=city,
        type_id=sub_type.id,
        time=time
    ).first()
    if not sub:
        sub = Subscription(
            user_id=user.id,
            city=city,
            type_id=sub_type.id,
            time=time
        )
        db.add(sub)
        db.commit()
    else:
        sub.time = time
        db.commit()
    return sub


def remove_subscription(
        db: Session,
        telegram_id: int,
        city: str = None,
        info_type_code: str = None,
        time: str = None
):
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        return
    q = db.query(Subscription).filter(Subscription.user_id == user.id)
    if city:
        q = q.filter(Subscription.city == city)
    if info_type_code:
        sub_type = get_subscription_type(db, info_type_code)
        if sub_type:
            q = q.filter(Subscription.type_id == sub_type.id)
    if time:
        q = q.filter(Subscription.time == time)
    for sub in q:
        db.delete(sub)
    db.commit()


def get_user_subscriptions(db: Session, telegram_id: int):
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        return []
    return (
        db.query(Subscription)
        .filter(Subscription.user_id == user.id)
        .join(Subscription.subscription_type)
        .all()
    )


def get_subscriptions_by_time(db: Session, time: str):
    return db.query(Subscription).filter(Subscription.time == time).all()
