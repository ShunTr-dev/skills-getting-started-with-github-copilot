from pathlib import Path

from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    # Restore state for subsequent tests
    activities[activity_name]["participants"].append(email)


def test_unregister_participant_returns_404_for_unknown_participant():
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_ui_refreshes_activity_list_after_success():
    app_js = Path("src/static/app.js").read_text()

    assert 'showMessage(result.message, "success");\n        signupForm.reset();\n        await fetchActivities();' in app_js
