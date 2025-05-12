import { getStateInstance } from '../src/api/getStateInstance';

describe('GetStateInstance API', () => {
  it('should return authorized state', async () => {
    const response = await getStateInstance();
    expect(response.status).toBe(200);
    expect(response.data).toHaveProperty('stateInstance');
    expect(response.data.stateInstance).toBe('authorized'); // дополнительная проверка
  });
});
