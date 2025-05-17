-- 1. Создание таблицы самой бд
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50),
    name VARCHAR(255) NOT NULL,
    participants INT CHECK (participants > 0),
    date DATE NOT NULL,
    location VARCHAR(100),
    organizer VARCHAR(150)
);

COPY events(type, name, participants, date, location, organizer) 
FROM '/Users/daniillickovaha/Documents/learning/SQL/projects/SEA/bd/dataset.csv' WITH CSV HEADER;

-- 2. Таблицы для логирования

-- Лог удаленных событий c полной информацией
CREATE TABLE IF NOT EXISTS deleted_events_log (
    log_id SERIAL PRIMARY KEY,
    event_id INT NOT NULL,
    type VARCHAR(50),
    name VARCHAR(255),
    participants INT,
    date DATE,
    location VARCHAR(100),
    organizer VARCHAR(150),
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Универсальный лог изменений
CREATE TABLE IF NOT EXISTS event_changes_log (
    log_id SERIAL PRIMARY KEY,
    event_id INT NOT NULL,
    changed_column VARCHAR(50) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Триггер 1: Полная валидация даты (INSERT и UPDATE)
CREATE OR REPLACE FUNCTION validate_event_date()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.date < CURRENT_DATE THEN
        RAISE EXCEPTION 'Дата события не может быть в прошлом: %', NEW.date
        USING HINT = 'Используйте дату в будущем для события';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Проверка даты при вставке
CREATE TRIGGER before_insert_validate_date
BEFORE INSERT ON events
FOR EACH ROW
EXECUTE FUNCTION validate_event_date();

-- Проверка даты при обновлении
CREATE TRIGGER before_update_validate_date
BEFORE UPDATE OF date ON events
FOR EACH ROW
EXECUTE FUNCTION validate_event_date();

-- Триггер 2: Полное логирование удалений
CREATE OR REPLACE FUNCTION log_full_deleted_event()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO deleted_events_log (
        event_id, type, name, participants, 
        date, location, organizer
    ) VALUES (
        OLD.id, OLD.type, OLD.name, OLD.participants,
        OLD.date, OLD.location, OLD.organizer
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- После удаления события
CREATE TRIGGER after_delete_log_event
AFTER DELETE ON events
FOR EACH ROW
EXECUTE FUNCTION log_full_deleted_event();

-- Триггер 3: Универсальное логирование изменений
CREATE OR REPLACE FUNCTION log_all_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- Логирование изменения названия
    IF NEW.name <> OLD.name THEN
        INSERT INTO event_changes_log 
            (event_id, changed_column, old_value, new_value)
        VALUES 
            (OLD.id, 'name', OLD.name::TEXT, NEW.name::TEXT);
    END IF;

    -- Логирование изменения даты
    IF NEW.date::DATE <> OLD.date::DATE THEN
        INSERT INTO event_changes_log 
            (event_id, changed_column, old_value, new_value)
        VALUES 
            (OLD.id, 'date', OLD.date::TEXT, NEW.date::TEXT);
    END IF;

    -- Логирование изменения количества участников
    IF NEW.participants <> OLD.participants THEN
        INSERT INTO event_changes_log 
            (event_id, changed_column, old_value, new_value)
        VALUES 
            (OLD.id, 'participants', OLD.participants::TEXT, NEW.participants::TEXT);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- После обновления любого поля
CREATE TRIGGER after_update_log_changes
AFTER UPDATE ON events
FOR EACH ROW
WHEN (
    OLD.name IS DISTINCT FROM NEW.name OR
    OLD.date IS DISTINCT FROM NEW.date OR
    OLD.participants IS DISTINCT FROM NEW.participants
)
EXECUTE FUNCTION log_all_changes();

SELECT * FROM events LIMIT 10;
