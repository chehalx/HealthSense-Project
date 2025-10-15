// HealthSense Charts JS

// Chart objects
let glucoseChart, bpChart, spo2Chart, heartRateChart;

// Chart colors
const chartColors = {
    glucose: {
        borderColor: 'rgba(255, 159, 64, 1)',
        backgroundColor: 'rgba(255, 159, 64, 0.2)'
    },
    bpSystolic: {
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)'
    },
    bpDiastolic: {
        borderColor: 'rgba(255, 99, 132, 0.6)',
        backgroundColor: 'rgba(255, 99, 132, 0.1)'
    },
    spo2: {
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)'
    },
    heartRate: {
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)'
    }
};

// Initialize all charts
function initializeCharts() {
    initGlucoseChart();
    initBPChart();
    initSpO2Chart();
    initHeartRateChart();
}

// Initialize Glucose Chart
function initGlucoseChart() {
    const ctx = document.getElementById('glucose-chart').getContext('2d');
    glucoseChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Glucose (mg/dL)',
                data: [],
                borderColor: chartColors.glucose.borderColor,
                backgroundColor: chartColors.glucose.backgroundColor,
                borderWidth: 2,
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 50,
                    max: 250,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                annotation: {
                    annotations: {
                        highLine: {
                            type: 'line',
                            yMin: 180,
                            yMax: 180,
                            borderColor: 'rgba(255, 0, 0, 0.5)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: 'High',
                                position: 'end'
                            }
                        },
                        lowLine: {
                            type: 'line',
                            yMin: 70,
                            yMax: 70,
                            borderColor: 'rgba(255, 0, 0, 0.5)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: 'Low',
                                position: 'end'
                            }
                        }
                    }
                }
            }
        }
    });
}

// Initialize Blood Pressure Chart
function initBPChart() {
    const ctx = document.getElementById('bp-chart').getContext('2d');
    bpChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Systolic (mmHg)',
                    data: [],
                    borderColor: chartColors.bpSystolic.borderColor,
                    backgroundColor: chartColors.bpSystolic.backgroundColor,
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Diastolic (mmHg)',
                    data: [],
                    borderColor: chartColors.bpDiastolic.borderColor,
                    backgroundColor: chartColors.bpDiastolic.backgroundColor,
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 40,
                    max: 200,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
}

// Initialize SpO2 Chart
function initSpO2Chart() {
    const ctx = document.getElementById('spo2-chart').getContext('2d');
    spo2Chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'SpO₂ (%)',
                data: [],
                borderColor: chartColors.spo2.borderColor,
                backgroundColor: chartColors.spo2.backgroundColor,
                borderWidth: 2,
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 80,
                    max: 100,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                annotation: {
                    annotations: {
                        dangerLine: {
                            type: 'line',
                            yMin: 90,
                            yMax: 90,
                            borderColor: 'rgba(255, 0, 0, 0.5)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: 'Danger',
                                position: 'end'
                            }
                        }
                    }
                }
            }
        }
    });
}

// Initialize Heart Rate Chart
function initHeartRateChart() {
    const ctx = document.getElementById('heart-rate-chart').getContext('2d');
    heartRateChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Heart Rate (BPM)',
                data: [],
                borderColor: chartColors.heartRate.borderColor,
                backgroundColor: chartColors.heartRate.backgroundColor,
                borderWidth: 2,
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 40,
                    max: 140,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                annotation: {
                    annotations: {
                        highLine: {
                            type: 'line',
                            yMin: 100,
                            yMax: 100,
                            borderColor: 'rgba(255, 255, 0, 0.5)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: 'High',
                                position: 'end'
                            }
                        },
                        lowLine: {
                            type: 'line',
                            yMin: 50,
                            yMax: 50,
                            borderColor: 'rgba(255, 255, 0, 0.5)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                display: true,
                                content: 'Low',
                                position: 'end'
                            }
                        }
                    }
                }
            }
        }
    });
}

// Update charts with new data point
function updateCharts(healthData) {
    // Format timestamp
    const timestamp = new Date(healthData.timestamp);
    const timeLabel = timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    
    // Add data to glucose chart
    addDataPoint(glucoseChart, timeLabel, healthData.glucose);
    
    // Add data to BP chart
    addBPDataPoint(bpChart, timeLabel, healthData.bp_systolic, healthData.bp_diastolic);
    
    // Add data to SpO2 chart
    addDataPoint(spo2Chart, timeLabel, healthData.spo2);
    
    // Add data to heart rate chart
    addDataPoint(heartRateChart, timeLabel, healthData.heart_rate);
}

// Update historical charts with multiple data points
function updateHistoricalCharts(historyData) {
    if (!historyData || historyData.length === 0) return;
    
    // Sort data by timestamp
    historyData.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    
    // Clear existing data
    clearChartData(glucoseChart);
    clearChartData(bpChart);
    clearChartData(spo2Chart);
    clearChartData(heartRateChart);
    
    // Add each data point
    historyData.forEach(data => {
        const timestamp = new Date(data.timestamp);
        const timeLabel = timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        addDataPoint(glucoseChart, timeLabel, data.glucose, false);
        addBPDataPoint(bpChart, timeLabel, data.bp_systolic, data.bp_diastolic, false);
        addDataPoint(spo2Chart, timeLabel, data.spo2, false);
        addDataPoint(heartRateChart, timeLabel, data.heart_rate, false);
    });
    
    // Update all charts
    glucoseChart.update();
    bpChart.update();
    spo2Chart.update();
    heartRateChart.update();
}

// Function to add a data point to a chart
function addDataPoint(chart, label, value, update = true) {
    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(value);
    
    // Limit data points to keep chart readable
    if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    
    if (update) {
        chart.update();
    }
}

// Function to add BP data points (systolic and diastolic)
function addBPDataPoint(chart, label, systolic, diastolic, update = true) {
    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(systolic);
    chart.data.datasets[1].data.push(diastolic);
    
    // Limit data points to keep chart readable
    if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
    }
    
    if (update) {
        chart.update();
    }
}

// Function to clear all data from a chart
function clearChartData(chart) {
    chart.data.labels = [];
    chart.data.datasets.forEach(dataset => {
        dataset.data = [];
    });
}
