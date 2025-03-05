from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from datetime import datetime, timezone
# from bson.objectid import ObjectId

# Connect to local MongoDB (for testing)
client = MongoClient("mongodb://localhost:27017/")

# Create a new database
db = client["Cluster0"]

# Drop existing collections (optional, to reset data)
db.pins.drop()
db.bathrooms.drop()
db.reviews.drop()
db.users.drop()

# Insert sample users
users_collection = db.users
users_collection.insert_many([
    {"_id": ObjectId(), "email": "user@nyu.edu", "password": generate_password_hash("password"), "is_admin": False},
    {"_id": ObjectId(), "email": "admin@nyu.edu", "password": generate_password_hash("password"), "is_admin": True},
])

# Insert sample pins (buildings)
pins_collection = db.pins
pins = pins_collection.insert_many([
    {"_id": ObjectId(), "name": "Bobst Library", "lat": 40.7295,
        "lng": -73.9972,},
    {"_id": ObjectId(), "name": "Kimmel Center","lat": 40.729822, "lng": -73.997919},
    {"_id": ObjectId(), "name": "La Maison Francaise", "lat": 40.731198931788775, "lng": -73.9954126045658},
    {"_id": ObjectId(), "name": "enter for Data Science", "lat": 40.73505683087452, "lng": -73.99477187220378},
    {"_id": ObjectId(), "name": "School of Professional Studies", "lat": 40.73456147370915, "lng": -73.99369068578089}
])

# Insert sample bathrooms
bathrooms_collection = db.bathrooms
bathrooms = bathrooms_collection.insert_many([
    {"_id": ObjectId(), "label": "1st Floor Unisex", "location_id": pins.inserted_ids[0], "floor": 1, "type": "Communal", "orientation": "Unisex", "sinks": 3, "toilets": 2, "img_url": "https://images.pexels.com/photos/1454804/pexels-photo-1454804.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"},
    {"_id": ObjectId(), "label": "2nd Floor Men's", "location_id": pins.inserted_ids[1], "floor": 2, "type": "Private", "orientation": "Male", "sinks": 1, "toilets": 1, "img_url": "https://images.pexels.com/photos/1571462/pexels-photo-1571462.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"},
    {"_id": ObjectId(), "label": "1st Floor Women's", "location_id": pins.inserted_ids[2], "floor": 1, "type": "Private", "orientation": "Female", "sinks": 1, "toilets": 1, "img_url": "https://images.pexels.com/photos/342800/pexels-photo-342800.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"},
    {"_id": ObjectId(), "label": "2nd Floor Women's", "location_id": pins.inserted_ids[3], "floor": 2, "type": "Communal", "orientation": "Female", "sinks": 2, "toilets": 1, "img_url": "https://images.pexels.com/photos/262005/pexels-photo-262005.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"},
    {"_id": ObjectId(), "label": "2nd Floor Unisex", "location_id": pins.inserted_ids[4], "floor": 2, "type": "Communal", "orientation": "Unisex", "sinks": 2, "toilets": 1, "img_url": "https://images.pexels.com/photos/3935352/pexels-photo-3935352.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"},
    {"_id": ObjectId(), "label": "2nd Floor Men's Communal", "location_id": pins.inserted_ids[4], "floor": 2, "type": "Communal", "orientation": "Male", "sinks": 2, "toilets": 1, "img_url": "https://images.pexels.com/photos/6487944/pexels-photo-6487944.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"}
])

# Insert sample reviews
reviews_collection = db.reviews
reviews_collection.insert_many([
    {"_id": ObjectId(), "bathroom_id": bathrooms.inserted_ids[0], "rating": 4, "comment": "Clean and spacious.", "date": datetime.now(timezone.utc)},
    {"_id": ObjectId(), "bathroom_id": bathrooms.inserted_ids[1], "rating": 3, "comment": "Could use more lighting.", "date": datetime.now(timezone.utc)},
    {"_id": ObjectId(), "bathroom_id": bathrooms.inserted_ids[2], "rating": 5, "comment": "Very private and well maintained.", "date": datetime.now(timezone.utc)},
    {"_id": ObjectId(), "bathroom_id": bathrooms.inserted_ids[3], "rating": 2, "comment": "Not very clean.", "date": datetime.now(timezone.utc)},
    {"_id": ObjectId(), "bathroom_id": bathrooms.inserted_ids[4], "rating": 4, "comment": "Good condition, but can be crowded.", "date": datetime.now(timezone.utc)},
    {"_id": ObjectId(), "bathroom_id": bathrooms.inserted_ids[5], "rating": 3, "comment": "Average, but functional.", "date": datetime.now(timezone.utc)}
])

print("Sample database initialized successfully!")