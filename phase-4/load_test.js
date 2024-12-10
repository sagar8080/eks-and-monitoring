import http from 'k6/http';
import { check, sleep } from 'k6';

// Configure test parameters
export let options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp-up to 20 virtual users (VUs)
    { duration: '30s', target: 20 },  // Hold at 20 VUs for 2 minutes
    { duration: '30s', target: 0 },  // Ramp-down to 0 VUs
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'], // 95% of requests should be below 200ms
    http_req_failed: ['rate<0.01'],   // Less than 1% of requests should fail
  },
};

export default function () {
  const url = 'http:localhost:3000'; // Replace with your service URL
  const payload = JSON.stringify({
    key1: 'value1',
    key2: 'value2',
  }); // Modify the payload based on your service requirements

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // Send POST request
  let response = http.post(url, payload, params);

  // Validate the response
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });

  sleep(1); // Pause for 1 second between iterations
}
