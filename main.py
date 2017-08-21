from bs4 import BeautifulSoup
import re
import fileinput


def process_inning(inning):
    td_tags  = inning.find_all("td")
    for td_tag in td_tags:
        text_data = td_tag.text.strip()
        if text_data.startswith('Pitching'):
            print(text_data)
        elif text_data.startswith('Batting'):
            print(text_data)
        elif text_data=='':
            i = 1
        else:
            at_bat_data = text_data.split("*")
            for pitch in  at_bat_data:
                print (pitch)


def process_inning2(inning):
    td_tags  = inning.find_all("td")
    for td_tag in td_tags:
        print(td_tag.string)




with fileinput.FileInput("game_1_log_DUB.html", inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace("<br>", "*"), end='')

soup = BeautifulSoup(open("game_1_log_DUB.html"), "html.parser")

# get the teams from the game log
teams = soup.find("div", class_="repsubtitle").text.split('@')
away = teams[0]
home = teams[1]
print(away.strip())
print(home.strip())

innings = soup.find_all("table", class_="data")
for inning in innings:
    process_inning(inning)

