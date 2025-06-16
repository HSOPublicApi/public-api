import axios from 'axios';

export async function getProviders(baseUrl, headers) {
  const res = await axios.get(`${baseUrl}/v1/providers`, headers);

  return res.data;
}