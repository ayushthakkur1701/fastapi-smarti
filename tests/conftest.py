from fastapi.testclient import TestClient
from app.main import app
import os
import pytest
from app.oauth2 import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db,Base
from app import models

POSTGRES_DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(POSTGRES_DB_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# client = TestClient(app)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
    
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    #run our code before we run out test
    yield TestClient(app)
    #run our code after the test is finished

@pytest.fixture
def test_user2(client):
    user_data = {"email":"test123@gmail.com","password":"password123"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

   
@pytest.fixture
def test_user(client):
    user_data = {"email":"hello123@gmail.com","password":"password123"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
    

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session,test_user2):
    # post_data = [{
    #     "title":"Post 1",
    #     "content":"Content 1",
    #     "owner_id":test_user['id']
    # },{
    #     "title":"Post 2",
    #     "content":"Content 2",
    #     "owner_id":test_user['id']
    # },
    # {
    #     "title":"Post 3",
    #     "content":"Content 3",
    #     "owner_id":test_user['id']
    # }]

    # def create_posts_model(post):
    #     models.Post(**post)

    # post_map=map(create_posts_model,post_data)

    # posts_list = list(post_map)

    # session.add_all(posts_list)
    # session.commit()
    # posts = session.query(models.Post).all()
     post1 = models.Post(title="Test Post 1", content="Content 1",owner_id=test_user['id'])
     post2 = models.Post(title="Test Post 2", content="Content 2",owner_id=test_user['id'])
     post3 = models.Post(title="Test Post 3", content="Content 3",owner_id=test_user2['id'])
     session.add(post1)
     session.add(post2)
     session.add(post3)
     session.commit()
     return [post1, post2,post3]
    # return posts