from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.Post(**post)
    post_map = map(validate,res.json())
    print(post_map)

    print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_post(client,test_posts):
    res = client.get("/posts")
    assert res.status_code ==401

def test_unauthorized_user_get_one_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code ==401

def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/0000")
    assert res.status_code ==404

def test_get_one_post_(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostWithVotes(**res.json())
    print(post)
    assert post.Post.id == test_posts[0].id
    assert res.status_code ==200

@pytest.mark.parametrize("title,content,published",[("title one","content one",True),
                                                     ("title 2","content 2",False),
                                                     ("title 3","content 3",True)])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    res =authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})

    post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published

def test_default_published_true(authorized_client,test_user,test_posts):
    res =authorized_client.post("/posts/",json={"title":"title","content":"content"})

    post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert post.title == "title"
    assert post.content == "content"
    assert post.published == True

def test_unauthorized_user_create_post(client,test_posts):
    res =client.post("/posts/",json={"title":"title","content":"content"})
    assert res.status_code ==401

def test_unauthorized_delete_post(client,test_user,test_posts):
    res =client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code ==401

def test_delete_post(authorized_client,test_user,test_posts):
    res =authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code ==204

def test_delete_post_nonexist(authorized_client,test_user,test_posts):
    res =authorized_client.delete(f"/posts/0000")
    assert res.status_code ==404

def test_delete_other_user_post(authorized_client,test_user,test_posts,test_user2):
    res =authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code ==403

def test_update_post(authorized_client,test_user,test_posts):
    data = {
        "title":"Update 1",
        "content":"Update 1",
        "id":test_posts[0].id
    }
    res =authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
    updated_post=schemas.Post(**res.json())
    assert res.status_code ==200
    assert updated_post.title == "Update 1"
    assert updated_post.content == "Update 1"

def test_update_other_user_post(authorized_client,test_user,test_posts,test_user2):
    data = {
        "title":"Update 1",
        "content":"Update 1",
        "id":test_posts[2].id
    }
    res =authorized_client.put(f"/posts/{test_posts[2].id}",json=data)
    assert res.status_code ==403
    

def test_unauthorized_update_post(client,test_user,test_posts):
    res =client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code ==401 

def test_update_post_nonexist(authorized_client,test_user,test_posts):
    data = {
        "title":"Update 1",
        "content":"Update 1",
        "id":test_posts[0].id
    }
    res =authorized_client.put(f"/posts/0000",json=data)
    assert res.status_code ==404
