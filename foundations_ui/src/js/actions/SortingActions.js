import CommonActions from './CommonActions';

class SortingActions {
  static sortbyColumn(jobs, colName) {
    const sortedObject = CommonActions.deepCopyArray(jobs);
    sortedObject.sort(this.dynamicSortMultiple(colName));
    return sortedObject;
  }

  static dynamicSortMultiple(colNameList) {
    return (obj1, obj2) => {
      let curProp = 0;
      let result = 0;
      const numberOfProperties = colNameList.length;
      while (result === 0 && curProp < numberOfProperties) {
        result = this.jobSort(colNameList[curProp])(obj1, obj2);
        curProp += 1;
      }
      return result;
    };
  }

  // private sort function
  static jobSort(property) {
    return ((obj1, obj2) => {
      let returnVal = 0;
      if (obj1[property] > obj2[property]) {
        returnVal = 1;
      }

      if (obj1[property] < obj2[property]) {
        returnVal = -1;
      }
      return returnVal;
    });
  }
}

export default SortingActions;
