import axios from 'axios';

export async function getAppointments(baseUrl, headers) {
  const res = await axios.get(`${baseUrl}/v1/appointments`, headers);

  return res.data;
}