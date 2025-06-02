import axios from 'axios';

export async function getPatients(baseUrl, headers) {
  const res = await axios.get(`${baseUrl}/v1/patients`, headers);

  return res.data;
}
