def assert_calls_no_errors(calls: list) -> None:
    for call in calls:
        assert "error" not in str(call).lower()
