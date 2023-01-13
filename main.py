import time
from fastapi import FastAPI, Depends
from multiprocessing import Process
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlite3 import connect

SQLALCHEMY_DATABASE_URL = "sqlite:///file::memory:?cache=shared"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def report_data():  # This is the function that is called by the Process to log server usage
    db = SessionLocal()
    db.execute("""
            CREATE TABLE usage (
                value INTEGER
            )
            """)
    db.execute("INSERT INTO usage (value) VALUES (0)")
    while True:
        result = db.execute("SELECT value FROM usage")
        result = result.one()
        print(f"Usage: {result[0]}")
        time.sleep(10)


def create_app():
    print("Creating app")
    process = Process(target=report_data)
    process.start()
    app = FastAPI()
    return app


app = create_app()


@app.get("/")
async def upload_endpoint(db: Session = Depends(get_db)):
    db.execute("UPDATE usage SET value = value + 1")
    result = db.execute("SELECT value FROM usage")
    result = result.one()
    print(f"Usage: {result[0]}")
    return {"message": "Usage incremented"}
