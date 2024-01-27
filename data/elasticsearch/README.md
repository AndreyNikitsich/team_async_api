# Elasticsearch

[Назад](../README.md)

## Индексы

### `/films`

* id: keyword
* imdb_rating: float
* genres: objects list
  * id
  * name
* title: keyword
* description: text
* directors: objects list
  * id
  * name
* actors: objects list
  * id
  * name
* writers: objects list
  * id
  * name

### `/genres`

* id: keyword
* name: text
* description: text

### `/people`

* id: keyword
* full_name: text
* roles: text

## Добавление данных

### Добавление индекса

Чтобы добавить новый индекс, необходимо создать файл `<имя_индекса>.json` 
в папке `./indexes` и пересобрать контейнер

### Добавление/изменений полей в индексе

Чтобы изменить поля индекса, необходимо отредактировать соответствующий `json` файл 
в папке `./indexes` и пересобрать контейнер

>После внесения любых изменений необходимо оставить краткое описание в разделе
>>[История изменений](#история-изменений)

## Команды Make

### Собрать контейнер

```bash
make build
```

Собирает контейнер и настраивает индексы

### Запустить контейнер

```bash
make run
```

Запускает контейнер с elasticsearch 

###  Остановить контейнер

```bash
make stop
```

Останавливает контейнер с elasticsearch

## История изменений

27.01.24 Базовая версия индексов

[Назад](../README.md)
