import { sendMessage } from '../src/api/sendMessage';

describe('SendMessage API', () => {
  it('should send a message without throwing an error', async () => {
    const chatId = '79524451967@c.us';
    const message = 'Hello from QA test!';
    await expect(sendMessage(message, chatId)).resolves.not.toThrow();
  });
});
