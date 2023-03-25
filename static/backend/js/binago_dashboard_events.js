const chartWidget = (domTarget, data) => {
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
        name: 'Access From',
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

chartWidget('#chart-widget-1', [
  {
    name: 'Unattended Users',
    value: 91,
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
    name: 'Attended Users',
    value: 78,
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

chartWidget('#chart-widget-2', [
  {
    name: 'Paid Events',
    value: 41,
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
    name: 'Free Events',
    value: 219,
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
