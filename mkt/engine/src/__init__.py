"""
╔═══════════════════════════════════════════════════════════════════════════════
║ MARKETING ENGINE — SRC
╠═══════════════════════════════════════════════════════════════════════════════
║ Pacote principal do Marketing Engine v5.3 — CMO 360°
╚═══════════════════════════════════════════════════════════════════════════════
"""

from .database import DatabaseHandler
from .processor import FileProcessor
from .watcher import DriveWatcher
from .obsidian import ObsidianBridge
from .kanban_board import KanbanBoard
from .priority_engine import PriorityEngine
from .marketing_strategy import MarketingStrategyEngine
from .goal_setting import GoalSettingEngine
from .marketing_calendar import MarketingCalendar
from .budget_tracker import BudgetTracker
from .ai_insights import AIInsightsEngine, LLMProvider, AIInsight
from .growth_marketing import GrowthMarketingEngine
from .brand_communication import BrandCommunicationEngine
from .executive_dashboard import ExecutiveDashboard
from .cmo_bench import CMOLearningLoop, CMOKnowledgeBase, CMOVerification, BusinessIssue
from .notification_dispatcher import NotificationDispatcher
from .email_templates import create_critical_alert_email, create_daily_digest_email, create_weekly_summary_email

__all__ = [
    # Core
    'DatabaseHandler',
    'FileProcessor',
    'DriveWatcher',
    'ObsidianBridge',

    # Management
    'KanbanBoard',
    'PriorityEngine',

    # Planning (v5.1)
    'MarketingStrategyEngine',
    'GoalSettingEngine',
    'MarketingCalendar',
    'BudgetTracker',

    # AI (v5.2)
    'AIInsightsEngine',
    'LLMProvider',
    'AIInsight',

    # CMO 360° (v5.3)
    'GrowthMarketingEngine',
    'BrandCommunicationEngine',
    'ExecutiveDashboard',

    # CMO-Bench (v6.0 - SWE-bench Intelligence)
    'CMOLearningLoop',
    'CMOKnowledgeBase',
    'CMOVerification',
    'BusinessIssue',

    # Notifications (v6.1)
    'NotificationDispatcher',
    'create_critical_alert_email',
    'create_daily_digest_email',
    'create_weekly_summary_email'
]
