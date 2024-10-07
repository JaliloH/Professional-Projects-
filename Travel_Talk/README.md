# Module 1 Group Assignment

CSCI 5117, Spring 2024, [assignment description](https://canvas.umn.edu/courses/413159/pages/project-1)

## App Info:

* Team Name: Ajay
* App Name: Travel Talk
* App Link: https://travel-talk.onrender.com/

### Students

* Abdou-Aljalil Hammida, hammi110@umn.edu
* Amanda Hertzel, hertz109@umn.edu
* Yousef Mahayni, mahay004@umn.edu
* Allen Nhan, nhan0008@umn.edu


## Key Features

**Describe the most challenging features you implemented
(one sentence per bullet, maximum 4 bullets):**

* Search through Google Maps API
* Linked Google Maps result to create_review form fields
* Allowed users to customize their username while remaining compatable with database and the Auth0 login

## Testing Notes

**Is there anything special we need to know in order to effectively test your app? (optional):**

* Comments are able to be edited if you click the comment text.
* To create a review, you must first locate a place/search a place on the main page. Then, you click a place, and then you click the "create review" button. This will auto populate all place information for the review.
* My Feed is the global 10 most recent reviews.
* My Reviews is your 10 most recent reviews.
* On "My Feed" you can filter through several categories by hovering over the search bar and selecting a filter criteria.


## Screenshots of Site

**[Add a screenshot of each key page (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository)
along with a very brief caption:**

![Explore Page](/screenshots_of_site/explore.png?raw=true "Explore Page")
Search for places to review using the map or name of the establishment

![Review Place](/screenshots_of_site/review_place.png?raw=true "Review Place")
After searching, select the desired place to review and see their existing reviews and/or create a new review

![Create Review](/screenshots_of_site/create_review.png?raw=true "Create Review")
Fill out the form for your review and post it!

![View Reviews](/screenshots_of_site/my_feed.png?raw=true "View Reviews")
View and search your timeline, sorted by most recent reviews first

![Edit Review](/screenshots_of_site/edit_review.png?raw=true "Edit Review")
Opinions are always changing! Feel free to revisit and change your reviews


## Mock-up 

There are a few tools for mock-ups. Paper prototypes (low-tech, but effective and cheap), Digital picture edition software (gimp / photoshop / etc.), or dedicated tools like moqups.com (I'm calling out moqups here in particular since it seems to strike the best balance between "easy-to-use" and "wants your money" -- the free teir isn't perfect, but it should be sufficient for our needs with a little "creative layout" to get around the page-limit)

In this space please either provide images (around 4) showing your prototypes, OR, a link to an online hosted mock-up tool like moqups.com

**[Add images/photos that show your paper prototype (around 4)](https://stackoverflow.com/questions/10189356/how-to-add-screenshot-to-readmes-in-github-repository) along with a very brief caption:**

Mock up Figma link: https://www.figma.com/file/MTItI6uf5faR4aoSzcrdtC/Travel-Talk?type=design&node-id=0%3A1&mode=design&t=yBZT7i1ivZB0VfPK-1


## External Dependencies

**Document integrations with 3rd Party code or services here.
Please do not document required libraries. or libraries that are mentioned in the product requirements**

* Library or service name: description of use
* ...

**If there's anything else you would like to disclose about how your project
relied on external code, expertise, or anything else, please disclose that
here:**
- [Used W3 Schools for creating the dropdown menu](https://www.w3schools.com/howto/howto_css_dropdown.asp)
- [For expertise, we also used a forum in order to properly create our CSS for the stars](https://stackoverflow.com/questions/77517679/how-to-make-5-star-rating-with-css)
- [Used W3 Schools to create the browse filter in Feed](https://www.w3schools.com/howto/howto_js_filter_lists.asp)
- [Used google maps JS api to create map and search bar]()
- [Used google maps places api to get list locations](https://developers.google.com/maps/documentation/javascript/places)
- [Used google maps geocode api to determine where user clicked on the map and to pull users current location](https://developers.google.com/maps/documentation/geocoding/overview)

