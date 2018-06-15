
// chart initialization
var ctx = document.getElementById("displayChart");
var displayChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [{
        label: '',
        data: [],
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255,99,132,1)',
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
      maintainAspectRatio: false
    }
});

var histogramData = {};
var centralLimitData = {};

// app initialization
var app = new Vue({
  el: '#app',
  data: {
    mean: 0,
    stdDev: 0,
    selectedType: 'scores mean',
  },
  methods: {
    selectType: function(type) {
      app.selectedType = type;
      parseData(type);
    }
  }
});

var readTextFile = function(file, histogram) {
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", file, false);
  rawFile.onreadystatechange = function() {
    if(rawFile.readyState === 4) {
      if(rawFile.status === 200 || rawFile.status == 0) {
        if (histogram) {
          histogramData = JSON.parse(rawFile.responseText);
          parseData(app.selectedType);
        } else {
          centralLimitData = JSON.parse(rawFile.responseText);
          readTextFile('http://localhost:3000/aggregate_data/histogram_values.json', true);
        }
      }
    }
  };
  rawFile.send(null);
};

var parseData = function(dataType) {
  var labels = [];
  var data = [];
  var mean = 0;
  var stdDev = 0;

  switch (dataType) {
    case 'scores mean':
      console.log(histogramData);
      data = histogramData.scoreMeansHistogram;
      labels = histogramData.scoreMeansBinEdges;
      mean = centralLimitData.totalScoreMeansMean;
      stdDev = centralLimitData.totalScoreMeansStdDev;
      break;
    case 'scores std dev':
      data = histogramData.scoreStdDevsHistogram;
      labels = histogramData.scoreStdDevsBinEdges;
      mean = centralLimitData.totalScoreStdDevsMean;
      stdDev = centralLimitData.totalScoreStdDevsStdDev;
      break;
    case 'comments mean':
      data = histogramData.commentsMeansHistogram;
      labels = histogramData.commentsMeansBinEdges;
      mean = centralLimitData.totalCommentsMeansMean;
      stdDev = centralLimitData.totalCommentsMeansStdDev;
      break;
    case 'comments std dev':
      data = histogramData.commentsStdDevsHistogram;
      labels = histogramData.commentsStdDevsBinEdges;
      mean = centralLimitData.totalCommentsStdDevsMean;
      stdDev = centralLimitData.totalCommentsStdDevsStdDev;
      break;
    case 'upvote ratios mean':
      data = histogramData.upvoteRatioMeansHistogram;
      labels = histogramData.upvoteRatioMeansBinEdges;
      mean = centralLimitData.totalUpvoteRatioMeansMean;
      stdDev = centralLimitData.totalUpvoteRatioMeansStdDev;
      break;
    case 'upvote ratios std dev':
      data = histogramData.upvoteRatioStdDevsHistogram;
      labels = histogramData.upvoteRatioStdDevsBinEdges;
      mean = centralLimitData.totalUpvoteRatioStdDevsMean;
      stdDev = centralLimitData.totalUpvoteRatioStdDevsStdDev;
      break;
    case 'sentiments mean':
      data = histogramData.sentimentMeansHistogram;
      labels = histogramData.sentimentMeansBinEdges;
      mean = centralLimitData.totalSentimentMeansMean;
      stdDev = centralLimitData.totalSentimentMeansStdDev;
      break;
    case 'sentiments std dev':
      data = histogramData.sentimentStdDevsHistogram;
      labels = histogramData.sentimentStdDevsBinEdges;
      mean = centralLimitData.totalSentimentStdDevsMean;
      stdDev = centralLimitData.totalSentimentStdDevsStdDev;
      break;
    default:
      data = histogramData.scoreMeansHistogram;
      labels = histogramData.scoreMeansBinEdges;
      mean = centralLimitData.totalScoreMeansMean;
      stdDev = centralLimitData.totalScoreMeansStdDev;
  }

  app.mean = mean;
  app.stdDev = stdDev;

  displayChart.data.datasets[0].label = dataType;
  displayChart.data.labels = labels;
  displayChart.data.datasets[0].data = data;
  displayChart.update();
};

readTextFile('http://localhost:3000/aggregate_data/central_limit_values.json', false);

