// AI Fashion Stylist - Final Fixed JavaScript

console.log('🚀 AI Fashion Stylist script loading...');

// Global variables
let isAnalyzing = false;
let currentFile = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM loaded, initializing app...');
    initializeApp();
});

function initializeApp() {
    // Get all elements
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('imageFile');
    const fileDropArea = document.getElementById('fileDropArea');
    const submitBtn = document.getElementById('submitBtn');
    const tryAgainBtn = document.getElementById('tryAgainBtn');
    
    console.log('📝 Elements found:', {
        uploadForm: !!uploadForm,
        fileInput: !!fileInput,
        submitBtn: !!submitBtn,
        tryAgainBtn: !!tryAgainBtn
    });
    
    // Initialize file upload
    if (fileDropArea && fileInput) {
        setupFileUpload(fileDropArea, fileInput, submitBtn);
    }
    
    // Setup form submission - FIXED VERSION
    if (uploadForm && fileInput) {
        setupFormSubmission(uploadForm, fileInput, submitBtn);
    }
    
    // Setup try again button
    if (tryAgainBtn) {
        tryAgainBtn.addEventListener('click', function() {
            resetApplication();
        });
    }
    
    // Test server connection
    testServerConnection();
    
    console.log('✅ App initialized successfully!');
}

function setupFileUpload(dropArea, fileInput, submitBtn) {
    console.log('🔧 Setting up file upload...');
    
    // Make drop area clickable
    dropArea.addEventListener('click', function(e) {
        if (e.target !== fileInput && !e.target.closest('button')) {
            fileInput.click();
        }
    });
    
    // File selection handler - FIXED
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        console.log('📁 File input changed:', file ? file.name : 'no file');
        handleFileSelect(file, submitBtn);
    });
    
    // Drag and drop handlers
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, handleDragOver, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, handleDragLeave, false);
    });
    
    dropArea.addEventListener('drop', function(e) {
        handleDrop(e, fileInput, submitBtn);
    });
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove('drag-over');
}

function handleDrop(e, fileInput, submitBtn) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        // Create new FileList for input
        const dt = new DataTransfer();
        dt.items.add(files[0]);
        fileInput.files = dt.files;
        
        handleFileSelect(files[0], submitBtn);
    }
}

function handleFileSelect(file, submitBtn) {
    console.log('📁 File selected:', file ? file.name : 'none');
    
    if (!file) {
        resetFileDisplay(submitBtn);
        currentFile = null;
        return;
    }
    
    // Store current file
    currentFile = file;
    
    // Validate file
    const validation = validateFile(file);
    if (!validation.valid) {
        showError(validation.message);
        resetFileDisplay(submitBtn);
        currentFile = null;
        return;
    }
    
    // Show file info
    displayFileInfo(file);
    
    // Enable submit button
    if (submitBtn) {
        submitBtn.disabled = false;
        const submitText = document.getElementById('submitText');
        if (submitText) {
            submitText.textContent = 'Analyze My Style';
        }
    }
    
    // Show preview
    showImagePreview(file);
    hideError();
}

function validateFile(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (!allowedTypes.includes(file.type)) {
        return { valid: false, message: 'Please select a valid image file (JPG, PNG, GIF, BMP, or WebP)' };
    }
    
    if (file.size > maxSize) {
        return { valid: false, message: 'File size must be less than 16MB' };
    }
    
    return { valid: true };
}

function displayFileInfo(file) {
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    
    if (fileInfo && fileName && fileSize) {
        fileName.textContent = file.name;
        fileSize.textContent = `Size: ${(file.size / 1024 / 1024).toFixed(2)} MB`;
        fileInfo.classList.remove('d-none');
    }
}

function showImagePreview(file) {
    const imagePreview = document.getElementById('imagePreview');
    if (!imagePreview) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.innerHTML = `
            <img src="${e.target.result}" class="file-preview" alt="Preview">
            <button type="button" class="btn btn-sm btn-danger mt-2" onclick="clearFile()">
                <i class="fas fa-times"></i> Remove Image
            </button>
        `;
    };
    reader.readAsDataURL(file);
}

function resetFileDisplay(submitBtn) {
    const fileInfo = document.getElementById('fileInfo');
    const imagePreview = document.getElementById('imagePreview');
    
    if (fileInfo) fileInfo.classList.add('d-none');
    if (imagePreview) imagePreview.innerHTML = '';
    
    if (submitBtn) {
        submitBtn.disabled = true;
        const submitText = document.getElementById('submitText');
        if (submitText) {
            submitText.textContent = 'Select an Image First';
        }
    }
}

