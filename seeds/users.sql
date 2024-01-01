
DROP TABLE IF EXISTS users CASCADE;


CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);


INSERT INTO users (username, email) VALUES ('john_doe', 'john@example.com');