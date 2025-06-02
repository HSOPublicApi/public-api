import { getAppointments } from './appointments.js';
import { getLocations } from './locations.js';
import { getPatients } from './patients.js';
import { getPracticeProcedures } from './practiceProcedures.js';
import { getProviders } from './providers.js';

export const routes = {
  'GET /appointments': async (req, res, config, headers) => {
    const data = await getAppointments(config.baseURL, headers);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  },

  'GET /locations': async (req, res, config, headers) => {
    const data = await getLocations(config.baseURL, headers);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  },

  'GET /patients': async (req, res, config, headers) => {
    const data = await getPatients(config.baseURL, headers);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  },

  'GET /practiceprocedures': async (req, res, config, headers) => {
    const data = await getPracticeProcedures(config.baseURL, headers);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  },

  'GET /providers': async (req, res, config, headers) => {
    const data = await getProviders(config.baseURL, headers);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  },
};