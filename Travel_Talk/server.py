import requests
import ast
from flask import Flask, render_template, request, jsonify, make_response
from db_cmds import create_app, edit_comment, post_comment, get_comments_for_review, delete_comment, check_if_user_owns_comment, check_if_user_owns_review, delete_review, get_user, edit_review, get_users_review, get_user_by_id, add_user, update_user, add_review, get_all_user_reviews, get_recent_reviews, get_review, get_location_reviews_by_id, get_bar_reviews, get_beauty_reviews, get_cafe_reviews, get_food_drink_reviews, get_restaurant_reviews, get_store_reviews, get_reviews_by_stars_asc, get_reviews_by_stars_desc, get_five_star_reviews, get_four_star_reviews, get_three_star_reviews, get_two_star_reviews, get_one_star_reviews


# app = Flask(__name__)
app = create_app() # Allen did it this way, but feel free to change the DB set up / initialization


# --> AUTH0 START HERE
from flask import redirect, session, url_for
import os
from os import environ as env # so we can do os.env instead of os.environ
import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth

app.secret_key = os.environ['FLASK_SECRET']
oauth = OAuth(app)
oauth.register(
        "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={ # keyword arguments
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
# NOTE: this has to match the callback url in our Auth0 "Application URI" area
def callback():
    token = oauth.auth0.authorize_access_token()
    user_exists = get_user(token['userinfo']['sub'])

    # if the current user exists, redirect them to the homepage
    if (user_exists):
        user = user_exists[0]
        session['user'] = {
            'sub': user[0],
            'avatar': user[1],
            'username': user[2],
            'email': user[3]
        }
        return redirect("/")
    
    else:
        session['user'] = {
            'sub': token['userinfo']['sub'],
            'avatar': token['userinfo']['picture'],
            'username': token['userinfo']['name'],
            'email': token['userinfo']['email']
        }
        add_user(token)

    # new user, therefore direct them to a welcome page
    return redirect("/welcome")

@app.route("/logout")
def logout():
    session.clear() # deletes session info
    return redirect( # brings them to the logout page page
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("mainpage", _external=True), # returns them to our main page (index.html)
                "client_id": env.get("AUTH0_CLIENT_ID"), 
            },
            quote_via=quote_plus,
        )
    )

# Put this before rendering pages like myReviews, createReviews, etc
def authorization_interceptor():
    if 'sub' in session:
        return
    else:
        login()
# --> AUTH0 END HERE

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

@app.route('/', methods=['GET'])
def mainpage(): ## Main page, accessible to all.
    return render_template('index.html')

@app.route('/welcome', methods=['GET'])
def welcome(): ## Welcome page, accessible to all
    return render_template('welcome.html')

@app.route('/feed')
def feed(): ## Main feed, do not need to be logged in.
    reviews = get_recent_reviews()
    return render_template('feed.html', reviews=reviews)

@app.route('/feed/<filter>')
def feed2(filter): ## Main feed, do not need to be logged in.
    if (filter == "bars"):
        print("hiii")
        reviews = get_bar_reviews()
    elif (filter == "beauty"):
        reviews = get_beauty_reviews()
    elif (filter == "cafes"):
        reviews = get_cafe_reviews()
    elif (filter == "edible"):
        reviews = get_food_drink_reviews()
    elif (filter == "restaurants"):
        reviews = get_restaurant_reviews()
    elif (filter == "stores"):
        reviews = get_store_reviews()
    elif (filter == "moststars"):
        reviews = get_reviews_by_stars_desc()
    elif (filter == "leaststars"):
        reviews = get_reviews_by_stars_asc()
    elif (filter == "fivestars"):
        reviews = get_five_star_reviews()
    elif (filter == "fourstars"):
        reviews = get_four_star_reviews()
    elif (filter == "threestars"):
        reviews = get_three_star_reviews()
    elif (filter == "twostars"):
        reviews = get_two_star_reviews()
    elif (filter == "onestar"):
        reviews = get_one_star_reviews()
    else:
        return render_template("error.html", error="Invalid filter criteria"), 404
    return render_template('feed.html', reviews=reviews)

