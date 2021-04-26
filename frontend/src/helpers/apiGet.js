export default function apiGet(
  url,
  processor=f=>f
) {
  fetch(url)
    .then(res => res.json())
    .then(processor)
    // .then(res => console.log('Get res:', res))
    .catch(console.error);
};
