from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)


class SubscriptionType(Base):
    __tablename__ = "subscription_types"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    city = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('subscription_types.id'), nullable=False)
    time = Column(String, nullable=False)

    user = relationship('User', passive_deletes=True)
    subscription_type = relationship('SubscriptionType')

    __table_args__ = (
        UniqueConstraint('user_id', 'city', 'type_id', 'time', name='_user_city_type_time_uc'),
    )
