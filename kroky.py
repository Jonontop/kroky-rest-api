import requests
import time
# import mysql.connector
import bs4

username = ""
password = ""

day = ["pon", "tor", "sre", "cet", "pet", "sob"]

main_url = "https://www.kroky.si/2016/?mod=register&action=order&pos=-3"
login_url = "https://www.kroky.si/2016/?mod=register&action=login"

"""mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

mycursor = mydb.cursor()"""


def kroky_command(username, password):
    menu = {}
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
                # print(soup.prettify())
                for i in day:
                    menu[i] = {}
                    for k in range(1, 12):
                        for j in soup.find_all("td", class_=f"st_menija_{k}_{i}"):
                            menu[i][f"{k}. meni"] = {
                                "ime": j.find("span", class_="lepo_ime").text,
                                "selected": True if j.find("input").has_attr("checked") else False
                            }
                print(menu)
            else:
                return f"Failed to access main URL: {main_response.status_code}"
        else:
            return f"Login failed: {response.status_code}"


"""def setup(bot):
    @bot.slash_command(name="kroky", description="Get Kroky data")
    async def kroky(ctx, username: str, password: str):
        await ctx.respond(kroky_command(username, password))
"""

print(kroky_command(username, password))

