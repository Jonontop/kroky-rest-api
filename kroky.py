from flask import Flask, jsonify, request
import requests
import bs4
import json

app = Flask(__name__)


@app.route('/kroky', methods=['GET'])
def kroky_command():
    # Get username and password from query parameters
    username = request.args.get('username')
    password = request.args.get('password')
    pos = request.args.get('pos')

    if not pos:
        pos = 0

    if not username or not password:
        return "Please provide both username and password as query parameters"

    day = ["pon", "tor", "sre", "cet", "pet", "sob"]
    main_url = "https://www.kroky.si/2016/"
    menu = []

    with requests.Session() as session:
        # Post the login data
        try:
            response = session.post(main_url, data={"username": username, "password": password}, params={"mod": "register", "action": "login"})
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

        if response.ok:
            print("Login successful")

            # Access the main URL using the same session
            main_response = session.get(main_url, params={"mod": "register", "action": "order", "pos": pos})

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
        

@app.route('/select_meal', methods=['GET'])
def select_meal():
    username = request.json.get('username')
    password = request.json.get('password')
    date = request.json.get("date")
    id = request.json.get("id")

    if not username or not password or not date or not id:
        print("Test")
        return "Please provide username, password, day, and id", 400

    selection_url = "https://www.kroky.si/2016/"
    success_message = "Meal selected successfully!"
    
    with requests.Session() as session:
        # Post the login data
        try:
            session.post(selection_url, data={"username": username, "password": password}, params={"mod": "register", "action": "login"})
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
            
        # Data to select the meal
        selection_data = {
            "c": int(34764),
            "date": str(date), #2024-12-02
        }
            
        # Send the POST request to select the meal
        selection_response = session.post(selection_url, data=selection_data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, params={"mod": "register", "action": "user2date2menu"})
        
        if not selection_response.ok:
            return f"Failed to select meal with status code: {selection_response.status_code}", 500

        return success_message



if __name__ == '__main__':
    app.run(debug=True, port=5002)