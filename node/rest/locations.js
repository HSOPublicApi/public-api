import axios from 'axios';

export async function getLocations(baseUrl, headers) {
  const res = await axios.get(`${baseUrl}/v1/locations`, headers);

  return res.data;
}