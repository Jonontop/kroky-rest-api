from flask import Flask, jsonify, request
import requests
import bs4

app = Flask(__name__)


@app.route('/kroky', methods=['GET'])
def kroky_command():
    # Get username and password from query parameters
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return "Please provide both username and password as query parameters"

    day = ["pon", "tor", "sre", "cet", "pet", "sob"]
    main_url = "https://www.kroky.si/2016/?mod=register&action=order&pos=-3"
    login_url = "https://www.kroky.si/2016/?mod=register&action=login"
    menu = []

    with requests.Session() as session:
        # Post the login data
        try:
            response = session.post(login_url, data={"username": username, "password": password})
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

        if response.ok:
            print("Login successful")

            # Access the main URL using the same session
            main_response = session.get(main_url)

            if main_response.ok:
                soup = bs4.BeautifulSoup(main_response.text, "html.parser")
                print(soup)
                for i in day:
                    day_menu = {}
                    day_menu[i] = []
                    for k in range(1, 12):
                        for j in soup.find_all("td", class_=f"st_menija_{k}_{i}"):
                            day_menu[i].append({
                                f"{k}. menu": j.find("span", class_="lepo_ime").text,
                                "selected": True if j.find("input").has_attr("checked") else False
                            })
                    menu.append(day_menu)

                print(menu)  # Print the menu list
                return jsonify(menu)  # Return the menu as JSON
            else:
                return f"Failed to access main URL: {main_response.status_code}"
        else:
            return f"Login failed: {response.status_code}"
        

@app.route('/select_meal', methods=['POST'])
def select_meal():
    username = request.json.get('username')
    password = request.json.get('password')
    day = request.json.get('day')  # e.g., "pon", "tor", etc.
    menu_number = request.json.get('menu_number')  # e.g., 1, 2, 3... corresponding to the menu option

    if not username or not password or not day or not menu_number:
        return "Please provide username, password, day, and menu_number", 400

    login_url = "https://www.kroky.si/2016/?mod=register&action=login"
    selection_url = "https://www.kroky.si/2016/?mod=register&action=order"  # You need to verify this URL
    success_message = "Meal selected successfully!"
    
    with requests.Session() as session:
        try:
            # Log in first
            response = session.post(login_url, data={"username": username, "password": password})
            if not response.ok:
                return f"Login failed with status code: {response.status_code}", 401
            
            # Mimic selecting the meal, just as the browser does when you submit the form.
            # You may need to customize these parameters based on what the site expects.
            selection_data = {
            '2024-12-02': menu_number,  # This corresponds to the day and the selected menu option
            #'xxl[34764]': '1' if xxl_selected else '',  # Only include if XXL is selected
            'menu_id': '1',  # The menu ID from the HTML, adjust if needed
            'cat_id': '34764',  # Category ID from the HTML, adjust if needed
            # Add any other hidden inputs or CSRF tokens from the form, if necessary
            }
            
            # Send the POST request to select the meal
            selection_response = session.post(selection_url, data=selection_data)
            if not selection_response.ok:
                return f"Failed to select meal with status code: {selection_response.status_code}", 500

            return success_message
        
        except requests.exceptions.RequestException as e:
            return f"An error occurred while processing the request: {e}", 500


if __name__ == '__main__':
    app.run(debug=False, port=5002)
