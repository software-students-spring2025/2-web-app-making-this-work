from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, make_response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime

# load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(16)  # Generate random key for session management

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.get_database("Cluster0")

# Collections
pins_collection = db.pins
bathrooms_collection = db.bathrooms
reviews_collection = db.reviews
users_collection = db.users  # Users collection

# ==================================================
# Account Signup, Login, Logout, Delete.

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to login page if unauthenticated

class User(UserMixin):
    def __init__(self, user_id, email, is_admin):
        self.id = user_id
        self.email = email
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(user_id=str(user["_id"]), email=user["email"], is_admin=user["is_admin"])
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            user_obj = User(user_id=str(user["_id"]), email=user["email"], is_admin=user["is_admin"])
            login_user(user_obj)
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        is_admin = "admin_privileges" in request.form  # Checkbox for admin privileges

        if not email.endswith("@nyu.edu"):
            flash("You must use an NYU email to register!", "danger")
            return redirect(url_for("signup"))

        if users_collection.find_one({"email": email}):
            flash("Email already exists!", "danger")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({"email": email, "password": hashed_password, "is_admin": is_admin})

        flash("Account created! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    # print("Logging out user:", current_user.email)
    
    logout_user()  # <- does not actually work when remember=true with login_user().
    session.pop('_flashes', None)
    session.permanent = False
    session.clear()
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie('session', '', expires=0)  # invalidate session cookie
    flash("You have been logged out.", "info")
    return resp

@app.route("/delete_profile", methods=["POST"])
@login_required
def delete_profile():
    try:
        # get userID and delete user from the DB
        user_id = current_user.id
        result = users_collection.delete_one({"_id": ObjectId(user_id)})

        # if deletion successful: logout then redirect to login page
        if result.deleted_count == 1:
            logout()
            flash("Your profile has been deleted.", "info")
            return redirect(url_for("login"))
        else:
            flash("An error occurred. Please try again later.", "danger")
            return redirect(url_for("profile"))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for("profile"))

# ==================================================

# Map Page Route
@app.route("/")
@login_required
def home():
    return render_template("index.html")

# Search Page Route
@app.route("/search")
@login_required
def search():
    return render_template("search.html")

# Profile Page Route
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

