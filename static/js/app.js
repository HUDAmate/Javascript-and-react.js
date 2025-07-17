// TikTube Studio - Frontend Application
class TikTubeStudio {
    constructor() {
        this.currentVideo = null;
        this.selectedTheme = null;
        this.analysisResults = null;
        this.selectedSegment = null;
        this.themes = {};
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadThemes();
        this.setupDragAndDrop();
    }
    
    setupEventListeners() {
        // File input
        document.getElementById('video-input').addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
        });
        
        // Target duration slider
        const durationSlider = document.getElementById('target-duration');
        const durationValue = document.getElementById('duration-value');
        
        durationSlider.addEventListener('input', (e) => {
            durationValue.textContent = `${e.target.value}s`;
        });
        
        // Analyze button
        document.getElementById('analyze-btn').addEventListener('click', () => {
            this.analyzeVideo();
        });
        
        // Download button
        document.getElementById('download-btn').addEventListener('click', () => {
            this.downloadVideo();
        });
        
        // Process another button
        document.getElementById('process-another-btn').addEventListener('click', () => {
            this.resetApplication();
        });
    }
    
    setupDragAndDrop() {
        const uploadArea = document.getElementById('upload-area');
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });
        
        uploadArea.addEventListener('click', () => {
            document.getElementById('video-input').click();
        });
    }
    
    async loadThemes() {
        try {
            const response = await fetch('/api/themes');
            this.themes = await response.json();
            this.renderThemes();
        } catch (error) {
            console.error('Error loading themes:', error);
            this.showError('Failed to load themes');
        }
    }
    
    renderThemes() {
        const themeContainer = document.getElementById('theme-cards');
        themeContainer.innerHTML = '';
        
        const themeIcons = {
            entertainment: 'fas fa-laugh-beam',
            educational: 'fas fa-graduation-cap',
            music: 'fas fa-music',
            gaming: 'fas fa-gamepad',
            lifestyle: 'fas fa-heart',
            news: 'fas fa-newspaper'
        };
        
        Object.entries(this.themes).forEach(([key, theme]) => {
            const themeCard = document.createElement('div');
            themeCard.className = 'col-md-4 col-lg-2 mb-3';
            themeCard.innerHTML = `
                <div class="theme-card" data-theme="${key}">
                    <i class="${themeIcons[key] || 'fas fa-video'}"></i>
                    <h5>${theme.name}</h5>
                    <p>${theme.description}</p>
                </div>
            `;
            
            themeCard.addEventListener('click', () => {
                this.selectTheme(key);
            });
            
            themeContainer.appendChild(themeCard);
        });
    }
    
    selectTheme(themeKey) {
        // Remove previous selection
        document.querySelectorAll('.theme-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Add selection to clicked theme
        document.querySelector(`[data-theme="${themeKey}"]`).classList.add('selected');
        this.selectedTheme = themeKey;
    }
    
    async handleFileSelect(file) {
        if (!file) return;
        
        // Validate file type
        if (!file.type.startsWith('video/')) {
            this.showError('Please select a valid video file');
            return;
        }
        
        // Validate file size (max 500MB)
        if (file.size > 500 * 1024 * 1024) {
            this.showError('File size must be less than 500MB');
            return;
        }
        
        this.currentVideo = file;
        await this.uploadVideo(file);
    }
    
    async uploadVideo(file) {
        const uploadProgress = document.getElementById('upload-progress');
        const uploadArea = document.getElementById('upload-area');
        const videoInfo = document.getElementById('video-info');
        
        // Show progress
        uploadArea.style.display = 'none';
        uploadProgress.classList.remove('d-none');
        
        const formData = new FormData();
        formData.append('video', file);
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Hide progress and show video info
                uploadProgress.classList.add('d-none');
                videoInfo.classList.remove('d-none');
                
                // Update video info
                document.getElementById('video-duration').textContent = 
                    `${Math.round(result.video_info.duration)}s`;
                document.getElementById('video-resolution').textContent = 
                    `${result.video_info.size[0]}x${result.video_info.size[1]}`;
                
                // Show theme selection
                document.getElementById('theme-selection').classList.remove('d-none');
                document.getElementById('theme-selection').classList.add('fade-in-up');
                
                this.currentVideo = {
                    filename: result.filename,
                    info: result.video_info
                };
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.showError(`Upload failed: ${error.message}`);
            
            // Reset upload area
            uploadProgress.classList.add('d-none');
            uploadArea.style.display = 'block';
        }
    }
    
    async analyzeVideo() {
        if (!this.currentVideo || !this.selectedTheme) {
            this.showError('Please select a video and theme first');
            return;
        }
        
        const analyzeBtn = document.getElementById('analyze-btn');
        const originalText = analyzeBtn.innerHTML;
        
        // Show loading state
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
        analyzeBtn.disabled = true;
        
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    filename: this.currentVideo.filename,
                    theme: this.selectedTheme,
                    target_duration: parseInt(document.getElementById('target-duration').value)
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.analysisResults = result.segments;
                this.renderAnalysisResults();
                
                // Show analysis results
                document.getElementById('analysis-results').classList.remove('d-none');
                document.getElementById('analysis-results').classList.add('fade-in-up');
                
                // Scroll to results
                document.getElementById('analysis-results').scrollIntoView({ 
                    behavior: 'smooth' 
                });
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showError(`Analysis failed: ${error.message}`);
        } finally {
            // Reset button
            analyzeBtn.innerHTML = originalText;
            analyzeBtn.disabled = false;
        }
    }
    
    renderAnalysisResults() {
        const container = document.getElementById('segments-container');
        container.innerHTML = '';
        
        this.analysisResults.forEach((segment, index) => {
            const segmentCard = document.createElement('div');
            segmentCard.className = 'col-md-6 col-lg-4 mb-3';
            segmentCard.innerHTML = `
                <div class="segment-card" data-segment="${index}">
                    <div class="segment-score">${(segment.score * 100).toFixed(0)}%</div>
                    <h6>Segment ${index + 1}</h6>
                    <p class="text-muted small mb-2">
                        ${this.formatTime(segment.start)} - ${this.formatTime(segment.end)}
                        (${segment.duration}s)
                    </p>
                    <p class="text-muted small mb-2">${segment.description}</p>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${segment.confidence * 100}%"></div>
                    </div>
                    <small class="text-muted">Confidence: ${(segment.confidence * 100).toFixed(0)}%</small>
                    <div class="mt-3">
                        <button class="btn btn-primary btn-sm select-segment-btn">
                            <i class="fas fa-check me-1"></i>
                            Select This Segment
                        </button>
                    </div>
                </div>
            `;
            
            segmentCard.addEventListener('click', () => {
                this.selectSegment(index);
            });
            
            container.appendChild(segmentCard);
        });
    }
    
    selectSegment(index) {
        // Remove previous selection
        document.querySelectorAll('.segment-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Add selection to clicked segment
        document.querySelector(`[data-segment="${index}"]`).classList.add('selected');
        this.selectedSegment = this.analysisResults[index];
        
        // Process the selected segment
        this.processVideo();
    }
    
    async processVideo() {
        if (!this.selectedSegment) {
            this.showError('Please select a segment first');
            return;
        }
        
        // Show processing status
        document.getElementById('processing-status').classList.remove('d-none');
        
        const options = {
            theme: this.selectedTheme,
            add_subtitles: document.getElementById('add-subtitles').checked,
            auto_effects: document.getElementById('auto-effects').checked,
            subtitle_font_size: 60,
            subtitle_color: 'white',
            subtitle_stroke_color: 'black',
            subtitle_stroke_width: 3
        };
        
        try {
            // Update processing message
            document.getElementById('processing-message').textContent = 'Extracting segment...';
            
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    filename: this.currentVideo.filename,
                    selected_segment: this.selectedSegment,
                    options: options
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Hide processing status
                document.getElementById('processing-status').classList.add('d-none');
                
                // Show results
                this.showProcessingResults(result);
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            console.error('Processing error:', error);
            document.getElementById('processing-status').classList.add('d-none');
            this.showError(`Processing failed: ${error.message}`);
        }
    }
    
    showProcessingResults(result) {
        // Store download URL
        this.downloadUrl = result.download_url;
        
        // Show results section
        document.getElementById('processing-results').classList.remove('d-none');
        document.getElementById('processing-results').classList.add('fade-in-up');
        
        // Scroll to results
        document.getElementById('processing-results').scrollIntoView({ 
            behavior: 'smooth' 
        });
        
        // Add success animation
        const checkmark = document.querySelector('#processing-results .fa-check-circle');
        checkmark.classList.add('success-checkmark');
    }
    
    downloadVideo() {
        if (this.downloadUrl) {
            window.location.href = this.downloadUrl;
        } else {
            this.showError('No video available for download');
        }
    }
    
    resetApplication() {
        // Reset all state
        this.currentVideo = null;
        this.selectedTheme = null;
        this.analysisResults = null;
        this.selectedSegment = null;
        this.downloadUrl = null;
        
        // Hide all sections except upload
        document.getElementById('video-info').classList.add('d-none');
        document.getElementById('theme-selection').classList.add('d-none');
        document.getElementById('analysis-results').classList.add('d-none');
        document.getElementById('processing-results').classList.add('d-none');
        
        // Reset upload area
        document.getElementById('upload-area').style.display = 'block';
        document.getElementById('upload-progress').classList.add('d-none');
        
        // Reset form inputs
        document.getElementById('video-input').value = '';
        document.getElementById('target-duration').value = 60;
        document.getElementById('duration-value').textContent = '60s';
        document.getElementById('add-subtitles').checked = true;
        document.getElementById('auto-effects').checked = true;
        
        // Clear theme selection
        document.querySelectorAll('.theme-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    showError(message) {
        // Create error toast
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-danger border-0 position-fixed';
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999;';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast element after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
    
    showSuccess(message) {
        // Create success toast
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-success border-0 position-fixed';
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999;';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-check-circle me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast element after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TikTubeStudio();
});

// Add smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});