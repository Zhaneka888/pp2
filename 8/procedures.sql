CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names  VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i       INT;
    v_name  VARCHAR;
    v_phone VARCHAR;
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS invalid_contacts (
        name   VARCHAR,
        phone  VARCHAR,
        reason TEXT
    ) ON COMMIT DELETE ROWS;

    FOR i IN 1 .. array_length(p_names, 1) LOOP
        v_name  := p_names[i];
        v_phone := p_phones[i];

        IF v_phone NOT LIKE '+7%' OR length(v_phone) != 12 THEN
            INSERT INTO invalid_contacts(name, phone, reason)
            VALUES (v_name, v_phone, 'Invalid phone format (must be +7XXXXXXXXXX)');
            CONTINUE;
        END IF;

        IF EXISTS (SELECT 1 FROM phonebook WHERE name = v_name) THEN
            UPDATE phonebook SET phone = v_phone WHERE name = v_name;
        ELSE
            INSERT INTO phonebook(name, phone) VALUES (v_name, v_phone);
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook WHERE name = p_value OR phone = p_value;
END;
$$;