from locust import HttpUser, task, between
from random import randrange

class AppUser(HttpUser):
    wait_time=between(2,5)

    @task()
    def get_all_matches(self):
        self.client.get("api/match/all")

    @task()
    def get_previous_season(self):
        self.client.get("api/match/previous-season")

    @task
    def get_all_stats(self):
        self.client.get("api/stats/all")

    @task
    def get_all_teams(self):
        self.client.get("api/team/all")

    @task
    def create_match(self):
        teams_response = self.client.get('api/team/all')
        teams = teams_response.json()

        if len(teams) < 2:
            return

        team1 = teams[randrange(len(teams))]
        team2 = teams[randrange(len(teams))]

        data = {
            "startDate": "2025-05-13T15:30:00",
            "location": "Sample Location",
            "localTeamId": team1['id'],
            "visitorTeamId": team2['id']
        }
        match_response = self.client.post('api/match', json=data)
        match = match_response.json()
        self.client.get('api/match/' + match['id'])

    @task
    def create_fault(self):
        matches = self.client.get("api/match/all").json()
        if len(matches) < 1:
            return

        #selects random match
        match_index = randrange(len(matches))
        match = matches[match_index]

        #selects random visitor or local team
        team = 'visitorTeam'
        if match_index % 2 == 0:
            team = 'localTeam'
        players = match[team]['players']
        #selects random player
        player_index = randrange(len(players))
        player = players[player_index]

        data = {
            "matchId": match['id'],
            "playerId": player['id'],
            "type": "YELLOW_CARD"
        }
        self.client.post('api/match/fault', json=data)

    @task
    def create_annotation(self):
        matches = self.client.get("api/match/all").json()
        if len(matches) < 1:
            return

        #selects random match
        match_index = randrange(len(matches))
        match = matches[match_index]

        #selects random visitor or local team
        team = 'visitorTeam'
        if match_index % 2 == 0:
            team = 'localTeam'
        players = match[team]['players']

        #selects random player
        player_index = randrange(len(players))
        player = players[player_index]

        data = {
            "matchId": match['id'],
            "playerId": player['id'],
            "points": 2
        }
        self.client.post('api/match/annotation', json=data)