
var assert = require('assert');

const urls = [
  'https://karlkarlkarl.com',
  'https://karlkarlkarl1.com'
];

const selector = 'span';
const expectedText = 'test';
const waitTimeoutMs = 15000;

async function checkUrl(url) {
  console.log(`Visiting: ${url}`);
  await $browser.get(url);

  const el = await $browser.waitForAndFindElement($driver.By.css(selector), waitTimeoutMs);

  const text = await el.getText();
  console.log(`Text found: "${text}" on ${url}`);

  assert.strictEqual(text, expectedText, `Text mismatch on ${url}`);
}

(async function run() {
  try {
    for (const url of urls) {
      await checkUrl(url);
    }
    console.log('All URLs passed.');
  } catch (err) {
    console.error(' Failure:', err && err.stack ? err.stack : err);
    throw err;
  }
})();
