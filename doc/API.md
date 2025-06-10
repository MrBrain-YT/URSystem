<p align="center"><img src='../images/API.png'></img></p>

[Вернуться на главную страницу](../README.md)

# API Documentation

| Метод | Описание | Параметры |
|-------|----------|-----------|
| `сreate-account` | Создание аккаунта пользователя или робота | [Посмотреть здесь](#CreateAccount) |
| `delete-account` | Удаление аккаунта пользователя или робота  кроме пользователей с ролями (`SuperAdmin` и `System`)| [Посмотреть здесь](#DeleteAccount) |
| `get-accounts` | Получение всех аккаунтов пользователей в системе кроме пользователей с ролями (`SuperAdmin` и `System`) | [Посмотреть здесь](#GetAccounts) |.
| `get-account-data` | Получение роли и токена по логину и паролю аккаунта (данные от аккаунта с ролью System не передаются) | [Посмотреть здесь](#GetRoleAccount) |
| `change-password` | Изменение пароля аккаунта пользователя или робота | [Посмотреть здесь](#ChangePass) |
| `get-token` | Получение токена пользователя или робота (токен аккаунта с ролью System не передаются)| [Посмотреть здесь](#GetToken) |
| `change-token` | Изменение токена пользователя или робота (токен аккаунта с ролью System или robot не изменяются) | [Посмотреть здесь](#ChangeToken) |
| `get-frames` | Получение всех фреймов | [Посмотреть здесь](#GetFrames) |
| `get-frame` | Получение фрейма по идентификационному номеру | [Посмотреть здесь](#GetFrame) |
| `set-frame` | Установка значения для фрейма по идентификационному номеру | [Посмотреть здесь](#SetFrame) |
| `add-kinematic` | Добавление файлов кинематики в систему | [Посмотреть здесь](#AddKinematics) |
| `bind-kinematic` | Привязка файлов кинематики к роботу | [Посмотреть здесь](#AddKinematics) |
| `get-robot-log` | Получение логов робота | [Посмотреть здесь](#GetRobotLogs) |
| `add-robot-log` | Добавление логов робота | [Посмотреть здесь](#AddRobotLog) |
| `get-system-log` | Получение системного лога  | [Посмотреть здесь](#GetSystemLogs) |
| `add-system-log` | Добавление системных логов | [Посмотреть здесь](#AddSystemLog) |
| `create-robot` | Создание нового робота | [Посмотреть здесь](#CreateRobot) |
| `import-cache` | Импортирование конфигурации оборудования с другого сервера | [Посмотреть здесь](#ImportCache) |
| `export-file-cache` | Экспортирование конфигурации оборудования из файла | [Посмотреть здесь](#ExportFileCache) |
| `export-cache` | Экспортирование конфигурации оборудования из памяти системы (Позволяет получить самые свежие данные) | [Посмотреть здесь](#ExportCache) |
| `get-robot` | Получение параметров робота | [Посмотреть здесь](#GetRobot) |
| `get-robots` | Получение параметров всех роботов в системе | [Посмотреть здесь](#GetRobots) |
| `get-position` | Получение актуальной позиции робота | [Посмотреть здесь](#GetCurentPosition) |
| `get-position-id` | Получение id позиции робота | [Посмотреть здесь](#GetPositionID) |
| `get-speed` | Получение актуальной скорости робота | [Посмотреть здесь](#GetCurentSpeed) |
| `get-cartesian-position` | Получение актуальной декартовой позиции робота | [Посмотреть здесь](#GetXYZPosition) |
| `get-angles-count` | Получение количество осей робота | [Посмотреть здесь](#GetRobotAnglesCount) |
| `set-motors-position` | Установка актуальной позиции робота | [Посмотреть здесь](#SetCurentMotorsPosition) |
| `get-ready` | Получение параметра готовности робота к следующей команде перемещения | [Посмотреть здесь](#GetRobotReady) |
| `get-emergency` | Получение параметра аварийной ситуации робота | [Посмотреть здесь](#GetRobotEmergency) |
| `set-ready` | Установка параметра готовности робота к следующей команде перемещения | [Посмотреть здесь](#SetRobotReady) |
| `set-emergency` | Установка параметра аварийной ситуации робота | [Посмотреть здесь](#SetRobotEmergency) |
| `set-position-id` | Установка id позиции робота | [Посмотреть здесь](#SetPositionID) |
| `set-position` | Установка актуальной позиции робота | [Посмотреть здесь](#CurentPosition) |
| `remove-curent-point-position` | Удаление первой целевой позиции в многоточечной позиции (`multipoint position`) | [Посмотреть здесь](#RemoveCurentPointPosition) |
| `remove-all-point-position` | Удаление всех целевых позиций в многоточечной позиции (`multipoint position`) | [Посмотреть здесь](#RemoveAllPointPosition) |
| `set-home-position` | Установка домашней позиции робота | [Посмотреть здесь](#HomePosition) |
| `set-speed` | Установка актуальной скорости робота | [Посмотреть здесь](#CurentSpeed) |
| `remove-curent-point-speed` | Удаление первой целевой скорости в многоточечной позиции (`multipoint position`) | [Посмотреть здесь](#RemoveCurentPointSpeed) |
| `remove-all-point-speed` | Удаление всех целевых скоростей в многоточечной позиции (`multipoint position`) | [Посмотреть здесь](#RemoveAllPointSpeed) |
| `set-standart-speed` | Установка скорости робота по умолчанию (при включении) | [Посмотреть здесь](#StandartSpeed) |
| `set-program` | Загрузить програму автоматики для робота | [Посмотреть здесь](#SetProgram) |
| `delete-program` | Удалить програму автоматики для робота (Останавливаеться программа автоматики или происходит адаление поле завершения программы)| [Посмотреть здесь](#DeleteProgram) |
| `angles-to-cartesian` | Преобразование углов в декартовые координаты | [Посмотреть здесь](#angle_to_xyz) |
| `cartesian-to-angles` | Преобразование декартовых координат в углы | [Посмотреть здесь](#XYZ_to_angle) |
| `set-cartesian-position` | Перемещение робота по декартовым координатам (установка актуальной позиции по координатам) | [Посмотреть здесь](#Move_XYZ) |
| `set-min-angles` | Установка минимальных ограничений для осей | [Посмотреть здесь](#MinAngles) |
| `set-max-angles` | Установка максимальных ограничений для осей | [Посмотреть здесь](#MaxAngles) |
| `set-program-run` | Установка состояния параметра готовности робота к следующей команде перемещения | [Посмотреть здесь](#SetProgramRun) |
| `set-robot-tool` | Привязка инструмента к роботу | [Посмотреть здесь](#set-robot-tool) |
| `set-robot-base` | Привязка базы к роботу | [Посмотреть здесь](#set-robot-base) |
| `get-tools` | Получение данных всех инструментов | [Посмотреть здесь](#GetTools) |
| `get-tool` | Получение данных инструмента по идентификационному номеру | [Посмотреть здесь](#GetTool) |
| `set-tool` | Установка значения для параметра инструмента | [Посмотреть здесь](#set-tool) |
| `set-tool-calibration` | Установка значения для параметра калибровки инструмента | [Посмотреть здесь](#set-tool-calibration) |
| `create-tool` | Создание нового инструмента | [Посмотреть здесь](#CreateTool) |
| `delete-tool` | Удаление инструмента | [Посмотреть здесь](#DeleteTool) |
| `get-bases` | Получение данных всех баз | [Посмотреть здесь](#get-bases) |
| `get-base` | Получение данных базы по идентификационному номеру | [Посмотреть здесь](#get-base) |
| `create-base` | создание базы | [Посмотреть здесь](#create-base) |
| `set-base` | установка значения каллибровки базы | [Посмотреть здесь](#set-base) |
| `delete-base` | Удаление базы | [Посмотреть здесь](#delete-base) |

## Возвращаемый результат
```JSON
{
    "status": True,
    "info": "Robot ...",
    "data": {"J1": 10, "J2": 0, ...}
}
```
- `status`- статус обработки запроса без ошибок обрабатываемых системой
- `info`- информация о результате обработки запроса
- `data`- данные которые были запрошены (параметр может отсутсвовать если запрос не подразумевает получение данных)

## Параметры методов
- <h3 id="CreateAccount"> create-account </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `name` | **String** |
    || `password` | **String** |
    || `user_role` | **String** |
    || `token` | **String** |
    - ### Пример
        ```python
        data = {
            "name": 'TestAccount',
            "password": '12345',
            "user_role": 'administrator',
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="DeleteAccount"> delete-account </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `name` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "name": 'TestAccount',
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetAccounts"> get-accounts </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `token` | **String** |

    - ### Пример
        ```python
        data = {
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetRoleAccount"> get-account-data </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `name` | **String** |
    || `password` | **String** |
    || `server_token` | **String** |

    - ### Пример
        ```python
        data = {
            "name": 'TestAccount',
            "password": '12345'
            "server_token": 'htf121jhbt124e...'
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="ChangePass"> change-password </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `name` | **String** |
    || `password` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "name": 'TestAccount',
            "password": '12345',
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetToken"> get-token </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `name` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "name": 'TestAccount',
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="ChangeToken"> change-token </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `name` | **String** |
    || `password` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "name": 'TestAccount',
            "password": '12345',
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetFrames"> get-frames </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `token` | **String** |

    - ### Пример
        ```python
        data = {
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetFrame"> get-frame </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "id": "TestFrame",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="SetFrame"> set-frame </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `config` | **Any** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "id": "TestFrame",
            "config": {'pos_robots': 5},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="DelFrame"> delete-frame </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "id": "TestFrame",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="AddKinematics"> add-kinematic </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `file` | **bytes** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "token": "akjy7wefwjgv6qohg..."
        }
        files = {
            "file": open("test.zip", "rb")
        }
        requests.post(url, verify=True, json=data, files=files)
        ```
    ---
- <h3 id="BindKinematics"> bind-kinematic </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `robot` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "id": "TestKinematic",
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetRobotLogs"> get-robot-logs </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `timestamp` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "timestamp": "1746013996", # Unix time (Не обязательный параметр)
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="AddRobotLog"> add-robot-log </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `text` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "text": "HelloWorld",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetSystemLogs"> get-system-logs </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `timestamp` | **Int** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "timestamp": 1746013996, # Unix time (Не обязательный параметр)
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="AddSystemLog"> add-system-log </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `module` | **String** |
    || `text` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "module": "MyModule",
            "text": "HelloWorld",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="CreateRobot"> crate-robot </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `password` | **String** |
    || `angle` | **Int** |
    || `id` | **String \| None** |
    || `code` | **String \| None** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angle": 5,
            "id": "KinematicID",
            "code": "TestCode123",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="ImportCache"> import-cache </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robots` | **Dict** |
    || `tools` | **Dict** |
    || `frames` | **Dict** |
    || `bases` | **Dict** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "robots": {"testRobot": ...},
            "tools": {"Tool_1": ...},
            "frames": {"Frame_1": ...},
            "bases": {"Base_1": ...},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="ExportFileCache"> export-file-cache </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `token` | **String** |

    - ### Пример
        ```python
        data = {
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="ExportCache"> export-cache </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `token` | **String** |

    - ### Пример
        ```python
        data = {
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetRobot"> get-robot </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetRobots"> get-robots </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `token` | **String** |

    - ### Пример
        ```python
        data = {
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="DelRobot"> delete-robot </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetCurentPosition"> get-position </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetPositionID"> get-position-id </h3>

| Метод | Параметр | Тип данных |
|-|----------|------------|
|POST| `robot` | **String** |
|| `token` | **String** |

- ### Пример
    ```python
    data = {
        "robot": "TestRobot",
        "token": "akjy7wefwjgv6qohg..."
    }
    requests.post(url, verify=True, json=data)
    ```
    ---
- <h3 id="GetCurentSpeed"> get-speed </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetXYZPosition"> get-cartesian-position </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetRobotAnglesCount"> get-angles-count </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="SetCurentMotorsPosition"> set-motors-position </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `angles` | **Dict** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angles": {"J1": 10, "J2": 20, ...},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetRobotReady"> get-ready </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetRobotEmergency"> get-emergency </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="SetRobotReady"> set-ready </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `state` | **Bool** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="SetRobotEmergency"> set-emergency </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `state` | **Bool** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "state": True,
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="SetPositionID"> set-position-id </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `code` | **String** |
    || `id` | **Int** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "code": "123654",
            "id": 10,
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="CurentPosition"> set-position </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `angles` | **Dict** |
    || `angles_data` | **Array** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angles": {"J1": 10, "J2": 20, ...}, # Передавать либо angles либо angles_data для multipoint position
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
        ```python
        data = {
            "robot": "TestRobot",
            "angles_data": [{"J1": 10, "J2": 20, ...}, {...}, ...],
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="RemoveCurentPointPosition"> remove-curent-point-position </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="RemoveAllPointPosition"> remove-all-point-position </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="HomePosition"> set-home-position </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `angles` | **Dict** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="CurentSpeed"> set-speed </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `angles` | **Dict** |
    || `angles_data` | **Array** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angles": {"J1": 1, "J2": 0.5, ...}, # Передавать либо angles либо angles_data для multipoint position
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
        ```python
        data = {
            "robot": "TestRobot",
            "angles_data": [{"J1": 1, "J2": 0.5, ...}, {...}, ...],
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="RemoveCurentPointSpeed"> remove-curent-point-speed </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="RemoveAllPointSpeed"> remove-all-point-speed </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="StandartSpeed"> set-standart-speed </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `angles` | **Dict** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angles": {"J1": 1, "J2": 0.5, ...},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="SetProgram"> set-program </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `program` | **hex** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angles": "ads3ffea12daww2...",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="DeleteProgram"> delete-program </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="angle_to_xyz"> angles-to-cartesian </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `angles` | **Dict** |
    || `angles_data` | **Array** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angles": {"J1": 10, "J2": 100, ...}, # Передавать либо angles либо angles_data для multipoint position
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
        ```python
        data = {
            "robot": "TestRobot",
            "angles_data": [{"J1": 10, "J2": 100, ...}, {...}, ...],
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="XYZ_to_angle"> cartesian-to-angles </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `position` | **Dict** |
    || `positions_data` | **Array** |
    || `coordinate_system` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "position": {"x": 10, "y": 100, "z": 0, "a": 0, "b": 90, "c": 0}, # Передавать либо point либо points_data для multipoint position
            "coordinate_system": "world",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
        ```python
        data = {
            "robot": "TestRobot",
            "positions_data": [{"x": 10, "y": 100, "z": 0, "a": 0, "b": 90, "c": 0}, {...}, ...],
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="Move_XYZ"> set-cartesian-position </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `position` | **Dict** |
    || `positions_data` | **Array** |
    || `coordinate_system` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "position": {"x": 10, "y": 100, "z": 0, "a": 0, "b": 90, "c": 0}, # Передавать либо angles либо angles_data для multipoint position
            "coordinate_system": "world",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
        ```python
        data = {
            "robot": "TestRobot",
            "positions_data": [{"x": 10, "y": 100, "z": 0, "a": 0, "b": 90, "c": 0}, {...}, ...],
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="MinAngles"> set-min-angles </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `angles` | **Dict** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angles": {"J1": 10, "J2": 100, ...},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="MaxAngles"> set-max-angles </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `angles` | **Dict** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angles": {"J1": 10, "J2": 100, ...},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="SetProgramRun"> set-program-run </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `state` | **Bool** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "angles": {"J1": 10, "J2": 100, ...},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="set-robot-tool"> set-robot-tool </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `code` | **String** |
    || `id` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "cade": "123654",
            "id": "ToolID",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="set-robot-base"> set-robot-base </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `code` | **String** |
    || `id` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "cade": "123654",
            "id": "BaseID",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetTools"> GetTools </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="GetTool"> get-tool </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="set-tool"> set-tool </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `config` | **Any** |
    || `parameter` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "config": {"status": 1},
            "parameter": "info",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="set-tool-calibration"> set-tool-calibration </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `calibration_data` | **Dict** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "calibration_data": {"x": 0, "y": 0, "z": 0},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="CreateTool"> CreateTool </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="DeleteTool"> DeleteTool </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="get-bases"> get-bases </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="get-base"> get-base </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="create-base"> create-base </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="set-base"> set-base </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `data` | **Dict** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "data": {"x": 0, "y": 150, "z": 0,
                "a": 0, "b": 0, "c": 45},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="delete-base"> delete-base </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---