// Global function to clear file
window.clearFile = function() {
    const fileInput = document.getElementById('imageFile');
    const submitBtn = document.getElementById('submitBtn');
    
    if (fileInput) fileInput.value = '';
    resetFileDisplay(submitBtn);
    currentFile = null;
};

function setupFormSubmission(form, fileInput, submitBtn) {
    console.log('📋 Setting up form submission...');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        console.log('🚀 Form submitted');
        console.log('📁 Current file:', currentFile ? currentFile.name : 'none');
        console.log('📁 File input files:', fileInput.files.length);
        
        if (isAnalyzing) {
            console.log('⏳ Analysis already in progress...');
            return;
        }
        
        // Check for file - FIXED VALIDATION
        const file = fileInput.files[0] || currentFile;
        if (!file) {
            console.log('❌ No file selected');
            showError('Please select an image file first');
            return;
        }
        
        console.log('✅ File validation passed:', file.name);
        
        const validation = validateFile(file);
        if (!validation.valid) {
            console.log('❌ File validation failed:', validation.message);
            showError(validation.message);
            return;
        }
        
        // Start analysis
        await performAnalysis(form, file);
    });
}

async function performAnalysis(form, file) {
    isAnalyzing = true;
    
    try {
        // Show loading state
        showLoading();
        disableForm();
        hideError();
        hideResults();
        
        console.log('📡 Starting analysis for:', file.name);
        
        // Create form data - FIXED
        const formData = new FormData();
        formData.append('image', file);
        
        // Add user_id if present
        const userIdInput = document.getElementById('userId');
        if (userIdInput && userIdInput.value.trim()) {
            formData.append('user_id', userIdInput.value.trim());
        } else {
            formData.append('user_id', '');
        }
        
        console.log('📤 Sending request...');
        console.log('📋 FormData contents:');
        for (let pair of formData.entries()) {
            if (pair[1] instanceof File) {
                console.log(`  ${pair[0]}: File(${pair[1].name}, ${pair[1].size} bytes)`);
            } else {
                console.log(`  ${pair[0]}: ${pair[1]}`);
            }
        }
        
        // Make request
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        console.log('📨 Response received:', response.status, response.statusText);
        
        // Parse response
        const data = await response.json();
        console.log('📊 Response data:', data);
        
        if (response.ok && data.success) {
            console.log('✅ Analysis successful!');
            displayAllResults(data);
        } else {
            console.log('❌ Analysis failed:', data.error);
            showError(data.error || 'Analysis failed. Please try again.');
        }
        
    } catch (error) {
        console.error('💥 Request error:', error);
        if (error.message.includes('Failed to fetch')) {
            showError('Cannot connect to server. Please make sure the server is running and try again.');
        } else {
            showError(`Error: ${error.message}`);
        }
    } finally {
        isAnalyzing = false;
        hideLoading();
        enableForm();
    }
}

function displayAllResults(data) {
    console.log('🎨 Displaying all results...');
    
    try {
        // Populate each section
        populateDetectedItems(data.detected_items || []);
        populateAISuggestions(data.ai_suggestions || '');
        populateShoppingLinks(data.shopping_links || []);
        
        // Show results
        showResults();
        
    } catch (error) {
        console.error('💥 Error displaying results:', error);
        showError('Error displaying results. Please try again.');
    }
}

