import { connectDB } from '$lib/database/database';
import { Message, Sender } from '$lib/index';

export async function getAllMessages(): Promise<Message[]> {
	const db = await connectDB();
	const rows = await db.all(`SELECT sender, content FROM messages`);
	return rows.map(row => new Message(row.sender as Sender, row.content));
}

export async function addMessage(content: string, sender: Sender) {
	const db = await connectDB();
	await db.run(`INSERT INTO messages (content, sender) VALUES (?,?)`, [content, sender]);
}

export async function getHistory(n: number): Promise<Message[]> {
	const db = await connectDB();
	const rows = await db.all(`SELECT sender, content FROM messages ORDER BY created_at DESC LIMIT ?`,
		[n]);
	return rows.map(row => new Message(row.sender as Sender, row.content).toJSON());
}