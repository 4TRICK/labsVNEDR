import os
import logging
from colorama import Fore, Style
import matplotlib

# Используем бэкенд для headless-режима
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def setup_logging(log_dir="logs"):
    """Настроить логирование с разными уровнями и цветами."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_format = "%(asctime)s [%(levelname)s]: %(message)s"
    formatter = logging.Formatter(log_format)

    log_levels = {
        "DEBUG": {"filename": "debug.log", "level": logging.DEBUG, "color": Fore.CYAN},
        "INFO": {"filename": "info.log", "level": logging.INFO, "color": Fore.GREEN},
        "ERROR": {"filename": "error.log", "level": logging.ERROR, "color": Fore.RED},
    }

    loggers = {}

    for level_name, config in log_levels.items():
        handler = logging.FileHandler(os.path.join(log_dir, config["filename"]))
        handler.setFormatter(formatter)
        logger = logging.getLogger(level_name)
        logger.setLevel(config["level"])
        logger.addHandler(handler)
        loggers[level_name] = logger

    def log_with_color(level_name, message):
        """Логировать сообщение с цветом и записью в файл."""
        if level_name in log_levels:
            colored_message = log_levels[level_name]["color"] + message + Style.RESET_ALL
            print(colored_message)
            loggers[level_name].log(log_levels[level_name]["level"], message)

    return log_with_color


def save_plot(filename, project_key, results_dir="results"):
    """Сохранить график в папку результатов."""
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    filepath = os.path.join(results_dir, f"{project_key}_{filename}.png")
    plt.savefig(filepath)
    plt.close()  # Освобождаем память после сохранения графика
    print(Fore.GREEN + f"График сохранен: {filepath}" + Style.RESET_ALL)


def get_user_input(prompt):
    """Получить ввод от пользователя."""
    try:
        return input(Fore.YELLOW + prompt + Style.RESET_ALL)
    except EOFError:
        return ""
