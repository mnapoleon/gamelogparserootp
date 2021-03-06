from bs4 import BeautifulSoup
from classes.playeratbat import PlayerAtBat
from classes.atbatoutcome import AtBatOutcome
from classes.team import Team
import sys
import re
import os
import fileinput
import structlog


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

    contains_distance = inplay_outcomes.__contains__('distance')
    contains_ev = inplay_outcomes.__contains__('ev')
    exit_velo = ''
    distance = ''

    if contains_ev or contains_distance:
        location = outcomes[1].strip()
    else:
        location = outcomes[1][:outcomes[1].index(')')].strip()

    if contains_ev and contains_distance:
        exitvelo_strings = outcomes[2].split()
        exit_velo = exitvelo_strings[1]
        distance_strings = outcomes[3].split()
        distance = distance_strings[2].strip()
    elif contains_ev and not contains_distance:
        exitvelo_strings = outcomes[2].split()
        exit_velo = exitvelo_strings[1].strip()
    elif contains_distance and not contains_ev:
        distance_strings = outcomes[2].split()
        distance = distance_strings[2].strip()

    atbat.exitvelo = exit_velo
    atbat.distance = distance
    atbat.hittype = hit_type
    atbat.hitlocation = location


def get_player_id_from_href(player_tag):
    player_href = player_tag['href']
    underscore_index = player_href.find('_')
    dot_html_index = player_href.find('.html')
    player_id = player_href[underscore_index+1:dot_html_index]
    return player_id


