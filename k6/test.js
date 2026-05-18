import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },  // rampa subida
    { duration: '1m',  target: 50 },  // carga sostenida
    { duration: '30s', target: 100 }, // saturación
    { duration: '20s', target: 0 },   // rampa bajada
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed:   ['rate<0.05'],
  },
};

const ALB_URL = __ENV.ALB_URL || 'http://flask-app-alb-463011915.us-east-1.elb.amazonaws.com';

export default function () {
  const r = http.get(`${ALB_URL}/health`);
  check(r, { 'status 200': (res) => res.status === 200 });

  const r2 = http.get(`${ALB_URL}/api/items`);
  check(r2, { 'items ok': (res) => res.status === 200 });

  sleep(1);
}