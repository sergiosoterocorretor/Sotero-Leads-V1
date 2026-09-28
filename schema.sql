PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS leads (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 external_lead_id TEXT UNIQUE,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 name TEXT NOT NULL, phone TEXT, email TEXT, city TEXT, neighborhood TEXT,
 niche TEXT NOT NULL, product TEXT, intent TEXT, budget TEXT, income_range TEXT,
 down_payment TEXT, deadline TEXT, source TEXT, campaign TEXT, ad_group TEXT,
 keyword TEXT, consent_contact INTEGER NOT NULL DEFAULT 0, score INTEGER NOT NULL DEFAULT 0,
 status TEXT NOT NULL DEFAULT 'NOVO', notes TEXT
);
CREATE TABLE IF NOT EXISTS lead_events (
 id INTEGER PRIMARY KEY AUTOINCREMENT, lead_id INTEGER NOT NULL,
 event_type TEXT NOT NULL, event_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 payload TEXT, FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_source ON leads(source);
