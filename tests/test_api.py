import uuid

async def test_health(client):
    response = await client.get("/")
    assert response.json() == {"Status": "Ok"}



async def test_get_all_tasks(client):
    response = await client.get("/tasks")
    data = response.json()
    assert response.status_code == 200
    assert type(data) == list



async def test_get_my_tasks(client, test_token):
    response = await client.get("/tasks/my", headers={
        "Authorization": f"Bearer {test_token}"
    })
    assert response.status_code == 200



async def test_add_task(test_task):
    assert test_task["task_title"] == "test task"
    assert test_task["is_completed"] == False
    assert "id" in test_task



async def test_get_task(client, test_token, test_task):
    response = await client.get(f"/tasks/{test_task['id']}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_task["id"]



async def test_update_task(client, test_token, test_task, test_updated_task):
    response = await client.put(f"/tasks/{test_task['id']}",
        headers={"Authorization": f"Bearer {test_token}"},
        json=test_updated_task
    )

    assert response.status_code == 200
    assert response.json()["is_completed"] == True



async def test_delete_task(client, test_token, test_task):
    response = await client.delete(f"/tasks/{test_task['id']}",
            headers={"Authorization": f"Bearer {test_token}"}
    )

    assert response.status_code == 204


async def test_register_user(client):
    unique_email = f"test_{uuid.uuid4()}@test.com"
    response = await client.post("/auth/register", json={
        "username": "newuser",
        "email": unique_email,
        "password": "password123"
    })
    assert response.status_code == 200



async def test_register_duplicate_user(client):
    await client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dup@test.com",
        "password": "password123"
    })
    response = await client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dup@test.com",
        "password": "password123"
    })
    assert response.status_code == 409



async def test_login_user(client):
    response = await client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()



async def test_login_wrong_password(client):
    response = await client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
