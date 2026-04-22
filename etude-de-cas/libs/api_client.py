import os
import requests
import unicodedata
from dotenv import dotenv_values

class APIFootballClient:
    """
    Cliente para conectarse a API-Football usando RapidAPI.
    Adaptado para Databricks Free Edition (carga .env desde Volumes).
    """

    def __init__(self, env_path:str = None):
        
        env = dotenv_values(env_path)
        self.api_key = env.get("API_FOOTBALL_KEY")

        if not self.api_key:
            raise ValueError("No se encontró API_FOOTBALL_KEY en el archivo .env")

        self.base_url = "https://v3.football.api-sports.io"

        self.headers = {
            "x-rapidapi-key": self.api_key
        }

    def get(self, endpoint: str, params: dict = None):
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

        return None

    def get_fixtures(self, league: int, season: int):
        params = {"league": league, "season": season}
        return self.get("fixtures", params)

    def normalize(self, text: str):
        if not text:
            return ""
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()

    def get_national_team_id(self, name: str):
        search_name = self.normalize(name)

        data = self.get("teams", params={"search": name})

        if not data or "response" not in data:
            return None

        candidates = []

        for item in data["response"]:
            team = item["team"]

            if team.get("national") is not True:
                continue

            api_name = self.normalize(team["name"])

            if api_name == search_name:
                return team["id"]

            if search_name in api_name:
                candidates.append(team["id"])

        if candidates:
            return candidates[0]

        return None
    
    def get_fixtures_by_team_id(self, team_id: int, start_year: int = 2023, end_year: int = 2026):
        all_fixtures = []

        for year in range(start_year, end_year + 1):
            data = self.get("fixtures", params={
                "team": team_id,
                "season": year
            })

            if data and "response" in data:
                all_fixtures.extend(data["response"])

        return all_fixtures
    
    def get_fixtures_for_multiple_teams(self, team_ids: list, start_year: int = 2023, end_year: int = 2026):
        all_fixtures = []

        for team_id in team_ids:
            fixtures = self.get_fixtures_by_team_id(team_id, start_year, end_year)
            all_fixtures.extend(fixtures)

        return all_fixtures
