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
    return `${Math.round(parseFloat(d) * 100 * 10) / 10}%`;
  },

  nullToNA: val => {
    return val === null ? "N/A" : val;
  }
};

export default CommonActions;
