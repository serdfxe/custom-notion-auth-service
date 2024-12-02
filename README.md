# Auth Service

## Обзор
Сервис аутентификации отвечает за обработку аутентификации и авторизации пользователей. Он управляет регистрацией, входом в систему, сбросом паролей и другими связанными функциями.

## Возможности
- Регистрация и вход пользователей
- Сброс и восстановление пароля
- Генерация и проверка JWT токенов


openssl genpkey -algorithm RSA -out jwt-private.key
openssl rsa -pubout -in jwt-private.key -out jwt-public.key