function populateDetectedItems(items) {
    console.log('👕 Populating detected items:', items.length);
    const container = document.getElementById('detectedItems');
    
    if (!container) {
        console.error('❌ Detected items container not found');
        return;
    }
    
    container.innerHTML = '';
    
    if (!items || items.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    No specific clothing items detected in the image. The AI will provide general styling suggestions.
                </div>
            </div>
        `;
        return;
    }
    
    items.forEach((item, index) => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'col-md-6 col-lg-4 mb-3 fade-in-up';
        itemDiv.style.animationDelay = `${index * 0.1}s`;
        
        const itemName = item.item || 'Unknown item';
        const confidence = Math.max(0, Math.min(1, item.confidence || 0));
        const color = item.color || 'unknown';
        const category = item.category || 'other';
        
        itemDiv.innerHTML = `
            <div class="detected-item">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h6 class="mb-0 text-capitalize fw-bold">
                        <i class="fas fa-tag me-2 text-primary"></i>
                        ${escapeHtml(itemName)}
                    </h6>
                    <span class="item-badge confidence-badge">
                        ${Math.round(confidence * 100)}%
                    </span>
                </div>
                <div class="d-flex gap-2 flex-wrap">
                    <span class="item-badge category-badge">
                        <i class="fas fa-layer-group me-1"></i>
                        ${escapeHtml(category)}
                    </span>
                    <span class="item-badge color-badge">
                        <i class="fas fa-palette me-1"></i>
                        ${escapeHtml(color)}
                    </span>
                </div>
            </div>
        `;
        
        container.appendChild(itemDiv);
    });
    
    console.log('✅ Detected items populated');
}

function populateAISuggestions(suggestions) {
    console.log('🤖 Populating AI suggestions...');
    const container = document.getElementById('aiSuggestions');
    
    if (!container) {
        console.error('❌ AI suggestions container not found');
        return;
    }
    
    if (!suggestions || suggestions.trim() === '') {
        container.innerHTML = `
            <div class="alert alert-warning">
                <h5><i class="fas fa-robot me-2"></i>AI Suggestions</h5>
                <p class="mb-2">AI suggestions are temporarily unavailable. Here are some general styling tips:</p>
                <ul class="mb-0">
                    <li>Ensure your clothes fit well and are comfortable</li>
                    <li>Choose colors that complement your skin tone</li>
                    <li>Add accessories to enhance your overall look</li>
                    <li>Consider the occasion when selecting your outfit</li>
                    <li>Layer pieces for depth and visual interest</li>
                </ul>
            </div>
        `;
        return;
    }
    
    try {
        // Format suggestions with HTML
        let formatted = suggestions
            .replace(/##\s+(.+?)(?=\n|$)/g, '<h3 class="text-primary mt-4 mb-3"><i class="fas fa-star me-2"></i>$1</h3>')
            .replace(/###\s+(.+?)(?=\n|$)/g, '<h4 class="text-secondary mt-3 mb-2"><i class="fas fa-chevron-right me-2"></i>$1</h4>')
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*([^*\n]+)\*/g, '<em>$1</em>')
            .replace(/^-\s+(.+)$/gm, '<li>$1</li>')
            .replace(/\n\n+/g, '</p><p>')
            .replace(/\n/g, '<br>');
        
        // Wrap lists
        formatted = formatted.replace(
            /(<li>.*?<\/li>)(\s*<br>\s*<li>.*?<\/li>)*/g,
            function(match) {
                return '<ul class="mb-3">' + match.replace(/<br>/g, '') + '</ul>';
            }
        );
        
        // Ensure paragraphs
        if (!formatted.includes('<h3>') && !formatted.includes('<p>')) {
            formatted = '<p>' + formatted + '</p>';
        }
        
        container.innerHTML = `<div class="suggestions-content">${formatted}</div>`;
        
    } catch (error) {
        console.error('💥 Error formatting suggestions:', error);
        container.innerHTML = `<div class="alert alert-secondary"><pre>${escapeHtml(suggestions)}</pre></div>`;
    }
    
    console.log('✅ AI suggestions populated');
}

function populateShoppingLinks(links) {
    console.log('🛍️ Populating shopping links:', links.length);
    const container = document.getElementById('shoppingLinks');
    
    if (!container) {
        console.error('❌ Shopping links container not found');
        return;
    }
    
    container.innerHTML = '';
    
    if (!links || links.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info">
                    <h5><i class="fas fa-shopping-cart me-2"></i>Shopping Recommendations</h5>
                    <p class="mb-2">Shopping links are temporarily unavailable. Try searching for similar items on these popular sites:</p>
                    <div class="d-flex gap-2 flex-wrap">
                        <a href="https://www.amazon.com/fashion" target="_blank" class="btn btn-sm btn-outline-primary">Amazon Fashion</a>
                        <a href="https://www.zara.com" target="_blank" class="btn btn-sm btn-outline-primary">Zara</a>
                        <a href="https://www2.hm.com" target="_blank" class="btn btn-sm btn-outline-primary">H&M</a>
                        <a href="https://www.asos.com" target="_blank" class="btn btn-sm btn-outline-primary">ASOS</a>
                    </div>
                </div>
            </div>
        `;
        return;
    }
    
    links.forEach((link, index) => {
        const linkDiv = document.createElement('div');
        linkDiv.className = 'col-md-6 col-lg-4 mb-4 fade-in-up';
        linkDiv.style.animationDelay = `${(index * 0.15)}s`;
        
        const title = link.title || 'Fashion Item';
        const price = link.price || 'Check price';
        const source = link.source || 'Online Store';
        const url = link.link && link.link !== '#' ? link.link : null;
        const image = link.image || 'https://via.placeholder.com/300x200/6c757d/ffffff?text=Fashion+Item';
        const rating = link.rating || 'No rating';
        
        linkDiv.innerHTML = `
            <div class="shopping-item h-100">
                <div class="card shopping-card h-100">
                    <div class="position-relative">
                        <img src="${escapeHtml(image)}" 
                             class="shopping-image" 
                             alt="${escapeHtml(title)}"
                             onerror="this.src='https://via.placeholder.com/300x200/6c757d/ffffff?text=Fashion+Item'"
                             loading="lazy">
                        <span class="position-absolute top-0 end-0 badge bg-primary m-2">${escapeHtml(source)}</span>
                    </div>
                    <div class="card-body d-flex flex-column">
                        <h6 class="card-title mb-2">${escapeHtml(truncateText(title, 60))}</h6>
                        
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <span class="price-tag">${escapeHtml(price)}</span>
                            <small class="rating-stars">
                                <i class="fas fa-star text-warning"></i> ${escapeHtml(rating)}
                            </small>
                        </div>
                        
                        <div class="mt-auto">
                            ${url ? 
                                `<a href="${escapeHtml(url)}" 
                                   target="_blank" 
                                   rel="noopener noreferrer"
                                   class="btn shop-now-btn w-100">
                                    <i class="fas fa-shopping-cart me-2"></i>Shop Now
                                </a>` :
                                `<button class="btn btn-secondary w-100" disabled>
                                    <i class="fas fa-link-slash me-2"></i>Link Unavailable
                                </button>`
                            }
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.appendChild(linkDiv);
    });
    
    console.log('✅ Shopping links populated');
}

// Utility functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text.toString();
    return div.innerHTML;
}

function truncateText(text, maxLength) {
    if (!text || text.length <= maxLength) return text || '';
    return text.substr(0, maxLength).trim() + '...';
}

// UI State functions
function showLoading() {
    const loading = document.getElementById('loadingIndicator');
    if (loading) {
        loading.classList.remove('d-none');
        console.log('⏳ Loading shown');
    }
}

function hideLoading() {
    const loading = document.getElementById('loadingIndicator');
    if (loading) {
        loading.classList.add('d-none');
        console.log('✅ Loading hidden');
    }
}

function showResults() {
    const results = document.getElementById('resultsSection');
    if (results) {
        results.classList.remove('d-none');
        results.scrollIntoView({ behavior: 'smooth' });
        console.log('📊 Results shown');
    }
}

function hideResults() {
    const results = document.getElementById('resultsSection');
    if (results) {
        results.classList.add('d-none');
        console.log('📊 Results hidden');
    }
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    
    if (errorDiv && errorText) {
        errorText.textContent = message;
        errorDiv.classList.remove('d-none');
        errorDiv.scrollIntoView({ behavior: 'smooth' });
        console.log('❌ Error shown:', message);
    }
}

function hideError() {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.classList.add('d-none');
    }
}

function disableForm() {
    const submitBtn = document.getElementById('submitBtn');
    const fileInput = document.getElementById('imageFile');
    
    if (submitBtn) {
        submitBtn.disabled = true;
        const submitText = document.getElementById('submitText');
        if (submitText) {
            submitText.textContent = 'Analyzing...';
        }
    }
    
    if (fileInput) {
        fileInput.disabled = true;
    }
}

function enableForm() {
    const submitBtn = document.getElementById('submitBtn');
    const fileInput = document.getElementById('imageFile');
    
    if (submitBtn && currentFile) {
        submitBtn.disabled = false;
        const submitText = document.getElementById('submitText');
        if (submitText) {
            submitText.textContent = 'Analyze My Style';
        }
    }
    
    if (fileInput) {
        fileInput.disabled = false;
    }
}

function resetApplication() {
    console.log('🔄 Resetting application...');
    
    // Reset form
    const form = document.getElementById('uploadForm');
    if (form) form.reset();
    
    // Clear file display
    if (window.clearFile) window.clearFile();
    
    // Hide sections
    hideResults();
    hideError();
    hideLoading();
    
    // Reset analyzing state
    isAnalyzing = false;
    currentFile = null;
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    console.log('✅ Application reset complete');
}

// Test server connection
async function testServerConnection() {
    try {
        console.log('🔌 Testing server connection...');
        const response = await fetch('/test', { method: 'GET' });
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Server connection successful:', data.status);
        } else {
            console.warn('⚠️ Server responded with error:', response.status);
        }
    } catch (error) {
        console.error('❌ Server connection failed:', error.message);
    }
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('💥 Global error:', e.error);
});

console.log('✅ AI Fashion Stylist script loaded completely!');