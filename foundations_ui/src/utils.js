import datetimeDifference from "datetime-difference";

// Convert time to local timezone and use 24 hour time
export function updateTime(timeString){
    var timeStamp = new Date(timeString);
    timeStamp.setHours( timeStamp.getHours() - 4 );
    var useTwentyFourHour = new Date(timeStamp).toLocaleString('en-GB');
    var yearFormat = useTwentyFourHour.split(',')[0].split('/').reverse().join('/')
    var ISODateFormat = yearFormat + useTwentyFourHour.split(',')[1]
    return ISODateFormat;
}

export function determineValue(index, job){
    if (job.input_params_dict[index]) {
      var obj = job.input_params_dict[index].value
      if (obj.type === 'stage'){
        return obj.stage_name;
      } else if (obj.type === 'constant'){
        return obj.value;
      } else if (obj.type === 'dynamic') {
        var jobParams = job.job_parameters;
        return jobParams[obj.name];
      }
    }
}

export function getTimeDifference(submitted_time){
    const currentTime = new Date();
    const dataTimeFormatted = new Date(submitted_time)
    dataTimeFormatted.setHours( dataTimeFormatted.getHours() - 4 );
    const newDate = new Date(dataTimeFormatted)
    const timeDiff = datetimeDifference(currentTime, newDate);
    return timeDiff
}

export function createTimeStamp(listOfJobs, key){
    listOfJobs.map(job => job.duration = getTimeDifference(job[key]).minutes + 'm:' + getTimeDifference(job[key]).seconds + 's')
}
