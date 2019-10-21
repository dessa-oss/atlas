const CommonActions = {
  deepEqual: (x, y) => {
    const ok = Object.keys;
    const tx = typeof x;
    const ty = typeof y;
    return x && y && tx === "object" && tx === ty ? (
      ok(x).length === ok(y).length
      && ok(x).every(key => CommonActions.deepEqual(x[key], y[key]))
    ) : (x === y);
  },

  isEmptyObject: obj => {
    return Object.entries(obj).length === 0;
  }
};

export default CommonActions;
