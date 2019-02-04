// react-testing-library renders your components to document.body,
// this will ensure they're removed after each test.
import 'react-testing-library/cleanup-after-each';
// this adds jest-dom's custom assertions
import 'jest-dom/extend-expect';

import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

function configureTests(){
  configure({ adapter: new Adapter() });
  // API Call timer
  jest.setTimeout(30000);
}

export default configureTests;