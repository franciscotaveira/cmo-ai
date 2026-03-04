import React from 'react';
import { Home, TrendingUp, Brain, Settings, LayoutDashboard } from 'lucide-react';

const Sidebar = () => {
    return (
        <aside className="w-64 bg-panel border-r border-white/5 h-screen fixed left-0 top-0 flex flex-col">
            <div className="p-6 flex items-center space-x-3">
                <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/50">
                    <LayoutDashboard className="w-5 h-5 text-primary" />
                </div>
                <span className="text-xl font-bold tracking-wider text-white">CMO <span className="text-primary">361°</span></span>
            </div>

            <nav className="flex-1 px-4 space-y-2 mt-4">
                <NavItem icon={<Home size={20} />} label="Command Center" active />
                <NavItem icon={<TrendingUp size={20} />} label="Growth & Ads" />
                <NavItem icon={<Brain size={20} />} label="AI Knowledge" />
                <NavItem icon={<Settings size={20} />} label="Conectores" />
            </nav>

            <div className="p-4 m-4 rounded-xl bg-white/5 border border-white/5">
                <p className="text-xs text-gray-400 mb-2">Status do Motor</p>
                <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 rounded-full bg-success animate-pulse"></div>
                    <span className="text-sm text-gray-200">Online & Ativo</span>
                </div>
            </div>
        </aside>
    );
};

const NavItem = ({ icon, label, active = false }) => (
    <button
        className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${active
                ? 'bg-primary/10 text-primary border border-primary/20'
                : 'text-gray-400 hover:bg-white/5 hover:text-white'
            }`}
    >
        {icon}
        <span className="font-medium text-sm">{label}</span>
    </button>
);

export default Sidebar;
