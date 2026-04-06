-- ================================================
-- EmiRise — Schéma Supabase
-- 4 logements : Jardin de Ponteves, La Suite 26, Villa Cezanne, Studio Mirabeau
-- ================================================

-- 1. TABLE LOGEMENTS
CREATE TABLE logements (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nom TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  description TEXT,
  adresse TEXT,
  capacite_max INTEGER DEFAULT 2,
  prix_nuit DECIMAL(10,2),
  photos TEXT[] DEFAULT '{}',
  equipements TEXT[] DEFAULT '{}',
  ical_url TEXT,
  actif BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. TABLE RESERVATIONS
CREATE TABLE reservations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  reference TEXT UNIQUE NOT NULL,
  logement_id UUID REFERENCES logements(id) ON DELETE CASCADE,
  prenom TEXT NOT NULL,
  nom TEXT NOT NULL,
  email TEXT NOT NULL,
  telephone TEXT,
  date_arrivee DATE NOT NULL,
  date_depart DATE NOT NULL,
  nb_voyageurs INTEGER DEFAULT 1,
  message TEXT,
  statut TEXT DEFAULT 'en_attente' CHECK (statut IN ('en_attente', 'confirme', 'refuse', 'annule')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. TABLE DISPONIBILITES (synchro iCal Airbnb)
CREATE TABLE disponibilites (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  logement_id UUID REFERENCES logements(id) ON DELETE CASCADE,
  date_debut DATE NOT NULL,
  date_fin DATE NOT NULL,
  source TEXT DEFAULT 'airbnb',
  uid_ical TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. TABLE LOGS SYNCHRO ICAL
CREATE TABLE ical_sync_log (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  logement_id UUID REFERENCES logements(id) ON DELETE CASCADE,
  statut TEXT DEFAULT 'ok' CHECK (statut IN ('ok', 'erreur')),
  nb_events INTEGER DEFAULT 0,
  message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ================================================
-- INDEX pour les recherches rapides
-- ================================================
CREATE INDEX idx_reservations_dates ON reservations(date_arrivee, date_depart);
CREATE INDEX idx_reservations_logement ON reservations(logement_id);
CREATE INDEX idx_reservations_statut ON reservations(statut);
CREATE INDEX idx_disponibilites_dates ON disponibilites(date_debut, date_fin);
CREATE INDEX idx_disponibilites_logement ON disponibilites(logement_id);

-- ================================================
-- FONCTION : Génération auto de référence (EMR-2026-0001)
-- ================================================
CREATE OR REPLACE FUNCTION generate_reservation_reference()
RETURNS TRIGGER AS $$
DECLARE
  year_part TEXT;
  seq_num INTEGER;
  new_ref TEXT;
BEGIN
  year_part := TO_CHAR(NOW(), 'YYYY');
  SELECT COUNT(*) + 1 INTO seq_num FROM reservations WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW());
  new_ref := 'EMR-' || year_part || '-' || LPAD(seq_num::TEXT, 4, '0');
  NEW.reference := new_ref;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reservation_reference
  BEFORE INSERT ON reservations
  FOR EACH ROW
  WHEN (NEW.reference IS NULL)
  EXECUTE FUNCTION generate_reservation_reference();

-- ================================================
-- FONCTION : updated_at automatique
-- ================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at := NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_logements_updated_at
  BEFORE UPDATE ON logements
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_reservations_updated_at
  BEFORE UPDATE ON reservations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ================================================
-- INSERTION DES 4 LOGEMENTS
-- ================================================
INSERT INTO logements (nom, slug, description) VALUES
  ('Jardin de Ponteves', 'jardin-de-ponteves', 'Logement avec jardin à Ponteves'),
  ('La Suite 26', 'la-suite-26', 'Suite élégante au coeur de la ville'),
  ('Villa Cezanne', 'villa-cezanne', 'Villa inspirée de l''art provençal'),
  ('Studio Mirabeau', 'studio-mirabeau', 'Studio cosy sur le cours Mirabeau');

-- ================================================
-- SÉCURITÉ RLS (Row Level Security)
-- ================================================
ALTER TABLE logements ENABLE ROW LEVEL SECURITY;
ALTER TABLE reservations ENABLE ROW LEVEL SECURITY;
ALTER TABLE disponibilites ENABLE ROW LEVEL SECURITY;
ALTER TABLE ical_sync_log ENABLE ROW LEVEL SECURITY;

-- Lecture publique des logements actifs
CREATE POLICY "Logements visibles publiquement" ON logements
  FOR SELECT USING (actif = true);

-- Création de réservation publique
CREATE POLICY "Créer une réservation" ON reservations
  FOR INSERT WITH CHECK (true);

-- Lecture dispo publique
CREATE POLICY "Disponibilités visibles" ON disponibilites
  FOR SELECT USING (true);
