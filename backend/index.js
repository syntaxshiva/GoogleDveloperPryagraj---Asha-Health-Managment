// index.js
const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

// --- Database Connection ---
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',       // your MySQL username
  password: '12345', // your MySQL password
  database: 'asha' // replace with your DB name
});

db.connect((err) => {
  if (err) {
    console.error('Database connection failed:', err);
    process.exit(1);
  }
  console.log('Connected to MySQL database.');
});

// --- Login Route ---
app.post('/login', (req, res) => {
  console.log('POST /login called');

  const { username, password } = req.body;
  console.log('Received credentials:', { username, password });

  if (!username || !password) {
    console.log('Missing username or password');
    return res.status(400).json({ message: 'Username and password are required.' });
  }

  const query = 'SELECT * FROM users WHERE username = ? AND password = ?';
  console.log('Executing query:', query);

  db.query(query, [username, password], (err, results) => {
    if (err) {
      console.error('Database query error:', err);
      return res.status(500).json({ message: 'Database query error.' });
    }

    console.log('Query results:', results);

    if (results.length > 0) {
      console.log('Login successful for user:', username);
      return res.json({ message: 'Login successful', user: results[0] });
    } else {
      console.log('Invalid username or password for user:', username);
      return res.status(401).json({ message: 'Invalid username or password' });
    }
  });
});

app.post("/add-visit", async (req, res) => {
  if (!req.session.user) {
    return res.status(401).json({ status: "error", message: "You must login first." });
  }

  const { patient_name, visit_type, blood_pressure, temperature, weight, pulse_rate, symptoms, additional_info } = req.body;

  try {
    const conn = await mysql.createConnection(dbConfig);
    const query = `
      INSERT INTO visits
      (patient_name, visit_type, blood_pressure, temperature, weight, pulse_rate, symptoms, additional_info, created_by)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;
    await conn.execute(query, [
      patient_name,
      visit_type,
      blood_pressure,
      temperature,
      weight,
      pulse_rate,
      JSON.stringify(symptoms), // store array as JSON string
      additional_info,
      req.session.user
    ]);
    await conn.end();

    res.json({ status: "success", message: `Visit added for ${patient_name} by ${req.session.user}.` });
  } catch (err) {
    res.json({ status: "error", message: err.message });
  }
});

// --- Start Server ---
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
