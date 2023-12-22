-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

-- First, we must delete (drop) all our tables
DROP TABLE IF EXISTS test_table;

-- Then, we recreate them
CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(255));

-- Finally, we add any records that are needed for the tests to run
INSERT INTO test_table (name) VALUES ('first_record');
