from colorama import Fore, Style
from tasks import (
    task_build_open_state_histogram,
    task_build_status_time_diagrams,
    task_build_daily_tasks_graph,
    task_build_user_task_chart,
    build_time_spent_histogram,
    task_build_priority_chart,
)
from utils import get_user_input, setup_logging
from jira_api import (
    fetch_jira_issues,
    get_project_issues,
    get_assignee_issues,
    analyse_time_spent,
    analyse_issues_with_priority,
)

logger = setup_logging()  # Настройка логирования
def choose_status():
    statuses = ["Open", "Closed", "Reopened", "Resolved", "Patch Available", "In Progress"]
    print("Выберите начальный статус:")
    for i, status in enumerate(statuses, 1):
        print(f"{i}) {status}")

    while True:
        try:
            choice = int(input("Введите номер статуса: "))
            if 1 <= choice <= len(statuses):
                return statuses[choice - 1]  # Возвращаем выбранный статус
            else:
                print(f"Пожалуйста, выберите номер от 1 до {len(statuses)}.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")

def main():
    try:
        # Приветствие
        print(Fore.GREEN + "Добро пожаловать и спасибо, что выбрали мой скрипт!" + Style.RESET_ALL)

        # Выбор проекта
        project_key = get_user_input("Введите ключ проекта (например, 'KAFKA'): ")
        print(Fore.GREEN + f"Проект '{project_key}' успешно выбран." + Style.RESET_ALL)

        # Основной цикл
        while True:
            print("\nВыберите команду:")
            print("1 - Построить гистограмму времени задач в открытом состоянии")
            print("2 - Построить диаграммы распределения времени по состояниям")
            print("3 - Построить график создания и закрытия задач с накопительным итогом")
            print("4 - Построить график задач для пользователей")
            print("5 - Построить гистограмму времени выполнения задач")
            print("6 - Построить график задач по степени серьезности")
            print("7 - Завершить работу")

            command = get_user_input("Введите номер команды: ")

            if command == "1":
                issues = fetch_jira_issues(project_key)
                task_build_open_state_histogram(issues, project_key)
            elif command == "2":
                # abo_bus = choose_status()
                # print(f"Выбранный статус: {abo_bus}")
                selected_status = choose_status()  # Запрос на выбор статуса
                # issues = fetch_jira_issues(project_key)
                issues = fetch_jira_issues(project_key, selected_status)
                task_build_status_time_diagrams(issues, project_key, selected_status)
            elif command == "3":
                issues = get_project_issues(project_key)
                task_build_daily_tasks_graph(issues, project_key)
            elif command == "4":
                issues = get_assignee_issues(project_key)
                task_build_user_task_chart(issues, project_key)
            elif command == "5":
                issues = analyse_time_spent(project_key)
                build_time_spent_histogram(issues, project_key)
            elif command == "6":
                issues = analyse_issues_with_priority(project_key)
                task_build_priority_chart(issues, project_key)
            elif command == "7":
                print(Fore.BLUE + "Завершение работы. Спасибо, что использовали мой скрипт!" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Неверная команда. Пожалуйста, выберите из списка." + Style.RESET_ALL)
    except Exception as e:
        logger("ERROR", f"Произошла ошибка: {str(e)}")
        print(Fore.RED + "Ошибка в работе программы. Проверьте логи для деталей." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
