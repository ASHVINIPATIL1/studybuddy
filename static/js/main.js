// ============================================
// MAIN JAVASCRIPT - Global functionality
// ============================================

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== NAVBAR TOGGLE ====================
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Animate toggle button
            const isOpen = navMenu.classList.contains('active');
            navToggle.innerHTML = isOpen ? `
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            ` : `
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
            `;
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInside = navMenu.contains(event.target) || navToggle.contains(event.target);
            if (!isClickInside && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
            }
        });
        
        // Close menu when clicking on a link
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
            });
        });
    }
    
    // ==================== SMOOTH SCROLLING ====================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            
            // Skip if href is just "#"
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for navbar height
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ==================== NAVBAR SHADOW ON SCROLL ====================
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 20) {
                navbar.style.boxShadow = 'var(--shadow-md)';
            } else {
                navbar.style.boxShadow = 'none';
            }
        });
    }
    
    // ==================== FORM VALIDATION HELPER ====================
    window.validateForm = function(formId) {
        const form = document.getElementById(formId);
        if (!form) return false;
        
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('error');
                
                // Show error message
                let errorMsg = input.parentElement.querySelector('.form-error');
                if (!errorMsg) {
                    errorMsg = document.createElement('p');
                    errorMsg.className = 'form-error';
                    errorMsg.textContent = 'This field is required';
                    input.parentElement.appendChild(errorMsg);
                }
            } else {
                input.classList.remove('error');
                const errorMsg = input.parentElement.querySelector('.form-error');
                if (errorMsg) errorMsg.remove();
            }
        });
        
        return isValid;
    };
    
    // ==================== MODAL FUNCTIONALITY ====================
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent background scrolling
        }
    };
    
    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = ''; // Restore scrolling
        }
    };
    
    // Close modal on overlay click
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                overlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
    
    // Close modal on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay.active').forEach(modal => {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            });
        }
    });
    
    // ==================== LOADING STATE HELPER ====================
    window.setLoadingState = function(button, isLoading) {
        if (isLoading) {
            button.disabled = true;
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = `
                <div class="spinner" style="width: 20px; height: 20px; border-width: 2px;"></div>
                Loading...
            `;
        } else {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText || button.innerHTML;
        }
    };
    
    // ==================== TOAST NOTIFICATION ====================
    window.showToast = function(message, type = 'info') {
        // Remove existing toast
        const existingToast = document.querySelector('.toast');
        if (existingToast) existingToast.remove();
        
        // Create toast
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    ${type === 'success' ? '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>' : 
                      type === 'error' ? '<circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line>' :
                      '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>'}
                </svg>
                <span>${message}</span>
            </div>
        `;
        
        // Style toast
        toast.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            padding: 1rem 1.5rem;
            background-color: ${type === 'success' ? 'var(--success)' : type === 'error' ? 'var(--error)' : 'var(--primary)'};
            color: white;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    };
    
    // ==================== COPY TO CLIPBOARD ====================
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            showToast('Failed to copy', 'error');
        });
    };
    
    // ==================== AUTO-RESIZE TEXTAREA ====================
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
    
    console.log('StudyBuddy app loaded successfully! 🎉');
});

// ==================== CSS ANIMATIONS ====================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .toast {
        animation: slideIn 0.3s ease;
    }
    
    input.error,
    textarea.error {
        border-color: var(--error);
    }
`;
document.head.appendChild(style);