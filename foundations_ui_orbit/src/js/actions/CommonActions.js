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
    return !(obj && typeof obj === "object" && Object.entries(obj).length > 0);
  },

  decimalToPercentage: d => {
    if (typeof d === "string") {
      d = parseFloat(d);
    }
    return `${Math.round(d * 100 * 100) / 100}%`;
  }
};

export default CommonActions;
