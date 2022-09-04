# imports
from datetime import datetime
import json
import pandas as pd
import random
import requests
from twython import Twython

# strings for API key, secret and access token and secret
API_KEY = 'vhpynkwKKfrL0ADQBOFSYDqgF'
API_SECRET = 'm61cuInSI3A7Fn0eS4B1WTeHRQtpoVpCJ6QUEjakT6tHXP736u'
ACCESS_TOKEN = '1566388810350469120-Os5H39GvUXlbr58h6w5vKLYv6k46EE'
ACCESS_SECRET = '779pyfK4NxSjHn5QWvSfcoZeIQaLOcIU00E9XdgegGei9'

api = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

# select a random year between 1970 and 2021
season = random.randrange(1970,2022)

# define the URI that we want to use to pull the data
uri = f'https://api.football-data.org/v4/teams/64/matches?status=FINISHED&season={season}'
headers = {'X-Auth-Token': 'f15598eb91484458b49704ed3a8a5885'}

# submit request to the API
submission = requests.get(uri, headers=headers)

# how many Liverpool matches were there in that season?
total_matches = len(submission.json()['matches'])

# select a random match
game_of_season = random.randrange(1,total_matches)

# get the competition
competition = submission.json()['matches'][game_of_season]['competition']['name']

#  get the result and other information that require
#  first get the date and arrange it into a readable format
match_date = submission.json()['matches'][game_of_season]['utcDate']
date_obj = datetime.strptime(match_date[0:10], '%Y-%m-%d')
year = str(date_obj.year)
month = date_obj.strftime('%B')
day = date_obj.day
if day == 1:
    day_string = '1st'
elif day == 2:
    day_string = '2nd'
elif day == 3:
    day_string = '3rd'
else:
    day_string = str(day) + 'th'

#  get the rest of the details
home_team = submission.json()['matches'][game_of_season]['homeTeam']['shortName']
away_team = submission.json()['matches'][game_of_season]['awayTeam']['shortName']
result = submission.json()['matches'][game_of_season]['score']['winner']
scoreline_home = str(submission.json()['matches'][game_of_season]['score']['fullTime']['home'])
scoreline_away = str(submission.json()['matches'][game_of_season]['score']['fullTime']['away'])
final_score = scoreline_home + '-' + scoreline_away

#  now loop through and create the text that we nee
if home_team == 'Liverpool':
    if result == 'DRAW':
        message = f'On the {day_string} of {month} {year}, {home_team} played {away_team} at home in the {competition}, and drew the game {final_score}.'
    elif result == 'HOME_TEAM':
        message = f'On the {day_string} of {month} {year}, {home_team} played {away_team} at home in the {competition}, and won {final_score}.'
    elif result == 'AWAY_TEAM':
        message = f'On the {day_string} of {month} {year}, {home_team} played {away_team} at home in the {competition}, and lost {final_score[::-1]}.'
elif away_team == 'Liverpool':
    if result == 'DRAW':
        message = f'On the {day_string} of {month} {year}, {away_team} played {home_team} away in the {competition} and drew the game {final_score}.'
    elif result == 'HOME_TEAM':
        message = f'On the {day_string} of {month} {year}, {away_team} played {home_team} away in the {competition} and lost the game {final_score}.'
    elif result == 'AWAY_TEAM':
        message = f'On the {day_string} of {month} {year}, {away_team} played {home_team} away in the {competition} and won {final_score[::-1]}.'

print(message)

api.update_status(status=message)

