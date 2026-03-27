def test_signup_successfully_adds_participant(client):
    email = "new.student@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_fails_for_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "a@b.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_fails_for_duplicate_participant(client):
    existing_email = "michael@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_requires_email_query_parameter(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422


def test_signup_is_case_sensitive_for_activity_name(client):
    response = client.post("/activities/chess%20club/signup", params={"email": "case@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_successfully_removes_participant(client):
    email = "daniel@mergington.edu"
    activity_name = "Chess Club"

    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_fails_for_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/signup", params={"email": "a@b.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_when_participant_not_registered(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "not.registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_twice_fails_on_second_attempt(client):
    email = "daniel@mergington.edu"
    url = "/activities/Chess%20Club/signup"

    first_response = client.delete(url, params={"email": email})
    second_response = client.delete(url, params={"email": email})

    assert first_response.status_code == 200
    assert second_response.status_code == 404
    assert second_response.json()["detail"] == "Participant not found in this activity"


def test_unregister_requires_email_query_parameter(client):
    response = client.delete("/activities/Chess%20Club/signup")

    assert response.status_code == 422
