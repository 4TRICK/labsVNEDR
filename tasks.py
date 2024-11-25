import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict
from utils import save_plot, setup_logging

# Настройка логирования
log = setup_logging()


def task_build_open_state_histogram(issues, project_key):
    """
    Построить гистограмму времени задач в открытом состоянии.
    :param issues: Список задач из Jira.
    :param project_key: Ключ проекта Jira.
    """
    try:
        open_times = []
        for issue in issues:
            created = datetime.strptime(issue['fields']['created'], "%Y-%m-%dT%H:%M:%S.%f%z")
            closed = datetime.strptime(issue['fields']['resolutiondate'], "%Y-%m-%dT%H:%M:%S.%f%z")
            open_time = (closed - created).days
            open_times.append(open_time)

        bin_size = 10  # Интервал для группировки
        bins = range(0, max(open_times) + bin_size, bin_size)
        plt.hist(open_times, bins=bins, alpha=0.8, color='skyblue', edgecolor='blue')
        plt.xlabel('Время в открытом состоянии (дни)')
        plt.ylabel('Количество задач')
        plt.title(f'Гистограмма времени в открытом состоянии (проект: {project_key})')
        plt.grid(axis='y')
        save_plot("open_state_histogram", project_key)
        log("INFO", "Гистограмма времени в открытом состоянии успешно построена.")
    except Exception as e:
        log("ERROR", f"Ошибка в task_build_open_state_histogram: {e}")



def task_build_status_time_diagrams(issues, project_key, selected_status):
    """Построить диаграммы распределения времени по состояниям задачи с учетом выбранного начального статуса."""
    try:
        status_data = defaultdict(list)
        for issue in issues:
            changelog = issue.get('changelog', {}).get('histories', [])
            previous_status = selected_status  # Начинаем с выбранного статуса
            previous_time = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')

            for history in changelog:
                if 'field' in history['items'][0] and history['items'][0]['field'] == 'status':
                    current_status = history['items'][0]['toString']
                    current_time = datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                    time_spent = (current_time - previous_time).days
                    if time_spent > 0:
                        status_data[previous_status].append(time_spent)
                    previous_status = current_status
                    previous_time = current_time

            resolved_time = datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')
            time_spent = (resolved_time - previous_time).days
            if time_spent > 0:
                status_data[previous_status].append(time_spent)

        for status, times in status_data.items():
            plt.hist(times, bins=20, alpha=0.8, color='skyblue', edgecolor='blue')
            plt.xlabel('Время (дни)')
            plt.ylabel('Количество задач')
            plt.title(f'Время в статусе {status} (проект: {project_key})')
            plt.grid(axis='y')
            save_plot(f"status_{status}_time_distribution", project_key)
        log("INFO", "Диаграммы распределения времени по состояниям успешно построены.")
    except Exception as e:
        log("ERROR", f"Ошибка в task_build_status_time_diagrams: {e}")



# Функция для построения гистограммы времени выполнения задач
def task_build_time_spent_histogram(issues, project_key):
    """
    Построить гистограмму времени выполнения задач.
    :param issues: Список задач из Jira.
    :param project_key: Ключ проекта Jira.
    """
    try:
        time_spent_counts = defaultdict(int)
        time_spent_values = []

        for issue in issues:
            time_spent = issue['fields'].get('timespent')
            if time_spent is not None:
                time_spent_hours = time_spent / 3600  # Переводим секунды в часы
                time_spent_counts[time_spent_hours] += 1
                time_spent_values.append(time_spent_hours)

        if not time_spent_values:
            log("INFO", "Нет данных для построения гистограммы времени выполнения задач.")
            return

        # Построение гистограммы
        plt.figure(figsize=(10, 6))
        # plt.bar(times, counts, color='skyblue', edgecolor='blue')
        counts, bins, patches = plt.hist(time_spent_values, bins=10, color='skyblue', edgecolor='blue')
        plt.xlabel('Затраченное время (часы)')
        plt.ylabel('Количество задач')
        plt.title(f'Гистограмма затраченного времени на выполнение задач (проект: {project_key})')
        plt.grid(axis='y')
        # plt.xticks(range(0, int(max(times))+1, 1)) # задает последовательность чисел от 0 до int(max(times)) + 1 с шагом 10
        save_plot(f"time_spent_histogram", project_key)

        # Печатаем количество задач в каждой корзине
        for i in range(len(counts)):
            print(f"Корзина {i + 1} (с интервалом от {bins[i]} до {bins[i + 1]}): {counts[i]} задач")

    except Exception as e:
        log("ERROR", f"Ошибка в task_build_time_spent_histogram: {e}")


