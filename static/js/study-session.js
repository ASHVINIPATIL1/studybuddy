// // ============================================
// // STUDY SESSION PAGE JAVASCRIPT
// // ============================================

// document.addEventListener('DOMContentLoaded', function() {
    
//     // ==================== FILE UPLOAD ====================
//     const uploadZone = document.getElementById('uploadZone');
//     const fileInput = document.getElementById('fileInput');
//     const fileList = document.getElementById('fileList');
    
//     // Click to browse
//     if (uploadZone && fileInput) {
//         uploadZone.addEventListener('click', () => {
//             fileInput.click();
//         });
        
//         // Drag and drop
//         uploadZone.addEventListener('dragover', (e) => {
//             e.preventDefault();
//             uploadZone.style.borderColor = 'var(--primary)';
//             uploadZone.style.backgroundColor = 'rgba(91, 79, 233, 0.05)';
//         });
        
//         uploadZone.addEventListener('dragleave', () => {
//             uploadZone.style.borderColor = 'var(--border-dark)';
//             uploadZone.style.backgroundColor = 'var(--bg-primary)';
//         });
        
//         uploadZone.addEventListener('drop', (e) => {
//             e.preventDefault();
//             uploadZone.style.borderColor = 'var(--border-dark)';
//             uploadZone.style.backgroundColor = 'var(--bg-primary)';
            
//             const files = e.dataTransfer.files;
//             handleFiles(files);
//         });
        
//         // File input change
//         fileInput.addEventListener('change', (e) => {
//             const files = e.target.files;
//             handleFiles(files);
//         });
//     }
    
//     // Handle uploaded files
//     function handleFiles(files) {
//         Array.from(files).forEach(file => {
//             if (file.type === 'application/pdf') {
//                 addFileToList(file);
//                 showToast(`Uploaded: ${file.name}`, 'success');
                
//                 // Simulate AI processing
//                 setTimeout(() => {
//                     showToast('AI is analyzing your document...', 'info');
//                 }, 1000);
                
//                 setTimeout(() => {
//                     showToast('Analysis complete! Topics and flashcards updated.', 'success');
//                 }, 3000);
//             } else {
//                 showToast('Please upload PDF files only', 'error');
//             }
//         });
//     }
    
//     // Add file to list
//     function addFileToList(file) {
//         const fileItem = document.createElement('div');
//         fileItem.className = 'file-item';
//         fileItem.innerHTML = `
//             <div class="file-icon">
//                 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
//                     <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
//                     <polyline points="14 2 14 8 20 8"/>
//                 </svg>
//             </div>
//             <div class="file-info">
//                 <p class="file-name">${file.name}</p>
//                 <p class="file-meta">${(file.size / (1024 * 1024)).toFixed(1)} MB • Uploading...</p>
//             </div>
//             <button class="file-delete">
//                 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
//                     <line x1="18" y1="6" x2="6" y2="18"/>
//                     <line x1="6" y1="6" x2="18" y2="18"/>
//                 </svg>
//             </button>
//         `;
        
//         fileList.appendChild(fileItem);
        
//         // Simulate upload
//         setTimeout(() => {
//             const meta = fileItem.querySelector('.file-meta');
//             meta.textContent = `${(file.size / (1024 * 1024)).toFixed(1)} MB • Uploaded`;
//         }, 1500);
        
//         // Delete file
//         const deleteBtn = fileItem.querySelector('.file-delete');
//         deleteBtn.addEventListener('click', (e) => {
//             e.stopPropagation();
//             fileItem.remove();
//             showToast('File removed', 'info');
//         });
//     }
    
//     // ==================== CHAT FUNCTIONALITY ====================
//     const chatInput = document.getElementById('chatInput');
//     const sendBtn = document.getElementById('sendBtn');
//     const chatMessages = document.getElementById('chatMessages');
    
