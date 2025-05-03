const assert = require('assert');
const { shoutText } = require('./text');

try {
  assert.strictEqual(shoutText('hello'), 'HELLO!');
  assert.strictEqual(shoutText('Node.js'), 'NODE.JS!');
  console.log('All tests passed!');
} catch (error) {
  console.error('Test failed:', error.message);
  process.exit(1);
}
