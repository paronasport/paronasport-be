from repositories.team_repo import TeamRepo
from models.team import Team

class TeamService:
    def __init__(self, repo: TeamRepo):
        self.repo = repo
    
    def create_team(self, team_data) -> None:
        if len(team_data.players) < 5 or len(team_data.players) > 10:
            raise ValueError("La squadra deve avere tra 5 e 10 giocatori")

        self.repo.create_team(team_data)

    def get_teams(self) -> list[Team]:
        return self.repo.get_teams()