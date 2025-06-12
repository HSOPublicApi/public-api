import http from 'http';
import url from 'url';
import axios from 'axios';
import { routes } from './router.js';
import { getConfigs } from './config/base.js';

const config = getConfigs();
const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const routeKey = `${req.method} ${parsedUrl.pathname}`;
  const handler = routes[routeKey];

  if (handler) {
    try {
      const headers = await getHeaders();

      await handler(req, res, config, { headers: headers });
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not Found' }));
  }
});

async function getHeaders() {
  const token = await getAccessToken();

  return {
    Authorization: token,
    'Organization-ID': config.organizationId,
    'Content-Type': 'application/json'
  }
}

async function getAccessToken() {
  const res = await axios.post(
    config.accessTokenURL,
    {
      'client_id': config.clientId,
      'client_secret': config.clientSecret
    },
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
  );

  return `${res?.data['token_type']} ${res?.data['access_token']}`
}

server.listen(config.port, () => {
  console.log(`Server running on port: ${config.port}`);
});