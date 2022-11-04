import os
import json
from datetime import datetime
from marshmallow import Schema, fields, validate, post_loadc

# define a simple Python class representing a Stadium
class Stadium(object):
    def __init__(self, id: int, name: str, latitude: float, longitude: float):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    
    def __str__(self):
        return f"Stadium({self.name})"
    
# define the schema of a Stadium object
class StadiumSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()

    @post_load
    def make_stadium(self, data, many: bool, partial: bool):
        if many:
            return [Stadium(d['id'], d['name'], d['latitude'], d['longitude']) \
                        for d in data]
        else:
            d = data
            return Stadium(d['id'], d['name'], d['latitude'], d['longitude'])

# define a simple Python class representing a Team
class Team(object):
    def __init__(self, id: int, name: str, alpha_2: str, alpha_3: str, 
                    official_name: str, colors: dict):
        self.id = id
        self.name = name
        self.alpha_2 = alpha_2
        self.alpha_3 = alpha_3
        self.official_name = official_name
        self.colors = colors
    
    def __str__(self):
        return f"Team({self.name})"

# define the schema of a Team object
class TeamSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    alpha_3 = fields.Str()
    alpha_2 = fields.Str()
    official_name = fields.Str()
    colors = fields.Dict(values=fields.List(fields.Str()),
        keys=fields.Str(validate=validate.OneOf(('primary', 'secondary'))))
    
    @post_load
    def make_team(self, data, many: bool, partial: bool):
        if many:
            return [Team(d['id'], d['name'], d['alpha_2'], d['alpha_3'], 
                    d['official_name'], d['colors']) \
                        for d in data]
        else:
            d = data
            return Team(d['id'], d['name'], d['alpha_2'], d['alpha_3'], 
                    d['official_name'], d['colors'])

# define the schema of a Match object
class MatchSchema(Schema):
    id = fields.Int()
    group = fields.Str()
    date = fields.DateTime(format='iso')
    stadium = fields.Nested(StadiumSchema())
    home_team = fields.Nested(TeamSchema())
    away_team = fields.Nested(TeamSchema())

    @post_load
    def make_match(self, data, many: bool, partial: bool):
        if many:
            return [Match(d['id'], d['group'], d['date'], 
                        d['stadium'], d['home_team'], d['away_team']) \
                            for d in data]
        else:
            d = data
            return Match(d['id'], d['group'], d['date'], 
                        d['stadium'], d['home_team'], d['away_team'])
    


# define a simple Python class representing a Match
class Match(object):
    def __init__(self, id: int, group: str, date: datetime, stadium: Stadium,
                    home_team: Team, away_team: Team):
        self.id = id
        self.group = group
        self.date = date
        self.stadium = stadium
        self.home_team = home_team
        self.away_team = away_team
    
    def __str__(self):
        return f"Match({self.home_team.name} vs {self.away_team.name})"


# get the full path to the directory containing this file
script_dir = os.path.abspath(os.path.dirname(__file__))
# get the path to the data directory within the same directory as this script
data_dir = os.path.join(script_dir, 'data')

# load data from the data directory
jsonfile = os.path.join(data_dir, 'matches.json')
with open(jsonfile, 'rt', encoding='utf-8') as fin:
    jsondata = json.load(fin)

# convert this data using Schemas
matches = []
ms = MatchSchema()
for match_id, match_data in jsondata.items():
    match = ms.load(match_data)
    matches.append(match)
