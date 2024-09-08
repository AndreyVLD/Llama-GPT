// place files you want to import through the `$lib` alias in this folder.
export enum Sender {
	User = 'user',
	Model = 'model'
}

export class Message {
	sender: Sender;
	content: string;

	constructor(user: Sender, content: string) {
		this.sender = user;
		this.content = content;
	}

	toJSON() {
		return { ...this };
	}
}
