# -*- coding: utf-8 -*-
"""
run_chapters.py

RU:
    Текстовое меню для запуска Python-файлов из папки chapters/.

    Скрипт:
      1. Ищет папку chapters в текущей директории.
      2. Находит подпапки глав/разделов.
      3. В каждой подпапке находит .py файлы.
      4. Позволяет выполнить:
         - один конкретный файл;
         - все файлы выбранной подпапки;
         - все файлы всех подпапок;
         - выйти через 0.

    Запускать из корня проекта:

        uv run python run_chapters.py

    Важно:
        Скрипт запускает файлы командой:

        uv run python ./chapters/<chapter_folder>/<file.py>

EN:
    Text menu for running Python files from the chapters/ directory.

    Run from project root:

        uv run python run_chapters.py
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


CHAPTERS_DIR = Path("chapters")
PYTHON_EXT = ".py"


@dataclass(frozen=True)
class PythonFile:
    """
    RU:
        Описание найденного Python-файла.

    EN:
        Description of a discovered Python file.
    """
    chapter_dir: Path
    file_path: Path

    @property
    def relative_path(self) -> Path:
        """RU/EN: Path relative to project root."""
        return self.file_path

    @property
    def command(self) -> list[str]:
        """
        RU:
            Команда запуска через uv.

        EN:
            Run command through uv.
        """
        return ["uv", "run", "python", str(self.relative_path)]


def find_chapter_dirs(chapters_dir: Path = CHAPTERS_DIR) -> list[Path]:
    """
    RU:
        Возвращает список подпапок внутри chapters/.

    EN:
        Returns a list of subdirectories inside chapters/.
    """
    if not chapters_dir.exists():
        raise FileNotFoundError(
            f"Folder not found: {chapters_dir.resolve()}\n"
            "Run this script from the project root, where the chapters/ folder is located."
        )

    if not chapters_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {chapters_dir.resolve()}")

    return sorted(
        [p for p in chapters_dir.iterdir() if p.is_dir()],
        key=lambda p: p.name.lower(),
    )


def find_python_files(chapter_dir: Path) -> list[PythonFile]:
    """
    RU:
        Находит .py файлы внутри одной подпапки главы.
        Используется только первый уровень вложенности, без рекурсивного обхода.

    EN:
        Finds .py files inside one chapter subfolder.
        Uses only the first nesting level, without recursive traversal.
    """
    files = sorted(
        [p for p in chapter_dir.iterdir() if p.is_file() and p.suffix.lower() == PYTHON_EXT],
        key=lambda p: p.name.lower(),
    )
    return [PythonFile(chapter_dir=chapter_dir, file_path=p) for p in files]


def collect_project_files() -> dict[Path, list[PythonFile]]:
    """
    RU:
        Собирает структуру:
            подпапка главы -> список Python-файлов.

    EN:
        Builds a structure:
            chapter folder -> list of Python files.
    """
    chapter_dirs = find_chapter_dirs()
    result: dict[Path, list[PythonFile]] = {}

    for chapter_dir in chapter_dirs:
        files = find_python_files(chapter_dir)
        if files:
            result[chapter_dir] = files

    return result


def print_header(title: str) -> None:
    """
    RU:
        Печатает визуальный заголовок меню.

    EN:
        Prints a visual menu header.
    """
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def print_project_summary(project_files: dict[Path, list[PythonFile]]) -> None:
    """
    RU:
        Печатает найденные подпапки и количество .py файлов.

    EN:
        Prints discovered chapter folders and number of .py files.
    """
    print_header("Найденные подпапки chapters/")

    if not project_files:
        print("В chapters/ не найдено подпапок с .py файлами.")
        return

    for idx, (chapter_dir, files) in enumerate(project_files.items(), start=1):
        print(f"{idx:>2}. {chapter_dir.name}  —  {len(files)} .py файлов")


def ask_int(prompt: str, min_value: int, max_value: int) -> int:
    """
    RU:
        Безопасно запрашивает целое число в диапазоне.

    EN:
        Safely asks for an integer within a range.
    """
    while True:
        raw = input(prompt).strip()

        if raw == "":
            print("Введите число.")
            continue

        try:
            value = int(raw)
        except ValueError:
            print("Введите целое число.")
            continue

        if min_value <= value <= max_value:
            return value

        print(f"Введите число от {min_value} до {max_value}.")


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    """
    RU:
        Запрашивает ответ да/нет.

    EN:
        Asks for a yes/no answer.
    """
    raw = input(prompt).strip().lower()

    if raw == "":
        return default

    return raw in {"y", "yes", "д", "да"}


def run_python_file(py_file: PythonFile, stop_on_error: bool = False) -> bool:
    """
    RU:
        Запускает один Python-файл через uv run python.
        Возвращает True, если файл завершился успешно.

    EN:
        Runs one Python file through uv run python.
        Returns True if the file completed successfully.
    """
    print()
    print("-" * 80)
    print(f"Запуск: {' '.join(py_file.command)}")
    print("-" * 80)

    completed = subprocess.run(py_file.command, cwd=Path.cwd())

    if completed.returncode == 0:
        print(f"OK: {py_file.relative_path}")
        return True

    print(f"ERROR: {py_file.relative_path} завершился с кодом {completed.returncode}")

    if stop_on_error:
        raise RuntimeError(f"Stopped on error: {py_file.relative_path}")

    return False


def run_many(files: list[PythonFile], stop_on_error: bool = False) -> None:
    """
    RU:
        Запускает список Python-файлов и печатает итоговую статистику.

    EN:
        Runs a list of Python files and prints summary statistics.
    """
    if not files:
        print("Нет файлов для запуска.")
        return

    ok_count = 0
    fail_count = 0

    for py_file in files:
        try:
            ok = run_python_file(py_file, stop_on_error=stop_on_error)
        except RuntimeError as exc:
            print(str(exc))
            fail_count += 1
            break

        if ok:
            ok_count += 1
        else:
            fail_count += 1

    print_header("Итог запуска")
    print(f"Успешно: {ok_count}")
    print(f"Ошибок:   {fail_count}")
    print(f"Всего:    {ok_count + fail_count}")


def choose_file_menu(files: list[PythonFile]) -> None:
    """
    RU:
        Меню выбора одного файла внутри выбранной подпапки.

    EN:
        Menu for selecting a single file inside the selected chapter folder.
    """
    print_header("Выберите файл для запуска")

    for idx, py_file in enumerate(files, start=1):
        print(f"{idx:>2}. {py_file.file_path.name}")

    print(" 0. Назад")

    choice = ask_int("Ваш выбор: ", 0, len(files))
    if choice == 0:
        return

    run_python_file(files[choice - 1])


def chapter_menu(chapter_dir: Path, files: list[PythonFile]) -> None:
    """
    RU:
        Меню действий для выбранной подпапки главы.

    EN:
        Action menu for a selected chapter folder.
    """
    while True:
        print_header(f"Подпапка: {chapter_dir.name}")

        print("1. Запустить один файл")
        print("2. Запустить все файлы этой подпапки")
        print("3. Показать список файлов")
        print("0. Назад")

        choice = ask_int("Ваш выбор: ", 0, 3)

        if choice == 0:
            return

        if choice == 1:
            choose_file_menu(files)

        elif choice == 2:
            stop = ask_yes_no("Остановиться при первой ошибке? [y/N]: ", default=False)
            run_many(files, stop_on_error=stop)

        elif choice == 3:
            print_header(f"Файлы в {chapter_dir.name}")
            for idx, py_file in enumerate(files, start=1):
                print(f"{idx:>2}. {py_file.relative_path}")


def main_menu(project_files: dict[Path, list[PythonFile]]) -> None:
    """
    RU:
        Главное меню запуска.

    EN:
        Main runner menu.
    """
    chapter_dirs = list(project_files.keys())

    while True:
        print_project_summary(project_files)
        print()
        print("A. Запустить все .py файлы во всех подпапках")
        print("R. Обновить список файлов")
        print("0. Выход")
        print()
        print("Введите номер подпапки, A, R или 0.")

        raw = input("Ваш выбор: ").strip().lower()

        if raw == "0":
            print("Выход.")
            return

        if raw == "r":
            project_files = collect_project_files()
            chapter_dirs = list(project_files.keys())
            continue

        if raw == "a":
            all_files: list[PythonFile] = []
            for files in project_files.values():
                all_files.extend(files)

            stop = ask_yes_no("Остановиться при первой ошибке? [y/N]: ", default=False)
            run_many(all_files, stop_on_error=stop)
            input("Нажмите Enter, чтобы вернуться в меню...")
            continue

        try:
            choice = int(raw)
        except ValueError:
            print("Неверный ввод.")
            continue

        if 1 <= choice <= len(chapter_dirs):
            chapter_dir = chapter_dirs[choice - 1]
            chapter_menu(chapter_dir, project_files[chapter_dir])
        else:
            print(f"Введите число от 1 до {len(chapter_dirs)}, A, R или 0.")


def main() -> None:
    """
    RU:
        Точка входа.

    EN:
        Entry point.
    """
    print_header("Chapter runner")

    try:
        project_files = collect_project_files()
    except Exception as exc:
        print(f"Ошибка: {exc}")
        sys.exit(1)

    if not project_files:
        print("Нет .py файлов в подпапках chapters/.")
        sys.exit(0)

    main_menu(project_files)


if __name__ == "__main__":
    main()
