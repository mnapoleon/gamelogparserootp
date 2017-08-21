from bs4 import BeautifulSoup
from classes.playeratbat import PlayerAtBat
import re
import fileinput

def process_inning(inning, pitcher):
    td_tags  = inning.find_all("td")
    batter = ""
    for td_tag in td_tags:
        text_data = td_tag.text.strip()
        if text_data.startswith('Pitching'):
            pitcher = td_tag.find("a").text
        elif text_data.startswith('Batting'):
            batter = td_tag.find("a").text
        elif text_data=='':
            i = 1
        else:
            at_bat_data = text_data.split("*")
            print (pitcher + " : " + batter)
            atbat = PlayerAtBat()
            atbat.pitcher = pitcher
            atbat.player = batter
            for pitch in at_bat_data:
                if re.match(r'^([0-3]-[0-2]:)', pitch):
                    pitch_data = re.split(":", pitch)
                    pitch_count = pitch_data[0]
                    pitch_outcome = pitch_data[1]
                    if pitch_outcome.strip() == 'Ball':
                        atbat.balls = atbat.balls + 1
                    elif pitch_outcome.strip() == 'Base on Balls':
                        atbat.balls = atbat.balls + 1
                        atbat.result = 'BB'
                    elif pitch_outcome.strip() == 'Called Strike':
                        atbat.called_strikes = atbat.called_strikes + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = True
                    elif pitch_outcome.strip() == 'Strikes out  looking':
                        atbat.called_strikes = atbat.called_strikes + 1
                        atbat.result = 'SO'
                    elif pitch_outcome.strip() == 'Swinging Strike':
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = True
                    elif pitch_outcome.strip() == ' Strikes out  swinging':
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        atbat.result = 'SO'
            print(atbat)



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
    #get the pitcher for the inning
    pitcher = inning.find_all("th")[1].find("a").text
    process_inning(inning, pitcher)