def process_inning(game_id,inning, pitcher, pitcher_id, inning_num, league, awayteam, hometeam, game_date):
    td_tags = inning.find_all("td", class_=lambda x: x != 'datathbg')

    # determine if we are in top or bottom of innning
    inning_info = inning.find("th").text
    if inning_info.startswith("TOP"):
        top = True
    else:
        top = False

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
                log = log.bind(exception="MalformedBatterException")
                log = log.bind(batter_tag=batter_tag)
                raise MalformedBatterException
        elif text_data == '':
            i = 1
        else:
            at_bat_data = text_data.split("*")
            atbat = PlayerAtBat()
            atbat.inning = inning_num
            atbat.pitcher_id = pitcher_id
            atbat.pitcher = pitcher
            atbat.player = batter
            atbat.player_id = batter_id
            atbat.game_date = game_date
            atbat.league = league
            atbat.game_id = game_id
            if top:
                atbat.player_team = awayteam
                atbat.pitcher_team = hometeam
            elif not top:
                atbat.player_team = hometeam
                atbat.pitcher_team = awayteam
            for pitch in at_bat_data:
                if re.match(r'^([0-3]-[0-2]:)', pitch):
                    pitch_data = re.split(":", pitch, 1)
                    pitch_count = pitch_data[0]
                    pitch_outcome = pitch_data[1].strip().lower()
                    loc_index = pitch_outcome.find('(')
                    if loc_index > 0:
                        inplay_outcome = pitch_outcome[loc_index:]
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
                            atbat.first_pitch_strike = 1
                            atbat.first_pitch_called_strike = 1
                    elif pitch_outcome.startswith(AtBatOutcome.CSO):
                        atbat.called_strikes = atbat.called_strikes + 1
                        atbat.called_strike_out = 1
                        atbat.result = 'SO'
                    elif pitch_outcome == AtBatOutcome.SWS:
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = 1
                            atbat.first_pitcher_swinging_strike = 1
                    elif pitch_outcome == AtBatOutcome.BUNTMISSED:
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = 1
                            atbat.first_pitcher_swinging_strike = 1
                    elif pitch_outcome.startswith(AtBatOutcome.SWSO):
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        atbat.swinging_strike_out = 1
                        atbat.result = 'SO'
                    elif pitch_outcome == AtBatOutcome.BUNTMISSED_SO:
                        atbat.swinging_strikes = atbat.swinging_strikes + 1
                        atbat.swinging_strike_out = 1
                        atbat.result = 'SO'
                    elif pitch_outcome.startswith(AtBatOutcome.FB):
                        atbat.foul_balls = atbat.foul_balls + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = 1
                            atbat.first_pitcher_swinging_strike = 1
                    elif pitch_outcome.startswith(AtBatOutcome.BFB):
                        atbat.foul_balls = atbat.foul_balls + 1
                        if pitch_count == '0-0':
                            atbat.first_pitch_strike = 1
                            atbat.first_pitcher_swinging_strike = 1
                    elif pitch_outcome.startswith(AtBatOutcome.FO):
                        atbat.ball_in_play = 1
                        if pitch_outcome.__contains__(AtBatOutcome.PO):
                            atbat.result = 'PO'
                        else:
                            atbat.result = 'FO'
                    elif pitch_outcome.startswith(AtBatOutcome.GO):
                        atbat.ball_in_play = 1
                        atbat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.GOS):
                        atbat.ball_in_play = 1
                        atbat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.FC):
                        atbat.ball_in_play = 1
                        atbat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.GOFC):
                        atbat.ball_in_play = 1
                        atbat.result = 'GO'
                    elif pitch_outcome.startswith(AtBatOutcome.GODP):
                        atbat.ball_in_play = 1
                        atbat.result = 'GO-DP'
                    elif pitch_outcome.startswith(AtBatOutcome.GOTP):
                        atbat.ball_in_play = 1
                        atbat.result = 'GO-TP'
                    elif pitch_outcome.startswith(AtBatOutcome.ROE):
                        atbat.ball_in_play = 1
                        atbat.result = 'ROE'
                    elif pitch_outcome.startswith(AtBatOutcome.RVE):
                        atbat.ball_in_play = 1
                        atbat.result = 'ROE'
                    elif pitch_outcome.startswith(AtBatOutcome.RCI):
                        atbat.ball_in_play = 1
                        atbat.result = 'RCI'
                    elif pitch_outcome.startswith(AtBatOutcome.SINGLE):
                        atbat.ball_in_play = 1
                        atbat.result = '1B'
                    elif pitch_outcome.startswith(AtBatOutcome.DOUBLE):
                        atbat.ball_in_play = 1
                        atbat.result = '2B'
                    elif pitch_outcome.startswith(AtBatOutcome.TRIPLE):
                        atbat.ball_in_play = 1
                        atbat.result = '3B'
                    elif pitch_outcome.__contains__(AtBatOutcome.HR):
                        atbat.home_run = 1
                        atbat.result = 'HR'
                    elif pitch_outcome.startswith(AtBatOutcome.SACBUNT):
                        atbat.ball_in_play = 1
                        if pitch_outcome.__contains__(AtBatOutcome.OUT):
                            atbat.result = 'SAC'
                        else:
                            atbat.result = '1B'
                    elif pitch_outcome.startswith(AtBatOutcome.SQZBUNT):
                        atbat.ball_in_play = 1
                        if pitch_outcome.__contains__(AtBatOutcome.SQZ_HOME_RUNNER_OUT) and pitch_outcome.__contains__(AtBatOutcome.SQZ_BATTER_SAFE):
                            atbat.result = 'GO'
                        elif pitch_outcome.__contains__(AtBatOutcome.SQZ_HOME_RUNNER_SAFE) and pitch_outcome.__contains__(AtBatOutcome.SQZ_BATTER_SAFE):
                            atbat.result = '1B'
                        elif pitch_outcome.__contains__(AtBatOutcome.SQZ_FIRST_OUT):
                            atbat.result = 'SAC'
                        elif pitch_outcome.__contains__(AtBatOutcome.SQZ_FIRST_SAFE):
                            atbat.result = '1B'
                        else:
                            log.msg("Unexpected Squeeze Play Outcome")
                    elif pitch_outcome.startswith(AtBatOutcome.BUNTFORHIT):
                        atbat.ball_in_play = 1
                        if pitch_outcome.__contains__(AtBatOutcome.OUT):
                            atbat.result = 'GO'
                        elif pitch_outcome.__contains__(AtBatOutcome.SAFE):
                            atbat.result = '1B'
                    elif pitch_outcome.startswith(AtBatOutcome.BUNTFO):
                        atbat.ball_in_play = 1
                        atbat.result = 'PO'
                    elif pitch_outcome.startswith(AtBatOutcome.LTP):
                        atbat.ball_in_play = 1
                        atbat.result = 'TP'
                    else:
                        log = log.bind(outcome=pitch_outcome)
                        log = log.bind(exception="MalformedPitchOutcome")
                        raise MalformedPitchOutcomeException

                    if pitch_count == '0-0' and atbat.ball_in_play == 1:
                        atbat.first_pitch_swinging_other = 1
            if len(inplay_outcome) > 0:
                process_inplay_outcomes(inplay_outcome, atbat)
            inplay_outcome = ''
            if pitch.startswith("Pinch") or pitch.startswith("Now at") or pitch.startswith("Now in"):
                pass
            else:
                batters.append(atbat)
    return batters


