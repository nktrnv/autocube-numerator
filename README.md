## Описание
Desktop-приложение для формирования последовательности номеров для УПД для центра коммерческой техники 
[Автокуб](https://autocube.su). Не рекомендуется передавать приложение сторонним лицам. Приложение предназначено для 
использования сотрудниками компании. Любой пользователь, получивший доступ к экземпляру приложения имеет возможность 
получать новые номера УПД.

## Установка зависимостей
```bash
poetry install
```

## Генерация ключа для YDB

Аутентификация от имени пользователя. Инструкцию по получению OAuth-токена можно найти 
[тут](https://cloud.yandex.ru/docs/iam/concepts/authorization/oauth-token).
```bash
yc config set token <OAuth-token>
```

Генерация статического ключа к базе данных.
```bash
yc iam key create --folder-id <folder-id> --service-account-name <serice-account-name> --output key-ydb-sa.json
```

## Сборка
```bash
pyinstaller application.spec
```

## Известные проблемы

- Приложение распознается антивирусом Microsoft Defender как ПО, содержащее вирусы. Связано со спецификой работы 
PyInstaller.
