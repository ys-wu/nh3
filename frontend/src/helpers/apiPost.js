export default function apiPost(url, data) {
  console.log('Post params:', data);
  fetch(url, {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain',
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: JSON.stringify(data),
  }) 
    .then(res => res.json())
    .then(res => console.log('Post res:', res))
    .catch(console.error);
};
