
// chart initialization
var ctx = document.getElementById("displayChart");
var displayChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      titles: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      datasets: [{
        label: '',
        data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      },
      tooltips: {
        callbacks: {
          afterLabel: function(tooltipItem, data) {
            return displayChart.data.titles[tooltipItem['index']];
          }
        }
      },
      maintainAspectRatio: false
    }
});

var currentDataString = '';
var interval = 0;

// app initialization
var app = new Vue({
  el: '#app',
  data: {
    mean: 0,
    stdDev: 0,
    selectedType: 'score',
    date: '',
    currentFile: 0,
    currentData: {},
    skipping: 0,
    numFiles: fileDirectory.length,
    numPosts: 0
  },
  methods: {
    selectType: function(type) {
      app.selectedType = type;
      parseData(currentDataString, type);
    },
    next: function() {
      if (app.currentFile > 0) {
        app.currentFile -= 1;
        visualize(app.currentFile);
      }
    },
    previous: function() {
      if (app.currentFile < app.numFiles - 1) {
        app.currentFile += 1;
        visualize(app.currentFile);
      }
    },
    fastForward: function() {
      if (app.skipping === 0 && app.currentFile > 0) {
        app.skipping = 2;
        clearInterval(interval);
        interval = setInterval(function() {
          if (app.currentFile > 0 && app.skipping === 2) {
            app.currentFile -= 1;
            visualize(app.currentFile);
          } else {
            app.skipping = 0;
            clearInterval(interval);
          }
        }, 100);
      } else {
        app.skipping = 0;
      }
    },
    rewind: function() {
      if (app.skipping === 0 && app.currentFile < app.numFiles - 1) {
        app.skipping = 1;
        clearInterval(interval);
        interval = setInterval(function() {
          if (app.currentFile < app.numFiles - 1 && app.skipping === 1) {
            app.currentFile += 1;
            visualize(app.currentFile);
          } else if (app.skipping === 1) {
            app.skipping = 0;
            clearInterval(interval);
          }
        }, 100);
      } else {
        app.skipping = 0;
      }
    }
  }
});

var readTextFile = function(file) {
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", file, false);
  rawFile.onreadystatechange = function() {
    if(rawFile.readyState === 4) {
      if(rawFile.status === 200 || rawFile.status == 0) {
        currentDataString = rawFile.responseText;
        parseData(currentDataString, app.selectedType);
      }
    }
  };
  rawFile.send(null);
};

var parseData = function(dataText, dataType) {
  var dataJSON = JSON.parse(dataText).data;
  app.currentData = dataJSON;
  var labels = [];
  var data = [];
  var titles = [];
  var mean = 0;
  var stdDev = 0;

  for (var i = 0; i < dataJSON.length; i++) {
    labels.push('Post ' + (dataJSON[i].count + 1));
    titles.push(dataJSON[i].title);

    switch (dataType) {
      case 'score':
        data.push(dataJSON[i].score);
        mean += dataJSON[i].score;
        break;
      case 'comments':
        data.push(dataJSON[i].comments);
        mean += dataJSON[i].comments;
        break;
      case 'upvoteRatio':
        data.push(dataJSON[i].upvoteRatio);
        mean += dataJSON[i].upvoteRatio;
        break;
      case 'sentiment':
        data.push(dataJSON[i].sentiment);
        mean += dataJSON[i].sentiment;
        break;
      default:
        data.push(dataJSON[i].count);
        mean += dataJSON[i].count;
    }
  }

  mean /= dataJSON.length;

  for (var j = 0; j < dataJSON.length; j++) {
    switch (dataType) {
      case 'score':
        stdDev += Math.pow(dataJSON[j].score - mean, 2);
        break;
      case 'comments':
        stdDev += Math.pow(dataJSON[j].comments - mean, 2);
        break;
      case 'upvoteRatio':
        stdDev += Math.pow(dataJSON[j].upvoteRatio - mean, 2);
        break;
      case 'sentiment':
        stdDev += Math.pow(dataJSON[j].sentiment - mean, 2);
        break;
      default:
        stdDev += Math.pow(dataJSON[j].count - mean, 2);
    }
  }

  stdDev = Math.sqrt(stdDev / (dataJSON.length - 1));

  app.numPosts = data.length;
  app.mean = mean;
  app.stdDev = stdDev;

  displayChart.data.datasets[0].label = dataType;
  displayChart.data.labels = labels;
  displayChart.data.datasets[0].data = data;
  displayChart.data.titles = titles;
  displayChart.update();
};

var visualize = function(currentFile) {
  var fileName = fileDirectory[currentFile];
  readTextFile('https://alan-ma.github.io/reddit-news-and-stocks/new_parsed_dates/' + fileName + '.json');
  var utcSeconds = parseInt(fileName);
  var date = new Date(0); // the 0 sets the date to the epoch
  date.setUTCSeconds(utcSeconds);
  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  app.date = days[date.getDay()] + ' ' + months[date.getMonth()] + ' ' + date.getDate() + ' ' + date.getFullYear();
};

visualize(app.currentFile);

