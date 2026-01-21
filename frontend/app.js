/**
 * AutoDoc Frontend Application
 */

// Configuration
// Use localhost for development, Render URL for production
const API_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://autodoc-lc7x.onrender.com';

// Model options per provider
const MODEL_OPTIONS = {
    openai: [
        { value: 'gpt-4o', label: 'GPT-4o (Recommandé)' },
        { value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
        { value: 'gpt-4', label: 'GPT-4' },
        { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
    ],
    anthropic: [
        { value: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet (Recommandé)' },
        { value: 'claude-3-opus-20240229', label: 'Claude 3 Opus' },
        { value: 'claude-3-haiku-20240307', label: 'Claude 3 Haiku' },
    ],
    custom: [
        { value: 'devstral-small-2-24b-instruct-2512', label: 'Devstral 24B (LM Studio)' },
        { value: 'qwen2.5-vl-32b-instruct', label: 'Qwen 2.5 VL 32B (LM Studio)' },
        { value: 'local-model', label: 'Autre modèle local' },
    ],
};

// State
let selectedFile = null;
let convertedHtml = null;
let convertedPdfBase64 = null;
let outputFilename = null;
let currentFormat = 'html';

// DOM Elements
const elements = {
    provider: document.getElementById('provider'),
    baseUrlGroup: document.getElementById('base-url-group'),
    baseUrl: document.getElementById('base-url'),
    apiKey: document.getElementById('api-key'),
    model: document.getElementById('model'),
    dropzone: document.getElementById('dropzone'),
    fileInput: document.getElementById('file-input'),
    fileInfo: document.getElementById('file-info'),
    fileName: document.getElementById('file-name'),
    fileSize: document.getElementById('file-size'),
    removeFile: document.getElementById('remove-file'),
    convertBtn: document.getElementById('convert-btn'),
    btnText: document.querySelector('.btn-text'),
    btnLoading: document.querySelector('.btn-loading'),
    status: document.getElementById('status'),
    statusMessage: document.getElementById('status-message'),
    resultSection: document.getElementById('result-section'),
    downloadBtn: document.getElementById('download-btn'),
    previewBtn: document.getElementById('preview-btn'),
    previewModal: document.getElementById('preview-modal'),
    previewIframe: document.getElementById('preview-iframe'),
    modalClose: document.getElementById('modal-close'),
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    handleProviderChange();
    loadSavedConfig();
});

function initializeEventListeners() {
    // Provider change
    elements.provider.addEventListener('change', handleProviderChange);

    // File input
    elements.dropzone.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileSelect);
    elements.removeFile.addEventListener('click', removeFile);

    // Drag and drop
    elements.dropzone.addEventListener('dragover', handleDragOver);
    elements.dropzone.addEventListener('dragleave', handleDragLeave);
    elements.dropzone.addEventListener('drop', handleDrop);

    // Convert button
    elements.convertBtn.addEventListener('click', handleConvert);

    // Result buttons
    elements.downloadBtn.addEventListener('click', downloadResult);
    elements.previewBtn.addEventListener('click', showPreview);
    elements.modalClose.addEventListener('click', closePreview);
    elements.previewModal.addEventListener('click', (e) => {
        if (e.target === elements.previewModal) closePreview();
    });

    // Save config on change
    elements.apiKey.addEventListener('change', saveConfig);
    elements.baseUrl.addEventListener('change', saveConfig);
    elements.model.addEventListener('change', saveConfig);

    // Output format change
    document.querySelectorAll('input[name="output-format"]').forEach(radio => {
        radio.addEventListener('change', handleFormatChange);
    });
}

function handleFormatChange() {
    const format = document.querySelector('input[name="output-format"]:checked').value;
    elements.btnText.textContent = format === 'pdf' ? 'Convertir en PDF' : 'Convertir en HTML';
}

// Provider handling
function handleProviderChange() {
    const provider = elements.provider.value;

    // Show/hide base URL field
    elements.baseUrlGroup.style.display = provider === 'custom' ? 'block' : 'none';

    // Set default base URL for custom provider (LM Studio)
    if (provider === 'custom' && !elements.baseUrl.value) {
        elements.baseUrl.value = 'http://localhost:1234';
    }

    // Update model options
    const models = MODEL_OPTIONS[provider] || [];
    elements.model.innerHTML = models
        .map(m => `<option value="${m.value}">${m.label}</option>`)
        .join('');

    // Update API key placeholder
    if (provider === 'openai') {
        elements.apiKey.placeholder = 'sk-...';
    } else if (provider === 'anthropic') {
        elements.apiKey.placeholder = 'sk-ant-...';
    } else {
        elements.apiKey.placeholder = 'Optionnel pour serveur local';
    }

    saveConfig();
    updateConvertButton();
}

// File handling
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) setFile(file);
}

function handleDragOver(e) {
    e.preventDefault();
    elements.dropzone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    elements.dropzone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    elements.dropzone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) setFile(file);
}

