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

if __name__ == '__main__':
    app.run(debug=False)