# each file needs the <br> tags between pitch outcomes replaced with something
# the BeautifulSoup won't strip away.
game_log_dir = sys.argv[1]
results = []
#log = wrap_logger(processors=[structlog.stdlib.filter_by_level,
#                                                           structlog.stdlib.add_logger_name,
#                                                           structlog.stdlib.add_log_level,
#                                                           structlog.stdlib.PositionalArgumentsFormatter(),
#                                                           structlog.processors.StackInfoRenderer(),
#                                                           structlog.processors.format_exc_info,
#                                                           structlog.processors.UnicodeDecoder(),
#                                                           structlog.stdlib.render_to_log_kwargs,
#                                                           JSONRenderer(indent=1, sort_keys=True)])

structlog.configure(processors=[structlog.processors.JSONRenderer()])
logger = structlog.get_logger()
for root, dirs, files in os.walk(game_log_dir, topdown=False):
    for name in files:
        log = logger.bind(file_name=name)
        if name.endswith(".html"):
            game_id = name[name.find('_')+1:name.find('.html')]
            with fileinput.FileInput(os.path.join(root, name), inplace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace("<br>", "*"), end='')

            soup = BeautifulSoup(open(os.path.join(root, name)), "html.parser")

            # get the league
            league = soup.find("div", class_="reptitle").text
            # get the teams from the game log
            teams = soup.find("div", class_="repsubtitle").text.split('@')
            away_team = Team.find_team_by_name(teams[0])
            home_team = Team.find_team_by_name(teams[1])
            away = away_team.name if away_team else ""
            home = home_team.name if home_team else ""

            # find the game date
            game_date = soup.find("div", class_="repsubtitle").find_next_sibling().text

            innings = soup.find_all("table", class_="data")
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
                    log = log.bind(pitcher_tag=th_link_pitcher)
                    log.msg("Issue with Pitcher th tags")
                    continue
                try:
                    results.append(process_inning(game_id, inning, pitcher, pitcher_id, inning_num,
                                                  league, away, home, game_date))
                except MalformedBatterException:
                    log.msg("There are malformed batter tags")
                    pass
                except MalformedPitchOutcomeException:
                    log.msg("There are malformed pitch outcomes")
                    pass
                except Exception:
                    log.msg("Haven't yet determine the exact issue.")
                    pass

#output_file = open('logresults.csv', 'w')
output_file = open(sys.argv[2], 'w')

output_file.write("GameId,League,BatterId,Batter,Batter Team,PitcherId,Pitcher,Pitcher Team,GameDate,Inning,BALLS,CS,SWS,FB,FPS,FPCS,FPSS,CSO,SWO,InP,HR,Result,HitType,HitLocation,Distance,ExitVelocity\n")
for plateappearances in results:
    for pa in plateappearances:

        output_file.write(str(pa.game_id) + "," + pa.league + "," + str(pa.player_id) + "," + pa.player + ","
                          + pa.player_team+"," + str(pa.pitcher_id) + "," + pa.pitcher + "," + pa.pitcher_team
                          + "," + pa.game_date + "," + pa.inning + "," + str(pa.balls) + "," + str(pa.called_strikes)
                          + "," + str(pa.swinging_strikes) + "," + str(pa.foul_balls) + "," + str(pa.first_pitch_strike)
                          + "," + str(pa.first_pitch_called_strike) + "," + str(pa.first_pitch_swinging_strike)
                          + "," + str(pa.first_pitch_swinging_other) + "," + str(pa.called_strike_out)+","
                          + str(pa.swinging_strike_out) + "," + str(pa.ball_in_play) + "," + str(pa.home_run) + ","
                          + pa.result + "," + pa.hittype + "," + pa.hitlocation + ","
                          + str(pa.distance) + "," + str(pa.exitvelo)+"\n")
output_file.close()