//     // Auto-resize textarea
//     if (chatInput) {
//         chatInput.addEventListener('input', function() {
//             this.style.height = 'auto';
//             this.style.height = Math.min(this.scrollHeight, 150) + 'px';
//         });
        
//         // Send on Enter (Shift+Enter for new line)
//         chatInput.addEventListener('keydown', function(e) {
//             if (e.key === 'Enter' && !e.shiftKey) {
//                 e.preventDefault();
//                 sendMessage();
//             }
//         });
//     }
    
//     // Send button click
//     if (sendBtn) {
//         sendBtn.addEventListener('click', sendMessage);
//     }
    
//     function sendMessage() {
//         const message = chatInput.value.trim();
//         if (!message) return;
        
//         // Add user message
//         addMessage(message, 'user');
        
//         // Clear input
//         chatInput.value = '';
//         chatInput.style.height = 'auto';
        
//         // Disable input while "thinking"
//         chatInput.disabled = true;
//         sendBtn.disabled = true;
        
//         // Simulate AI thinking
//         setTimeout(() => {
//             addTypingIndicator();
//         }, 500);
        
//         // Simulate AI response
//         setTimeout(() => {
//             removeTypingIndicator();
//             const aiResponse = generateAIResponse(message);
//             addMessage(aiResponse, 'assistant');
            
//             // Re-enable input
//             chatInput.disabled = false;
//             sendBtn.disabled = false;
//             chatInput.focus();
//         }, 2000);
//     }
    
//     function addMessage(text, type) {
//         const messageDiv = document.createElement('div');
//         messageDiv.className = `message ${type}-message`;
        
//         if (type === 'user') {
//             messageDiv.innerHTML = `
//                 <div class="message-content">
//                     <div class="message-text">
//                         <p>${escapeHtml(text)}</p>
//                     </div>
//                 </div>
//                 <div class="message-avatar user-avatar">
//                     <span>U</span>
//                 </div>
//             `;
//         } else {
//             messageDiv.innerHTML = `
//                 <div class="message-avatar">
//                     <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
//                         <rect width="24" height="24" rx="6" fill="#5B4FE9"/>
//                         <path d="M12 6L18 9V15L12 18L6 15V9L12 6Z" fill="white"/>
//                     </svg>
//                 </div>
//                 <div class="message-content">
//                     <div class="message-text">
//                         ${text}
//                     </div>
//                 </div>
//             `;
//         }
        
//         chatMessages.appendChild(messageDiv);
//         chatMessages.scrollTop = chatMessages.scrollHeight;
//     }
    
//     function addTypingIndicator() {
//         const typingDiv = document.createElement('div');
//         typingDiv.className = 'message assistant-message typing-indicator';
//         typingDiv.id = 'typingIndicator';
//         typingDiv.innerHTML = `
//             <div class="message-avatar">
//                 <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
//                     <rect width="24" height="24" rx="6" fill="#5B4FE9"/>
//                     <path d="M12 6L18 9V15L12 18L6 15V9L12 6Z" fill="white"/>
//                 </svg>
//             </div>
//             <div class="message-content">
//                 <div class="message-text">
//                     <p style="color: var(--text-tertiary);">Thinking...</p>
//                 </div>
//             </div>
//         `;
//         chatMessages.appendChild(typingDiv);
//         chatMessages.scrollTop = chatMessages.scrollHeight;
//     }
    
//     function removeTypingIndicator() {
//         const indicator = document.getElementById('typingIndicator');
//         if (indicator) indicator.remove();
//     }
    
//     // Generate dummy AI responses
//     function generateAIResponse(question) {
//         const responses = [
//             `<h4>Great Question!</h4>
//             <p>Based on your uploaded materials, here's what I found:</p>
//             <ul>
//                 <li>This topic appeared in the 2023 question paper</li>
//                 <li>It's typically worth 8-10 marks</li>
//                 <li>Focus on understanding the algorithm and time complexity</li>
//             </ul>
//             <div class="info-box">
//                 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
//                     <circle cx="12" cy="12" r="10"/>
//                     <line x1="12" y1="16" x2="12" y2="12"/>
//                     <line x1="12" y1="8" x2="12.01" y2="8"/>
//                 </svg>
//                 <p><strong>Tip:</strong> Practice drawing diagrams for this concept - they often appear in exams!</p>
//             </div>`,
            
