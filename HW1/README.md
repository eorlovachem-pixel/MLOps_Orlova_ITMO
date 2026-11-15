# Домашнее задание №1 · Инструментарий Python (uv, Ruff, ty)

**Дисциплина:** MLOps Basic, ИТМО, осень 2026.

## Условие из переписки

«Повторить то, что делали на первой лекции и практике. Создать любой GitHub проект с установленными и работающими uv, Ruff и ty. Сам код писать необязательно, можно написать минимальную одну функцию какую-нибудь любую».

## Что сделано

Создан **автономный** проект с простейшей функцией `normalized_mean`, аннотациями типов, тестами, настройкой `pyproject.toml` и GitHub Actions для проверки качества. Ни DVC, ни GitFlow, ни сложное ML-обучение для этого задания не нужны.

| Инструмент | Назначение | Где показано |
|---|---|---|
| uv | воспроизводимое окружение и управление пакетами | `pyproject.toml`, команды ниже |
| Ruff | статический линтинг и форматирование | `[tool.ruff]`, CI |
| ty | контроль Python-типов без запуска кода | `[tool.ty]`, типы в `quality.py` |
| pytest | необязательное дополнение: проверка функции | `tests/test_quality.py` |

## Выполнение (Windows PowerShell и Linux/macOS)

Из корня этой папки, при установленном `uv`:

```sh
uv --version
uv sync
uv run python main.py
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest -q
```

`uv sync` создаёт `.venv` и **настоящий** `uv.lock`; добавьте `uv.lock` в коммит. `uv.lock` нельзя заменять вымышленным текстом. Для повторения в новой среде используют `uv sync --locked` после формирования и коммита lockfile.

```sh
git init
git add .
git commit -m "feat(hw1): configure uv Ruff and ty"
git remote add origin https://github.com/YOUR_USERNAME/ITMO-MLOps-HW1.git
git branch -M main
git push -u origin main
```

Укажите **свой** GitHub URL вместо `YOUR_USERNAME`. Если репозиторий создан на GitHub с README, сначала согласуйте истории, не выполняйте принудительный push.

## Как защищать работу

Покажите `pyproject.toml`, объясните различие между спецификацией зависимостей и `uv.lock`, запустите четыре команды: программу, Ruff lint, Ruff format check и ty. После этого предъявите URL репозитория и успешный запуск CI.

> **Статус проверки:** Python-код и pytest проверяются в среде подготовки. Самих CLI Ruff/ty и сетевой установки пакетов здесь нет; результат их запуска на компьютере студента пока не подтверждён. Сведения о проверках приведены в общем отчёте.

### Официальные источники

- https://docs.astral.sh/uv/guides/projects/
- https://docs.astral.sh/ruff/formatter/
- https://docs.astral.sh/ty/configuration/


## Размещение в репозитории курса

Эта работа находится в собственной директории `HW1` репозитория [`MLOps_Orlova_ITMO`](https://github.com/eorlovachem-pixel/MLOps_Orlova_ITMO). Все команды запускаются **из папки `HW1`**, а не из корня репозитория. Блоки с `git init`, `git remote add` и отдельными репозиториями выше сохранены для понимания самостоятельной сдачи, но **не выполняйте их внутри общего репозитория**.
