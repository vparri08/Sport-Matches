from sqlalchemy.orm import Session
import models, schemas

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_team_by_name(db: Session, name: str):
    return db.query(models.Team).filter(models.Team.name == name).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(name=team.name, country=team.country, description=team.description)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(db: Session, team_id: int, team: schemas.TeamUpdate):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    db_team.name = team.name
    db_team.country = team.country
    db_team.description = team.description
    db.commit()
    db.refresh(db_team)
    return db_team

def delete_team(db: Session, team_id: int):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    db.delete(db_team)
    db.commit()
    return db_team

def get_competition(db: Session, competition_id: int):
    return db.query(models.Competition).filter(models.Competition.id == competition_id).first()

def get_competition_by_name(db: Session, name: str):
    return db.query(models.Competition).filter(models.Competition.name == name).first()

def get_competitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Competition).offset(skip).limit(limit).all()

def create_competition(db: Session, competition: schemas.CompetitionCreate):
    db_competition = models.Competition(name=competition.name, category=competition.category, sport=competition.sport)
    db.add(db_competition)
    db.commit()
    db.refresh(db_competition)
    return db_competition

def update_competition(db: Session, competition_id: int, competition: schemas.CompetitionUpdate):
    db_competition = db.query(models.Competition).filter(models.Competition.id == competition_id).first()
    db_competition.name = competition.name
    db_competition.category = competition.category
    db_competition.sport = competition.sport
    db.commit()
    db.refresh(db_competition)
    return db_competition

def delete_competition(db: Session, competition_id: int):
    db_competition = db.query(models.Competition).filter(models.Competition.id == competition_id).first()
    db.delete(db_competition)
    db.commit()
    return db_competition

def get_match(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id == match_id).first()

def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Match).offset(skip).limit(limit).all()

def create_match(db: Session, match: schemas.MatchCreate):
    db_match = models.Match(date=match.date, price=match.price)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def update_match(db: Session, match_id: int, match: schemas.MatchUpdate):
    db_match = db.query(models.Match).filter(models.Match.id == match_id).first()
    db_match.date = match.date
    db_match.price = match.price
    db.commit()
    db.refresh(db_match)
    return db_match

def delete_match(db: Session, match_id: int):
    db_match = db.query(models.Match).filter(models.Match.id == match_id).first()
    db.delete(db_match)
    db.commit()
    return db_match
