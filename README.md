# Kroky Scraper Documentation

This Flask application scrapes the daily menu from the Kroky website (https://www.kroky.si/) and returns it as a JSON response.

## Requirements

* Flask (https://flask.palletsprojects.com/en/2.3.x/)
* requests (https://requests.readthedocs.io/)
* Beautiful Soup 4 (https://beautiful-soup-4.readthedocs.io/)

## Functionality


### /Kroky

1. **Retrieves User Credentials:** It expects the username and password to be provided as query parameters (`username` and `password`) in the request URL.
2. **Login:** It attempts to log in to the Kroky website using the provided credentials.
3. **Scrapes Menu:** If login is successful, it scrapes the main URL to extract the daily menu for the weekdays (Monday to Saturday).
4. **Returns JSON:** Finally, the script returns the constructed menu list as a JSON-formatted response.

### /Select_Meal
1. **Retrieves User Credentials:** It expects the username and password to be provided as query parameters (`username` and `password`) in the request URL.
2. **Login:** It attempts to log in to the Kroky website using the provided credentials.
3. **POSTING DATA** If login is successful then it proseds to create json based on `date` and `id` and it selects that meal.
4. **Returns Message** Finally, if everything went smoothly and without any errors it will return `Meal selected successfuly!` else it will return error.


## Usage Tutorial

**1. Set Up the Environment:**

   - Install the required libraries: `pip install Flask requests beautifulsoup4

   - Run the code in python executer

   - Get data from api


### Kroky - json with all meals in that week with bool for selected meal
#### Curl
```bash
 curl -X GET http://localhost:5000/kroky?username=YOUR_USERNAME&password=YOUR_PASSWORD
 ```

#### Web Url
```bash
http://localhost:5000/kroky?username=YOUR_USERNAME&password=YOUR_PASSWORD
```

### Select_meal
#### Curl
```bash
curl -X GET http://127.0.0.1:5000/select_meal -H "Content-Type: application/json" -d '{"username": "YOUR_USERNAME", "password": "YOUR_PASSWORD"}'
```
#### Web Url
```bash
http://127.0.0.1:5000/select_meal?username=YOUR_USERNAME&password=YOUR_PASSWORD&date=DATE_OF_MEAL&id=CATEGORY_OF_MEAL
```
