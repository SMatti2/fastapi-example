from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres@localhost/fast_api_tutorial'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

















# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', user='postgres', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connected successfully')
#         break
#     except Exception as error:
#         print('Connection to database failed')
#         print(error)
#         time.sleep(2)