//             `<h4>Let me break this down:</h4>
//             <h5>Definition</h5>
//             <p>This is a fundamental concept in data structures that appeared in multiple question papers.</p>
//             <h5>Key Points to Remember</h5>
//             <ul>
//                 <li>Time Complexity: O(n log n)</li>
//                 <li>Space Complexity: O(1)</li>
//                 <li>Use cases: When you need efficient sorting</li>
//             </ul>
//             <p>Would you like me to show you an example from the 2022 paper?</p>`,
            
//             `<p>I found this topic in your uploaded materials! Here's a structured explanation:</p>
//             <ol>
//                 <li><strong>Step 1:</strong> Initialize the data structure</li>
//                 <li><strong>Step 2:</strong> Process the input</li>
//                 <li><strong>Step 3:</strong> Return the result</li>
//             </ol>
//             <div class="info-box">
//                 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
//                     <circle cx="12" cy="12" r="10"/>
//                     <line x1="12" y1="16" x2="12" y2="12"/>
//                     <line x1="12" y1="8" x2="12.01" y2="8"/>
//                 </svg>
//                 <p><strong>From 2023 Paper:</strong> Question 5 asked about this exact concept for 12 marks.</p>
//             </div>`
//         ];
        
//         return responses[Math.floor(Math.random() * responses.length)];
//     }
    
//     // Escape HTML to prevent XSS
//     function escapeHtml(text) {
//         const div = document.createElement('div');
//         div.textContent = text;
//         return div.innerHTML;
//     }
    
//     // ==================== TOPIC TAGS ====================
//     const topicTags = document.querySelectorAll('.topic-tag');
//     topicTags.forEach(tag => {
//         tag.addEventListener('click', () => {
//             const topic = tag.textContent.replace(/\d+/g, '').trim();
//             chatInput.value = `Explain ${topic}`;
//             chatInput.focus();
//         });
//     });
    
//     // ==================== SIDEBAR TOGGLES ====================
//     const leftSidebar = document.getElementById('leftSidebar');
//     const rightSidebar = document.getElementById('rightSidebar');
//     const toggleLeftBtn = document.getElementById('toggleLeftSidebar');
    
//     if (toggleLeftBtn && leftSidebar) {
//         toggleLeftBtn.addEventListener('click', () => {
//             leftSidebar.classList.toggle('active');
//         });
//     }
    
//     // Mobile sidebar toggles
//     if (window.innerWidth <= 1024) {
//         if (leftSidebar) leftSidebar.classList.remove('active');
//         if (rightSidebar) rightSidebar.classList.remove('active');
//     }
    
//     // ==================== RESOURCE CARD CLICKS ====================
//     window.openFlashcards = function() {
//         showToast('Opening flashcards...', 'info');
//         // TODO: Implement flashcard modal/page
//         console.log('Opening flashcards');
//     };
    
//     window.openNotes = function() {
//         showToast('Opening generated notes...', 'info');
//         // TODO: Implement notes modal/page
//         console.log('Opening notes');
//     };
    
//     // ==================== SAVE SESSION ====================
//     const saveBtn = document.querySelector('[title="Save session"]');
//     if (saveBtn) {
//         saveBtn.addEventListener('click', () => {
//             showToast('Session saved successfully!', 'success');
//         });
//     }
    
//     // ==================== AUTO-SCROLL TO BOTTOM ====================
//     // Scroll to bottom on page load
//     if (chatMessages) {
//         chatMessages.scrollTop = chatMessages.scrollHeight;
//     }
    
//     console.log('Study session page loaded! 📚');
// });