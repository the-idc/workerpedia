let claim_matches = (re_search, c) => (re_search.test(c.claim) || re_search.test(c.response) || c.keywords.some(k => re_search.test(k)));

u("#search").on("input", event => {
  let search = event.target.value;
  let re_search = new RegExp(search, 'i');
  u("#claims").empty();
  CLAIMS
    .filter(c => claim_matches(re_search, c))
    .map(c => u("#claims").append(`<li><a href="#response" data-claim="${c.claim}">${c.claim}</a></li>`));
  console.log(CLAIMS);
})

u("#claims").on("click", "li a", event => {
  let c = CLAIMS.find(c => (c.claim == event.target.dataset.claim));

  u("#response").html(`
    <h2>${c.claim}</h2>
    ${c.response}`);
});
