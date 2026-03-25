from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.team import Team
from models.player import Player
from schemas.team import TeamCreate
from exceptions import AlreadyExistsException

class TeamRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_team(self, team_data: TeamCreate, user_id: str) -> None:
        db_team = Team(
            name=team_data.name,
            user_id=user_id,
            players=[
                Player(
                    name=player.name,
                    surname=player.surname,
                    ciId=player.ciId,
                    birthDate=player.birthDate
                )
                for player in team_data.players
            ]
        )

        try:
            self.db.add(db_team)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            error_msg = str(e.orig).lower()
            if "unique" in error_msg:
                if "team_name_key" in error_msg:
                    raise AlreadyExistsException("Squadra già creata")
                elif "player_ciid_key" in error_msg:
                    raise AlreadyExistsException("Un giocatore è già presente, ricontrollare CI ID")
            raise Exception("Errore durante la creazione della squadra")
            
    
    def get_teams(self) -> list[Team]:
        return self.db.query(Team).all()
    
    def get_team_by_name(self, name: str) -> Team | None:
        return self.db.query(Team).filter(Team.name == name).first()
        