from bs4 import BeautifulSoup
from classes.playeratbat import PlayerAtBat
from classes.atbatoutcome import AtBatOutcome
from classes.team import Team
import re
import os
import fileinput

def process_inning(inning, pitcher, inning_num, awayteam, hometeam, game_date):
    td_tags = inning.find_all("td", class_=lambda x: x != 'datathbg')

    # determine if we are in top or bottom of innning
    inning_info = inning.find("th").text
    if inning_info.startswith("TOP"):
        top = True
    else:
        top = False

    batter = ""
    batters = []
    for td_tag in td_tags:
        text_data = td_tag.text.strip()
        # checks to see if a pitching change occurred during the inning
        if text_data.startswith('Pitching'):
            pitcher = td_tag.find("a").text
        elif text_data.startswith('Batting'):
            batter = td_tag.find("a").text
        elif text_data == '':
            i = 1
        else:
            at_bat_data = text_data.split("*")
            atbat = PlayerAtBat()
            atbat.inning = inning_num
            atbat.pitcher = pitcher
            atbat.player = batter
            atbat.game_date = game_date
            if top:
                atbat.player_team = awayteam
                atbat.pitcher_team = hometeam
            elif not top:
                atbat.player_team = hometeam
                atbat.pitcher_team = awayteam
            for pitch in at_bat_data:
                if re.match(r'^([0-3]-[0-2]:)', pitch):
                    pitch_data = re.split(":", pitch)
                    pitch_count = pitch_data[0]
                    pitch_outcome = pitch_data[1].strip().lower()
                    if pitch_outcome == AtBatOutcome.BALL:
                        atbat.balls = atbat.balls + 1
                    elif pitch_outcome == AtBatOutcome.BB:
                        atbat.balls = atbat.balls + 1
                        atbat.result = 'BB'
                    elif pitch_outcome.startswith(AtBatOutcome.HB):
                        atbat.balls = atbat.balls + 1
                        atbat.result = 'HB'
                    elif pitch_outcome == AtBatOutcome.IBB:
                        atbat.result = 'IBB'
                    elif pitch_outcome == AtBatOutcome.CS:
                        atbat.called_strikes = atbat.called_strikes + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = True
                    elif pitch_outcome.startswith(AtBatOutcome.CSO):
                        atbat.called_strikes = atbat.called_strikes + 1
                        atbat.result = 'SO'
                    elif pitch_outcome == AtBatOutcome.SWS:
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = True
                    elif pitch_outcome == AtBatOutcome.BUNTMISSED:
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = True
                    elif pitch_outcome.startswith(AtBatOutcome.SWSO):
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        atbat.result = 'SO'
                    elif pitch_outcome.startswith(AtBatOutcome.FB):
                        atbat.foul_balls = atbat.foul_balls + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = True
                    elif pitch_outcome.startswith(AtBatOutcome.BFB):
                        atbat.foul_balls = atbat.foul_balls + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = True
                    elif pitch_outcome.startswith(AtBatOutcome.FO):
                        atbat.ball_in_play = True
                        atbat.result = 'FO'
                    elif pitch_outcome.startswith(AtBatOutcome.GO):
                        atbat.ball_in_play = True
                        atbat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.GOS):
                        atbat.ball_in_play = True
                        atbat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.FC):
                        atbat.ball_in_play = True
                        atbat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.GOFC):
                        atbat.ball_in_play = True
                        atbat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.GODP):
                        atbat.ball_in_play = True
                        atbat.result = 'GO-DP'
                    elif pitch_outcome.startswith(AtBatOutcome.ROE):
                        atbat.ball_in_play = True
                        atbat.result = 'ROE'
                    elif pitch_outcome.startswith(AtBatOutcome.RVE):
                        atbat.ball_in_play = True
                        atbat.result = 'ROE'
                    elif pitch_outcome.startswith(AtBatOutcome.RCI):
                        atbat.ball_in_play = True
                        atbat.result = 'RCI'
                    elif pitch_outcome.startswith(AtBatOutcome.SINGLE):
                        atbat.ball_in_play = True
                        atbat.result = '1B'
                    elif pitch_outcome.startswith(AtBatOutcome.DOUBLE):
                        atbat.ball_in_play = True
                        atbat.result = '2B'
                    elif pitch_outcome.startswith(AtBatOutcome.TRIPLE):
                        atbat.ball_in_play = True
                        atbat.result = '3B'
                    elif pitch_outcome.__contains__(AtBatOutcome.HR):
                        atbat.home_run = True
                        atbat.result = 'HR'
                    elif pitch_outcome.startswith(AtBatOutcome.SACBUNT):
                        atbat.ball_in_play = True
                        if pitch_outcome.__contains__(AtBatOutcome.OUT):
                            atbat.result = 'SAC'
                        else:
                            atbat.result = '1B'
                    elif pitch_outcome.startswith(AtBatOutcome.BUNTFORHIT):
                        atbat.ball_in_play = True
                        if pitch_outcome.__contains__(AtBatOutcome.OUT):
                            atbat.result = 'GO'
                        elif pitch_outcome.__contains__(AtBatOutcome.SAFE):
                            atbat.result = '1B'
                    elif pitch_outcome.startswith(AtBatOutcome.BUNTFO):
                        atbat.ball_in_play = True
                        atbat.result = 'PO'
                    elif pitch_outcome.startswith(AtBatOutcome.LTP):
                        atbat.ball_in_play = True
                        atbat.result = 'TP'
                    else:
                        i=1
                        print(pitch_outcome)
            if pitch.startswith("Pinch") or pitch.startswith("Now at") or pitch.startswith("Now in"):
                i = 1
            else :
                batters.append(atbat)
    return batters



# each file needs the <br> tags between pitch outcomes replaced with something
# the BeautifulSoup won't strip away.
results = []
for root, dirs, files in os.walk('logs', topdown=False):
    for name in files:
        if name.endswith(".html"):
            with fileinput.FileInput(os.path.join(root, name), inplace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace("<br>", "*"), end='')

            soup = BeautifulSoup(open(os.path.join(root, name)), "html.parser")

            # get the teams from the game log
            teams = soup.find("div", class_="repsubtitle").text.split('@')
            away = Team.find_team_by_name(teams[0]).name
            home = Team.find_team_by_name(teams[1]).name

            #find the game date
            game_date =  soup.find("div", class_="repsubtitle").find_next_sibling().text

            innings = soup.find_all("table", class_="data")
            for inning in innings:
                #determine inning
                inning_num = inning.find("th").text.split(" ")[-1]
                #get the pitcher for the inning
                th_link_pitcher = inning.find_all("th")[1].find("a")
                if (th_link_pitcher):
                    pitcher = th_link_pitcher.text
                #pitcher = inning.find_all("th")[1].find("a").text
                results.append(process_inning(inning, pitcher, inning_num, away, home, game_date))

output_file = open('logresults.csv', 'w')

output_file.write("Batter,Batter Team,Pitcher,Pitcher Team,GameDate,Inning,Balls,Called Strikes,Swinging Strikes,Foul Balls,First Pitch Strike,In Play,HR,Result\n")
for plateappearances in results:
    for pa in plateappearances:

        output_file.write(pa.player+","+pa.player_team+","+pa.pitcher+","+pa.pitcher_team+","+pa.game_date+","+pa.inning+","+str(pa.balls)+","+str(pa.called_strikes)+","
               +str(pa.swinging_strikes)+","+str(pa.foul_balls)+","
               +str(pa.first_pitch_strike)+","+str(pa.ball_in_play)+","+str(pa.home_run)+","+pa.result+"\n")
output_file.close()