-- SQLite schema for Luxury Rentals

CREATE TABLE IF NOT EXISTS users (
  username TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  full_name TEXT,
  email TEXT,
  phone TEXT,
  city TEXT,
  joined TEXT,
  role TEXT DEFAULT 'customer'
);

CREATE TABLE IF NOT EXISTS orders (
  order_id TEXT PRIMARY KEY,
  username TEXT,
  full_name TEXT,
  email TEXT,
  phone TEXT,
  city TEXT,
  address TEXT,
  item_id INTEGER,
  item_name TEXT,
  item_emoji TEXT,
  item_category TEXT,
  price REAL,
  quantity INTEGER,
  deposit REAL,
  subtotal REAL,
  delivery_fee REAL,
  total REAL,
  pay_method TEXT,
  event_date TEXT,
  status TEXT,
  placed_at TEXT,
  placed_ip TEXT,
  items_json TEXT,
  FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  name TEXT,
  email TEXT,
  phone TEXT,
  message TEXT,
  sent_at TEXT,
  admin_reply TEXT,
  reply_subject TEXT,
  reply_sent_at TEXT,
  reply_to TEXT,
  status TEXT,
  FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS reviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER,
  username TEXT,
  name TEXT,
  rating INTEGER,
  comment TEXT,
  created_at TEXT
);

CREATE TABLE IF NOT EXISTS wishlist_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  item_id INTEGER,
  item_name TEXT,
  emoji TEXT,
  price REAL,
  quantity INTEGER,
  item_json TEXT,
  FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS loyalty (
  username TEXT PRIMARY KEY,
  points INTEGER,
  referral_code TEXT,
  referred_friends INTEGER,
  FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS promo_codes (
  code TEXT PRIMARY KEY,
  discount REAL,
  type TEXT,
  active INTEGER
);
