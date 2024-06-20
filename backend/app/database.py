from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
# Reemplaza estos valores con los detalles reales de tu base de datos en Render
DATABASE_USER = "ub_sd_p2_db_uhic_user"
DATABASE_PASSWORD = "T94SUTgZRO1LB30mo7ojIjF3V68Xzp2r"
DATABASE_HOST = "dpg-cpbprmect0pc73aa0rng-a.frankfurt-postgres.render.com"
DATABASE_PORT = "5432"  # usualmente el puerto de PostgreSQL es 5432
DATABASE_NAME = "ub_sd_p2_db_uhic"
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgres://ub_sd_p2_db_uhic_user:T94SUTgZRO1LB30mo7ojIjF3V68Xzp2r@dpg-cpbprmect0pc73aa0rng-a/ub_sd_p2_db_uhic"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# check_same_thread...is needed only for SQLite. It's not needed for other databases.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()