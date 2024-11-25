import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"


# def fetch_jira_issues(project_key):
def fetch_jira_issues(project_key, selected_status):
    """Получить задачи из Jira для проекта."""
    try:
        params = {
            # "jql": f"project={project_key} AND status=Closed",
            "jql": f"project={project_key} AND status={selected_status}",
            "fields": "created, resolutiondate, status",
            "maxResults": 1000,
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Загружено {len(data.get('issues', []))} задач для проекта {project_key}.")
        return data.get("issues", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе задач Jira: {str(e)}")
        raise


def get_project_issues(project_key):
    """Получить задачи для анализа по проекту."""
    try:
        params = {
            "jql": f"project={project_key} AND status in (Open, Closed) AND created >= -60d",
            "fields": "created, resolutiondate",
            "maxResults": 1000,
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Загружено {len(data.get('issues', []))} задач для проекта {project_key} за последние 60 дней.")
        return data.get("issues", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе задач Jira: {str(e)}")
        raise


def get_assignee_issues(project_key):
    """Получить задачи с исполнителями и репортерами."""
    try:
        params = {
            "jql": f"project={project_key} AND assignee IS NOT EMPTY AND reporter IS NOT EMPTY",
            "fields": "assignee, reporter",
            "maxResults": 1000,
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Загружено {len(data.get('issues', []))} задач с назначенными исполнителями и репортерами.")
        return data.get("issues", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе задач Jira: {str(e)}")
        raise


def analyse_time_spent(project_key):
    """Анализ времени выполнения задач."""
    try:
        params = {
            "jql": f'project="{project_key}" AND status=Closed',
            "fields": "timespent",
            "maxResults": 1000,
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Загружено {len(data.get('issues', []))} задач для анализа времени выполнения.")
        return data.get("issues", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе задач Jira: {str(e)}")
        raise


def analyse_issues_with_priority(project_key):
    """Анализ задач по приоритету."""
    try:
        params = {
            "jql": f'project="{project_key}" AND status=Closed',
            "fields": "priority",
            "maxResults": 1000,
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Загружено {len(data.get('issues', []))} задач для анализа приоритетов.")
        return data.get("issues", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе задач Jira: {str(e)}")
        raise
