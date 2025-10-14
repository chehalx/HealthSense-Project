// HealthSense Dashboard JS
document.addEventListener('DOMContentLoaded', function() {
    // Connect to WebSocket server for real-time updates
    const socket = io();
    
    // Dashboard elements
    const glucoseValue = document.getElementById('glucose-value');
    const bpValue = document.getElementById('bp-value');
    const spo2Value = document.getElementById('spo2-value');
    const heartRateValue = document.getElementById('heart-rate-value');
    const lastUpdateTime = document.getElementById('last-update-time');
    
    // Prediction elements
    const diabetesRisk = document.getElementById('diabetes-risk');
    const heartDiseaseRisk = document.getElementById('heart-disease-risk');
    const hypoxiaRisk = document.getElementById('hypoxia-risk');
    
    // Alerts container
    const alertsContainer = document.getElementById('alerts-container');
    
    // Initialize charts
    initializeCharts();
    
    // Load initial data
    fetchLatestData();
    fetchHistoricalData();
    fetchAlerts();
    
    // Set up refresh intervals
    setInterval(fetchHistoricalData, 60000); // Update historical data every minute
    setInterval(fetchAlerts, 30000); // Update alerts every 30 seconds
    
    // Socket event for real-time data
    socket.on('new_health_data', function(data) {
        console.log('Received real-time data:', data);
        updateDashboardWithData(data.health_data, data.prediction);
        updateCharts(data.health_data);
        
        // Check for new alerts
        if (data.alerts && data.alerts.length > 0) {
            data.alerts.forEach(alert => {
                addAlert(alert);
            });
        }
    });
    
    // Function to fetch latest health data
    function fetchLatestData() {
        fetch('/api/latest')
            .then(response => {
                if (!response.ok) {
                    throw new Error('No data available');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    updateDashboardWithData(data.health_data, data.prediction);
                    
                    // Check for alerts
                    if (data.alerts && data.alerts.length > 0) {
                        data.alerts.forEach(alert => {
                            addAlert(alert);
                        });
                    }
                }
            })
            .catch(error => {
                console.error('Error fetching latest data:', error);
            });
    }
    
    // Function to fetch historical data
    function fetchHistoricalData() {
        fetch('/api/history?hours=24&limit=100')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateHistoricalCharts(data.data);
                }
            })
            .catch(error => {
                console.error('Error fetching historical data:', error);
            });
    }
    
    // Function to fetch active alerts
    function fetchAlerts() {
        fetch('/api/alerts?acknowledged=false')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Clear current alerts
                    alertsContainer.innerHTML = '';
                    
                    // Add each alert
                    data.alerts.forEach(alert => {
                        addAlert(alert);
                    });
                    
                    // Update alert count
                    updateAlertCount(data.alerts.length);
                }
            })
            .catch(error => {
                console.error('Error fetching alerts:', error);
            });
    }
    
    // Function to update dashboard with latest data
    function updateDashboardWithData(healthData, prediction) {
        // Update vital signs
        glucoseValue.textContent = healthData.glucose;
        bpValue.textContent = `${healthData.bp_systolic}/${healthData.bp_diastolic}`;
        spo2Value.textContent = healthData.spo2;
        heartRateValue.textContent = healthData.heart_rate;
        
        // Update time
        const timestamp = new Date(healthData.timestamp);
        lastUpdateTime.textContent = timestamp.toLocaleTimeString();
        
        // Set classes based on values (for color-coding)
        setValueClass(glucoseValue, healthData.glucose, 70, 180);
        setValueClass(spo2Value, healthData.spo2, 94, 101, true);
        setValueClass(heartRateValue, healthData.heart_rate, 50, 100);
        
        // Update BP class
        const systolicNormal = healthData.bp_systolic >= 90 && healthData.bp_systolic <= 140;
        const diastolicNormal = healthData.bp_diastolic >= 60 && healthData.bp_diastolic <= 90;
        if (systolicNormal && diastolicNormal) {
            bpValue.className = 'value normal';
        } else {
            bpValue.className = 'value abnormal';
        }
        
        // Update prediction values if available
        if (prediction) {
            updatePredictionDisplay(diabetesRisk, prediction.diabetes_risk);
            updatePredictionDisplay(heartDiseaseRisk, prediction.heart_disease_risk);
            updatePredictionDisplay(hypoxiaRisk, prediction.hypoxia_risk);
        }
    }
    
    // Function to set class based on value range
    function setValueClass(element, value, min, max, invert = false) {
        const isNormal = invert ? 
            (value >= min) : 
            (value >= min && value <= max);
            
        if (isNormal) {
            element.className = 'value normal';
        } else {
            element.className = 'value abnormal';
        }
    }
    
    // Function to update prediction display
    function updatePredictionDisplay(element, riskValue) {
        const percentage = Math.round(riskValue * 100);
        element.textContent = `${percentage}%`;
        
        // Set class based on risk level
        if (percentage < 20) {
            element.className = 'prediction-value low-risk';
        } else if (percentage < 50) {
            element.className = 'prediction-value medium-risk';
        } else {
            element.className = 'prediction-value high-risk';
        }
        
        // Update progress bar if it exists
        const progressBar = element.nextElementSibling;
        if (progressBar && progressBar.classList.contains('progress-bar')) {
            progressBar.style.width = `${percentage}%`;
            
            // Set appropriate class
            progressBar.className = 'progress-bar';
            if (percentage < 20) {
                progressBar.classList.add('bg-success');
            } else if (percentage < 50) {
                progressBar.classList.add('bg-warning');
            } else {
                progressBar.classList.add('bg-danger');
            }
        }
    }
    
    // Function to add an alert to the dashboard
    function addAlert(alert) {
        const alertElem = document.createElement('div');
        alertElem.className = `alert alert-dismissible fade show`;
        
        // Set alert color based on severity
        if (alert.severity === 'high') {
            alertElem.classList.add('alert-danger');
        } else if (alert.severity === 'medium') {
            alertElem.classList.add('alert-warning');
        } else {
            alertElem.classList.add('alert-info');
        }
        
        // Format time
        const timestamp = new Date(alert.timestamp);
        const timeStr = timestamp.toLocaleTimeString();
        
        // Create alert content
        alertElem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${timeStr}</strong>: ${alert.message}
                </div>
                <div>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" 
                        onclick="acknowledgeAlert('${alert.id}')"></button>
                </div>
            </div>
        `;
        
        // Add to container
        alertsContainer.appendChild(alertElem);
        
        // Update count
        updateAlertCount();
    }
    
    // Function to update alert count
    function updateAlertCount(count = null) {
        const alertCount = document.getElementById('alert-count');
        if (!alertCount) return;
        
        const alertNum = count !== null ? count : alertsContainer.childElementCount;
        alertCount.textContent = alertNum;
        
        // Show/hide based on count
        if (alertNum > 0) {
            alertCount.style.display = 'inline-block';
        } else {
            alertCount.style.display = 'none';
        }
    }
});

// Function to acknowledge an alert
function acknowledgeAlert(alertId) {
    fetch(`/api/alerts/${alertId}/acknowledge`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Alert acknowledged:', data);
    })
    .catch(error => {
        console.error('Error acknowledging alert:', error);
    });
}

// Function to simulate a device
function startDeviceSimulation() {
    const scenario = document.getElementById('scenario-select').value;
    const interval = document.getElementById('interval-select').value;
    
    fetch('/api/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            scenario: scenario,
            interval: parseInt(interval)
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Simulation started:', data);
        document.getElementById('simulation-status').textContent = 'Running...';
    })
    .catch(error => {
        console.error('Error starting simulation:', error);
    });
}
