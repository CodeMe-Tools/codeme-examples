-- Unsafe destructive migration: dropping column without deprecation period
ALTER TABLE users DROP COLUMN email;
