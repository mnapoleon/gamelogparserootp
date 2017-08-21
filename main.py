from bs4 import BeautifulSoup
from classes.playeratbat import PlayerAtBat
import re
import fileinput

def process_inning(inning, pitcher, inning_num):
    td_tags  = inning.find_all("td", class_=lambda x: x != 'datathbg')
    batter = ""
    batters = []
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
            #print (pitcher + " : " + batter)
            atbat = PlayerAtBat()
            atbat.inning = inning_num
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
                    elif pitch_outcome.strip() == 'Strikes out  swinging':
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        atbat.result = 'SO'
                    elif pitch_outcome.strip().startswith('Foul Ball,'):
                        atbat.foul_balls = atbat.foul_balls + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = True
                    elif pitch_outcome.strip().startswith('Bunted foul'):
                        atbat.foul_balls = atbat.foul_balls + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = True
                    elif pitch_outcome.strip().startswith('Fly out'):
                        atbat.ball_in_play = True
                        atbat.result = 'FO'
                    elif pitch_outcome.strip().startswith('Ground out'):
                        atbat.ball_in_play = True
                        atbat.result = 'GO'
                    elif pitch_outcome.strip().startswith('Fielders Choice'):
                        atbat.ball_in_play = True
                        atbat.result = 'GO'
                    elif pitch_outcome.strip().startswith('Grounds into double play'):
                        atbat.ball_in_play = True
                        atbat.result = 'GO-DP'
                    elif pitch_outcome.strip().startswith('Reached on error'):
                        atbat.ball_in_play = True
                        atbat.result = 'ROE'
                    elif pitch_outcome.strip().startswith('Reached via error'):
                        atbat.ball_in_play = True
                        atbat.result = 'ROE'
                    elif pitch_outcome.strip().startswith('SINGLE'):
                        atbat.ball_in_play = True
                        atbat.result = '1B'
                    elif pitch_outcome.strip().startswith('DOUBLE'):
                        atbat.ball_in_play = True
                        atbat.result = '2B'
                    elif pitch_outcome.strip().startswith('TRIPLE'):
                        atbat.ball_in_play = True
                        atbat.result = '3B'
                    elif pitch_outcome.strip().__contains__('HOME RUN'):
                        atbat.home_run = True
                        atbat.result = 'HR'
                    elif pitch_outcome.strip().startswith('Sac Bunt'):
                        atbat.ball_in_play = True
                        if pitch_outcome.__contains__("OUT"):
                            atbat.result = 'SAC'
                        else:
                            atbat.result = "1B"
                    else:
                        i=1
                        print(pitch_outcome)
            if pitch.startswith("Pinch") or pitch.startswith("Now at"):
                i = 1
            else :
                batters.append(atbat)
    return batters



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
results = []
for inning in innings:
    #determine inning
    inning_num = inning.find("th").text.split(" ")[-1]
    #get the pitcher for the inning
    pitcher = inning.find_all("th")[1].find("a").text
    results.append(process_inning(inning, pitcher, inning_num))

print ("Batter,Pitcher,inning,Balls,Called Strikes,Swinging Strikes,Foul Balls,First Pitch Strike,In Play,HR,Result")
for atbats in results:
    for atbat in atbats:

        print (atbat.player+","+atbat.pitcher+","+atbat.inning+","+str(atbat.balls)+","+str(atbat.called_strikes)+","
               +str(atbat.swinging_strikes)+","+str(atbat.foul_balls)+","
               +str(atbat.first_pitch_strike)+","+str(atbat.ball_in_play)+","+str(atbat.home_run)+","+atbat.result)
