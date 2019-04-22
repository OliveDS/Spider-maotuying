from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class SitesDB(DeclarativeBase):
    __tablename__ = "sites_table"

    id = Column(Integer, primary_key=True)
    site_name = Column('site_name', String(50))
    site_url = Column('site_url', String(300))

# mysql> describe sites_table;                                                    
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | id         | int(11)      | NO   | PRI | NULL    | auto_increment |
# | sites_name | varchar(50)  | YES  |     | NULL    |                |
# | sites_url  | varchar(300) | YES  |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+
# 3 rows in set (0.00 sec)