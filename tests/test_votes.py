import pytest
from app import models

@pytest.fixture
def test_vote(test_posts,session,test_user):
    new_vote = models.Vote(post_id=test_posts[0].id,user_id=test_user["id"])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client,test_posts):
    res = authorized_client.post("vote",json={"post_id":test_posts[0].id,"dir":1})
    res.status_code ==201

def test_vote_twice_post(authorized_client,test_posts,test_vote):
    res = authorized_client.post("/vote",json={"post_id":test_posts[0].id,"dir":1})
    assert res.status_code ==409

def test_delete_vote(authorized_client,test_posts,test_vote):
    res = authorized_client.post("/vote",json={"post_id":test_posts[0].id,"dir":0})
    res.status_code ==201

def test_delete_vote_nonexist(authorized_client,test_posts):
    res = authorized_client.post("/vote",json={"post_id":test_posts[1].id,"dir":0})
    res.status_code ==404

def test_delete_vote_nonexist(authorized_client,test_posts):
    res = authorized_client.post("/vote",json={"post_id":0000,"dir":1})
    res.status_code ==404

def test_vote_unauthorized_user(client,test_posts):
    res = client.post("/vote",json={"post_id":test_posts[1].id,"dir":1})
    res.status_code ==401