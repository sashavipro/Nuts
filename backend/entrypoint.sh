#!/bin/bash

set -e

echo "Сборка статических файлов..."
python manage.py collectstatic --noinput --clear

echo "Применение миграций базы данных..."
python manage.py migrate --noinput

echo "Проверка базы данных гео-локаций (cities_light)..."

RAW_OUTPUT=$(python manage.py shell -c "from cities_light.models import Country; print(Country.objects.count())" 2>/dev/null || echo "0")

COUNT=$(echo "$RAW_OUTPUT" | grep -oE '[0-9]+' | tail -n 1)

if [ -z "$COUNT" ]; then
    COUNT=0
fi

if [ "$COUNT" -eq "0" ]; then
    echo "База городов пуста. Запускаем загрузку GeoNames (это займет время)..."
    python manage.py cities_light
else
    echo "Гео-данные уже существуют (найдено стран: $COUNT). Пропуск."
fi

exec "$@"
