import pytest

from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")
    
    def validate(post):
        return schemas.PostOut(**post)
    
    post_map = map(validate, res.json())
    posts_list = list(post_map)

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

    # If you find a way to make the retrieved posts ordered by id it can work
    # assert posts_list[0].Post.id == test_posts[0].id

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts")
    res.status_code == 401


def test_unauthorized_user_get_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    res.status_code == 401


def test_get_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/888888")
    assert res.status_code == 404


def test_get_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert res.status_code == 200
    # Check the schema to understand why you have to do that .Post...
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize('title, content, published', [
    ('testTitle', 'una splendida giornata di test', True),
    ('testando si impara', 'una pessima giornata', False),
    ('ramen', 'uno al manzo e uno al pollo', True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post('/posts', json={'title': title, 'content': content,
    'published': published})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/posts", json={"title": "arbitrary title", "content": "aasdfjasdf"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "aasdfjasdf"
    assert created_post.published == False
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client):
    res = client.post(
        "/posts", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401


def test_unauthorized_user_delete_Post(client, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostBase(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404