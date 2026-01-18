PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  CHECK (email LIKE '%_@__%.__%')
);

CREATE TABLE IF NOT EXISTS homes (
  home_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  nickname TEXT NOT NULL,
  zip_code TEXT,
  CHECK (zip_code IS NULL OR length(zip_code) = 5),
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);
CREATE TABLE IF NOT EXISTS item_category (
  category_id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS usage_type (
  usage_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
  usage_type_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS electrical_item (
  item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  home_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  usage_type_id INTEGER NOT NULL,
  nickname TEXT NOT NULL,
  rated_watts REAL,
  FOREIGN KEY (home_id) REFERENCES homes(home_id),
  FOREIGN KEY (category_id) REFERENCES item_category(category_id),
  FOREIGN KEY (usage_type_id) REFERENCES usage_type(usage_type_id)
);

CREATE TABLE IF NOT EXISTS item_usage_event (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER NOT NULL,
  start_ts TEXT NOT NULL, -- store ISO-8601 string
  end_ts TEXT,
  CHECK (end_ts IS NULL OR end_ts > start_ts),
  FOREIGN KEY (item_id) REFERENCES electrical_item(item_id)
);

CREATE INDEX IF NOT EXISTS idx_item_usage_event_item_start
ON item_usage_event(item_id, start_ts);

CREATE TABLE IF NOT EXISTS meter (
  meter_id INTEGER PRIMARY KEY AUTOINCREMENT,
  home_id INTEGER NOT NULL,
  utility_meter_number TEXT NOT NULL UNIQUE,
  FOREIGN KEY (home_id) REFERENCES homes(home_id)
);

CREATE TABLE IF NOT EXISTS meter_hourly_reading (
  reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
  meter_id INTEGER NOT NULL,
  start_ts TEXT NOT NULL,
  end_ts TEXT NOT NULL,
  consumed_kwh REAL NOT NULL,
  CHECK (end_ts > start_ts),
  FOREIGN KEY (meter_id) REFERENCES meter(meter_id)
);

CREATE TABLE IF NOT EXISTS monthly_utility_rate (
  rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
  home_id INTEGER NOT NULL,
  month_year TEXT NOT NULL, -- format 'YYYY-MM'
  bill REAL NOT NULL,
  consumed_kwh REAL NOT NULL,
  FOREIGN KEY (home_id) REFERENCES homes(home_id)
);