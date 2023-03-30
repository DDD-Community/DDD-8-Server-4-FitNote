/* globals Chart:false, feather:false */

(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  const ctx0 = document.getElementById('myChart0')
  const ctx1 = document.getElementById('myChart1')
  const ctx2 = document.getElementById('myChart2')
  const ctx3 = document.getElementById('myChart3')
  const ctx4 = document.getElementById('myChart4')
  const ctx5 = document.getElementById('myChart5')

  // eslint-disable-next-line no-unused-vars
  const myChart0 = new Chart(ctx0, {
    type: 'line',
    plugins: [ChartDataLabels],
    data: {
      labels: [
        '15회',
        '15회',
        '15회',
        '',
        '',
        '',
      ],
      datasets: [{
        data: [
          0,
          0,
          0,
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff',
      }]
    },
    options: {
      plugins: {
        legend: { // 범례 사용 안 함
          display: false,
        },
        tooltip: { // 기존 툴팁 사용 안 함
          enabled: false
        },
        animation: { // 차트 애니메이션 사용 안 함 (옵션)
          duration: 0,
        },
        datalabels: {
          align: 'top',
          offset: 8,
          font: { // font 설정
            size: '14px',
          },
          color: '#222', // font color
        },
      },

      scales: {
        x: {
          grid: {
            display: false,
          }
        },
        y: {
          display: false,
          beginAtZero: true,
          max: 1, // max 값 조정
          ticks: { // y축 줄당 표시 값
            stepSize: 1
          }
        },
      },

    }
  })

  const myChart1 = new Chart(ctx1, {
    type: 'line',
    plugins: [ChartDataLabels],
    data: {
      labels: [
        '15회',
        '15회',
        '15회',
        '15회',
        '15회',
        '',
      ],
      datasets: [{
        data: [
          0,
          0,
          0,
          0,
          0,
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff',
      }]
    },
    options: {
      plugins: {
        legend: { // 범례 사용 안 함
          display: false,
        },
        tooltip: { // 기존 툴팁 사용 안 함
          enabled: false
        },
        animation: { // 차트 애니메이션 사용 안 함 (옵션)
          duration: 0,
        },
        datalabels: {
          align: 'top',
          offset: 8,
          font: { // font 설정
            size: '14px',
          },
          color: '#222', // font color
        },
      },

      scales: {
        x: {
          grid: {
            display: false,
          }
        },
        y: {
          display: false,
          beginAtZero: true,
          max: 1, // max 값 조정
          ticks: { // y축 줄당 표시 값
            stepSize: 1
          }
        },
      },

    }
  })

  const myChart2 = new Chart(ctx2, {
    type: 'line',
    plugins: [ChartDataLabels],
    data: {
      labels: [
        '15회',
        '15회',
        '15회',
        '15회',
        '15회',
        '15회'
      ],
      datasets: [{
        data: [
          0,
          0,
          0,
          0,
          0,
          0,
          0
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff',
      }]
    },
    options: {
      plugins: {
        legend: { // 범례 사용 안 함
          display: false,
        },
        tooltip: { // 기존 툴팁 사용 안 함
          enabled: false
        },
        animation: { // 차트 애니메이션 사용 안 함 (옵션)
          duration: 0,
        },
        datalabels: {
          align: 'top',
          offset: 8,
          font: { // font 설정
            size: '14px',
          },
          color: '#222', // font color
        },
      },

      scales: {
        x: {
          grid: {
            display: false,
          }
        },
        y: {
          display: false,
          beginAtZero: true,
          max: 1, // max 값 조정
          ticks: { // y축 줄당 표시 값
            stepSize: 1
          }
        },
      },

    }
  })

  const myChart3 = new Chart(ctx3, {
    type: 'line',
    plugins: [ChartDataLabels],
    data: {
      labels: [
        '15회',
        '15회',
        '',
        '',
        '',
        '',
      ],
      datasets: [{
        data: [
          0,
          0,
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff',
      }]
    },
    options: {
      plugins: {
        legend: { // 범례 사용 안 함
          display: false,
        },
        tooltip: { // 기존 툴팁 사용 안 함
          enabled: false
        },
        animation: { // 차트 애니메이션 사용 안 함 (옵션)
          duration: 0,
        },
        datalabels: {
          align: 'top',
          offset: 8,
          font: { // font 설정
            size: '14px',
          },
          color: '#222', // font color
        },
      },

      scales: {
        x: {
          grid: {
            display: false,
          }
        },
        y: {
          display: false,
          beginAtZero: true,
          max: 1, // max 값 조정
          ticks: { // y축 줄당 표시 값
            stepSize: 1
          }
        },
      },

    }
  })

  const myChart4 = new Chart(ctx4, {
    type: 'line',
    plugins: [ChartDataLabels],
    data: {
      labels: [
        '15회',
        '15회',
        '',
        '',
        '',
        '',
      ],
      datasets: [{
        data: [
          0,
          0,
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff',
      }]
    },
    options: {
      plugins: {
        legend: { // 범례 사용 안 함
          display: false,
        },
        tooltip: { // 기존 툴팁 사용 안 함
          enabled: false
        },
        animation: { // 차트 애니메이션 사용 안 함 (옵션)
          duration: 0,
        },
        datalabels: {
          align: 'top',
          offset: 8,
          font: { // font 설정
            size: '14px',
          },
          color: '#222', // font color
        },
      },

      scales: {
        x: {
          grid: {
            display: false,
          }
        },
        y: {
          display: false,
          beginAtZero: true,
          max: 1, // max 값 조정
          ticks: { // y축 줄당 표시 값
            stepSize: 1
          }
        },
      },

      
    }
  })

  const myChart5 = new Chart(ctx5, {
    type: 'line',
    plugins: [ChartDataLabels],
    data: {
      labels: [
        '15회',
        '15회',
        '',
        '',
        '',
        '',
      ],
      datasets: [{
        data: [
          0,
          0,
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff',
      }]
    },
    options: {
      plugins: {
        legend: { // 범례 사용 안 함
          display: false,
        },
        tooltip: { // 기존 툴팁 사용 안 함
          enabled: false
        },
        animation: { // 차트 애니메이션 사용 안 함 (옵션)
          duration: 0,
        },
        datalabels: {
          align: 'top',
          offset: 8,
          font: { // font 설정
            size: '14px',
          },
          color: '#222', // font color
        },
      },

      scales: {
        x: {
          grid: {
            display: false,
          }
        },
        y: {
          display: false,
          beginAtZero: true,
          max: 1, // max 값 조정
          ticks: { // y축 줄당 표시 값
            stepSize: 1
          }
        },
      },

      
    }
  })

})()
