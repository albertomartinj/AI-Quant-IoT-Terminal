const express = require('express');
const cors = require('cors');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');

// Load environment variables from the root .env file
require('dotenv').config({ path: path.join(__dirname, '../.env') });

const app = express();
const PORT = process.env.PORT || 3000;

// Setup Encryption Key
const ENCRYPTION_KEY = Buffer.from(process.env.ENCRYPTION_KEY || '', 'hex');

/**
 * Decrypts AES-256-GCM hex string back to float.
 */
function decryptData(hexString) {
    if (!hexString) return null;
    try {
        const data = Buffer.from(hexString, 'hex');
        const nonce = data.slice(0, 12);
        const ciphertext = data.slice(12, data.length - 16);
        const authTag = data.slice(data.length - 16);

        const decipher = crypto.createDecipheriv('aes-256-gcm', ENCRYPTION_KEY, nonce);
        decipher.setAuthTag(authTag);
        let decrypted = decipher.update(ciphertext, null, 'utf8');
        decrypted += decipher.final('utf8');
        
        return parseFloat(decrypted);
    } catch (error) {
        console.error('[Security Error] Failed to decrypt data:', error.message);
        return null;
    }
}

// Enable Cross-Origin Resource Sharing (CORS) to allow requests from the frontend
app.use(cors());

// Parse JSON bodies (as sent by API clients)
app.use(express.json());

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// -----------------------------------------------------------------------------
// Database Connection
// -----------------------------------------------------------------------------

// Path to the SQLite database (assuming it's saved in the project root by Module 1)
const dbPath = path.join(__dirname, '../quant_data.db');

// Establish a read-only connection to the SQLite database
const db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
    if (err) {
        console.error('[Database Error] Failed to connect:', err.message);
    } else {
        console.log('[Database] Connected to the SQLite database in read-only mode.');
    }
});

// -----------------------------------------------------------------------------
// Database Queries
// -----------------------------------------------------------------------------

/**
 * Fetches the latest portfolio status and alerts from the database.
 * Returns a Promise to allow async/await usage in the route handler.
 */
function getLatestPortfolioStatus() {
    return new Promise((resolve, reject) => {
        // SQL query to extract the most recent row based on timestamp.
        // Assuming 'portfolio_metrics' is the table name created by Module 1.
        const sql = `
            SELECT 
                timestamp,
                asset_symbol AS asset,
                current_price,
                entry_price,
                stop_loss_threshold,
                sentiment_label,
                action_signal,
                alert_severity
            FROM portfolio_metrics
            ORDER BY timestamp DESC
            LIMIT 1;
        `;

        db.get(sql, [], (err, row) => {
            if (err) {
                reject(err);
            } else if (row) {
                // Decrypt sensitive metrics before sending to the client
                row.current_price = decryptData(row.current_price);
                row.entry_price = decryptData(row.entry_price);
                row.stop_loss_threshold = decryptData(row.stop_loss_threshold);
                resolve(row);
            } else {
                resolve(null);
            }
        });
    });
}

// -----------------------------------------------------------------------------
// API Endpoints
// -----------------------------------------------------------------------------

/**
 * Endpoint: GET /api/portfolio/status
 * Returns the real-time data from the Python engine (Module 1).
 */
app.get('/api/portfolio/status', async (req, res) => {
    try {
        const latestData = await getLatestPortfolioStatus();

        if (!latestData) {
            // Return a 404 if the database is empty or the table has no rows
            return res.status(404).json({
                success: false,
                message: 'No data found in the database.'
            });
        }

        // Return the formatted JSON response matching our frontend requirements
        res.json({
            success: true,
            data: latestData
        });

    } catch (error) {
        console.error('[API Error]:', error.message);
        res.status(500).json({
            success: false,
            message: 'Internal server error while fetching portfolio status.'
        });
    }
});

/**
 * Mock Data Endpoint: Portfolio Performance (Historical)
 */
app.get('/api/portfolio', (req, res) => {
    const mockData = [
        { timestamp: '2023-01-01T00:00:00Z', value: 10000 },
        { timestamp: '2023-01-02T00:00:00Z', value: 10200 },
        { timestamp: '2023-01-03T00:00:00Z', value: 10150 },
        { timestamp: '2023-01-04T00:00:00Z', value: 10500 },
    ];
    res.json({ success: true, data: mockData });
});

// Fallback route: serve index.html for any other route (SPA behavior)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the HTTP server
app.listen(PORT, () => {
    console.log(`[Server] Dashboard API listening on http://localhost:${PORT}`);
    console.log(`[Server] Serving frontend from ${path.join(__dirname, 'public')}`);
});