@app.route('/review')   ## Viewing a single review, delete & edit buttons appear if user owns review
def singleReview():
    review_id = request.args.get('id') ## If a review id isn't given, go back to home?
    if not review_id: ## Review_id not provided
        return render_template("error.html", error="Review id not provided"),400
    reviews = get_review(review_id)
    if len(reviews) == 0: ## No review with that id exists
        return render_template("error.html", error="No review with that id exists"), 404
    user_owns_review = False
    if reviews[0][1] == getSub(): ## if user owns the review
        user_owns_review = True
    is_user_logged_in = False
    if getSub():
        is_user_logged_in = True
    comments = get_comments_for_review(review_id)
    return render_template('review_page.html', reviews=reviews, user_owns_review=user_owns_review, comments=comments, is_user_logged_in=is_user_logged_in,current_user_sub=getSub())

# @app.route("/api/userReviews", methods=["GET"])
# def apiUserReviews(): ## Returns all reviews of a user. 
#     authorization_interceptor() ## will establish a session, or check if it exists
#     if getSub(): ## session has been established
#         user_reviews = get_all_user_reviews(getSub())
#         return jsonify(user_reviews)
#     else:
#         return jsonify("error") ## If there is no session established, this is a 401 error
        

@app.route('/myReviews') ## users personal reviews
def myReviews():
    authorization_interceptor()
    if getSub():
        reviews = get_all_user_reviews(getSub())
    else:
        return render_template("error.html", error="Session not established, please log in"), 401
    return render_template("my_reviews.html", reviews=reviews) ##  Myreviews will fetch the api/userReviews

@app.route("/api/recentReviews", methods=["GET"]) ## globally recent reviews 
def apiAllReviews(): ## Get 10 most recent recent reviews
    ## No need to be logged in!
    reviews = get_recent_reviews()
    return jsonify(reviews)
# @app.route("")
# @app.route("/login", methods=["GET"])
# def login():
#     return render_template("login.html")


@app.route("/search", methods=["GET"])
def search():
    search_results_dict = {}
    if(request.args.get("lat") == None or request.args.get("long") == None):
        placeIdurl = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={request.args.get("search_value")}&key=AIzaSyAxVyQIWCItA5uLeG8sk0O0lMZjnA2qReU';
        response = requests.get(placeIdurl)
        lat = response.json()["results"][0]["geometry"]["location"]["lat"]
        lng = response.json()["results"][0]["geometry"]["location"]["lng"]
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=100&key=AIzaSyAxVyQIWCItA5uLeG8sk0O0lMZjnA2qReU'
    else:
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={request.args.get("lat")},{request.args.get("long")}&radius=100&key=AIzaSyAxVyQIWCItA5uLeG8sk0O0lMZjnA2qReU'
    

    api_response = requests.get(url)
    json_response = api_response.json()
    type = "point of interest "
    types_list = ["food", "cafe", "restaurant", "spa", "beauty_salon", "bar", "store"]
    for x in range(len(json_response["results"])):
        types = json_response["results"][x]["types"]
        for type in types:
            if type in types_list:
                # print(json_response["results"][x]["name"])
                if("photos" in json_response["results"][x]):
                    photo_ref = json_response["results"][x]["photos"][0]["photo_reference"]
                    photo_url = f'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key=AIzaSyAxVyQIWCItA5uLeG8sk0O0lMZjnA2qReU'
                    search_results_dict[json_response["results"][x]["name"]] = [photo_url, json_response["results"][x]["vicinity"], json_response["results"][x]["place_id"], type]
                break
    

    return redirect(url_for('search_results', search_results_dict=search_results_dict))

@app.route("/search_results", methods=["GET"])
def search_results():
    search_results = request.args['search_results_dict']
    search_results_dict = ast.literal_eval(search_results)
    return render_template("search_results.html", search_results_dict=search_results_dict)

@app.route("/get_reviews")
def get_reviews():
    location_name = request.args.get("location_name")
    location_photo = request.args.get("location_photo")
    location_id = request.args.get("location_id")
    location_type = request.args.get("location_type")
    reviews = get_location_reviews_by_id(location_id)
    return render_template("location_view.html", location_name=location_name, location_photo=location_photo, location_type=location_type, location_id=location_id, reviews=reviews)


@app.route("/createreview/<location_name>,<location_type>,<place_id>", methods=["GET"])
def createReview(location_name, location_type, place_id): ## when user fills out the post, it'll send all information to here
    if request.method == "GET":
        authorization_interceptor() ## Ensure user is logged in
        if not getSub():
            # Sub sticll not established
            return render_template("error.html", error="Please login before posting a review"), 401
        return render_template("create_review.html", location_name=location_name, location_type=location_type, place_id=place_id)
