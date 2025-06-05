// 🚀 Orion CEO Dashboard - Enhanced JavaScript
// Comprehensive dashboard functionality for seamless user experience

class OrionDashboard {
    constructor() {
        this.currentModule = 'overview';
        this.refreshInterval = 30000; // 30 seconds
        this.isAutoRefresh = true;
        this.apiBase = '/api';
        this.initializeDashboard();
    }

    initializeDashboard() {
        console.log('🚀 Initializing Orion CEO Dashboard...');
        this.setupEventListeners();
        this.startAutoRefresh();
        this.loadModuleData(this.currentModule);
        this.setupNavigationHighlight();
    }

    setupEventListeners() {
        // Navigation buttons
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleNavigation(e));
        });

        // Refresh controls
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.manualRefresh());
        }

        // Auto-refresh toggle
        const autoRefreshToggle = document.getElementById('autoRefreshToggle');
        if (autoRefreshToggle) {
            autoRefreshToggle.addEventListener('change', (e) => {
                this.isAutoRefresh = e.target.checked;
                if (this.isAutoRefresh) {
                    this.startAutoRefresh();
                } else {
                    this.stopAutoRefresh();
                }
            });
        }

        // Window resize handler
        window.addEventListener('resize', () => this.handleResize());
    }

    handleNavigation(event) {
        event.preventDefault();
        const targetModule = event.target.getAttribute('data-module');
        
        if (targetModule && targetModule !== this.currentModule) {
            this.switchModule(targetModule);
        }
    }

    switchModule(module) {
        console.log(`🔄 Switching to module: ${module}`);
        
        // Update navigation highlight
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        const activeBtn = document.querySelector(`[data-module="${module}"]`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }

        // Hide all modules
        document.querySelectorAll('.module-content').forEach(content => {
            content.style.display = 'none';
        });

        // Show target module
        const targetContent = document.getElementById(`${module}Module`);
        if (targetContent) {
            targetContent.style.display = 'block';
            targetContent.classList.add('fade-in');
        }

        this.currentModule = module;
        this.loadModuleData(module);
        this.updateModuleBreadcrumb(module);
    }

    async loadModuleData(module) {
        try {
            const response = await fetch(`${this.apiBase}/${module}`);
            const data = await response.json();
            
            this.updateModuleContent(module, data);
            this.updateLastRefreshTime();
            
        } catch (error) {
            console.error(`❌ Error loading ${module} data:`, error);
            this.showErrorMessage(module, error.message);
        }
    }

    updateModuleContent(module, data) {
        switch (module) {
            case 'overview':
                this.updateOverviewModule(data);
                break;
            case 'trading':
                this.updateTradingModule(data);
                break;
            case 'research':
                this.updateResearchModule(data);
                break;
            case 'knowledge':
                this.updateKnowledgeModule(data);
                break;
            case 'risk':
                this.updateRiskModule(data);
                break;
            case 'actions':
                this.updateActionsModule(data);
                break;
        }
    }

    updateOverviewModule(data) {
        // Update portfolio values
        this.updateElement('totalPortfolio', this.formatCurrency(data.portfolio?.total || 10000));
        this.updateElement('dailyPnL', this.formatCurrency(data.portfolio?.daily_pnl || 0));
        this.updateElement('totalPnL', this.formatCurrency(data.portfolio?.total_pnl || 0));
        this.updateElement('winRate', `${data.portfolio?.win_rate || 0}%`);

        // Update system health
        this.updateElement('systemHealth', `${data.system?.health_score || 0}/100`);
        this.updateElement('activeAgents', data.system?.active_agents || 0);
        this.updateElement('systemUptime', `${data.system?.uptime || 100}%`);
        
        // Update market overview
        this.updateElement('btcPrice', this.formatCurrency(data.market?.btc_price || 0));
        this.updateElement('ethPrice', this.formatCurrency(data.market?.eth_price || 0));
        this.updateElement('fearGreed', data.market?.fear_greed || 50);
    }

    updateTradingModule(data) {
        // Update trading performance
        this.updateElement('tradingROI', `${data.performance?.roi || 0}%`);
        this.updateElement('totalTrades', data.performance?.total_trades || 0);
        this.updateElement('activeTrades', data.performance?.active_trades || 0);
        this.updateElement('sharpeRatio', data.performance?.sharpe_ratio || 0);

        // Update strategy performance
        if (data.strategies) {
            this.updateStrategyTable(data.strategies);
        }
    }

    updateResearchModule(data) {
        this.updateElement('researchSources', data.sources?.active || 0);
        this.updateElement('newsAnalyzed', data.analysis?.news_count || 0);
        this.updateElement('sentimentScore', data.analysis?.sentiment_score || 0);
        this.updateElement('signalStrength', data.analysis?.signal_strength || 0);
    }

    updateKnowledgeModule(data) {
        this.updateElement('knowledgeItems', data.knowledge?.total_items || 0);
        this.updateElement('confidenceScore', `${data.knowledge?.avg_confidence || 0}%`);
        this.updateElement('processingQueue', data.knowledge?.queue_size || 0);
        this.updateElement('learningRate', data.knowledge?.learning_rate || 0);
    }

    updateRiskModule(data) {
        this.updateElement('riskScore', `${data.risk?.current_score || 0}/100`);
        this.updateElement('maxDrawdown', `${data.risk?.max_drawdown || 0}%`);
        this.updateElement('positionSizing', `${data.risk?.position_size || 2}%`);
        this.updateElement('portfolioVaR', this.formatCurrency(data.risk?.var || 0));

        // Update risk status color
        const riskElement = document.getElementById('riskScore');
        if (riskElement) {
            const score = data.risk?.current_score || 0;
            riskElement.className = `risk-${this.getRiskLevel(score)}`;
        }
    }

    updateActionsModule(data) {
        this.updateElement('totalActions', data.actions?.total || 35);
        this.updateElement('pendingActions', data.actions?.pending || 0);
        this.updateElement('completedToday', data.actions?.completed_today || 0);
        this.updateElement('automatedActions', data.actions?.automated || 0);

        // Update action list
        if (data.action_list) {
            this.updateActionList(data.action_list);
        }
    }

    updateStrategyTable(strategies) {
        const tableBody = document.querySelector('#strategyTable tbody');
        if (!tableBody) return;

        tableBody.innerHTML = '';
        strategies.forEach(strategy => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${strategy.name}</td>
                <td>$${strategy.allocation?.toLocaleString() || '10,000'}</td>
                <td class="return-${strategy.return_percent >= 0 ? 'positive' : 'negative'}">
                    ${strategy.return_percent?.toFixed(2) || '0.00'}%
                </td>
                <td>${strategy.trades || 0}</td>
                <td>${strategy.win_rate || 0}%</td>
                <td class="status-${strategy.status?.toLowerCase() || 'active'}">${strategy.status || 'Active'}</td>
            `;
            tableBody.appendChild(row);
        });
    }

    updateActionList(actions) {
        const actionsList = document.getElementById('actionsList');
        if (!actionsList) return;

        actionsList.innerHTML = '';
        actions.slice(0, 10).forEach(action => {
            const item = document.createElement('div');
            item.className = `action-item priority-${action.priority?.toLowerCase() || 'medium'}`;
            item.innerHTML = `
                <div class="action-header">
                    <span class="action-title">${action.title}</span>
                    <span class="action-priority">${action.priority || 'Medium'}</span>
                </div>
                <div class="action-description">${action.description}</div>
                <div class="action-meta">
                    <span>Module: ${action.module}</span>
                    <span>Status: ${action.status}</span>
                </div>
            `;
            actionsList.appendChild(item);
        });
    }

    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
            element.classList.add('updated');
            setTimeout(() => element.classList.remove('updated'), 1000);
        }
    }

    formatCurrency(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    }

    getRiskLevel(score) {
        if (score <= 30) return 'low';
        if (score <= 60) return 'medium';
        return 'high';
    }

    startAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        
        this.refreshTimer = setInterval(() => {
            if (this.isAutoRefresh) {
                this.loadModuleData(this.currentModule);
                this.updateTickerData();
            }
        }, this.refreshInterval);
    }

    stopAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
    }

    manualRefresh() {
        console.log('🔄 Manual refresh triggered');
        this.loadModuleData(this.currentModule);
        this.showRefreshNotification();
    }

    updateTickerData() {
        // Update scrolling news ticker
        fetch(`${this.apiBase}/news/ticker`)
            .then(response => response.json())
            .then(data => {
                const ticker = document.querySelector('.news-ticker');
                if (ticker && data.news) {
                    ticker.innerHTML = data.news.map(item => 
                        `<span class="ticker-item">${item.title}</span>`
                    ).join('');
                }
            })
            .catch(error => console.error('❌ Error updating ticker:', error));
    }

    updateLastRefreshTime() {
        const timeElement = document.getElementById('lastRefresh');
        if (timeElement) {
            const now = new Date();
            timeElement.textContent = now.toLocaleTimeString();
        }
    }

    setupNavigationHighlight() {
        const firstBtn = document.querySelector('[data-module="overview"]');
        if (firstBtn) {
            firstBtn.classList.add('active');
        }
    }

    updateModuleBreadcrumb(module) {
        const breadcrumb = document.getElementById('moduleBreadcrumb');
        if (breadcrumb) {
            const moduleNames = {
                overview: 'Portfolio Overview',
                trading: 'Trading Performance',
                research: 'Research Center',
                knowledge: 'Knowledge Center',
                risk: 'Risk Management',
                actions: 'Action Center'
            };
            breadcrumb.textContent = moduleNames[module] || 'Dashboard';
        }
    }

    showErrorMessage(module, message) {
        const moduleContent = document.getElementById(`${module}Module`);
        if (moduleContent) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.innerHTML = `
                <div class="error-icon">⚠️</div>
                <div class="error-text">
                    <strong>Error loading ${module} data</strong><br>
                    ${message}
                </div>
            `;
            moduleContent.insertBefore(errorDiv, moduleContent.firstChild);
            
            setTimeout(() => errorDiv.remove(), 5000);
        }
    }

    showRefreshNotification() {
        const notification = document.createElement('div');
        notification.className = 'refresh-notification';
        notification.innerHTML = '✅ Dashboard refreshed';
        document.body.appendChild(notification);
        
        setTimeout(() => notification.remove(), 2000);
    }

    handleResize() {
        // Handle responsive behavior
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        
        if (window.innerWidth <= 768) {
            sidebar?.classList.add('mobile');
            mainContent?.classList.add('mobile');
        } else {
            sidebar?.classList.remove('mobile');
            mainContent?.classList.remove('mobile');
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.orionDashboard = new OrionDashboard();
    console.log('✅ Orion CEO Dashboard initialized successfully');
});

// Add CSS animations and styles
const style = document.createElement('style');
style.textContent = `
    .fade-in {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .updated {
        animation: highlight 1s ease-out;
    }
    
    @keyframes highlight {
        0% { background-color: rgba(0, 255, 255, 0.3); }
        100% { background-color: transparent; }
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .refresh-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #00d2ff, #3a7bd5);
        color: white;
        padding: 10px 20px;
        border-radius: 6px;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    
    .risk-low { color: #27ae60; }
    .risk-medium { color: #f39c12; }
    .risk-high { color: #e74c3c; }
    
    .return-positive { color: #27ae60; }
    .return-negative { color: #e74c3c; }
    
    .status-active { color: #27ae60; }
    .status-paused { color: #f39c12; }
    .status-stopped { color: #e74c3c; }
    
    .priority-critical { border-left: 4px solid #e74c3c; }
    .priority-high { border-left: 4px solid #f39c12; }
    .priority-medium { border-left: 4px solid #3498db; }
    .priority-low { border-left: 4px solid #95a5a6; }
    
    @media (max-width: 768px) {
        .sidebar.mobile {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }
        
        .main-content.mobile {
            margin-left: 0;
            width: 100%;
        }
    }
`;
document.head.appendChild(style);

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OrionDashboard;
} 