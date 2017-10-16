# Basic Hotel

## Problem description

Choosing the programming language of your choice, implement a simple REST API that:
* takes care of the basic CRUD operations on a hypothetical Hotel model, allowing to manipulate its basic attributes (id, name, address, star_rating, and accomodation_type)

* provides a method that allows searching for a hotel by typing part of its name or address

Then use Ruby on Rails to build a simple web application that consumes the aforementioned API in all its CRUD operations, and build a simple autocomplete search box to look for a given hotel using the other API method.

Requirements:

* The API and the web application should be developed and deployed as two independent systems

* You can assume the data that describes the catalog of hotels is available to you in any storage/DB solution, feel free to use whatever you think is the best for the sake of task (and explain why)

* Deploy your solution on Heroku (or anywhere else where we can try it out of the box)

* Build a working solution: it doesn't have to be perfect, but explain the reasoning behind the trade­offs you made


# Work done

Web: `http://ec2-54-162-116-194.compute-1.amazonaws.com:3000/` but please read this README first.

## System Description
This project shows a way to design and implement a very basic hotel management platform.

The system is divided into two distinct components: **Web** and **API**.

### Web
The web app is built using Ruby on Rails and allows the use to perform the most basic operations (create hotel, retrieve hotel, update hotel, delete hotel and search through autocompletion) through an user interface.

### API
The API was developed in Python 3 (Flask) and it is used as an interface betweem the Web app and the database. All the operations performed in the web app are relegated to the API. So the API is responsible by the creation, retrieval, update and deletion of hotels from the database.

The root endpoint is `/api/v1.0/hotels/`. The use of `/v1.0/` is useful for versioning since we can implement a new version of the API (let's say `2.0`) without changing anything from the version `1.0`. This way, a client using the version `1.0` can still use it without any change and at the same time new clients can start using the new version `2.0`

Available operations:
* Create Hotel:
  * Endpoint: `/api/v1.0/hotels/`
  * Method: `POST`
  * Body: `{
 	'name': <hotel_name>,
 	'address': <hotel_address,
 	'accommodation_id': <accommodation_id>,
 	'stars_rating_id': <stars_rating_id>
 }`
  * Headers: `Content-Type: application/json`

* Retrieve Hotel:
  * Endpoint: `/api/v1.0/hotels/<:id>`
  * Method: `GET`

* Update Hotel:
  * Endpoint: `/api/v1.0/hotels/<:id>`
  * Method: `PUT`
  * Body: `{
 	'name': <hotel_name>,
 	'address': <hotel_address,
 	'accommodation_id': <accommodation_id>,
 	'stars_rating_id': <stars_rating_id>`
 }`
  * Headers: `Content-Type: application/json`

* Delete Hotel:
  * Endpoint: `/api/v1.0/hotels/<:id>`
  * Method: `DELETE`

* Retrieve All Hotels:
  * Endpoint: `/api/v1.0/hotels/`
  * Method: `GET`

* Get Suggestions:
  * Endpoint: `/api/v1.0/suggestions/`
  * Method: `POST`
  * Body: `{
 	'term': <term>
 }`
  * Headers: `Content-Type: application/json`

* Retrieve All Accommodations Type:
  * Endpoint: `/api/v1.0/accommodations/`
  * Method: `GET`

* Retrieve All Stars Rating:
  * Endpoint: `/api/v1.0/5000/api/v1.0/stars_rating/`
  * Method: `GET`


### Installation
If you want to run both components in your local machine you will need to:

1. Install MySQL server (user `root` and no password);

2. Run the `db.sql` (can be found in root directory of `api` folder) in your MySQL server

3. Install `requirements.txt` in `api` root directory

4. Install Ruby (version > 2.1)

5. Install Ruby on Rails

6. Run `bundle install` in `web` root directory

Then in with two terminals just run (you can use one terminal only if you run the processes in background `&`:

1. `python runserver.py` in `api` directory

2. `rails server` in `web` directory

## Online Service
**I have both services running in AWS. To access the web app just open your browser and visit `http://ec2-54-162-116-194.compute-1.amazonaws.com:3000/`**

# Notes

### Improvements
There are a lot of things to improve and some are easy to spot. 

Due the small amount of time I had to do this part of the challenge, I can point some problems I know that exist:

1. UI is minimal;

2. I'm not handling errors properly (some examples):
    * If the API is down you cannot open the web platform
    * I'm not handling responses with status code != 200 so no proper error handling

3. The autocomplete should be an overlayed box right next to the search box but because I didn't explore too much the UI I'm showing the autocompletion as hotel objects (as you can understand, the step from that to a pure autocompletion is very very small - instead of showing the object itself, I would show the name/address only and wait for the user to click on);

4. The text search using wildcards can be less effective with MySQL when the database grows to the millions of entries (it can be a problem specially in autocompletion which must give some feedback to the user as fast as possible). Since we are searching text, we might use ElasticSearch which is a search engine;

5. I'm not using any kind of caching, etc.

6. It was the second time I worked with ruby and rails so might be there some place to improve but I like the challenge of learn a new language and framework;

7. The system is running in the most basic AWS EC2 instance so there must be some network delays;

8. There is no input validation in create/edit form. Bootstrap does some work with that when the fields are marked as required but as you know there are ways to circumvent the JS behaviour since it runs in the client side and the request being sent to the server can be changed after the JS validation;

9. Make both the API and the web app more configurable and less hard coded (like database host/port and credentials are hardcoded, API url hardcoded, etc.);

10. There is API authentication.

### Trade-offs
1. It was not clear how the autocompletion should work, since we can have different autocompletion algorithms. For example, we can try to match a continuous strings (both starting the match in the beginning of the name/address or match any part of the name/address), we can also have a autocompletion that tokenizes a string (like Google) and tries to match the multiple parts, etc. I've implemented the first option: continuous string to be matched in any part of the hotel name/address.

2. The database choice, as mentioned before, can be a subject of discussion.
