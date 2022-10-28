import logging

from bs4 import BeautifulSoup
from classes.playeratbat import PlayerAtBat
from classes.atbatoutcome import AtBatOutcome
from classes.team import Team
import sys
import re
import os
import fileinput
from pythonjsonlogger import jsonlogger

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)
logger.propagate = False
logHandler = logging.FileHandler('warn.log')
logHandler.setLevel(logging.INFO)
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


class MalformedPitchOutcomeException(Exception):
    """Pitch outcome html is malformed"""
    pass


class MalformedBatterException(Exception):
    """Batter html is malformed"""
    pass


def process_inplay_outcomes(inplay_outcomes, atbat):
    outcomes = inplay_outcomes.split(',')
    hit_type_raw = outcomes[0]
    hit_type = hit_type_raw[1:]

    (contains_distance, contains_ev) = 'distance' in inplay_outcomes, 'ev' in inplay_outcomes
    exit_velo = ''
    distance = ''

    match (contains_distance, contains_ev):
        case (True, True):
            exit_velo = outcomes[2].split()[1]
            distance = outcomes[3].split()[2].strip()
            location = outcomes[1].strip()
        case (False, True):
            exit_velo = outcomes[2].split()[1].strip()
            location = outcomes[1].strip()
        case (True, False):
            distance = outcomes[2].split()[2].strip()
            location = outcomes[1].strip()
        case _:
            location = outcomes[1][:outcomes[1].index(')')].strip()

    atbat.exitvelo = exit_velo
    atbat.distance = distance
    atbat.hittype = hit_type
    atbat.hitlocation = location


def get_player_id_from_href(player_tag):
    player_href = player_tag['href']
    underscore_index = player_href.find('_')
    dot_html_index = player_href.find('.html')
    player_id = player_href[underscore_index + 1:dot_html_index]
    return player_id


