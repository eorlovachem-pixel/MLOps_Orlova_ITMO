# Домашнее задание №2 · Git, ветки, merge и GitFlow

**Дисциплина:** MLOps Basic, ИТМО, осень 2026.

## Что достоверно известно

Точная формулировка второго ДЗ не содержится в переданной переписке. По второй презентации и практическому конспекту преподаватель разбирал Git internals, `add`, `commit`, `log`, ветвление, `merge`, конфликты, GitFlow, совместную работу и Git LFS. Поэтому здесь подготовлен **самостоятельный практический проект с демонстрацией истории Git**. Git LFS включён как инструкция для дополнительного эксперимента, а не как обязательное условие.

## Реализовано

Крошечный ML-модуль `metrics.py` с метрикой accuracy и валидацией бинарных меток. Для репозитория создана настоящая локальная история:

- `main` — стабильная линия;
- `develop` — интеграционная линия;
- `feature/accuracy` — отдельная реализация метрики;
- `feature/validation` — валидация меток;
- `release/0.1.0` — выпуск;
- `hotfix/empty-dataset` — отдельное исправление;
- `feature/pr-demo` — **не слита** в `develop`, подготовлена для реального GitHub Pull Request.

Запустите:

```sh
git status
git branch -a
git log --graph --oneline --all --decorate
python -m unittest discover -s tests -v
```

Все коммиты доступны прямо в `.git` архивного проекта. Также приложен `history.bundle` — самостоятельная резервная копия всей истории: `git bundle verify history.bundle`.

## Публикация на GitHub (настоящий Pull Request)

1. Создайте **отдельный пустой** репозиторий `MLOps_Orlova_ITMO/HW2`.
2. Свяжите локальный репозиторий с GitHub:

```sh
git remote add origin https://github.com/YOUR_USERNAME/ITMO-MLOps-HW2.git
git push -u origin main
git push origin develop
git push origin feature/pr-demo
git push origin --tags
```

3. На GitHub откройте PR **`feature/pr-demo` → `develop`**, не сливайте без необходимости.
4. Сохраните ссылку на PR и скриншот графа коммитов для сдачи. Локальный merge, даже реальный, **не является** GitHub PR.

## Конфликт слияния: как показать

На двух ветках измените одну строку `MODEL_THRESHOLD`, выполните `git merge`, наблюдайте `<<<<<<<`, `=======`, `>>>>>>>`. Измените конфликтный файл, удалите маркеры, `git add`, `git commit`. Для отката незавершённого слияния: `git merge --abort`. Делайте конфликтный эксперимент в новых ветках, чтобы сохранить историю выше.

## Git LFS — дополнительное упражнение

Установите `git-lfs`, затем:

```sh
git lfs install
git lfs track "*.bin"
git add .gitattributes
git commit -m "chore: track binary models via Git LFS"
```

LFS-хранилище нужно для больших бинарных файлов; здесь намеренно не создаются большие веса модели и не делается ложных заявлений о проверенном LFS push.

> Автор демонстрационных коммитов: `ITMO MLOps Demonstration <mlops-demo@example.invalid>`. Это учебная локальная история; не утверждается, что эти коммиты сделаны студентом лично.


## Размещение в репозитории курса

Эта работа находится в собственной директории `HW2` репозитория [`MLOps_Orlova_ITMO`](https://github.com/eorlovachem-pixel/MLOps_Orlova_ITMO). Все команды запускаются **из папки `HW2`**, а не из корня репозитория. Блоки с `git init`, `git remote add` и отдельными репозиториями выше сохранены для понимания самостоятельной сдачи, но **не выполняйте их внутри общего репозитория**.

**Для проверки сохранённой истории:** `git clone history.bundle hw2-history`, затем `cd hw2-history && git log --all --graph --oneline --decorate`. GitHub не переносит коммиты из вложенного standalone-репозитория при добавлении папки в общий репозиторий, поэтому файл bundle сохраняет отдельную учебную историю.
