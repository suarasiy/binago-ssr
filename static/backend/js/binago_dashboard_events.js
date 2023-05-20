const chartWidget = (domTarget, seriesName, data) => {
  const chartDomWidget = document.querySelector(domTarget);
  const myChartWidget = echarts.init(chartDomWidget);
  const optionWidgetDonut = {
    tooltip: {
      trigger: 'item',
    },
    legend: {
      show: false,
      top: '5%',
      left: 'center',
    },
    series: [
      {
        name: seriesName,
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: false,
            fontSize: 40,
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
        data,
      },
    ],
  };

  optionWidgetDonut && myChartWidget.setOption(optionWidgetDonut);
};

var valueComparisonRegisteredUser = document.querySelector('#summary_comparison_registered_user').value;
var data = JSON.parse(valueComparisonRegisteredUser);

chartWidget('#chart-widget-1', 'Registered User', [
  {
    name: 'Last Month',
    value: data.lm,
    itemStyle: {
      opacity: 0.8,
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        {
          offset: 0,
          color: '#C6C6C6',
        },
        {
          offset: 1,
          color: '#7F7F7F',
        },
      ]),
    },
  },
  {
    name: 'Current Month',
    value: data.cm,
    itemStyle: {
      opacity: 0.8,
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        {
          offset: 0,
          color: '#2DCE89',
        },
        {
          offset: 1,
          color: '#0AB36A',
        },
      ]),
    },
  },
]);

var valueComparisonEventsPublished = document.querySelector('#summary_comparison_events_published').value;
var data = JSON.parse(valueComparisonEventsPublished);

chartWidget('#chart-widget-2', 'Registered Event', [
  {
    name: 'Last Month',
    value: data.lm,
    itemStyle: {
      opacity: 0.8,
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        {
          offset: 0,
          color: '#5E72E4',
        },
        {
          offset: 1,
          color: '#2943D8',
        },
      ]),
    },
  },
  {
    name: 'Current Month',
    value: data.cm,
    itemStyle: {
      opacity: 0.8,
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        {
          offset: 0,
          color: '#2DCE89',
        },
        {
          offset: 1,
          color: '#0AB36A',
        },
      ]),
    },
  },
]);