def task_build_daily_tasks_graph(issues, project_key):
    """Построить график количества заведенных и закрытых задач."""
    try:
        created_task_counts = defaultdict(int)
        closed_task_counts = defaultdict(int)

        for issue in issues:
            created_date = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
            created_task_counts[created_date] += 1
            if issue['fields']['resolutiondate']:
                closed_date = datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
                closed_task_counts[closed_date] += 1

        min_date = min(created_task_counts.keys() | closed_task_counts.keys())
        max_date = max(created_task_counts.keys() | closed_task_counts.keys())
        all_dates = [min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)]

        daily_created_counts = []
        daily_closed_counts = []
        cumulative_created = []
        cumulative_closed = []
        cumulative_created_total = 0
        cumulative_closed_total = 0

        for date in all_dates:
            daily_created_counts.append(created_task_counts.get(date, 0))
            daily_closed_counts.append(closed_task_counts.get(date, 0))
            cumulative_created_total += created_task_counts.get(date, 0)
            cumulative_closed_total += closed_task_counts.get(date, 0)
            cumulative_created.append(cumulative_created_total)
            cumulative_closed.append(cumulative_closed_total)

        plt.figure(figsize=(12, 6))
        plt.plot(all_dates, daily_created_counts, label="Ежедневно создано", color="blue")
        plt.plot(all_dates, daily_closed_counts, label="Ежедневно закрыто", color="green")
        plt.plot(all_dates, cumulative_created, label="Накопленный итог созданных", color="blue", linestyle="--")
        plt.plot(all_dates, cumulative_closed, label="Накопленный итог закрытых", color="red", linestyle="--")
        plt.xlabel("Дата")
        plt.ylabel("Количество задач")
        plt.legend()
        plt.grid(True)
        plt.title(f"График создания и закрытия задач (проект: {project_key})")
        save_plot("daily_tasks_graph", project_key)
        log("INFO", "График создания и закрытия задач успешно построен.")
    except Exception as e:
        log("ERROR", f"Ошибка в task_build_daily_tasks_graph: {e}")


def task_build_user_task_chart(issues, project_key):
    """Построить график задач для пользователей."""
    try:
        user_task_counts = defaultdict(int)
        for issue in issues:
            assignee = issue['fields'].get('assignee', {}).get('displayName')
            reporter = issue['fields'].get('reporter', {}).get('displayName')
            if assignee:
                user_task_counts[assignee] += 1
            if reporter:
                user_task_counts[reporter] += 1

        top_users = sorted(user_task_counts.items(), key=lambda x: x[1], reverse=True)[:30]
        usernames = [user[0] for user in top_users]
        task_counts = [user[1] for user in top_users]

        plt.barh(usernames, task_counts, color='skyblue')
        plt.xlabel("Количество задач")
        plt.ylabel("Пользователи")
        plt.title(f"Топ-30 пользователей по задачам (проект: {project_key})")
        plt.grid(axis='x')
        plt.gca().invert_yaxis()
        save_plot("user_task_chart", project_key)
        log("INFO", "График задач для пользователей успешно построен.")
    except Exception as e:
        log("ERROR", f"Ошибка в task_build_user_task_chart: {e}")


def build_time_spent_histogram(issues, project_key):
    """
    Построить гистограмму времени выполнения задач.
    :param issues: Список задач из Jira.
    :param project_key: Ключ проекта Jira.
    """
    try:
        # Словарь для хранения затраченного времени
        time_spent_counts = defaultdict(int)
        time_spent_values = []

        # Обрабатываем каждую задачу
        for issue in issues:
            time_spent = issue['fields'].get('timespent')
            if time_spent is not None:  # Проверка, если поле `timespent` не пустое
                time_spent_hours = time_spent / 3600  # Переводим секунды в часы
                time_spent_counts[time_spent_hours] += 1
                time_spent_values.append(time_spent_hours)
                print(f"ID задачи {issue['id']} ")
                print("Затраченное время", time_spent_hours)
        # Если данных нет, выводим сообщение
        if not time_spent_values:
            log("INFO", "Нет данных для построения гистограммы времени выполнения задач.")
            return

        # Строим гистограмму
        plt.figure(figsize=(10, 6))
        counts, bins, patches = plt.hist(time_spent_values, bins=10, color='skyblue', edgecolor='blue')
        plt.xlabel('Затраченное время (часы)')
        plt.ylabel('Количество задач')
        plt.title(f'Гистограмма затраченного времени на выполнение задач (проект: {project_key})')
        plt.grid(axis='y')

        # Сохраняем график
        save_plot(f"time_spent_histogram", project_key)

        # Печатаем количество задач в каждой корзине
        for i in range(len(counts)):
            print(f"Корзина {i + 1} (с интервалом от {bins[i]} до {bins[i + 1]}): {counts[i]} задач")

        log("INFO", f"Гистограмма времени выполнения задач для проекта '{project_key}' успешно построена.")

    except Exception as e:
        log("ERROR", f"Ошибка в task_build_time_spent_histogram: {e}")

def task_build_priority_chart(issues, project_key):
    """Построить график задач по степени серьезности."""
    try:
        priority_counts = defaultdict(int)
        for issue in issues:
            priority = issue['fields'].get('priority', {}).get('name')
            if priority:
                priority_counts[priority] += 1

        priorities = list(priority_counts.keys())
        counts = list(priority_counts.values())

        plt.bar(priorities, counts, color='skyblue', edgecolor='blue')
        plt.xlabel("Приоритет задачи")
        plt.ylabel("Количество задач")
        plt.title(f"Распределение задач по приоритетам (проект: {project_key})")
        plt.grid(axis='y')
        save_plot("priority_chart", project_key)
        log("INFO", "График задач по степени серьезности успешно построен.")
    except Exception as e:
        log("ERROR", f"Ошибка в task_build_priority_chart: {e}")
