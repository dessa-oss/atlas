
module.exports = {
  "extends": [
    "airbnb",
    "plugin:react/recommended"
  ],
  "env": {
          "browser": true,
          "node": true,
          "es6": true
  },
  "parserOptions": {
    "ecmaFeatures": {
        "jsx": true
    }
  },
  "rules": {
    "class-methods-use-this": 0,
    "no-unused-vars": 1,
    "arrow-body-style": 0,
    "react/jsx-filename-extension": 0,
    "react/prefer-stateless-function": 0,
    "react/destructuring-assignment": [1, "always", { "ignoreClassFields": true }],
    "react/forbid-prop-types": 0,
    "react/jsx-one-expression-per-line": 0,
    "react/no-unused-prop-types": [1],
    "max-len": [2, {"code": 120, "tabWidth": 2, "ignoreUrls": true}],
    "import/no-cycle": 1,
    "jsx-a11y/label-has-associated-control": 0,
    "jsx-a11y/label-has-for": 0,
    "no-param-reassign": 1,
    "jsx-a11y/no-noninteractive-element-interactions": 0,
    "array-callback-return": 0,
    "consistent-return": 0,
    "prefer-const": 1,
    "prefer-destructuring": 1,
    "react/sort-comp": 1,
  }
};

