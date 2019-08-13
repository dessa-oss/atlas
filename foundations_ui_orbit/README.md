Requirements:
- yarn or npm
- node
- libsass

Install:
- Download Foundations
- UI code lives in foundations_ui folder
- yarn or npm install

Running:
- cp env_example.sh env.sh
- edit env.sh to point to your api
- source ./env.sh
- yarn or npm start

Testing:
- Tests are in /src/tests
- Test must be in format of file.test.js
- yarn or npm test
- Remember after you change UI code you may need to update your snapshots
  - either stop and restart the test script
  - or press u (for update) when prompted after tests run

Linting:
- Lint settings are in .eslintrc.js
- Files to ignore are in .eslintignore
- To see how many lint errors/warnings run ./check_lint.sh
- To attempt to automatically fix lint errors/warnings run ./fix_lint.sh
