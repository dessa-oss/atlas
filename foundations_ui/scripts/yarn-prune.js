/**
 * Approximate `npm prune --production` using `yarn remove`.
 * @see https://github.com/yarnpkg/yarn/issues/696
 */
const exec = require('child_process').exec;
const devDependencies = Object.keys(require('../package.json').devDependencies).join(' ');
const command = 'yarn remove ' + devDependencies;

const child = exec(command, (err, stdout, stderr) => {
  if (err) throw err;
  console.log(`stdout: \n${stdout}`);
  console.log(`stderr: \n${stderr}`);
});