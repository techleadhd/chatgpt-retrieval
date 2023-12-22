
DROP TABLE IF EXISTS chat_messages;


CREATE TABLE IF NOT EXISTS chat_messages (
    message_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    chatbot_response BOOLEAN DEFAULT FALSE,
    message_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);



INSERT INTO chat_messages (user_id, chatbot_response, message_text) VALUES (1, FALSE, 'Hello, chatbot!');
INSERT INTO chat_messages (user_id, chatbot_response, message_text) VALUES (NULL, TRUE, 'Hello, I am the chatbot.');



