from job_tracker.tracking.database import init_db, add_application, get_all_applications, update_status, delete_application

def test_database_crud():
    """Test full create-read-update-delete cycle."""
    init_db()

    app_id = add_application({
        "company": "TestCorp",
        "role": "Test Engineer",
        "location": "Remote",
        "required_skills": ["Python", "testing"]
    })
    assert app_id is not None

    apps = get_all_applications()
    test_app = next((a for a in apps if a["id"] == app_id), None)
    assert test_app is not None
    assert test_app["company"] == "TestCorp"

    update_status(app_id, "applied")
    apps = get_all_applications()
    test_app = next((a for a in apps if a["id"] == app_id), None)
    assert test_app["status"] == "applied"

    delete_application(app_id)
    apps = get_all_applications()
    test_app = next((a for a in apps if a["id"] == app_id), None)
    assert test_app is None