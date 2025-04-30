<p align="center"><img src='../images/API.png'></img></p>

[Вернуться на главную страницу](../README.md)

# API Documentation

| Метод | Описание | Параметры |
|-------|----------|-----------|
| `CreateAccount` | Создание аккаунта пользователя или робота | [Посмотреть здесь](#CreateAccount) |
| `DeleteAccount` | Удаление аккаунта пользователя или робота  кроме пользователей с ролями (`SuperAdmin` и `System`)| [Посмотреть здесь](#DeleteAccount) |
| `GetAccounts` | Получение всех аккаунтов пользователей в системе кроме пользователей с ролями (`SuperAdmin` и `System`) | [Посмотреть здесь](#GetAccounts) |.
| `GetRoleAccount` | Получение роли и токена по логину и паролю аккаунта (данные от аккаунта с ролью System не передаются) | [Посмотреть здесь](#GetRoleAccount) |
| `ChangePass` | Изменение пароля аккаунта пользователя или робота | [Посмотреть здесь](#ChangePass) |
| `GetToken` | Получение токена пользователя или робота (токен аккаунта с ролью System не передаются)| [Посмотреть здесь](#GetToken) |
| `ChangeToken` | Изменение токена пользователя или робота (токен аккаунта с ролью System или robot не изменяются) | [Посмотреть здесь](#ChangeToken) |
| `GetFrames` | Получение всех фреймов | [Посмотреть здесь](#GetFrames) |
| `GetFrame` | Получение фрейма по идентификационному номеру | [Посмотреть здесь](#GetFrame) |
| `SetFrame` | Установка значения для фрейма по идентификационному номеру | [Посмотреть здесь](#SetFrame) |
| `AddKinematics` | Добавление файлов кинематики в систему | [Посмотреть здесь](#AddKinematics) |
| `BindKinematics` | Привязка файлов кинематики к роботу | [Посмотреть здесь](#AddKinematics) |
| `GetRobotLogs` | Получение логов робота | [Посмотреть здесь](#GetRobotLogs) |
| `AddRobotLog` | Добавление логов робота | [Посмотреть здесь](#AddRobotLog) |
| `GetSystemLogs` | Получение системного лога  | [Посмотреть здесь](#GetSystemLogs) |
| `AddSystemLog` | Добавление системных логов | [Посмотреть здесь](#AddSystemLog) |
| `CreateRobot` | Создание нового робота | [Посмотреть здесь](#CreateRobot) |
| `ImportCache` | Импортирование конфигурации оборудования с другого сервера | [Посмотреть здесь](#ImportCache) |
| `ExportFileCache` | Экспортирование конфигурации оборудования из файла | [Посмотреть здесь](#ExportFileCache) |
| `ExportCache` | Экспортирование конфигурации оборудования из памяти системы (Позволяет получить самые свежие данные) | [Посмотреть здесь](#ExportCache) |
| `GetRobot` | Получение параметров робота | [Посмотреть здесь](#GetRobot) |
| `GetRobots` | Получение параметров всех роботов в системе | [Посмотреть здесь](#GetRobots) |
| `GetCurentPosition` | Получение актуальной позиции робота | [Посмотреть здесь](#GetCurentPosition) |
| `GetPositionID` | Получение id позиции робота | [Посмотреть здесь](#GetPositionID) |
| `GetCurentSpeed` | Получение актуальной скорости робота | [Посмотреть здесь](#GetCurentSpeed) |
| `GetXYZPosition` | Получение актуальной декартовой позиции робота | [Посмотреть здесь](#GetXYZPosition) |
| `GetRobotAnglesCount` | Получение количество осей робота | [Посмотреть здесь](#GetRobotAnglesCount) |
| `SetCurentMotorsPosition` | Установка актуальной позиции робота | [Посмотреть здесь](#SetCurentMotorsPosition) |
| `GetRobotReady` | Получение параметра готовности робота к следующей команде перемещения | [Посмотреть здесь](#GetRobotReady) |
| `GetRobotEmergency` | Получение параметра аварийной ситуации робота | [Посмотреть здесь](#GetRobotEmergency) |
| `SetRobotReady` | Установка параметра готовности робота к следующей команде перемещения | [Посмотреть здесь](#SetRobotReady) |
| `SetRobotEmergency` | Установка параметра аварийной ситуации робота | [Посмотреть здесь](#SetRobotEmergency) |
| `SetPositionID` | Установка id позиции робота | [Посмотреть здесь](#SetPositionID) |
| `CurentPosition` | Установка актуальной позиции робота | [Посмотреть здесь](#CurentPosition) |
| `RemoveCurentPointPosition` | Удаление первой целевой позиции в многоточечной позиции (`multipoint position`) | [Посмотреть здесь](#RemoveCurentPointPosition) |
| `RemoveAllPointPosition` | Удаление всех целевых позиций в многоточечной позиции (`multipoint position`) | [Посмотреть здесь](#RemoveAllPointPosition) |
| `HomePosition` | Установка домашней позиции робота | [Посмотреть здесь](#HomePosition) |
| `CurentSpeed` | Установка актуальной скорости робота | [Посмотреть здесь](#CurentSpeed) |
| `RemoveCurentPointSpeed` | Удаление первой целевой скорости в многоточечной позиции (`multipoint position`) | [Посмотреть здесь](#RemoveCurentPointSpeed) |
| `RemoveAllPointSpeed` | Удаление всех целевых скоростей в многоточечной позиции (`multipoint position`) | [Посмотреть здесь](#RemoveAllPointSpeed) |
| `StandartSpeed` | Установка скорости робота по умолчанию (при включении) | [Посмотреть здесь](#StandartSpeed) |
| `SetProgram` | Загрузить програму автоматики для робота | [Посмотреть здесь](#SetProgram) |
| `DeleteProgram` | Удалить програму автоматики для робота (Останавливаеться программа автоматики или происходит адаление поле завершения программы)| [Посмотреть здесь](#DeleteProgram) |
| `angle_to_xyz` | Преобразование углов в декартовые координаты | [Посмотреть здесь](#angle_to_xyz) |
| `XYZ_to_angle` | Преобразование декартовых координат в углы | [Посмотреть здесь](#XYZ_to_angle) |
| `Move_XYZ` | Перемещение робота по декартовым координатам (установка актуальной позиции по координатам) | [Посмотреть здесь](#Move_XYZ) |
| `MinAngles` | Установка минимальных ограничений для осей | [Посмотреть здесь](#MinAngles) |
| `MaxAngles` | Установка максимальных ограничений для осей | [Посмотреть здесь](#MaxAngles) |
| `SetProgramRun` | Установка состояния параметра готовности робота к следующей команде перемещения | [Посмотреть здесь](#SetProgramRun) |
| `GetTools` | Получение данных всех инструментов | [Посмотреть здесь](#GetTools) |
| `GetTool` | Получение данных инструмента по идентификационному номеру | [Посмотреть здесь](#GetTool) |
| `CreateTool` | Создание нового инструмента | [Посмотреть здесь](#CreateTool) |
| `DeleteTool` | Удаление инструмента | [Посмотреть здесь](#DeleteTool) |

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
- <h3 id="CreateAccount"> CreateAccount </h3>

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
- <h3 id="DeleteAccount"> DeleteAccount </h3>

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
- <h3 id="GetAccounts"> GetAccounts </h3>

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
- <h3 id="GetRoleAccount"> GetRoleAccount </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `name` | **String** |
    || `password` | **String** |

    - ### Пример
        ```python
        data = {
            "name": 'TestAccount',
            "password": '12345'
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="ChangePass"> ChangePass </h3>

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
- <h3 id="GetToken"> GetToken </h3>

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
- <h3 id="ChangeToken"> ChangeToken </h3>

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
- <h3 id="GetFrames"> GetFrames </h3>

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
- <h3 id="GetFrame"> GetFrames </h3>

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
- <h3 id="SetFrame"> SetFrame </h3>

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
- <h3 id="DelFrame"> DelFrame </h3>

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
- <h3 id="AddKinematics"> AddKinematics </h3>

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
- <h3 id="BindKinematics"> BindKinematics </h3>

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
- <h3 id="GetRobotLogs"> GetRobotLogs </h3>

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
- <h3 id="AddRobotLog"> AddRobotLog </h3>

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
- <h3 id="GetSystemLogs"> GetSystemLogs </h3>

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
<!-- - <h3 id="AddSystemLog"> AddSystemLog </h3>

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
    --- -->
- <h3 id="CreateRobot"> CreateRobot </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
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
- <h3 id="ImportCache"> ImportCache </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robots` | **Dict** |
    || `tools` | **Dict** |
    || `frames` | **Dict** |
    || `token` | **String** |

    - ### Пример
        ```python
        data = {
            "robots": {"testRobot": ...},
            "tools": {"Tool_1": ...},
            "frames": {"Frame_1": ...},
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
- <h3 id="ExportFileCache"> ExportFileCache </h3>

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
- <h3 id="ExportCache"> ExportCache </h3>

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
- <h3 id="GetRobot"> GetRobot </h3>

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
- <h3 id="GetRobots"> GetRobots </h3>

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
- <h3 id="DelRobot"> DelRobot </h3>

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
- <h3 id="GetCurentPosition"> GetCurentPosition </h3>

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
- <h3 id="GetPositionID"> GetPositionID </h3>

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
- <h3 id="GetCurentSpeed"> GetCurentSpeed </h3>

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
- <h3 id="GetXYZPosition"> GetXYZPosition </h3>

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
- <h3 id="GetRobotAnglesCount"> GetRobotAnglesCount </h3>

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
- <h3 id="SetCurentMotorsPosition"> GetRobotAnglesCount </h3>

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
- <h3 id="GetRobotReady"> GetRobotReady </h3>

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
- <h3 id="GetRobotEmergency"> GetRobotEmergency </h3>

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
- <h3 id="SetRobotReady"> SetRobotReady </h3>

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
- <h3 id="SetRobotEmergency"> SetRobotEmergency </h3>

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
- <h3 id="SetPositionID"> SetPositionID </h3>

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
- <h3 id="SetRobotEmergency"> SetRobotEmergency </h3>

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
- <h3 id="CurentPosition"> CurentPosition </h3>

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
- <h3 id="RemoveCurentPointPosition"> RemoveCurentPointPosition </h3>

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
- <h3 id="RemoveAllPointPosition"> RemoveAllPointPosition </h3>

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
- <h3 id="HomePosition"> HomePosition </h3>

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
- <h3 id="CurentSpeed"> CurentSpeed </h3>

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
- <h3 id="RemoveCurentPointSpeed"> RemoveCurentPointSpeed </h3>

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
- <h3 id="RemoveAllPointSpeed"> RemoveAllPointSpeed </h3>

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
- <h3 id="StandartSpeed"> StandartSpeed </h3>

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
- <h3 id="SetProgram"> SetProgram </h3>

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
- <h3 id="DeleteProgram"> DeleteProgram </h3>

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
- <h3 id="angle_to_xyz"> angle_to_xyz </h3>

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
- <h3 id="XYZ_to_angle"> XYZ_to_angle </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `position` | **Dict** |
    || `positions_data` | **Array** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "position": {"x": 10, "y": 100, "z": 0, "a": 0, "b": 90, "c": 0}, # Передавать либо point либо points_data для multipoint position
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
- <h3 id="Move_XYZ"> Move_XYZ </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `robot` | **String** |
    || `position` | **Dict** |
    || `positions_data` | **Array** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "robot": "TestRobot",
            "position": {"x": 10, "y": 100, "z": 0, "a": 0, "b": 90, "c": 0}, # Передавать либо angles либо angles_data для multipoint position
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
- <h3 id="MinAngles"> MinAngles </h3>

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
- <h3 id="MaxAngles"> MaxAngles </h3>

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
- <h3 id="SetProgramRun"> SetProgramRun </h3>

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
- <h3 id="GetTool"> GetTool </h3>

    | Метод | Параметр | Тип данных |
    |-|----------|------------|
    |POST| `id` | **String** |
    || `type` | **String** |
    || `config` | **Any** |
    || `token` | **String** |
    
    - ### Пример
        ```python
        data = {
            "id": "ToolID",
            "type": "read",
            "config": "", # При type="read" config не обязателен (можно не указывать)
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```

        ```python
        data = {
            "id": "ToolID",
            "type": "write",
            "config": {"enable": True},
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
            "id": "ToolID"
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
            "id": "ToolID"
            "token": "akjy7wefwjgv6qohg..."
        }
        requests.post(url, verify=True, json=data)
        ```
    ---
