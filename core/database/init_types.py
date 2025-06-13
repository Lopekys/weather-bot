from core.database.models import SubscriptionType
from core.database.db_connector import SessionLocal

DEFAULT_TYPES = [
    {"code": "weather", "description": "Current Weather"},
    {"code": "hourly", "description": "Hourly Forecast"},
    {"code": "sun", "description": "Sunrise & Sunset"},
    {"code": "wind", "description": "Wind"},
    {"code": "air", "description": "Air Quality"},
    {"code": "details", "description": "Full Details"},
]

def init_subscription_types():
    with SessionLocal() as db:
        for t in DEFAULT_TYPES:
            if not db.query(SubscriptionType).filter_by(code=t["code"]).first():
                db.add(SubscriptionType(**t))
        db.commit()
