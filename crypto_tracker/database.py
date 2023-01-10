import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

load_dotenv()

DATABASE_URL = os.getenv("DBURL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

mapper_registry = registry()

Base = mapper_registry.generate_base()