function setFile(file) {
    // Validate file type
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const validExtensions = ['.pdf', '.docx'];
    const extension = '.' + file.name.split('.').pop().toLowerCase();

    if (!validTypes.includes(file.type) && !validExtensions.includes(extension)) {
        showStatus('error', 'Type de fichier non supporté. Utilisez PDF ou DOCX.');
        return;
    }

    // Validate file size (50 MB)
    if (file.size > 50 * 1024 * 1024) {
        showStatus('error', 'Fichier trop volumineux (max 50 MB).');
        return;
    }

    selectedFile = file;
    elements.fileName.textContent = file.name;
    elements.fileSize.textContent = formatFileSize(file.size);
    elements.fileInfo.style.display = 'flex';
    elements.dropzone.style.display = 'none';

    hideStatus();
    updateConvertButton();
}

function removeFile() {
    selectedFile = null;
    elements.fileInput.value = '';
    elements.fileInfo.style.display = 'none';
    elements.dropzone.style.display = 'block';
    elements.resultSection.style.display = 'none';
    convertedHtml = null;
    convertedPdfBase64 = null;
    outputFilename = null;
    currentFormat = 'html';
    updateConvertButton();
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Conversion
function updateConvertButton() {
    const provider = elements.provider.value;
    const apiKey = elements.apiKey.value.trim();
    const hasFile = selectedFile !== null;

    // Custom provider doesn't require API key
    const hasApiKey = provider === 'custom' || apiKey.length > 0;

    elements.convertBtn.disabled = !hasFile || !hasApiKey;
}

async function handleConvert() {
    if (!selectedFile) return;

    const provider = elements.provider.value;
    const apiKey = elements.apiKey.value.trim();
    const model = elements.model.value;
    const baseUrl = elements.baseUrl.value.trim();
    const outputFormat = document.querySelector('input[name="output-format"]:checked').value;

    // Build LLM config
    const llmConfig = {
        provider: provider,
        api_key: apiKey || 'none',
        model: model,
    };

    if (provider === 'custom' && baseUrl) {
        llmConfig.base_url = baseUrl;
    }

    // Show loading state
    setLoading(true);
    hideStatus();
    elements.resultSection.style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('llm_config', JSON.stringify(llmConfig));
        formData.append('output_format', outputFormat);

        const response = await fetch(`${API_URL}/convert`, {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (result.success) {
            convertedHtml = result.html;
            convertedPdfBase64 = result.pdf_base64;
            outputFilename = result.filename;
            currentFormat = result.format || 'html';

            // Update download button text
            elements.downloadBtn.innerHTML = currentFormat === 'pdf'
                ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                   </svg>
                   Télécharger PDF`
                : `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                   </svg>
                   Télécharger HTML`;

            // Hide preview for PDF (can't preview PDF in iframe easily)
            elements.previewBtn.style.display = currentFormat === 'pdf' ? 'none' : 'inline-flex';

            showStatus('success', 'Conversion réussie !');
            elements.resultSection.style.display = 'block';
        } else {
            showStatus('error', result.error || 'Erreur lors de la conversion.');
        }
    } catch (error) {
        console.error('Conversion error:', error);
        showStatus('error', 'Erreur de connexion au serveur. Vérifiez que le backend est démarré.');
    } finally {
        setLoading(false);
    }
}

function setLoading(loading) {
    elements.convertBtn.disabled = loading;
    elements.btnText.style.display = loading ? 'none' : 'inline';
    elements.btnLoading.style.display = loading ? 'flex' : 'none';
}

// Status messages
function showStatus(type, message) {
    elements.status.className = `status ${type}`;
    elements.statusMessage.textContent = message;
    elements.status.style.display = 'flex';
}

function hideStatus() {
    elements.status.style.display = 'none';
}

// Result actions
function downloadResult() {
    if (currentFormat === 'pdf' && convertedPdfBase64) {
        // Download PDF from base64
        const byteCharacters = atob(convertedPdfBase64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = outputFilename || 'document.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } else if (convertedHtml) {
        // Download HTML
        const blob = new Blob([convertedHtml], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = outputFilename || 'document.html';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

function showPreview() {
    if (!convertedHtml) return;

    const blob = new Blob([convertedHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    elements.previewIframe.src = url;
    elements.previewModal.style.display = 'flex';
}

function closePreview() {
    elements.previewModal.style.display = 'none';
    elements.previewIframe.src = '';
}

// Config persistence (localStorage)
function saveConfig() {
    const config = {
        provider: elements.provider.value,
        baseUrl: elements.baseUrl.value,
        model: elements.model.value,
        // Note: API key is NOT saved for security
    };
    localStorage.setItem('autodoc_config', JSON.stringify(config));
}

function loadSavedConfig() {
    const saved = localStorage.getItem('autodoc_config');
    if (saved) {
        try {
            const config = JSON.parse(saved);
            if (config.provider) {
                elements.provider.value = config.provider;
                handleProviderChange();
            }
            if (config.baseUrl) elements.baseUrl.value = config.baseUrl;
            if (config.model) elements.model.value = config.model;
        } catch (e) {
            console.error('Error loading saved config:', e);
        }
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Escape to close modal
    if (e.key === 'Escape' && elements.previewModal.style.display === 'flex') {
        closePreview();
    }
});
