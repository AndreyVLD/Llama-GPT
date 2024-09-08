import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

export async function connectDB() {
	return await open({
		filename: './database/chat.db',
		driver: sqlite3.Database
	});
}

async function initializeDB() {
	const db = await connectDB();

	await db.exec(`
    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      content TEXT NOT NULL,
      sender TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    );
  `);

	console.log('Database initialized');
	return db;
}

initializeDB().catch((err) => {
	console.error('Error initializing database:', err);
});
