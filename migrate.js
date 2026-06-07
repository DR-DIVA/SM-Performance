require('dotenv').config();
const { Client } = require('pg');
const fs = require('fs');
const path = require('path');

async function runMigration() {
    console.log('Connecting to Supabase...');
    const client = new Client({
        connectionString: process.env.DATABASE_URL,
    });

    try {
        await client.connect();
        console.log('Successfully connected to the database.');

        const schemaPath = path.join(__dirname, 'supabase_schema.sql');
        const sql = fs.readFileSync(schemaPath, 'utf8');

        console.log('Executing migration script...');
        await client.query(sql);

        console.log('Migration completed successfully! All tables created.');
    } catch (error) {
        console.error('Migration failed:', error);
    } finally {
        await client.end();
        console.log('Database connection closed.');
    }
}

runMigration();
