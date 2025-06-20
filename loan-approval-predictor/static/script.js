// Loan Approval Prediction App JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize animations
    initializeAnimations();
});

function initializeFormValidation() {
    const form = document.getElementById('loanForm');
    if (!form) return;
    
    form.addEventListener('submit', function(event) {
        if (!validateForm()) {
            event.preventDefault();
            event.stopPropagation();
        } else {
            showLoadingState();
        }
        
        form.classList.add('was-validated');
    });
    
    // Real-time validation for numerical inputs
    const numericalInputs = document.querySelectorAll('input[type="number"]');
    numericalInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateNumericalInput(this);
        });
        
        input.addEventListener('blur', function() {
            formatNumericalInput(this);
        });
    });
    
    // Income ratio calculator
    const incomeInputs = document.querySelectorAll('#applicant_income, #coapplicant_income, #loan_amount');
    incomeInputs.forEach(input => {
        input.addEventListener('input', calculateIncomeRatio);
    });
}

function validateForm() {
    let isValid = true;
    const requiredFields = document.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Validate numerical constraints
    const applicantIncome = parseFloat(document.getElementById('applicant_income').value);
    const loanAmount = parseFloat(document.getElementById('loan_amount').value);
    
    if (applicantIncome <= 0) {
        showFieldError(document.getElementById('applicant_income'), 'Income must be greater than 0');
        isValid = false;
    }
    
    if (loanAmount <= 0) {
        showFieldError(document.getElementById('loan_amount'), 'Loan amount must be greater than 0');
        isValid = false;
    }
    
    // Validate income to loan ratio
    const coApplicantIncome = parseFloat(document.getElementById('coapplicant_income').value) || 0;
    const totalIncome = applicantIncome + coApplicantIncome;
    const incomeRatio = loanAmount / totalIncome;
    
    if (incomeRatio > 10) {
        showAlert('Warning: Loan amount is significantly higher than total income. This may affect approval chances.', 'warning');
    }
    
    return isValid;
}

function validateNumericalInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.getAttribute('min')) || 0;
    const max = parseFloat(input.getAttribute('max')) || Infinity;
    
    if (isNaN(value) || value < min || value > max) {
        input.classList.add('is-invalid');
        return false;
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        return true;
    }
}

function formatNumericalInput(input) {
    if (input.value && !isNaN(input.value)) {
        const value = parseFloat(input.value);
        if (input.step === '0.01') {
            input.value = value.toFixed(2);
        }
    }
}

function calculateIncomeRatio() {
    const applicantIncome = parseFloat(document.getElementById('applicant_income').value) || 0;
    const coApplicantIncome = parseFloat(document.getElementById('coapplicant_income').value) || 0;
    const loanAmount = parseFloat(document.getElementById('loan_amount').value) || 0;
    
    const summaryDiv = document.getElementById('financial-summary');
    
    if (applicantIncome > 0 || loanAmount > 0) {
        const totalIncome = applicantIncome + coApplicantIncome;
        
        let summaryHtml = `
            <div class="row text-center">
                <div class="col-4">
                    <div class="text-info">
                        <strong>$${formatNumber(totalIncome)}</strong>
                        <br><small>Total Income</small>
                    </div>
                </div>
                <div class="col-4">
                    <div class="text-warning">
                        <strong>$${formatNumber(loanAmount)}</strong>
                        <br><small>Loan Amount</small>
                    </div>
                </div>
                <div class="col-4">
        `;
        
        if (totalIncome > 0 && loanAmount > 0) {
            const ratio = (loanAmount / totalIncome) * 100;
            let ratioColor = 'text-success';
            let ratioText = 'Excellent';
            
            if (ratio > 50) {
                ratioColor = 'text-danger';
                ratioText = 'High Risk';
            } else if (ratio > 30) {
                ratioColor = 'text-warning';
                ratioText = 'Moderate';
            }
            
            summaryHtml += `
                    <div class="${ratioColor}">
                        <strong>${ratio.toFixed(1)}%</strong>
                        <br><small>${ratioText}</small>
                    </div>
            `;
        } else {
            summaryHtml += `
                    <div class="text-muted">
                        <strong>--</strong>
                        <br><small>Ratio</small>
                    </div>
            `;
        }
        
        summaryHtml += `
                </div>
            </div>
        `;
        
        summaryDiv.innerHTML = summaryHtml;
    } else {
        summaryDiv.innerHTML = '<small class="text-muted">Fill in the amounts above to see your financial ratio</small>';
    }
}

function showIncomeRatioIndicator(ratio) {
    let existingIndicator = document.getElementById('income-ratio-indicator');
    if (existingIndicator) {
        existingIndicator.remove();
    }
    
    const loanAmountField = document.getElementById('loan_amount');
    const indicator = document.createElement('div');
    indicator.id = 'income-ratio-indicator';
    indicator.className = 'mt-1 small';
    
    let colorClass, message;
    if (ratio <= 30) {
        colorClass = 'text-success';
        message = `Excellent ratio: ${ratio.toFixed(1)}% of income`;
    } else if (ratio <= 50) {
        colorClass = 'text-warning';
        message = `Good ratio: ${ratio.toFixed(1)}% of income`;
    } else {
        colorClass = 'text-danger';
        message = `High ratio: ${ratio.toFixed(1)}% of income - may affect approval`;
    }
    
    indicator.className += ' ' + colorClass;
    indicator.innerHTML = `<i class="fas fa-info-circle me-1"></i>${message}`;
    
    loanAmountField.parentNode.insertBefore(indicator, loanAmountField.nextSibling);
}

function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    // Remove existing error message
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
    
    // Add new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function showLoadingState() {
    const submitButton = document.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="loading me-2"></span>Processing...';
    }
}

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips if needed
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeFormEnhancements() {
    // Auto-format currency inputs on focus
    const currencyInputs = document.querySelectorAll('input[name$="_income"], input[name="loan_amount"]');
    currencyInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.select();
        });
    });
    
    // Smart defaults based on other inputs
    const marriedField = document.getElementById('married');
    const coApplicantField = document.getElementById('coapplicant_income');
    
    if (marriedField && coApplicantField) {
        marriedField.addEventListener('change', function() {
            if (this.value === 'No') {
                coApplicantField.value = '0';
                coApplicantField.disabled = true;
            } else {
                coApplicantField.disabled = false;
            }
        });
    }
    
    // Update dependents field based on marital status
    const dependentsField = document.getElementById('dependents');
    if (marriedField && dependentsField) {
        marriedField.addEventListener('change', function() {
            if (this.value === 'No' && dependentsField.value === '') {
                dependentsField.value = '0';
            }
        });
    }
}

function initializeAnimations() {
    // Animate progress bars on page load
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
    
    // Animate cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe cards for animation
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('en-US').format(number);
}

// Export functions for potential testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateForm,
        validateNumericalInput,
        calculateIncomeRatio,
        formatCurrency,
        formatNumber
    };
}
