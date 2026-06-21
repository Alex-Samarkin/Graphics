# -*- coding: utf-8 -*-
"""
run_chapters_menu.py

RU:
    Интерактивное текстовое меню для запуска Python-файлов из папки chapters/.

    Основной режим:
        questionary — красивое меню со стрелками.

    Установка:
        uv add questionary

    Запуск из корня проекта:
        uv run python run_chapters_menu.py

    Что умеет:
        - найти подпапки в ./chapters;
        - найти .py файлы внутри каждой подпапки;
        - запустить один файл;
        - запустить все файлы выбранной подпапки;
        - запустить все файлы всех подпапок;
        - обновить список файлов;
        - выйти.

    Команда запуска файлов:
        uv run python ./chapters/<chapter_folder>/<file.py>

EN:
    Interactive text menu for running Python files from ./chapters.

    Install:
        uv add questionary

    Run:
        uv run python run_chapters_menu.py
"""
from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


CHAPTERS_DIR = Path("chapters")
PYTHON_EXT = ".py"


try:
    import questionary
    from questionary import Choice

    HAS_QUESTIONARY = True
except ImportError:
    questionary = None
    Choice = None
    HAS_QUESTIONARY = False


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
        Рекурсивный обход не используется: только файлы первого уровня.

    EN:
        Finds .py files inside one chapter subfolder.
        No recursive traversal: only first-level files.
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
    result: dict[Path, list[PythonFile]] = {}

    for chapter_dir in find_chapter_dirs():
        files = find_python_files(chapter_dir)
        if files:
            result[chapter_dir] = files

    return result


def print_header(title: str) -> None:
    """
    RU:
        Печатает заголовок.

    EN:
        Prints a header.
    """
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def ask_yes_no(message: str, default: bool = False) -> bool:
    """
    RU:
        Запрашивает подтверждение.

    EN:
        Asks for confirmation.
    """
    if HAS_QUESTIONARY:
        answer = questionary.confirm(message, default=default).ask()
        return bool(answer)

    raw = input(f"{message} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
    if raw == "":
        return default
    return raw in {"y", "yes", "д", "да"}


def run_python_file(py_file: PythonFile, stop_on_error: bool = False) -> bool:
    """
    RU:
        Запускает один Python-файл через uv run python.

    EN:
        Runs one Python file through uv run python.
    """
    print()
    print("-" * 88)
    print(f"Запуск: {' '.join(py_file.command)}")
    print("-" * 88)

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
        Запускает несколько файлов и печатает итог.

    EN:
        Runs multiple files and prints a summary.
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


def pause() -> None:
    """
    RU:
        Пауза перед возвратом в меню.

    EN:
        Pause before returning to menu.
    """
    input("\nНажмите Enter, чтобы вернуться в меню...")


def choose_from_list(title: str, choices: list[tuple[str, object]], allow_back: bool = True) -> object | None:
    """
    RU:
        Универсальный выбор из списка.
        Если установлен questionary, используется меню со стрелками.
        Иначе используется числовой fallback.

    EN:
        Generic list selector.
        Uses arrow-key questionary menu when installed.
        Otherwise uses a numeric fallback.
    """
    if allow_back:
        choices = choices + [("← Назад / выход", None)]

    if HAS_QUESTIONARY:
        q_choices = [Choice(title=label, value=value) for label, value in choices]
        return questionary.select(title, choices=q_choices, use_shortcuts=True).ask()

    print_header(title)
    for idx, (label, _) in enumerate(choices, start=1):
        print(f"{idx:>2}. {label}")

    while True:
        raw = input("Ваш выбор: ").strip()
        try:
            idx = int(raw)
        except ValueError:
            print("Введите число.")
            continue

        if 1 <= idx <= len(choices):
            return choices[idx - 1][1]

        print(f"Введите число от 1 до {len(choices)}.")


def choose_file_menu(files: list[PythonFile]) -> None:
    """
    RU:
        Меню выбора одного файла.

    EN:
        Single-file selection menu.
    """
    choices = [
        (f"{idx:02d}. {py_file.file_path.name}", py_file)
        for idx, py_file in enumerate(files, start=1)
    ]

    selected = choose_from_list("Выберите файл для запуска", choices, allow_back=True)
    if selected is None:
        return

    run_python_file(selected)
    pause()


def chapter_menu(chapter_dir: Path, files: list[PythonFile]) -> None:
    """
    RU:
        Меню выбранной подпапки.

    EN:
        Selected chapter-folder menu.
    """
    while True:
        action = choose_from_list(
            f"Подпапка: {chapter_dir.name}",
            [
                ("Запустить один файл", "one"),
                (f"Запустить все файлы этой подпапки ({len(files)} файлов)", "chapter_all"),
                ("Показать список файлов", "list"),
            ],
            allow_back=True,
        )

        if action is None:
            return

        if action == "one":
            choose_file_menu(files)

        elif action == "chapter_all":
            stop = ask_yes_no("Остановиться при первой ошибке?", default=False)
            run_many(files, stop_on_error=stop)
            pause()

        elif action == "list":
            print_header(f"Файлы в {chapter_dir.name}")
            for idx, py_file in enumerate(files, start=1):
                print(f"{idx:>2}. {py_file.relative_path}")
            pause()


def main_menu(project_files: dict[Path, list[PythonFile]]) -> None:
    """
    RU:
        Главное меню.

    EN:
        Main menu.
    """
    while True:
        chapter_choices = [
            (f"{chapter_dir.name}  —  {len(files)} .py файлов", ("chapter", chapter_dir))
            for chapter_dir, files in project_files.items()
        ]

        global_choices = [
            ("▶ Запустить все .py файлы во всех подпапках", ("all", None)),
            ("↻ Обновить список файлов", ("refresh", None)),
        ]

        selected = choose_from_list(
            "Главное меню: выберите подпапку или действие",
            global_choices + chapter_choices,
            allow_back=True,
        )

        if selected is None:
            print("Выход.")
            return

        action, value = selected

        if action == "refresh":
            project_files = collect_project_files()
            continue

        if action == "all":
            all_files: list[PythonFile] = []
            for files in project_files.values():
                all_files.extend(files)

            stop = ask_yes_no("Остановиться при первой ошибке?", default=False)
            run_many(all_files, stop_on_error=stop)
            pause()
            continue

        if action == "chapter":
            chapter_dir = value
            chapter_menu(chapter_dir, project_files[chapter_dir])


def main() -> None:
    """
    RU:
        Точка входа.

    EN:
        Entry point.
    """
    print_header("Chapter runner menu")

    if not HAS_QUESTIONARY:
        print(
            "Модуль questionary не установлен. Будет использовано обычное числовое меню.\n"
            "Для меню со стрелками выполните:\n"
            "    uv add questionary\n"
        )

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
