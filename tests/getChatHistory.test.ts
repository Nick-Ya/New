import { getChatHistory } from '../src/api/getChatHistory';

describe('GetChatHistory API', () => {
  it('should return chat history (status 200)', async () => {
    const response = await getChatHistory();
    expect(response.status).toBe(200);
    expect(Array.isArray(response.data)).toBe(true);
  });
});