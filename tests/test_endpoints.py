EXPECTED_ACTIVITY_KEYS = {
    "description",
    "schedule",
    "max_participants",
    "participants",
}


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload) == 9

    for activity_name, details in payload.items():
        assert isinstance(activity_name, str)
        assert EXPECTED_ACTIVITY_KEYS.issubset(details.keys())
        assert isinstance(details["description"], str)
        assert isinstance(details["schedule"], str)
        assert isinstance(details["max_participants"], int)
        assert isinstance(details["participants"], list)


def test_get_activities_includes_known_activity_names(client):
    response = client.get("/activities")
    payload = response.json()

    assert "Chess Club" in payload
    assert "Robotics Club" in payload
    assert "Debate Team" in payload
