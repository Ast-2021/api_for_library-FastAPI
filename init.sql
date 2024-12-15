CREATE DATABASE api_for_library_db;

\c api_for_library_db;

CREATE USER library_user WITH PASSWORD 'library_user';

GRANT ALL PRIVILEGES ON DATABASE api_for_library_db TO library_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO library_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO library_user;