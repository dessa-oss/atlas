let shouldSkip = false;
module.exports = on => {
  on('task', {
    shouldSkip(value) {
      if (value !== null) {
        shouldSkip = value;
      }
      return shouldSkip;
    }
  });
}