def process_inning(game_id, inning, pitcher, pitcher_id, inning_num, league, awayteam, hometeam, game_date):
    td_tags = inning.find_all("td", class_=lambda x: x != 'datathbg')

    # determine if we are in top or bottom of innning
    inning_info = inning.find("th").text
    if inning_info.startswith("TOP"):
        is_top_of_inning = True
    else:
        is_top_of_inning = False

    batter = ""
    batter_id = 0
    batters = []
    inplay_outcome = ''
    for td_tag in td_tags:
        text_data = td_tag.text.strip()
        # checks to see if a pitching change occurred during the inning
        if text_data.startswith('Pitching'):
            pitcher_tag = td_tag.find("a")
            pitcher = pitcher_tag.text
            pitcher_id = get_player_id_from_href(pitcher_tag)
        elif text_data.startswith('Batting') or text_data.startswith('Pinch Hitting'):
            try:
                batter_tag = td_tag.find("a")
                if batter_tag:
                    batter = batter_tag.text
                    batter_id = get_player_id_from_href(batter_tag)
            except Exception:
                print(f"issue with batter tag :: ${batter_tag}")
                # log = log.bind(exception="MalformedBatterException")
                # log = log.bind(batter_tag=batter_tag)
                raise MalformedBatterException
        elif text_data == '':
            pass
        else:
            at_bat_data = text_data.split("*")
            at_bat = PlayerAtBat()
            at_bat.inning = inning_num
            at_bat.pitcher_id = pitcher_id
            at_bat.pitcher = pitcher
            at_bat.player = batter
            at_bat.player_id = batter_id
            at_bat.game_date = game_date
            at_bat.league = league
            at_bat.game_id = game_id
            if is_top_of_inning:
                at_bat.player_team = awayteam
                at_bat.pitcher_team = hometeam
            elif not is_top_of_inning:
                at_bat.player_team = hometeam
                at_bat.pitcher_team = awayteam
            for pitch in at_bat_data:
                if re.match(r'^([0-3]-[0-2]:)', pitch):
                    pitch_data = re.split(":", pitch, 1)
                    pitch_count = pitch_data[0]
                    pitch_outcome = pitch_data[1].strip().lower()
                    loc_index = pitch_outcome.find('(')
                    if loc_index > 0:
                        inplay_outcome = pitch_outcome[loc_index:]
                    if pitch_outcome == AtBatOutcome.BALL:
                        at_bat.balls = at_bat.balls + 1
                    elif pitch_outcome == AtBatOutcome.BB:
                        at_bat.balls = at_bat.balls + 1
                        at_bat.result = 'BB'
                    elif pitch_outcome.startswith(AtBatOutcome.HB):
                        at_bat.balls = at_bat.balls + 1
                        at_bat.result = 'HB'
                    elif pitch_outcome == AtBatOutcome.IBB:
                        at_bat.result = 'IBB'
                    elif pitch_outcome == AtBatOutcome.CS:
                        at_bat.called_strikes = at_bat.called_strikes + 1
                        if pitch_count == '0-0':
                            at_bat.first_pitch_strike = 1
                            at_bat.first_pitch_called_strike = 1
                    elif pitch_outcome.startswith(AtBatOutcome.CSO):
                        at_bat.called_strikes = at_bat.called_strikes + 1
                        at_bat.called_strike_out = 1
                        at_bat.result = 'SO'
                    elif pitch_outcome == AtBatOutcome.SWS:
                        at_bat.swinging_strikes = at_bat.swinging_strikes + 1
                        if pitch_count == '0-0':
                            at_bat.first_pitch_strike = 1
                            at_bat.first_pitcher_swinging_strike = 1
                    elif pitch_outcome == AtBatOutcome.BUNTMISSED:
                        at_bat.swinging_strikes = at_bat.swinging_strikes + 1
                        if pitch_count == '0-0':
                            at_bat.first_pitch_strike = 1
                            at_bat.first_pitcher_swinging_strike = 1
                    elif pitch_outcome.startswith(AtBatOutcome.SWSO):
                        at_bat.swinging_strikes = at_bat.swinging_strikes + 1
                        at_bat.swinging_strike_out = 1
                        at_bat.result = 'SO'
                    elif pitch_outcome == AtBatOutcome.BUNTMISSED_SO:
                        at_bat.swinging_strikes = at_bat.swinging_strikes + 1
                        at_bat.swinging_strike_out = 1
                        at_bat.result = 'SO'
                    elif pitch_outcome.startswith(AtBatOutcome.FB):
                        at_bat.foul_balls = at_bat.foul_balls + 1
                        if pitch_count == '0-0':
                            at_bat.first_pitch_strike = 1
                            at_bat.first_pitcher_swinging_strike = 1
                    elif pitch_outcome.startswith(AtBatOutcome.BFB):
                        at_bat.foul_balls = at_bat.foul_balls + 1
                        if pitch_count == '0-0':
                            at_bat.first_pitch_strike = 1
                            at_bat.first_pitcher_swinging_strike = 1
                    elif pitch_outcome.startswith(AtBatOutcome.FO):
                        at_bat.ball_in_play = 1
                        if AtBatOutcome.PO in pitch_outcome:
                            at_bat.result = 'PO'
                        else:
                            at_bat.result = 'FO'
                    elif pitch_outcome.startswith(AtBatOutcome.GO):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.GOS):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.FC):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.GOFC):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.GODP):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'GO-DP'
                    elif pitch_outcome.startswith(AtBatOutcome.GOTP):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'GO-TP'
                    elif pitch_outcome.startswith(AtBatOutcome.ROE):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'ROE'
                    elif pitch_outcome.startswith(AtBatOutcome.RVE):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'ROE'
                    elif pitch_outcome.startswith(AtBatOutcome.RCI):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'RCI'
                    elif pitch_outcome.startswith(AtBatOutcome.SINGLE):
                        at_bat.ball_in_play = 1
                        at_bat.result = '1B'
                    elif pitch_outcome.startswith(AtBatOutcome.DOUBLE):
                        at_bat.ball_in_play = 1
                        at_bat.result = '2B'
                    elif pitch_outcome.startswith(AtBatOutcome.TRIPLE):
                        at_bat.ball_in_play = 1
                        at_bat.result = '3B'
                    elif AtBatOutcome.HR in pitch_outcome:
                        at_bat.home_run = 1
                        at_bat.result = 'HR'
                    elif pitch_outcome.startswith(AtBatOutcome.SACBUNT):
                        at_bat.ball_in_play = 1
                        if AtBatOutcome.OUT in pitch_outcome:
                            at_bat.result = 'SAC'
                        else:
                            at_bat.result = '1B'
                    elif pitch_outcome.startswith(AtBatOutcome.SQZBUNT):
                        at_bat.ball_in_play = 1
                        if AtBatOutcome.SQZ_HOME_RUNNER_OUT in pitch_outcome and AtBatOutcome.SQZ_BATTER_SAFE in pitch_outcome:
                            at_bat.result = 'GO'
                        elif AtBatOutcome.SQZ_HOME_RUNNER_SAFE in pitch_outcome and AtBatOutcome.SQZ_BATTER_SAFE:
                            at_bat.result = '1B'
                        elif AtBatOutcome.SQZ_FIRST_OUT:
                            at_bat.result = 'SAC'
                        elif AtBatOutcome.SQZ_BATTER_SAFE:
                            at_bat.result = '1B'
                        else:
                            logger.error("Unexpected Squeeze Play Outcome")
                    elif pitch_outcome.startswith(AtBatOutcome.BUNTFORHIT):
                        at_bat.ball_in_play = 1
                        if AtBatOutcome.OUT in pitch_outcome:
                            at_bat.result = 'GO'
                        elif AtBatOutcome.SAFE in pitch_outcome:
                            at_bat.result = '1B'
                    elif pitch_outcome.startswith(AtBatOutcome.BUNTFO):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'PO'
                    elif pitch_outcome.startswith(AtBatOutcome.LTP):
                        at_bat.ball_in_play = 1
                        at_bat.result = 'TP'
                    else:
                        # log = log.bind(outcome=pitch_outcome)
                        # log = log.bind(exception="MalformedPitchOutcome")
                        raise MalformedPitchOutcomeException

                    if pitch_count == '0-0' and at_bat.ball_in_play == 1:
                        at_bat.first_pitch_swinging_other = 1
            if len(inplay_outcome) > 0:
                process_inplay_outcomes(inplay_outcome, at_bat)
            inplay_outcome = ''
            if pitch.startswith("Pinch") or pitch.startswith("Now at") or pitch.startswith("Now in"):
                pass
            else:
                batters.append(at_bat)
    return batters


