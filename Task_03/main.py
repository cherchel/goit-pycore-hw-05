import sys
from datetime import datetime


def parse_log_line(line: str) -> dict:
    parts = line.strip().split(maxsplit=3)

    if len(parts) != 4:
        raise ValueError(f"Неправильний формат рядка: {line.strip()}")

    date, time, level, message = parts

    datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")

    if level not in ("INFO", "DEBUG", "ERROR", "WARNING"):
        raise ValueError(f"Невідомий рівень логування: {level}")

    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }


def load_logs(file_path: str) -> list:
    logs = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                logs.append(parse_log_line(line))

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:

    return [log for log in logs if log["level"] == level.upper()]


def count_logs_by_level(logs: list) -> dict:
    counts = {}

    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1

    return counts


def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<16} | Кількість")
    print(f"{'-' * 17}|{'-' * 10}")

    for level, count in counts.items():
        print(f"{level:<16} | {count}")


def main():
    if len(sys.argv) not in (2, 3):
        print("Використання: python main.py шлях_до_файлу [рівень]")
        return

    file_path = sys.argv[1]

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
        return
    except (OSError, UnicodeError) as error:
        print(f"Помилка читання файлу: {error}")
        return
    except ValueError as error:
        print(f"Помилка формату логу: {error}")
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) == 3:
        level = sys.argv[2].upper()
        filtered_logs = filter_logs_by_level(logs, level)

        print(f"\nДеталі логів для рівня '{level}':")

        if not filtered_logs:
            print("Записів не знайдено.")

        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()