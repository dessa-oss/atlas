

// This is a custom Jest transformer turning style imports into empty objects.
// http://facebook.github.io/jest/docs/en/webpack.html

module.exports = {
  process: function () {
    return "module.exports = {};";
  },
  getCacheKey: function () {
    // The output is always the same.
    return "cssTransform";
  }
};
