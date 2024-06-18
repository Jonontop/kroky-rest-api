# Kroky Scraper Documentation

This Flask application scrapes the daily menu from the Kroky website (https://www.kroky.si/) and returns it as a JSON response.

## Requirements

* Flask (https://flask.palletsprojects.com/en/2.3.x/)
* requests (https://requests.readthedocs.io/)
* Beautiful Soup 4 (https://beautiful-soup-4.readthedocs.io/)

## Functionality

The script performs the following actions:

1. **Retrieves User Credentials:** It expects the username and password to be provided as query parameters (`username` and `password`) in the request URL.
2. **Login:** It attempts to log in to the Kroky website using the provided credentials.
3. **Scrapes Menu:** If login is successful, it scrapes the main URL to extract the daily menu for the weekdays (Monday to Saturday).
4. **Parses Menu:** The script parses the HTML content using Beautiful Soup and constructs a list of dictionaries representing the menu for each day. Each dictionary contains the following information:
   - Day abbreviation (e.g., "pon" for Monday)
   - A list of menus for the day, where each menu entry is a dictionary with:
     - Menu number (e.g., "1. menu")
     - Menu description (text content of the `.lepo_ime` class)
     - Selection status (True if the menu item is selected, False otherwise)
5. **Returns JSON:** Finally, the script returns the constructed menu list as a JSON-formatted response.

## Code Structure

The code is organized as follows:

- **Imports:** The necessary libraries (`Flask`, `requests`, and `bs4`) are imported.
- **Flask App Initialization:** A Flask app instance is created.
- **`kroky_command` Route:** This route handles GET requests to the `/kroky` endpoint.
   - **Retrieves Credentials:** It extracts the username and password from the query parameters.
   - **Input Validation:** It checks if both username and password are provided. If not, it returns an error message.
   - **Defines URLs:** It defines the main URL and login URL for the Kroky website.
   - **Initiates Session:** It creates a `requests.Session` object to maintain cookies across requests.
   - **Login Request:** It attempts to log in to the Kroky website using `session.post` and provided credentials.
     - **Error Handling:** If a network error occurs, it returns an error message.
   - **Login Success:** If the login is successful, it proceeds to scrape the menu.
     - **Main URL Request:** It fetches the main URL using `session.get`.
     - **Soup Creation:** It parses the HTML content using Beautiful Soup.
     - **Iterates Through Days:** It iterates through a list of day abbreviations (`day`).
       - **Day Menu Initialization:** An empty dictionary (`day_menu`) is created for each day.
       - **Iterates Through Menus:** It iterates through a loop from 1 to 11 (assuming 11 menus per day).
         - **Scrapes Menu Entries:** It finds all table cells (`td`) with the appropriate class (`st_menija_{k}_{i}`) for the current menu number (`k`) and day abbreviation (`i`).
           - **Menu Entry Creation:** For each menu entry, it creates a dictionary with:
             - Menu number (formatted as a string)
             - Menu description (extracted from the `.lepo_ime` class span)
             - Selection status (based on the presence of the `checked` attribute on the input element)
         - **Appends Menu Entries:** The menu entry dictionary is appended to the `day_menu` list.
       - **Appends Day Menu:** The `day_menu` dictionary for the current day is appended to the `menu` list.
     - **Prints Menu:** The scraped menu list is printed for debugging purposes (optional).
     - **Returns JSON:** The script returns the `menu` list as a JSON response.
   - **Main URL Access Failure:** If the main URL cannot be accessed, it returns an error message indicating the status code.
- **Login Failure:** If the login fails, it returns an error message indicating the status code.
- **Main Execution:** If the script is run directly (`if __name__ == '__main__'`), it runs the Flask app in debug mode (set `debug=True` for development).

## Usage Tutorial

**1. Set Up the Environment:**

   - Install the required libraries: `pip install Flask requests beautifulsoup4

   - Run the code in python executer

   - Get data from api

### Curl
```bash
 curl -X GET http://localhost:5000/kroky?username=YOUR_USERNAME&password=YOUR_PASSWORD
 ```

### Web Url
   - http://localhost:5000/kroky?username=YOUR_USERNAME&password=YOUR_PASSWORD
