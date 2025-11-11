// DNU Major Trends - Main JavaScript

// Sidebar toggle
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }
    
    // Update current date
    const currentDate = document.getElementById('currentDate');
    if (currentDate) {
        const today = new Date();
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        currentDate.textContent = today.toLocaleDateString('vi-VN', options);
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// API Helper Functions
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

async function postAPI(endpoint, data) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Chart color palettes
const chartColors = {
    primary: 'rgb(75, 192, 192)',
    primaryAlpha: 'rgba(75, 192, 192, 0.2)',
    secondary: 'rgb(54, 162, 235)',
    secondaryAlpha: 'rgba(54, 162, 235, 0.2)',
    success: 'rgb(75, 192, 75)',
    successAlpha: 'rgba(75, 192, 75, 0.2)',
    warning: 'rgb(255, 205, 86)',
    warningAlpha: 'rgba(255, 205, 86, 0.2)',
    danger: 'rgb(255, 99, 132)',
    dangerAlpha: 'rgba(255, 99, 132, 0.2)',
    info: 'rgb(153, 102, 255)',
    infoAlpha: 'rgba(153, 102, 255, 0.2)',
    
    palette: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(75, 192, 192)',
        'rgb(153, 102, 255)',
        'rgb(255, 159, 64)',
        'rgb(199, 199, 199)',
        'rgb(83, 102, 255)',
        'rgb(255, 99, 255)',
        'rgb(99, 255, 132)'
    ]
};

// Number formatting
function formatNumber(num) {
    return num.toLocaleString('vi-VN');
}

function formatPercent(num, decimals = 1) {
    return num.toFixed(decimals) + '%';
}

// Show loading indicator
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="text-center my-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">Đang tải dữ liệu...</p>
            </div>
        `;
    }
}

// Show error message
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle"></i>
                ${message || 'Đã có lỗi xảy ra. Vui lòng thử lại.'}
            </div>
        `;
    }
}

// Toast notification
function showToast(message, type = 'info') {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for use in templates
window.DNU = {
    fetchAPI,
    postAPI,
    chartColors,
    formatNumber,
    formatPercent,
    showLoading,
    showError,
    showToast,
    debounce
};
