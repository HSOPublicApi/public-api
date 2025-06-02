import axios from 'axios';

export async function getPracticeProcedures(baseUrl, headers) {
  const res = await axios.get(`${baseUrl}/v1/practiceprocedures`, headers);

  return res.data;
}