@app.route("/createreview", methods=["POST"]) 
def createReview2():
    if request.method == "POST":
        authorization_interceptor() ## Ensure user is logged in
        if not getSub():
            # Sub still not established
            return render_template("error.html", error="Please login before posting a review"), 401
        review_text = request.form.get("review-text")
        place_reviewed = request.form.get("place-reviewed")
        place_type = request.form.get("create-place-type")
        star_count = request.form.get("rating")
        place_id = request.form.get("place-id")
        #image = request.files["image"]
        #print(image.read())    #<FileStorage: 'chicken.jpeg' ('image/jpeg')>
        if review_text and place_reviewed and place_type and star_count and place_id:
            if len(review_text) > 500:
                return render_template("error.html", error="Please limit your input to a maximum of 500 characters."), 400
            add_review(getSub(),place_reviewed, place_type, star_count, review_text,place_id)
            return redirect(url_for("feed"))
        else: ## Missing fields
            return render_template("error.html", error="Missing fields in review"), 400

@app.route("/editReview", methods=["GET","POST"])
def editReview():
    if request.method == "GET": ## Getting the edit_review page
        review_id = request.args.get("id")
        if not review_id:
            return render_template("error.html", error="Review id not provided"),400
        review_data = get_review(review_id)
        if len(review_data) == 0: ## Review doesn't exist
            return render_template("error.html", error="Review does not exist"),404
        ret_review = review_data[0]
        user_owns_review = ret_review and ret_review[1] == getSub() ## Check if user owns the review they are editing
        if not user_owns_review:
            return render_template("error.html", error="User does not own review"), 403
        return render_template("edit_review.html", review=ret_review)
    elif request.method == "POST":
        ## Check if user who posted actually owns the review
        review_id = request.form.get("id")
        if not review_id:
            return render_template("error.html", error="Review id not provided"), 400
        review = get_users_review(getSub(),review_id)
        if len(review) > 0: ## Indicates user does actually own review with review_id.
            review_text = request.form.get("edit-text")
            place_reviewed = request.form.get("edit-place-name")
            place_type = request.form.get("edit-place-type")
            star_count = request.form.get("rating")
            if review_text and place_reviewed and place_type and star_count:
                if star_count > "5" or star_count < "0":
                    return render_template("error.html",error="Invalid star-count."), 400
                if len(review_text) > 500:
                    return render_template("error.html",error="Please limit your input to a maximum of 500 characters."), 400
                edit_review(review_id, getSub(),place_reviewed, place_type, star_count, review_text)
                return redirect(url_for("singleReview", id=review_id)) # Successfully edited
            else: ## Missing fields
                return render_template("error.html", error="Missing fields in review"), 400
        else: ## User unauthorized to edit this review
            return render_template("error.html", error="Unauthorized to edit review"), 403

@app.route("/deleteReview", methods=["POST","DELETE"]) 
def deleteReview():
    review_id = request.args.get("id")
    if not review_id:
        ## Review_id not provided
        return render_template("error", error="Review id not provided"), 400
    review = get_users_review(getSub(),review_id)
    if len(review) > 0:
        # Review exists and person owns
        delete_review(review_id,getSub())
        return redirect(url_for("feed"))
    else: ## Review doesn't exist OR they don't own it
        return redirect(url_for("feed"))

@app.route("/postComment", methods=["POST"])
def postComment():
    authorization_interceptor() ## Ensure user is logged in
    review_id = request.args.get("id")
    if not review_id:
        return render_template("error.html", error="Review id not provided"), 400
    sub = getSub()
    if not sub:
        return render_template("error.html",error="Must be logged in to post comment"), 401
    if len(get_review(review_id)) == 0:
        return render_template("error.html",error="No such review with id exists"), 404
    comment_text = request.form.get("comment-text")
    if comment_text:
        if len(comment_text) > 250:
            return render_template("error.html",error="Please limit your input to a maximum of 250 characters."), 400
        post_comment(sub, review_id, comment_text)
        return redirect(url_for("singleReview", id=review_id))
    else:
        return render_template("error.html", error="Missing fields for comment"), 400

def getSub():
    user = session.get("user")
    if session and user:
        if user.get("sub"):
            sub = user.get("sub")
            return sub
    return None
            