# Dashboard for Admins Route
@app.route("/dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return "Access Denied", 403  # Restrict access to admins only

    # Fetch statistics from the database
    total_buildings = pins_collection.count_documents({})
    total_bathrooms = bathrooms_collection.count_documents({})
    normal_users = users_collection.count_documents({"is_admin": False})
    admin_users = users_collection.count_documents({"is_admin": True})
    total_reviews = reviews_collection.count_documents({})  # Count all reviews

    return render_template("dashboard.html", 
        total_buildings=total_buildings, 
        total_bathrooms=total_bathrooms,
        normal_users=normal_users,
        admin_users=admin_users,
        total_reviews=total_reviews
    )

# Individual Bathroom Page Route
@app.route("/bathroom/<bathroomID>")
@login_required
def bathroom(bathroomID):
    bathroom = bathrooms_collection.find_one({"_id": ObjectId(bathroomID)})
    bathroomName=pins_collection.find_one({"_id":bathroom.get("location_id")}).get("name")
    fullLocation = bathroomName+", Floor "+str(bathroom.get("floor"))
    reviews = reviews_collection.find({"bathroom_id": ObjectId(bathroomID)})
    imageURL=str(bathroom.get("img_url"))
    bathroom_name = bathroom.get("label", "Unknown Bathroom")
    imageURL = bathroom.get("img_url", None)

    # Get the location details using location_id from bathroom
    location = pins_collection.find_one({"_id": bathroom.get("location_id")})
    
    # Extract latitude and longitude from the location document
    latitude = location.get("lat")
    longitude = location.get("lng")
    
    i=0
    revSum=0
    for review in reviews:
        i+=1
        revSum+=review["rating"]
    revSum=revSum/i
    overallRating=""
    
    i=0
    while (i<revSum):
        i+=1
        if i>revSum:
            overallRating+="<i class='fa-solid fa-star-half-stroke'></i>"
        else:
            overallRating+="<i class='fa-solid fa-star'></i>"
    while (i<5):
        i+=1
        overallRating +="<i class='fa-regular fa-star'></i>"

    reviews = list(reviews_collection.find({"bathroom_id": ObjectId(bathroomID)}))
    # print(reviews)
    
    return render_template(
        "bathroom.html", 
        bathroomID=bathroomID,
        bathroom=bathroom, 
        rating=overallRating, 
        bathroomLocation=fullLocation, 
        bathroomImage=imageURL, 
        bathroomReviews=reviews, 
        user=current_user, 
        bathroomName=bathroom_name,
        latitude=latitude,
        longitude=longitude)

# Bathroom review page 
@app.route('/write_review/<bathroom_id>', methods=['GET', 'POST'])
@login_required
def write_review(bathroom_id):
    if request.method == 'POST':
        # Get form data
        review_text = request.form.get('review_text')
        rating = request.form.get('rating')


        # Insert the review into the MongoDB collection
        reviews_collection.insert_one({"bathroom_id": ObjectId(bathroom_id), "comment": review_text, "rating": int(rating), "date":datetime.now()})
        return redirect("/bathroom/"+bathroom_id)

    return render_template("write_review.html",bathroomID=bathroom_id)

# Admin edit bathrooms route
@app.route('/bathroom/<bathroomID>/update', methods=['POST'])
@login_required
def update_bathroom(bathroomID):
    # print("Session Admin Status:", session.get("is_admin"))
    if not current_user.is_admin:  # Check if user is admin
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    updated_fields = {
        "label": data.get("label"),
        "floor": int(data.get("floor", 0)),
        "orientation": data.get("orientation"),
        "type": data.get("type"),
        "sinks": int(data.get("sinks", 0)),
        "toilets": int(data.get("toilets", 0)),
        "img_url": data.get("img_url")
    }

    db.bathrooms.update_one({"_id": ObjectId(bathroomID)}, {"$set": updated_fields})
    return jsonify({"message": "Bathroom updated successfully!"})

# Get Pins Route
@app.route('/api/pins')
def get_pins():
    pins = list(db.pins.find({}, {"_id": 1, "name": 1, "lat": 1, "lng": 1}))  # Explicitly include _id

    # Convert MongoDB ObjectId to a string for JSON compatibility
    for pin in pins:
        pin['_id'] = str(pin['_id'])

    return jsonify(pins)

# helper function, converts ObjectId to string
def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    else:
        return obj

@app.route("/api/search", methods=["GET"])
def search_api():
    query = request.args.get("q", "").lower()
    floor_filter = request.args.get("floor")
    type_filter = request.args.get("type")
    orientation_filter = request.args.get("orientation")
    sinks_filter = request.args.get("sinks")
    toilets_filter = request.args.get("toilets")

    # fetch building by name (case-insensitive)
    building = pins_collection.find_one({"name": {"$regex": query, "$options": "i"}})

    # return empty list of bathrooms if no building found
    if not building:
        return jsonify({"bathrooms": []})
    
    bathroom_query = {"location_id": building["_id"]}

    if floor_filter:
        bathroom_query["floor"] = int(floor_filter)  # Convert to integer
    if type_filter:
        bathroom_query["type"] = type_filter  # Match bathroom type
    if orientation_filter:
        bathroom_query["orientation"] = orientation_filter
    if sinks_filter:
        bathroom_query["sinks"] = int(sinks_filter)  # Convert to integer
    if toilets_filter:
        bathroom_query["toilets"] = int(toilets_filter)  # Convert to integer

    # Fetch bathrooms that match filters
    bathrooms = list(bathrooms_collection.find(bathroom_query))

    # convert ObjectId fields to string
    building = convert_objectid(building)
    bathrooms = convert_objectid(bathrooms)

    # return bathrooms list as the response
    return jsonify({"bathrooms": bathrooms})

@app.route("/building/<building_id>")
@login_required
def view_building(building_id):
    # Fetch building details
    building = pins_collection.find_one({"_id": ObjectId(building_id)})

    if not building:
        return "Building not found", 404

    # Fetch bathrooms associated with this building
    bathrooms = list(bathrooms_collection.find({"location_id": ObjectId(building_id)}))

    return render_template("building.html", building=building, bathrooms=bathrooms)

if __name__ == "__main__":
    app.run(debug=True)
