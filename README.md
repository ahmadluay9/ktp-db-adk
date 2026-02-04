
#mcp-toolbox
```
http://34.101.127.72:5001
```

```
static/
├── chatbot.js                 
├── index.html             
└── question.json             
```

## index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DataDash - Enterprise Analytics</title>
    <style>
        :root {
            /* Core Colors */
            --bg-color: #f1f5f9;
            --card-bg: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --accent: #0f766e; 
            --accent-hover: #115e59; 
            --accent-light: #ccfbf1; 
            --border-color: #e2e8f0;
            --error: #ef4444;
            --success: #10b981;
        }

        body {
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
        }

        /* --- Utility Classes --- */
        .hidden { display: none !important; }
        .flex { display: flex; }
        .items-center { align-items: center; }
        .justify-center { justify-content: center; }
        .justify-between { justify-content: space-between; }
        .w-full { width: 100%; }
        
        /* --- Login & Loading Container (Centered Card) --- */
        .auth-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #0f172a; /* Dark background only for login */
            color: #f8fafc;
        }

        .auth-container {
            background-color: #1e293b;
            padding: 2.5rem;
            border-radius: 1rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            max-width: 400px;
            width: 90%;
            text-align: center;
            border: 1px solid #334155;
        }

        /* --- Login Specific Styles --- */
        .logo { font-size: 2rem; margin-bottom: 0.5rem; }
        .auth-container h1 { margin: 0 0 0.5rem 0; font-size: 1.5rem; font-weight: 600; color: white;}
        .auth-container p { color: #94a3b8; margin-bottom: 2rem; line-height: 1.5; }
        
        .oauth-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 0.75rem;
            background-color: white;
            color: #1f2937;
            border: 1px solid #e5e7eb;
            border-radius: 0.5rem;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.2s;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        .oauth-btn:hover { background-color: #f9fafb; }
        .oauth-btn img { width: 1.25rem; height: 1.25rem; margin-right: 0.75rem; }

        .divider {
            display: flex;
            align-items: center;
            margin: 1.5rem 0;
            color: #94a3b8;
            font-size: 0.875rem;
        }
        .divider::before, .divider::after {
            content: "";
            flex: 1;
            border-bottom: 1px solid #334155;
        }
        .divider::before { margin-right: 0.5rem; }
        .divider::after { margin-left: 0.5rem; }

        .debug-info {
            margin-top: 2rem;
            font-size: 0.7rem;
            color: #475569;
            text-align: left;
            border-top: 1px solid #334155;
            padding-top: 0.5rem;
        }

        /* --- Loading Spinner --- */
        .loading-spinner {
            border: 3px solid rgba(255,255,255,0.1);
            border-radius: 50%;
            border-top: 3px solid #3b82f6;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* --- Main Website Layout (Dashboard) --- */
        .main-layout {
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
        }

        /* Header / Navbar */
        header {
            background-color: white;
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 50;
        }

        .navbar {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 700;
            font-size: 1.5rem;
            color: var(--accent);
            text-decoration: none;
        }

        .nav-search {
            flex: 1;
            max-width: 500px;
            margin: 0 2rem;
            position: relative;
            display: none; /* Hidden on very small screens */
        }
        @media (min-width: 768px) { .nav-search { display: block; } }

        .search-input {
            width: 100%;
            padding: 0.75rem 1rem;
            border-radius: 999px;
            border: 1px solid var(--border-color);
            background-color: #f8fafc;
            outline: none;
            font-size: 0.95rem;
        }
        .search-input:focus { border-color: var(--accent); background: white; }

        .nav-actions {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .user-menu {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            cursor: pointer;
            padding: 0.25rem;
            border-radius: 99px;
            transition: background 0.2s;
        }
        .user-menu:hover { background-color: #f1f5f9; }

        .nav-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--accent);
        }

        .nav-username {
            font-weight: 500;
            font-size: 0.9rem;
            display: none;
        }
        @media (min-width: 640px) { .nav-username { display: block; } }

        .btn-logout {
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 0.85rem;
            cursor: pointer;
            text-decoration: underline;
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
            color: white;
            padding: 4rem 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        .hero h1 { font-size: 2.5rem; margin: 0 0 1rem 0; }
        .hero p { font-size: 1.1rem; opacity: 0.9; margin-bottom: 2rem; }
        
        .btn-cta {
            background-color: white;
            color: var(--accent);
            padding: 0.85rem 2rem;
            border-radius: 0.5rem;
            font-weight: 600;
            text-decoration: none;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            transition: transform 0.1s;
        }
        .btn-cta:active { transform: scale(0.98); }

        /* Dashboard Grid */
        .dashboard-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem 4rem 1.5rem;
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: var(--text-primary);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Services Grid */
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }

        .service-card {
            background: white;
            padding: 1.5rem;
            border-radius: 0.75rem;
            border: 1px solid var(--border-color);
            transition: transform 0.2s, box-shadow 0.2s;
            text-align: center;
            cursor: pointer;
        }
        .service-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
            border-color: var(--accent-light);
        }
        .service-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            display: block;
        }
        .service-title { font-weight: 600; margin-bottom: 0.5rem; color: var(--text-primary); }
        .service-desc { font-size: 0.85rem; color: var(--text-secondary); }

        /* Products Grid */
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1.5rem;
        }

        .product-card {
            background: white;
            border-radius: 0.75rem;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }
        .product-img {
            width: 100%;
            height: 160px;
            object-fit: cover;
            background-color: #f1f5f9;
        }
        .product-info { padding: 1rem; }
        .product-cat { font-size: 0.75rem; color: var(--accent); font-weight: 600; text-transform: uppercase; }
        .product-title { font-weight: 600; margin: 0.25rem 0 0.5rem 0; font-size: 1rem; }
        .product-price { font-weight: 700; color: var(--text-primary); }
        .btn-add {
            width: 100%;
            padding: 0.5rem;
            margin-top: 1rem;
            background-color: white;
            border: 1px solid var(--accent);
            color: var(--accent);
            border-radius: 0.375rem;
            cursor: pointer;
            font-weight: 500;
        }
        .btn-add:hover { background-color: var(--accent); color: white; }

        #error-message {
            color: var(--error);
            font-size: 0.9rem;
            margin-bottom: 1rem;
            padding: 0.5rem;
            background: rgba(239, 68, 68, 0.1);
            border-radius: 0.5rem;
            display: none;
        }

        /* CHATBOT WIDGET STYLES                        */
        
        #chatbot-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Floating Action Button */
        .chatbot-fab {
            position: relative;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(15, 118, 110, 0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chatbot-fab:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(15, 118, 110, 0.5);
        }

        .chatbot-fab:active {
            transform: scale(0.95);
        }

        .fab-icon {
            font-size: 28px;
            transition: all 0.3s;
        }

        .fab-icon-close {
            position: absolute;
            font-size: 24px;
            color: white;
            font-weight: bold;
        }

        .chatbot-badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background: #ef4444;
            color: white;
            font-size: 12px;
            font-weight: bold;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid white;
            animation: pulse-badge 2s infinite;
        }

        @keyframes pulse-badge {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        /* Chat Window */
        .chatbot-window {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 420px; /* Increased from 380px */
            height: 650px; /* Increased from 600px */
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transform: scale(0.9) translateY(20px);
            opacity: 0;
            pointer-events: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .chatbot-window.show {
            transform: scale(1) translateY(0);
            opacity: 1;
            pointer-events: all;
        }

        /* Header */
        .chatbot-header {
            background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
            color: white;
            padding: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .chatbot-header-content {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .chatbot-avatar {
            width: 40px;
            height: 40px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }

        .chatbot-title {
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 2px;
        }

        .chatbot-status {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            opacity: 0.9;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse-dot 2s infinite;
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .chatbot-minimize {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 24px;
            line-height: 1;
            transition: background 0.2s;
        }

        .chatbot-minimize:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        /* Messages Area */
        .chatbot-messages {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            background: #f8fafc;
            scroll-behavior: smooth;
        }

        .chatbot-messages::-webkit-scrollbar {
            width: 6px;
        }

        .chatbot-messages::-webkit-scrollbar-track {
            background: transparent;
        }

        .chatbot-messages::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 3px;
        }

        /* Message Bubbles */
        .message {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .message.user {
            flex-direction: row-reverse;
        }

        .message-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }

        .message.user .message-avatar {
            background: #64748b;
        }

        .message-content {
            max-width: 70%;
        }

        .message-bubble {
            background: white;
            padding: 10px 14px;
            border-radius: 16px;
            border-bottom-left-radius: 4px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            word-wrap: break-word;
        }

        .message.user .message-bubble {
            background: #0f766e;
            color: white;
            border-radius: 16px;
            border-bottom-right-radius: 4px;
        }

        .message-time {
            font-size: 11px;
            color: #94a3b8;
            margin-top: 4px;
            padding: 0 6px;
        }

        /* Markdown Content Styles*/
        .message-bubble p {
            margin: 0 0 8px 0;
        }
        .message-bubble p:last-child {
            margin-bottom: 0;
        }
        .message-bubble ul, .message-bubble ol {
            margin: 0 0 8px 0;
            padding-left: 20px;
        }
        .message-bubble strong {
            font-weight: 700;
        }
        .message-bubble pre {
            background-color: rgba(0, 0, 0, 0.1);
            padding: 10px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 8px 0;
            font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
            font-size: 0.85em;
        }
        .message-bubble code {
            font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
            background-color: rgba(0, 0, 0, 0.05);
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 0.9em;
        }
        /* Darker code blocks for user messages (which have dark background) */
        .message.user .message-bubble pre {
            background-color: rgba(0, 0, 0, 0.3);
            color: #e2e8f0;
        }
        .message.user .message-bubble code {
            background-color: rgba(0, 0, 0, 0.2);
        }
        .message-bubble a {
            color: inherit;
            text-decoration: underline;
        }

        /* Style for the Generated SQL block */
        .sql-debug-block {
            background: #e0f2fe; 
            padding: 8px; 
            border-radius: 4px; 
            font-family: monospace; 
            font-size: 11px; 
            color: #0c4a6e; 
            border: 1px solid #bae6fd;
            margin-top: 10px;
        }

        /* Quick Actions */
        .chatbot-quick-actions {
            padding: 12px 16px;
            background: white;
            border-top: 1px solid #e2e8f0;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            max-height: 200px;
            overflow-y: auto;
        }

        .quick-action-btn {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 10px 12px;
            border-radius: 8px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
            text-align: left;
            color: var(--text-primary);
        }

        .quick-action-btn:hover {
            border-color: var(--accent);
            background: var(--accent-light);
        }

        .quick-action-nav {
            background-color: #f1f5f9 !important;
            color: var(--accent) !important;
            font-weight: 600;
            border: 1px dashed var(--accent) !important;

            padding: 5px 10px !important;
            font-size: 0.85rem !important;
            width: fit-content !important;
            margin: 0 auto;

            grid-column: 1 / -1;
            justify-self: center;
            margin-top: 15px;
        }

        .quick-action-nav:hover {
            background-color: var(--accent-light) !important;
        }

        /* Input Area */
        .chatbot-input-area {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 16px;
            background: white;
            border-top: 1px solid #e2e8f0;
        }

        .chatbot-attach-btn {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            padding: 8px;
            border-radius: 8px;
            transition: background 0.2s;
        }

        .chatbot-attach-btn:hover {
            background: #f1f5f9;
        }

        .chatbot-input {
            flex: 1;
            border: none;
            outline: none;
            font-size: 14px;
            padding: 10px 12px;
            background: #f8fafc;
            border-radius: 20px;
        }

        .chatbot-input:focus {
            background: #f1f5f9;
        }

        .chatbot-send-btn {
            background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
            border: none;
            color: white;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
        }

        .chatbot-send-btn:hover {
            transform: scale(1.1);
        }

        .chatbot-send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Typing Indicator */
        .chatbot-typing {
            padding: 8px 16px;
            background: white;
            border-top: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .typing-indicator {
            display: flex;
            gap: 4px;
            padding: 8px 12px;
            background: #f1f5f9;
            border-radius: 16px;
        }

        .typing-indicator span {
            width: 6px;
            height: 6px;
            background: #64748b;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }

        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }

        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }

        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
                opacity: 0.7;
            }
            30% {
                transform: translateY(-10px);
                opacity: 1;
            }
        }

        .typing-text {
            font-size: 12px;
            color: #64748b;
        }

        /* Mobile Responsive */
        @media (max-width: 480px) {
            .chatbot-window {
                width: calc(100vw - 40px);
                height: calc(100vh - 100px);
                bottom: 80px;
                right: 20px;
            }

            #chatbot-container {
                right: 20px;
                bottom: 20px;
            }
        }

        /* Accessibility */
        .chatbot-fab:focus,
        .chatbot-send-btn:focus,
        .chatbot-minimize:focus,
        .quick-action-btn:focus {
            outline: 2px solid #0f766e;
            outline-offset: 2px;
        }

                /* Header Actions Container */
        .chatbot-header-actions {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .chatbot-header-btn {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }

        .chatbot-header-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }

        .chatbot-header-btn:active {
            transform: scale(0.95);
        }

        #chatbot-reset:hover {
            animation: spin-once 0.5s ease-out;
        }

        @keyframes spin-once {
            from { transform: rotate(0deg) scale(1.1); }
            to { transform: rotate(360deg) scale(1.1); }
        }

        /* Session Info Bar */
        .chatbot-session-bar {
            background: linear-gradient(135deg, #115e59 0%, #0f766e 100%);
            padding: 8px 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11px;
            color: rgba(255, 255, 255, 0.9);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .session-label {
            font-weight: 600;
            color: rgba(255, 255, 255, 0.7);
        }

        .session-id {
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            background: rgba(0, 0, 0, 0.2);
            padding: 3px 8px;
            border-radius: 4px;
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            flex: 1;
        }

        .session-copy-btn {
            background: rgba(255, 255, 255, 0.15);
            border: none;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
            flex-shrink: 0;
        }

        .session-copy-btn:hover {
            background: rgba(255, 255, 255, 0.25);
        }

        .session-copy-btn.copied {
            background: #10b981;
        }

        /* Reset Confirmation Modal */
        .chatbot-modal-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            border-radius: 16px;
            animation: fadeIn 0.2s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .chatbot-modal {
            background: white;
            padding: 24px;
            border-radius: 12px;
            max-width: 300px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            animation: slideUp 0.3s ease-out;
        }

        @keyframes slideUp {
            from { 
                opacity: 0;
                transform: translateY(20px);
            }
            to { 
                opacity: 1;
                transform: translateY(0);
            }
        }

        .chatbot-modal-icon {
            font-size: 48px;
            margin-bottom: 16px;
        }

        .chatbot-modal h3 {
            margin: 0 0 8px 0;
            color: var(--text-primary);
            font-size: 18px;
        }

        .chatbot-modal p {
            margin: 0 0 20px 0;
            color: var(--text-secondary);
            font-size: 14px;
            line-height: 1.5;
        }

        .chatbot-modal-actions {
            display: flex;
            gap: 12px;
            justify-content: center;
        }

        .chatbot-modal-btn {
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            border: none;
        }

        .chatbot-modal-btn.cancel {
            background: #f1f5f9;
            color: var(--text-primary);
        }

        .chatbot-modal-btn.cancel:hover {
            background: #e2e8f0;
        }

        .chatbot-modal-btn.confirm {
            background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
            color: white;
        }

        .chatbot-modal-btn.confirm:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(15, 118, 110, 0.3);
        }

        /* Toast Notification */
        .chatbot-toast {
            position: absolute;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            background: #1e293b;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            animation: toastIn 0.3s ease-out, toastOut 0.3s ease-in 2.7s forwards;
            z-index: 101;
        }

        @keyframes toastIn {
            from {
                opacity: 0;
                transform: translateX(-50%) translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }

        @keyframes toastOut {
            from {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
            to {
                opacity: 0;
                transform: translateX(-50%) translateY(20px);
            }
        }

        /* History Panel Styles */
        .chatbot-history-panel {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: white;
            z-index: 50;
            transform: translateX(-100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            border-radius: 16px;
        }

        .chatbot-history-panel.show {
            transform: translateX(0);
        }

        .history-panel-header {
            background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
            color: white;
            padding: 20px 16px;
            text-align: center;
        }

        .history-panel-header h3 {
            margin: 0 0 4px 0;
            font-size: 18px;
            font-weight: 600;
        }

        .history-panel-subtitle {
            font-size: 12px;
            opacity: 0.9;
        }

        .history-panel-list {
            flex: 1;
            overflow-y: auto;
            padding: 12px;
            background: #f8fafc;
        }

        /* History Item */
        .history-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: white;
            border-radius: 10px;
            margin-bottom: 8px;
            cursor: pointer;
            border: 1px solid #e2e8f0;
            transition: all 0.2s;
        }

        .history-item:hover {
            border-color: #0f766e;
            box-shadow: 0 2px 8px rgba(15, 118, 110, 0.1);
            transform: translateX(4px);
        }

        .history-item.active {
            background: linear-gradient(135deg, #ccfbf1 0%, #d1fae5 100%);
            border-color: #0f766e;
        }

        .history-item-icon {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #f1f5f9;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }

        .history-item.active .history-item-icon {
            background: #0f766e;
            color: white;
        }

        .history-item-content {
            flex: 1;
            min-width: 0;
        }

        .history-item-title {
            font-weight: 600;
            font-size: 14px;
            color: var(--text-primary);
            margin-bottom: 4px;
        }

        .history-item-meta {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .history-item-date {
            font-size: 12px;
            color: var(--text-secondary);
        }

        .history-item-id {
            font-size: 10px;
            color: #94a3b8;
            font-family: 'Monaco', 'Menlo', monospace;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .history-item-arrow {
            font-size: 20px;
            color: #94a3b8;
            font-weight: 300;
            transition: transform 0.2s;
        }

        .history-item:hover .history-item-arrow {
            transform: translateX(4px);
            color: #0f766e;
        }

        /* History Loading State */
        .history-loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            color: var(--text-secondary);
            gap: 12px;
        }

        .history-spinner {
            width: 32px;
            height: 32px;
            border: 3px solid #e2e8f0;
            border-top-color: #0f766e;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        /* History Empty State */
        .history-empty {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            text-align: center;
            color: var(--text-secondary);
        }

        .history-empty span {
            font-size: 48px;
            margin-bottom: 12px;
        }

        .history-empty p {
            margin: 0 0 4px 0;
            font-weight: 500;
            color: var(--text-primary);
        }

        .history-empty small {
            font-size: 12px;
        }

        /* Active History Button */
        #chatbot-history.active {
            background: rgba(255, 255, 255, 0.4);
        }

        /* Loading Session State */
        .loading-session {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: var(--text-secondary);
            gap: 16px;
        }

        .loading-spinner-chat {
            width: 40px;
            height: 40px;
            border: 3px solid #e2e8f0;
            border-top-color: #0f766e;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        .loading-session p {
            margin: 0;
            font-size: 14px;
        }

        /* Back button for history panel */
        .history-back-btn {
            position: absolute;
            top: 16px;
            left: 16px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }

        .history-back-btn:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        /* Scrollbar for history list */
        .history-panel-list::-webkit-scrollbar {
            width: 6px;
        }

        .history-panel-list::-webkit-scrollbar-track {
            background: transparent;
        }

        .history-panel-list::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 3px;
        }

        .history-panel-list::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
</head>
<body>


    <!-- AUTHENTICATION  -->

    <div id="login-view" class="auth-wrapper">
        <div class="auth-container">
            <div class="logo">📊</div>
            <h1>DataDash</h1>
            <p>Secure access to enterprise data and analytics.</p>

            <div id="error-message"></div>

            <button onclick="initiateOAuth()" class="oauth-btn" id="google-login-btn">
                <img src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google Logo">
                Sign in with Google
            </button>

            <div class="divider">or</div>

            <button class="oauth-btn" style="background-color: #24292F; color: white; border: none;">
                <img src="https://www.svgrepo.com/show/512317/github-142.svg" style="filter: invert(1);" alt="GitHub Logo">
                Sign in with GitHub
            </button>

            <div class="debug-info">
                Status Config: <span id="config-status">Loading...</span><br>
                Redirect URI: <span id="debug-redirect">...</span>
            </div>
        </div>
    </div>

    
    <!-- LOADING (Centered Dark Card) -->
    
    <div id="loading-view" class="auth-wrapper hidden">
        <div class="auth-container">
            <div class="loading-spinner"></div>
            <h2 style="color:white; margin:0;">Authenticating...</h2>
            <p style="margin-bottom:0;">Verifying your credentials.</p>
        </div>
    </div>

    
    <!-- DASHBOARD (Full Website Layout) -->
    
    <div id="dashboard-view" class="main-layout hidden">
        <!-- Navigation -->
        <header>
            <nav class="navbar">
                <a href="#" class="brand">
                    <span>📊</span> DataDash
                </a>
                
                <div class="nav-search">
                    <input type="text" class="search-input" placeholder="Search reports, users, or system logs...">
                </div>

                <div class="nav-actions">
                    <div class="user-menu">
                        <!-- IDs user-avatar, user-name, user-email preserved for JS -->
                        <img src="https://via.placeholder.com/36" alt="Profile" class="nav-avatar" id="user-avatar">
                        <div style="display:flex; flex-direction:column; align-items:flex-start; margin-right:0.5rem;">
                            <span class="nav-username" id="user-name">Loading...</span>
                            <span id="user-email" style="display:none;"></span> <!-- Hidden but kept for data -->
                        </div>
                    </div>
                    <button onclick="logout()" class="btn-logout">Sign Out</button>
                </div>
            </nav>
        </header>

        <!-- Hero Section -->
        <div class="hero">
            <h1>Data-Driven Decisions</h1>
            <p>Real-time analytics, inventory tracking, and sales reporting at your fingertips.</p>
            <div style="display:flex; gap:1rem; justify-content:center;">
                <button class="btn-cta">View Reports</button>
                <button class="btn-cta" style="background:transparent; border:1px solid white; color:white;">System Status</button>
            </div>
        </div>

        <!-- Main Content -->
        <div class="dashboard-container">
            
            <!-- Quick Services -->
            <div class="section-title">
                <span>Quick Actions</span>
            </div>
            <div class="services-grid">
                <div class="service-card">
                    <span class="service-icon">📈</span>
                    <div class="service-title">Sales Reports</div>
                    <div class="service-desc">Monthly performance overview</div>
                </div>
                <div class="service-card">
                    <span class="service-icon">📦</span>
                    <div class="service-title">Inventory</div>
                    <div class="service-desc">Check stock levels</div>
                </div>
                <div class="service-card">
                    <span class="service-icon">👥</span>
                    <div class="service-title">User Management</div>
                    <div class="service-desc">Manage access and roles</div>
                </div>
                <div class="service-card">
                    <span class="service-icon">⚙️</span>
                    <div class="service-title">System Settings</div>
                    <div class="service-desc">Configure integrations</div>
                </div>
            </div>

            <!-- Featured Products -->
            <div class="section-title">
                <span>Top Selling Products</span>
                <a href="#" style="color:var(--accent); text-decoration:none; font-size:0.9rem;">View All</a>
            </div>
            <div class="products-grid">
                <!-- Product 1 -->
                <div class="product-card">
                    <img src="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&q=80&w=400" class="product-img" alt="Laptop">
                    <div class="product-info">
                        <div class="product-cat">Electronics</div>
                        <div class="product-title">Pro Laptop 15"</div>
                        <div class="product-price">$1,299.00</div>
                        <button class="btn-add">View Details</button>
                    </div>
                </div>
                <!-- Product 2 -->
                <div class="product-card">
                    <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=400" class="product-img" alt="Headphones">
                    <div class="product-info">
                        <div class="product-cat">Audio</div>
                        <div class="product-title">Noise Cancelling Headphones</div>
                        <div class="product-price">$299.50</div>
                        <button class="btn-add">View Details</button>
                    </div>
                </div>
                <!-- Product 3 -->
                <div class="product-card">
                    <img src="https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&q=80&w=400" class="product-img" alt="Monitor">
                    <div class="product-info">
                        <div class="product-cat">Displays</div>
                        <div class="product-title">4K Ultra Monitor</div>
                        <div class="product-price">$450.00</div>
                        <button class="btn-add">View Details</button>
                    </div>
                </div>
                <!-- Product 4 -->
                <div class="product-card">
                    <img src="https://images.unsplash.com/photo-1587829741301-dc798b91a603?auto=format&fit=crop&q=80&w=400" class="product-img" alt="Keyboard">
                    <div class="product-info">
                        <div class="product-cat">Accessories</div>
                        <div class="product-title">Mechanical Keyboard</div>
                        <div class="product-price">$129.99</div>
                        <button class="btn-add">View Details</button>
                    </div>
                </div>
            </div>

            <!-- Debug Token -->
            <div class="profile-info" id="token-display" style="margin-top:4rem; opacity:0.5; font-size:0.75rem;">
                <!-- Token details will appear here -->
            </div>
        </div>
    </div>

    <!-- Load external script -->
    <script src="/static/script.js"></script>

    <!-- CHATBOT WIDGET  -->
    <div id="chatbot-container">
        <!-- Floating Action Button -->
        <button id="chatbot-toggle" class="chatbot-fab" aria-label="Open Chat">
            <span class="fab-icon fab-icon-chat">💬</span>
            <span class="fab-icon fab-icon-close" style="display:none;">✕</span>
            <span class="chatbot-badge" style="display:none;">1</span>
        </button>

        <!-- Chat Window -->
        <div id="chatbot-window" class="chatbot-window">
            <!-- Header -->
            <div class="chatbot-header">
                <div class="chatbot-header-content">
                    <div class="chatbot-avatar">🤖</div>
                    <div>
                        <div class="chatbot-title">Data Assistant</div>
                        <div class="chatbot-status">
                            <span class="status-dot"></span>
                            <span>Online • Ready to analyze</span>
                        </div>
                    </div>
                </div>
                <div class="chatbot-header-actions">
                    <button class="chatbot-header-btn" id="chatbot-history" aria-label="Chat History" title="View Chat History">
                        📜
                    </button>
                    <button class="chatbot-header-btn" id="chatbot-reset" aria-label="New Chat" title="Start New Chat">
                        🔄
                    </button>
                    <button class="chatbot-header-btn" id="chatbot-minimize" aria-label="Minimize" title="Minimize">
                        −
                    </button>
                </div>
            </div>

            <!-- Session Info Bar -->
            <div class="chatbot-session-bar" id="chatbot-session-bar">
                <span class="session-label">Session:</span>
                <span class="session-id" id="chatbot-session-id">Not started</span>
                <button class="session-copy-btn" id="session-copy-btn" title="Copy Session ID">📋</button>
            </div>

            <!-- History Panel (Slide-in from left) -->
            <div class="chatbot-history-panel" id="chatbot-history-panel">
                <div class="history-panel-header">
                    <!-- BACK BUTTON -->
                    <button class="history-back-btn" id="history-back-btn" aria-label="Close history">←</button>
                    <h3>💬 Chat History</h3>
                    <span class="history-panel-subtitle">Select a session to view</span>
                </div>
                <div class="history-panel-list" id="chatbot-history-list">
                    <!-- Sessions will be loaded here -->
                </div>
            </div>

            <!-- Messages Area -->
            <div class="chatbot-messages" id="chatbot-messages">
                <!-- Welcome message will be added by JS -->
            </div>

            <!-- Quick Actions -->
            <div class="chatbot-quick-actions" id="chatbot-quick-actions">
                <!-- Buttons will be injected here by JavaScript -->
            </div>

            <!-- Input Area -->
            <div class="chatbot-input-area">
                <button class="chatbot-attach-btn" aria-label="Attach file" title="Attach file">
                    📎
                </button>
                <input 
                    type="text" 
                    id="chatbot-input" 
                    class="chatbot-input" 
                    placeholder="Ask about sales, inventory..."
                    autocomplete="off"
                >
                <button id="chatbot-send" class="chatbot-send-btn" aria-label="Send message">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <path d="M2 10L18 2L12 18L10 11L2 10Z" fill="currentColor"/>
                    </svg>
                </button>
            </div>

            <!-- Typing Indicator -->
            <div class="chatbot-typing" id="chatbot-typing" style="display:none;">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <span class="typing-text">Assistant is typing...</span>
            </div>
        </div>
    </div>


    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dompurify/dist/purify.min.js"></script>
    <!-- Load chatbot script -->
    <script src="/static/chatbot.js"></script>
</body>
</html>
```

## chatbot.js
```javascript
// ============================================
// CHATBOT WIDGET - DataDash Agent
// ============================================

// --- CONFIGURATION ---
// !!!!!! CHANGE URL!!!!!!
const AGENT_API_URL =
  (window.location.hostname === 'localhost' ||
   window.location.hostname === '127.0.0.1')
    ? 'http://127.0.0.1:8000'
    : 'https://your-production-api-url.com';

// !!!!!! IMPORTANT !!!!!! APP NAME
const APP_NAME = "sales_a2a_agent";

class Chatbot {
    constructor() {
        this.isOpen = false;
        this.messageCount = 0;
        
        // Session State
        this.userId = null;
        this.sessionId = null;
        this.historyLoaded = false;
        this.sessionsList = [];
        this.isHistoryPanelOpen = false;

        // Question State
        this.allQuestions = [];
        this.showingAllQuestions = false; 
        
        // DOM Elements
        this.container = document.getElementById('chatbot-container');
        this.toggleBtn = document.getElementById('chatbot-toggle');
        this.window = document.getElementById('chatbot-window');
        this.messages = document.getElementById('chatbot-messages');
        this.input = document.getElementById('chatbot-input');
        this.sendBtn = document.getElementById('chatbot-send');
        this.minimizeBtn = document.getElementById('chatbot-minimize');
        this.resetBtn = document.getElementById('chatbot-reset');
        this.historyBtn = document.getElementById('chatbot-history');
        this.historyBackBtn = document.getElementById('history-back-btn');
        this.historyPanel = document.getElementById('chatbot-history-panel');
        this.historyList = document.getElementById('chatbot-history-list');
        this.quickActions = document.getElementById('chatbot-quick-actions'); 
        this.typingIndicator = document.getElementById('chatbot-typing');
        this.badge = this.toggleBtn.querySelector('.chatbot-badge');
        this.iconChat = this.toggleBtn.querySelector('.fab-icon-chat');
        this.iconClose = this.toggleBtn.querySelector('.fab-icon-close');
        this.sessionIdDisplay = document.getElementById('chatbot-session-id');
        this.sessionCopyBtn = document.getElementById('session-copy-btn');
        
        this.init();
    }

    async init() {
        if (!this.toggleBtn || !this.window) {
            console.error('Chatbot: Required elements not found');
            return;
        }

        // Load Questions from JSON
        await this.loadQuestions();

        // Event Listeners
        this.toggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggle();
        });
        
        this.minimizeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggle();
        });        

        if (this.resetBtn) {
            this.resetBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.showResetConfirmation();
            });
        }

        if (this.historyBtn) {
            this.historyBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggleHistoryPanel();
            });
        }

        if (this.historyBackBtn) {
            this.historyBackBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.closeHistoryPanel();
            });
        }

        if (this.sessionCopyBtn) {
            this.sessionCopyBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.copySessionId();
            });
        }
        
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Click outside history panel
        document.addEventListener('click', (e) => {
            if (this.isHistoryPanelOpen && 
                !this.historyPanel.contains(e.target) && 
                !this.historyBtn.contains(e.target)) {
                this.closeHistoryPanel();
            }
        });

        // Initial welcome
        this.showWelcomeMessage();
        this.updateSessionDisplay();

        // Initial Quick Actions Render
        this.refreshQuickActions();

        // Notification badge demo
        setTimeout(() => {
            if (!this.isOpen && this.messageCount === 0) {
                this.showNotification();
            }
        }, 3000);

        console.log(`Chatbot initialized. Connected to: ${AGENT_API_URL}`);
    }

    // Question Management
    async loadQuestions() {
        try {
            const response = await fetch('/static/questions.json');
            if (!response.ok) throw new Error("Failed to load questions");
            this.allQuestions = await response.json();
        } catch (error) {
            console.error("Error loading questions.json:", error);
            // Fallback questions if file fails
            this.allQuestions = [
                "halo",
                "Top performing products"
            ];
        }
    }

    refreshQuickActions() {
        if (!this.quickActions || this.allQuestions.length === 0) return;

        this.quickActions.innerHTML = '';

        if (!this.showingAllQuestions) {
            
            // Shuffle and pick 2
            const shuffled = [...this.allQuestions].sort(() => 0.5 - Math.random());
            const selected = shuffled.slice(0, 2);

            // Render Questions
            selected.forEach(q => this.createQuestionBtn(q));

            // Render "View All" Button
            const moreBtn = document.createElement('button');
            moreBtn.className = 'quick-action-btn quick-action-nav';
            moreBtn.innerHTML = 'Sample Questions ⇲';
            moreBtn.onclick = (e) => {
                e.preventDefault();
                this.showingAllQuestions = true;
                this.refreshQuickActions();
            };
            this.quickActions.appendChild(moreBtn);

        } else {
            // Render All Questions
            const sortedQuestions = [...this.allQuestions].sort();
            sortedQuestions.forEach(q => this.createQuestionBtn(q));

            // Render "Back" Button
            const backBtn = document.createElement('button');
            backBtn.className = 'quick-action-btn quick-action-nav';
            backBtn.innerHTML = '← Back';
            
            backBtn.onclick = (e) => {
                e.preventDefault();
                this.showingAllQuestions = false;
                this.refreshQuickActions();
            };
            this.quickActions.appendChild(backBtn);
        }

        // Ensure it's visible
        this.quickActions.style.display = 'grid';
    }

    // Question Button
    createQuestionBtn(text) {
        const btn = document.createElement('button');
        btn.className = 'quick-action-btn';
        btn.textContent = text;
        
        // Populate input
        btn.addEventListener('click', () => {
            this.input.value = text;
            this.input.focus();
            // Optional: Reset view to default after selection?
            // this.showingAllQuestions = false; 
            // this.refreshQuickActions();
        });
        
        this.quickActions.appendChild(btn);
    }

    // Force new session (called on fresh login)
    async forceNewSession() {
        const email = this.getUserEmail();
        if (!email) {
            console.log('forceNewSession: No email yet, will create session when user opens chat');
            this.pendingNewSession = true;
            return;
        }

        this.userId = email;
        this.sessionId = `${this.userId}-${Math.floor(Date.now() / 1000)}`;
        this.historyLoaded = true;
        this.messageCount = 0;

        this.messages.innerHTML = '';
        this.showWelcomeMessage();

        // Show and Refresh Quick Actions
        this.refreshQuickActions();

        this.updateSessionDisplay();
        await this.initBackendSession();
        console.log('New session forced on login:', this.sessionId);
    }

    clearSessionData() {
        this.userId = null;
        this.sessionId = null;
        this.historyLoaded = false;
        this.messageCount = 0;
        this.sessionsList = [];
        this.pendingNewSession = false;

        this.messages.innerHTML = '';
        this.showWelcomeMessage();
        
        // Reset Quick Actions
        this.refreshQuickActions();

        this.updateSessionDisplay();
        
        if (this.isOpen) {
            this.toggle();
        }
        console.log('Chatbot session data cleared');
    }

    async toggleHistoryPanel() {
        if (this.isHistoryPanelOpen) {
            this.closeHistoryPanel();
        } else {
            await this.openHistoryPanel();
        }
    }

    async openHistoryPanel() {
        const email = this.getUserEmail();
        if (!email) {
            this.showToast('⚠️ Please sign in first');
            return;
        }

        this.userId = email;
        this.isHistoryPanelOpen = true;
        this.historyPanel.classList.add('show');
        this.historyBtn.classList.add('active');

        this.historyList.innerHTML = `
            <div class="history-loading">
                <div class="history-spinner"></div>
                <span>Loading sessions...</span>
            </div>
        `;

        try {
            await this.fetchSessionsList();
            this.renderSessionsList();
        } catch (error) {
            console.error('Error fetching sessions:', error);
            this.historyList.innerHTML = `
                <div class="history-empty">
                    <span>⚠️</span>
                    <p>Failed to load sessions</p>
                </div>
            `;
        }
    }

    closeHistoryPanel() {
        this.isHistoryPanelOpen = false;
        this.historyPanel.classList.remove('show');
        this.historyBtn.classList.remove('active');
    }

    async fetchSessionsList() {
        const url = `/api/sessions?user_id=${encodeURIComponent(this.userId)}&app_name=${APP_NAME}`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch sessions: ${response.status}`);
        }

        const sessions = await response.json();
        
        this.sessionsList = sessions.sort((a, b) => {
            const timeA = this.extractTimestamp(a.id);
            const timeB = this.extractTimestamp(b.id);
            return timeB - timeA;
        });

        return this.sessionsList;
    }

    extractTimestamp(sessionId) {
        const parts = sessionId.split('-');
        const timestamp = parseInt(parts[parts.length - 1]) || 0;
        return timestamp;
    }

    formatSessionDate(sessionId) {
        const timestamp = this.extractTimestamp(sessionId);
        if (!timestamp) return 'Unknown date';
        
        const date = new Date(timestamp * 1000);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)} min ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`;
        if (diff < 604800000) return `${Math.floor(diff / 86400000)} days ago`;
        
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
        });
    }

    renderSessionsList() {
        if (!this.sessionsList || this.sessionsList.length === 0) {
            this.historyList.innerHTML = `
                <div class="history-empty">
                    <span>💬</span>
                    <p>No previous sessions</p>
                    <small>Start chatting to create your first session</small>
                </div>
            `;
            return;
        }

        let html = '';
        this.sessionsList.forEach((session, index) => {
            const isActive = session.id === this.sessionId;
            const formattedDate = this.formatSessionDate(session.id);
            const truncatedId = session.id.length > 25 
                ? session.id.substring(0, 12) + '...' + session.id.slice(-8)
                : session.id;

            html += `
                <div class="history-item ${isActive ? 'active' : ''}" 
                     data-session-id="${session.id}"
                     onclick="chatbot.loadSession('${session.id}')">
                    <div class="history-item-icon">
                        ${isActive ? '✓' : '💬'}
                    </div>
                    <div class="history-item-content">
                        <div class="history-item-title">
                            ${isActive ? 'Current Session' : `Session ${index + 1}`}
                        </div>
                        <div class="history-item-meta">
                            <span class="history-item-date">${formattedDate}</span>
                            <span class="history-item-id" title="${session.id}">${truncatedId}</span>
                        </div>
                    </div>
                    <div class="history-item-arrow">›</div>
                </div>
            `;
        });

        this.historyList.innerHTML = html;
    }

    async loadSession(sessionId) {
        if (sessionId === this.sessionId) {
            this.closeHistoryPanel();
            this.showToast('✓ Already viewing this session');
            return;
        }

        const email = this.getUserEmail();
        if (!email) {
            this.showToast('⚠️ Please sign in first');
            return;
        }

        this.userId = email;
        this.closeHistoryPanel();

        this.messages.innerHTML = `
            <div class="loading-session">
                <div class="loading-spinner-chat"></div>
                <p>Loading session...</p>
            </div>
        `;

        try {
            const url = `/api/sessions/${encodeURIComponent(sessionId)}?user_id=${encodeURIComponent(this.userId)}&app_name=${APP_NAME}`;
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`Failed to load session: ${response.status}`);
            }

            const sessionData = await response.json();

            this.sessionId = sessionId;
            this.historyLoaded = true;
            this.updateSessionDisplay();

            this.messages.innerHTML = '';
            if (sessionData.events && sessionData.events.length > 0) {
                this.renderHistory(sessionData.events);
                // Even if history exists, we show fresh quick actions at the bottom
                this.refreshQuickActions();
            } else {
                this.showWelcomeMessage();
                this.refreshQuickActions();
            }

            this.showToast('✓ Session loaded');
            console.log('Loaded session:', sessionId);

        } catch (error) {
            console.error('Error loading session:', error);
            this.showWelcomeMessage();
            this.showToast('⚠️ Failed to load session');
        }
    }

    updateSessionDisplay() {
        if (this.sessionIdDisplay) {
            if (this.sessionId) {
                const displayId = this.sessionId.length > 30 
                    ? this.sessionId.substring(0, 15) + '...' + this.sessionId.slice(-10)
                    : this.sessionId;
                this.sessionIdDisplay.textContent = displayId;
                this.sessionIdDisplay.title = this.sessionId;
            } else {
                this.sessionIdDisplay.textContent = 'Not started';
                this.sessionIdDisplay.title = '';
            }
        }
    }

    copySessionId() {
        if (!this.sessionId) {
            this.showToast('⚠️ No active session');
            return;
        }

        navigator.clipboard.writeText(this.sessionId).then(() => {
            if (this.sessionCopyBtn) {
                this.sessionCopyBtn.textContent = '✓';
                this.sessionCopyBtn.classList.add('copied');
                setTimeout(() => {
                    this.sessionCopyBtn.textContent = '📋';
                    this.sessionCopyBtn.classList.remove('copied');
                }, 2000);
            }
            this.showToast('✓ Session ID copied!');
        }).catch(() => {
            this.showToast('⚠️ Failed to copy');
        });
    }

    showResetConfirmation() {
        const overlay = document.createElement('div');
        overlay.className = 'chatbot-modal-overlay';
        overlay.innerHTML = `
            <div class="chatbot-modal">
                <div class="chatbot-modal-icon">🔄</div>
                <h3>Start New Chat?</h3>
                <p>This will create a new session. Your current conversation history will be saved but won't appear in the new session.</p>
                <div class="chatbot-modal-actions">
                    <button class="chatbot-modal-btn cancel">Cancel</button>
                    <button class="chatbot-modal-btn confirm">New Chat</button>
                </div>
            </div>
        `;

        this.window.appendChild(overlay);

        const cancelBtn = overlay.querySelector('.cancel');
        const confirmBtn = overlay.querySelector('.confirm');

        cancelBtn.addEventListener('click', () => {
            overlay.remove();
        });

        confirmBtn.addEventListener('click', () => {
            overlay.remove();
            this.resetSession();
        });

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.remove();
            }
        });
    }

    async resetSession() {
        const email = this.getUserEmail();
        if (!email) {
            this.showToast('⚠️ Please sign in first');
            return;
        }

        this.userId = email;
        this.sessionId = `${this.userId}-${Math.floor(Date.now() / 1000)}`;
        this.historyLoaded = false;
        this.messageCount = 0;

        this.messages.innerHTML = '';
        this.showWelcomeMessage();

        // Refresh buttons on reset
        this.refreshQuickActions();

        this.updateSessionDisplay();

        await this.initBackendSession();

        this.showToast('✓ New chat session started!');
        console.log('New session created:', this.sessionId);
    }

    showToast(message) {
        const existingToast = this.window.querySelector('.chatbot-toast');
        if (existingToast) {
            existingToast.remove();
        }

        const toast = document.createElement('div');
        toast.className = 'chatbot-toast';
        toast.textContent = message;
        this.window.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    getUserEmail() {
        const emailEl = document.getElementById('user-email');
        return (emailEl && emailEl.textContent !== '...' && emailEl.textContent !== 'Loading...') ? emailEl.textContent : null;
    }

    async loadHistory() {
        // Check if we should create a new session instead of loading history
        if (this.pendingNewSession) {
            this.pendingNewSession = false;
            await this.forceNewSession();
            return;
        }

        if (this.historyLoaded) return;
        
        const email = this.getUserEmail();
        if (!email) return;

        this.userId = email;
        
        try {
            const listRes = await fetch(`/api/sessions?user_id=${encodeURIComponent(this.userId)}&app_name=${APP_NAME}`);
            if (!listRes.ok) throw new Error("Failed to list sessions");
            
            const sessions = await listRes.json();
            
            if (sessions && sessions.length > 0) {
                sessions.sort((a, b) => {
                    const timeA = parseInt(a.id.split('-').pop()) || 0;
                    const timeB = parseInt(b.id.split('-').pop()) || 0;
                    return timeB - timeA;
                });

                const lastSession = sessions[0];
                this.sessionId = lastSession.id;
                this.updateSessionDisplay();
                console.log("Restoring session:", this.sessionId);

                const detailRes = await fetch(`/api/sessions/${this.sessionId}?user_id=${encodeURIComponent(this.userId)}&app_name=${APP_NAME}`);
                if (detailRes.ok) {
                    const sessionData = await detailRes.json();
                    this.renderHistory(sessionData.events);
                    this.historyLoaded = true;
                    
                    // Show actions even if history loaded
                    this.refreshQuickActions();
                    return;
                }
            }
        } catch (e) {
            console.error("Error loading history:", e);
        }

        if (!this.sessionId) {
            this.sessionId = `${this.userId}-${Math.floor(Date.now() / 1000)}`;
            this.updateSessionDisplay();
            await this.initBackendSession();
            // Show actions for new session
            this.refreshQuickActions();
        }
    }

    async initBackendSession() {
        try {
            const url = `${AGENT_API_URL}/apps/${APP_NAME}/users/${this.userId}/sessions/${this.sessionId}`;
            const payload = {
                userId: this.userId,
            };
            await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            console.log('Backend session initialized:', this.sessionId);
        } catch (e) {
            console.error("Backend session init failed", e);
        }
    }

    renderHistory(events) {
        if (!events || events.length === 0) return;
        
        this.messages.innerHTML = '';
        this.messageCount = events.length;

        events.forEach(event => {
            let text = "";
            if (event.parts) {
                event.parts.forEach(p => text += p.text);
            }
            if (!text) return;

            const author = (event.author || "").toLowerCase();
            const role = (event.role || "").toLowerCase();
            
            let uiSender = 'bot';
            if (author === 'user' || (role === 'user' && author !== 'rootagent')) {
                uiSender = 'user';
            }

            this.addMessage(text, uiSender, false);
        });
        
        this.scrollToBottom();
    }

    // Messaging Logic

    async sendMessage(messageText = null) {
        const text = messageText || this.input.value.trim();
        if (!text) return;

        const email = this.getUserEmail();
        if (!email) {
            this.addMessage("Please sign in to chat.", 'bot');
            return;
        }

        if (!this.sessionId) {
            await this.loadHistory();
        }

        // Hide actions while waiting for response
        if (this.quickActions) this.quickActions.style.display = 'none';
        
        this.addMessage(text, 'user');
        this.input.value = '';
        this.showTyping();

        try {
            const url = `${AGENT_API_URL}/run`;
            const payload = {
                appName: APP_NAME,
                userId: this.userId,
                sessionId: this.sessionId,
                newMessage: {
                    role: "user",
                    parts: [{ text: text }]
                }
            };

            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error(`API Error: ${response.status}`);
            
            const data = await response.json();
            this.hideTyping();
            this.handleAgentResponse(data);

        } catch (e) {
            console.error(e);
            this.hideTyping();
            this.addMessage("Sorry, I encountered a connection error.", 'bot');
            // Re-show actions on error
            if (this.quickActions) this.quickActions.style.display = 'grid';
        }
    }

    handleAgentResponse(data) {
        let finalText = "";
        let foundResponse = false;
        let generatedSql = null;

        if (Array.isArray(data)) {
            for (let i = data.length - 1; i >= 0; i--) {
                const item = data[i];
                const role = item.role || (item.content && item.content.role);
                
                if (role === 'model') {
                    const content = item.content || {};
                    const parts = content.parts || [];
                    for (const part of parts) {
                        if (part.text) {
                            finalText = part.text;
                            foundResponse = true;
                            break;
                        }
                    }
                }
                if (foundResponse) break;
            }

            for (const item of data) {
                if (item.actions && item.actions.stateDelta && item.actions.stateDelta.generated_sql) {
                    generatedSql = item.actions.stateDelta.generated_sql;
                }
            }
        }

        if (!finalText && !foundResponse) {
            finalText = "I processed your request but didn't generate a text response (Check logs).";
        }

        if (generatedSql) {
            finalText += `<br><br><div style="background:#e0f2fe; padding:8px; border-radius:4px; font-family:monospace; font-size:11px; color:#0c4a6e; border:1px solid #bae6fd;"><strong>Generated SQL:</strong><br>${generatedSql}</div>`;
        }

        this.addMessage(finalText, 'bot');
        
        // ROTATE AND SHOW BUTTONS AFTER RESPONSE
        this.refreshQuickActions();
    }

    // UI Helpers

    addMessage(text, sender, autoScroll = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        let avatarHTML;
        if (sender === 'bot') {
            avatarHTML = '<div class="message-avatar">🤖</div>';
        } else {
            const userAvatarEl = document.getElementById('user-avatar');
            const hasProfilePic = userAvatarEl && userAvatarEl.src && !userAvatarEl.src.includes('placeholder');
            
            if (hasProfilePic) {
                avatarHTML = `<img src="${userAvatarEl.src}" class="message-avatar" style="object-fit: cover;" alt="User">`;
            } else {
                avatarHTML = '<div class="message-avatar">👤</div>';
            }
        }
        
        let formattedText = text.replace(/\n/g, '<br>');
        
        marked.setOptions({ breaks: true });
        let rawHtml = marked.parse(text);
        let safeHtml = DOMPurify.sanitize(rawHtml);

        messageDiv.innerHTML = `
            ${avatarHTML}
            <div class="message-content">
                <div class="message-bubble">${safeHtml}</div>
                <div class="message-time">${this.getCurrentTime()}</div>
            </div>
        `;
        
        this.messages.appendChild(messageDiv);
        this.messageCount++;
        if (autoScroll) this.scrollToBottom();
    }

    showWelcomeMessage() {
        const welcomeMsg = `
            <div class="message bot">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div class="message-bubble">
                        👋 Welcome to DataDash!
                        <br><br>
                        I am here to answer your questions to the best of my knowledge.
                    </div>
                    <div class="message-time">${this.getCurrentTime()}</div>
                </div>
            </div>
        `;
        this.messages.innerHTML = welcomeMsg;
    }

    toggle() {
        this.isOpen = !this.isOpen;
        if (this.isOpen) {
            if (this.pendingNewSession && this.getUserEmail()) {
                this.pendingNewSession = false;
                this.forceNewSession();
            } else if (!this.historyLoaded) {
                this.loadHistory();
            }
            this.window.classList.add('show');
            this.iconChat.style.display = 'none';
            this.iconClose.style.display = 'flex';
            this.input.focus();
            this.hideNotification();
        } else {
            this.window.classList.remove('show');
            this.iconChat.style.display = 'flex';
            this.iconClose.style.display = 'none';
        }
    }

    showNotification() {
        if (this.badge) {
            this.badge.textContent = '1';
            this.badge.style.display = 'flex';
        }
    }

    hideNotification() {
        if (this.badge) this.badge.style.display = 'none';
    }

    showTyping() {
        if (this.typingIndicator) {
            this.typingIndicator.style.display = 'flex';
            this.scrollToBottom();
        }
    }

    hideTyping() {
        if (this.typingIndicator) this.typingIndicator.style.display = 'none';
    }

    scrollToBottom() {
        setTimeout(() => {
            if (this.messages) this.messages.scrollTop = this.messages.scrollHeight;
        }, 100);
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString('en-US', { 
            hour: 'numeric', minute: '2-digit', hour12: true 
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new Chatbot();
});
```

## questions.json
```json
[
    "tampilkan statistik jumlah penduduk berdasarkan status perkawinan.",
    "informasi mengenai NIK 3171016804084130.",
    "Cari informasi penduduk dengan nama Hani Hidayat.",
    "List penduduk yang di tinggal di kecamatan gubeng.",
    "Berapa jumlah penduduk per kecamatan",
    "statistik sebaran penduduk berdasarkan Agama",
    "List 10 pekerjaan penduduk terbanyak"
]
```