-- Migration 002: Add status column safely with default
ALTER TABLE users ADD COLUMN status VARCHAR(32) DEFAULT 'active';
