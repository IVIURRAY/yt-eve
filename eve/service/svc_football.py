import json
import urllib.request
from collections import defaultdict
from datetime import datetime


def calculate_match_points(team1, team2, score1, score2):
    if score1 == score2:
        return {team1: 1, team2: 1}
    elif score1 > score2:
        return {team1: 3, team2: 0}
    else:
        return {team1: 0, team2: 3}


class Football:
    def table(self, league):
        year = int(datetime.now().strftime("%Y"))
        season = (
            f"{year}-{str(year+1)[-2:]}"
            if datetime.now().month >= 8
            else f"{year-1}-{str(year)[-2:]}"
        )
        results_url = f"https://raw.githubusercontent.com/openfootball/football.json/master/{season}/{league}.json"
        final_table = defaultdict(lambda: {"points": 0, "gd": 0})

        with urllib.request.urlopen(results_url) as url:
            results = json.loads(url.read().decode())

        print(f"Running {results['name']} table generator")
        for match in results["matches"]:
            if match.get("score"):
                team1 = match["team1"]
                team2 = match["team2"]
                score1 = match["score"]["ft"][0]
                score2 = match["score"]["ft"][1]

                match_outcome = calculate_match_points(team1, team2, score1, score2)
                final_table[team1] = {
                    "name": team1,
                    "points": final_table[team1]["points"] + match_outcome[team1],
                    "gd": final_table[team1]["gd"] + (score1 - score2),
                }
                final_table[team2] = {
                    "name": team2,
                    "points": final_table[team2]["points"] + match_outcome[team2],
                    "gd": final_table[team2]["gd"] + (score2 - score1),
                }

        return sorted(final_table.values(), key=lambda x: (-x["points"], -x["gd"]))
