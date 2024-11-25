import unittest
from tasks import task_build_open_state_histogram

class TestTaskBuildOpenStateHistogram(unittest.TestCase):
    def test_empty_issues(self):
        """Тест с пустым списком задач."""
        self.assertIsNone(task_build_open_state_histogram([], "TEST"))

    def test_valid_issues(self):
        """Тест с валидными данными задач."""
        issues = [
            {"fields": {"created": "2023-09-01T12:00:00.000+0000", "resolutiondate": "2023-09-05T12:00:00.000+0000"}},
            {"fields": {"created": "2023-08-15T12:00:00.000+0000", "resolutiondate": "2023-08-20T12:00:00.000+0000"}},
        ]
        self.assertIsNone(task_build_open_state_histogram(issues, "TEST"))
