import pytest
from fastapi import HTTPException

from src.app import activities, signup_for_activity, unregister_from_activity


def test_signup_function_appends_participant_and_returns_message():
    email = "unit.student@mergington.edu"
    activity_name = "Robotics Club"

    result = signup_for_activity(activity_name, email)

    assert result == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_function_raises_for_duplicate_participant():
    duplicate_email = "michael@mergington.edu"

    with pytest.raises(HTTPException) as exc:
        signup_for_activity("Chess Club", duplicate_email)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Student already signed up"


def test_unregister_function_raises_when_participant_missing():
    with pytest.raises(HTTPException) as exc:
        unregister_from_activity("Music Band", "missing@mergington.edu")

    assert exc.value.status_code == 404
    assert exc.value.detail == "Participant not found in this activity"


def test_unregister_function_removes_existing_participant():
    email = "alex@mergington.edu"
    activity_name = "Robotics Club"

    result = unregister_from_activity(activity_name, email)

    assert result == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]