def process_innings(innings, league, away, home, game_date):
    innings_results = []
    for inning in innings:
        # determine inning
        inning_num = inning.find("th").text.split(" ")[-1]
        # get the pitcher for the inning
        try:
            th_link_pitcher = inning.find_all("th")[1].find("a")
            if th_link_pitcher:
                pitcher = th_link_pitcher.text
                pitcher_id = get_player_id_from_href(th_link_pitcher)
        except Exception:
            logger.error("Issue with Pitcher th tags")
            continue
        try:
            innings_results.append(
                process_inning(game_id, inning, pitcher, pitcher_id, inning_num,league, away, home, game_date))
        except MalformedBatterException:
            logger.error("There are malformed batter tags")
            pass
        except MalformedPitchOutcomeException:
            logger.error("There are malformed pitch outcomes")
            pass
        except Exception:
            logger.error("Haven't yet determine the exact issue.")
            pass
    return innings_results


def process_game_log(game_log):
    # get the league
    league = game_log.find("div", class_="reptitle").text
    # get the teams from the game log
    teams = game_log.find("div", class_="repsubtitle").text.split('@')
    away_team = Team.find_team_by_name(teams[0])
    home_team = Team.find_team_by_name(teams[1])
    away = away_team.name if away_team else ""
    home = home_team.name if home_team else ""

    # find the game date
    game_date = game_log.find("div", class_="repsubtitle").find_next_sibling().text
    innings = game_log.find_all("table", class_="data")
    return process_innings(innings, league, away, home, game_date)


# each file needs the <br> tags between pitch outcomes replaced with something
# the BeautifulSoup won't strip away.
game_log_dir = sys.argv[1]
results = []
for root, dirs, files in os.walk(game_log_dir, topdown=False):
    for name in files:
        logger.info(f"Processing file {name}")
        if name.endswith(".html"):
            game_id = name[name.find('_') + 1:name.find('.html')]
            with fileinput.FileInput(os.path.join(root, name), inplace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace("<br>", "*"), end='')

            soup = BeautifulSoup(open(os.path.join(root, name)), "html.parser")
            results.extend(process_game_log(soup))

output_file = open('logresults.csv', 'w')
# output_file = open(sys.argv[2], 'w')

output_file.write(
    "game_id,league,batter_id,batter_name,batter_team,pitcher_id,pitcher_name,pitcher_team,game_date,inning,BALLS,CS,SWS,FB,"
    "FPS,FPCS,FPSS,FPSO,CSO,SWO,InP,HR,result,hit_type,hit_location,distance,exit_velocity\n")
for plate_appearances in results:
    for pa in plate_appearances:
        output_file.write(str(pa.game_id) + "," + pa.league + "," + str(pa.player_id) + "," + pa.player + ","
                          + pa.player_team + "," + str(pa.pitcher_id) + "," + pa.pitcher + "," + pa.pitcher_team
                          + "," + pa.game_date + "," + pa.inning + "," + str(pa.balls) + "," + str(pa.called_strikes)
                          + "," + str(pa.swinging_strikes) + "," + str(pa.foul_balls) + "," + str(pa.first_pitch_strike)
                          + "," + str(pa.first_pitch_called_strike) + "," + str(pa.first_pitch_swinging_strike)
                          + "," + str(pa.first_pitch_swinging_other) + "," + str(pa.called_strike_out) + ","
                          + str(pa.swinging_strike_out) + "," + str(pa.ball_in_play) + "," + str(pa.home_run) + ","
                          + pa.result + "," + pa.hittype + "," + pa.hitlocation + ","
                          + str(pa.distance) + "," + str(pa.exitvelo) + "\n")
output_file.close()
