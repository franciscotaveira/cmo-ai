import React from 'react';
import Sidebar from './Sidebar';
import CopilotPanel from './CopilotPanel';

const MainLayout = ({ children }) => {
    return (
        <div className="flex bg-background min-h-screen font-sans text-white overflow-hidden relative">
            {/* Elementos Estéticos de Fundo (Glow Effect) */}
            <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-primary/20 blur-[150px] rounded-full pointer-events-none z-0"></div>
            <div className="absolute bottom-[-20%] right-[10%] w-[40%] h-[40%] bg-secondary/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

            {/* Navegação Principal */}
            <Sidebar />

            {/* Conteúdo Central */}
            <main className="flex-1 ml-64 mr-80 p-8 h-screen overflow-y-auto relative z-10 custom-scrollbar">
                {children}
            </main>

            {/* Assessor IA Lateral */}
            <CopilotPanel />
        </div>
    );
};

export default MainLayout;
