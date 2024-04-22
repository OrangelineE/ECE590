-- Drop existing tables
DROP TABLE IF EXISTS reminders, slots, pills, boxes, patients CASCADE;

-- Create new tables
CREATE TABLE patients (
    p_patientid SERIAL PRIMARY KEY,
    p_email VARCHAR(255) NOT NULL,
    p_name VARCHAR(255) NOT NULL,
    p_password VARCHAR(255) NOT NULL,
    p_age INT
);

CREATE TABLE boxes (
    b_boxid SERIAL PRIMARY KEY,
    b_patientid INT REFERENCES patients (p_patientid)
);

CREATE TABLE pills (
    pill_pillid SERIAL PRIMARY KEY,
    pillname VARCHAR(255) NOT NULL,
    pill_description TEXT
);

CREATE TABLE slots (
    s_slotid SERIAL PRIMARY KEY,
    s_boxid INT REFERENCES boxes (b_boxid),
    s_pillid INT REFERENCES pills (pill_pillid),
    s_pillnum INT NOT NULL CHECK (s_pillnum >= 0)
);

CREATE TABLE reminders (
    r_reminderid SERIAL PRIMARY KEY,
    r_slotid INT REFERENCES slots (s_slotid),
    r_alarm TIMESTAMP NOT NULL,
    r_frequency INTERVAL DEFAULT '1 day',
    r_quantity INT NOT NULL CHECK (r_quantity > 0)
);


-- Insert initial data for a single patient
INSERT INTO patients (p_email, p_name, p_password, p_age) VALUES
('john.doe@example.com', 'John Doe', 'password123', 30);

-- Insert a box linked to the single patient
INSERT INTO boxes (b_patientid) VALUES
((SELECT p_patientid FROM patients WHERE p_email = 'john.doe@example.com'));

-- Insert pill types
INSERT INTO pills (pillname, pill_description) VALUES
('Aspirin', 'Used to reduce fever and relieve mild to moderate pain.'),
('Paracetamol', 'Commonly used for pain relief and to reduce fever.'),
('Ibuprofen', 'Anti-inflammatory drug used for pain relief, fever reduction, and against swelling.');

-- Retrieve the box id for use in slot creation
INSERT INTO slots (s_boxid, s_pillid, s_pillnum) VALUES
((SELECT b_boxid FROM boxes WHERE b_patientid = (SELECT p_patientid FROM patients WHERE p_email = 'john.doe@example.com')), (SELECT pill_pillid FROM pills WHERE pillname = 'Aspirin'), 10),
((SELECT b_boxid FROM boxes WHERE b_patientid = (SELECT p_patientid FROM patients WHERE p_email = 'john.doe@example.com')), (SELECT pill_pillid FROM pills WHERE pillname = 'Paracetamol'), 8),
((SELECT b_boxid FROM boxes WHERE b_patientid = (SELECT p_patientid FROM patients WHERE p_email = 'john.doe@example.com')), (SELECT pill_pillid FROM pills WHERE pillname = 'Ibuprofen'), 5);

-- Create reminders for each slot
INSERT INTO reminders (r_slotid, r_alarm, r_frequency, r_quantity) VALUES
((SELECT s_slotid FROM slots WHERE s_pillid = (SELECT pill_pillid FROM pills WHERE pillname = 'Aspirin')), '2024-01-01 08:00:00', '12 hours', 1),
((SELECT s_slotid FROM slots WHERE s_pillid = (SELECT pill_pillid FROM pills WHERE pillname = 'Paracetamol')), '2024-01-01 09:00:00', '24 hours', 2),
((SELECT s_slotid FROM slots WHERE s_pillid = (SELECT pill_pillid FROM pills WHERE pillname = 'Ibuprofen')), '2024-01-01 07:00:00', '8 hours', 1);