CREATE DATABASE api_for_library_db;
CREATE USER library_user WITH PASSWORD 'library_user';
GRANT ALL PRIVILEGES ON DATABASE api_for_library_db TO library_user;
ALTER USER myuser WITH;