@app.route("/deleteComment", methods=["POST"])      
def deleteComment():
    comment_id = request.args.get("comment_id")
    if not comment_id:
        return render_template("error.html", error="Comment id not provided"), 400
    if len(check_if_user_owns_comment(comment_id,getSub())) == 0: ## No comment associated with comment_id and user logged in
        return render_template("error.html",error="Unauthorized to delete comment"), 403
    #If we get here, the comment exists and the user owns it
    review_id = delete_comment(comment_id,getSub())
    review_id = review_id[0]
    return redirect(url_for("singleReview", id=review_id))

@app.route("/editComment", methods=["GET","POST"])
def editComment():
    if request.method=="GET":
        comment_id = request.args.get("comment_id")
        if not comment_id:
            return render_template("error.html", error="Comment id not provided"), 400
        user_comment = check_if_user_owns_comment(comment_id,getSub())
        if len(user_comment) == 0:
            return render_template("error.html", error="Comment does not exist/unauthorized"),404
        user_owns_comment = user_comment and user_comment[0][1] == getSub() ## Check if user owns the comment they are editing
        if not user_owns_comment:
            return render_template("error.html", error="User does not own comment"),403
        print(user_comment)
        return render_template("edit_comment.html", comment=user_comment[0])
    if request.method=="POST":
        comment_id = request.form.get("comment_id")
        if not comment_id:
            return render_template("error.html", error="Comment id not provided"), 400
        user_comment = check_if_user_owns_comment(comment_id,getSub())
        if len(user_comment) == 0:
            return render_template("error.html", error="Comment does not exist/unauthorized"),404
        comment_text = request.form.get("comment-text")
        if comment_text:
            if len(comment_text) > 250:
                return render_template("error.html", error="Please limit your input to a maximum of 250 characters."),400
            review_id = edit_comment(comment_id,getSub(),comment_text)
            review_id = review_id[0]
            return redirect(url_for("singleReview", id=review_id))
        else:
            return render_template("error.html", error="Missing fields in comment"), 400

@app.route('/profile', methods=["GET"])
def profile():
    return render_template('edit_profile.html', avatar=session['user']['avatar'], username=session['user']['username'])

# @app.route('/api/updateavatar', methods=["POST"])
# def updateAvatar():
#     if ("avatar" in request.files):
#         updated_field = request.files.get('avatar')
#         # print(updated_filed)

#         update_user(session['user']['sub'], "avatar", updated_field) # database
#         sub = session['user']['sub']
#         username = session['user']['username']
#         email = session['user']['email']
#         session.clear()
#         session['user'] = {
#             'sub': sub,
#             'avatar': updated_field,
#             'username': username,
#             'email': email
#         }

#         return redirect('/profile')
#     else:
#         return redirect(url_for("profile"), 400)

@app.route('/api/updateusername', methods=["POST"])
def updateUsername():
    if ("username" in request.form):
        updated_field = request.form.get('username')

        update_user(session['user']['sub'], "username", updated_field) # database
        sub = session['user']['sub']
        avatar = session['user']['avatar']
        email = session['user']['email']
        session.clear()
        session['user'] = {
            'sub': sub,
            'avatar': avatar,
            'username': updated_field,
            'email': email
        }

        return redirect('/profile')
    else:
        return redirect(url_for("profile"), 400)

def check_if_session_exists():
    if ('user' in session):
        return True
    else:
        return False

@app.route('/api/session', methods=["GET"])
def check_session():
    if ('user' in session):
        return jsonify({'exists': True, 'user': session['user']})
    else:
        return jsonify({'exists': False})


@app.route('/images/<int:image_id>')
def get_image(image_id):    #https://blog.finxter.com/5-best-ways-to-convert-python-bytes-to-jpeg/
    # (get a cursor "cur")
    cur.execute("SELECT * FROM images where img_id=%s", (img_id,))
    image_row = cur.fetchone() # just another way to interact with cursors
    
    # in memory pyhton IO stream
    stream = io.BytesIO(image_row["img"])
        
    # use special "send_file" function
    return send_file(stream, attachment_filename=image_row["filename"])

@app.route('/aboutus')
def about_us():
    return render_template("about_us.html")

# pipenv run flask --app server.py run
# pipenv run flask run --port 9001          # run this for Postman since Apple took port 5000 from us -.-