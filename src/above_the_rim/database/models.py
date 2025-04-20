from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from above_the_rim.database.db import Base

class Team(Base):
    __tablename__ = 'teams'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    SHORT = Column(String(3), unique=True, nullable=False)
    NAME = Column(String(50), unique=True, nullable=False)

class Game(Base):
    __tablename__ = 'games'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    HOME_TEAM_ID = Column(Integer, ForeignKey("teams.ID", ondelete="CASCADE", onupdate="CASCADE"))
    VISITING_TEAM_ID = Column(Integer, ForeignKey("teams.ID", ondelete="CASCADE", onupdate="CASCADE"))
    HOME_TEAM_SCORE = Column(Integer, default=0)
    VISITING_TEAM_SCORE = Column(Integer, default=0)
    home_team = relationship(Team, foreign_keys=[HOME_TEAM_ID])
    visiting_team = relationship(Team, foreign_keys=[VISITING_TEAM_ID])

class Quarters(Base):
    __tablename__ = 'quarters'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    GAME_ID = Column(Integer, ForeignKey("games.ID", ondelete="CASCADE", onupdate="CASCADE"))
    QUARTERS = Column(String(50))
    game = relationship(Game, foreign_keys=[GAME_ID])