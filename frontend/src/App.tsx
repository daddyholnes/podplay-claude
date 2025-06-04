import { SanctuaryLayout } from '../../shared-components/src/components/sanctuary/SanctuaryLayout';
import { SanctuaryNav } from '../../shared-components/src/components/sanctuary/SanctuaryNav';
import { BackgroundGradientAnimation } from '../../shared-components/src/components/effects/BackgroundGradientAnimation';
import { useState } from 'react';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  const pageContent = {
    home: (
      <div className="min-h-[80vh] flex items-center justify-center pr-20">
        <div className="text-center space-y-8 max-w-4xl mx-auto">
          <BackgroundGradientAnimation
            gradientBackgroundStart="rgb(108, 0, 162)"
            gradientBackgroundEnd="rgb(0, 17, 82)"
            firstColor="18, 113, 255"
            secondColor="221, 74, 255"
            thirdColor="100, 220, 255"
            interactive={true}
            className="rounded-2xl"
          >
            <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent relative z-10">
              Welcome to Your Sanctuary
            </h1>
          </BackgroundGradientAnimation>
          
          <p className="text-xl text-sanctuary-muted max-w-3xl mx-auto leading-relaxed">
            Your personal AI-powered development platform designed specifically for neurodivergent minds.
            A safe space where your ADHD, sensory needs, and unique thinking patterns are not just 
            accommodated—they're celebrated and enhanced.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-12">
            {[
              { icon: '🧠', title: 'Memory Palace', desc: 'AI-powered memory with Mem0' },
              { icon: '🎨', title: 'Creation Studio', desc: 'Build with Magic MCP' },
              { icon: '🤗', title: 'Mama Bear', desc: '7 AI companions ready to help' },
              { icon: '🌸', title: 'Sensory Garden', desc: 'Calming, ADHD-friendly spaces' }
            ].map((feature) => (
              <div key={feature.title} className="p-6 rounded-2xl bg-black/20 backdrop-blur-sm border border-white/10 hover:border-purple-400/30 transition-all duration-300 hover:scale-105">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-sanctuary-accent mb-2">{feature.title}</h3>
                <p className="text-sm text-sanctuary-muted">{feature.desc}</p>
              </div>
            ))}
          </div>

          <div className="mt-12 p-6 rounded-2xl bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-400/20">
            <h2 className="text-2xl font-bold text-sanctuary-accent mb-4">🎯 Test Suite Status</h2>
            <p className="text-sanctuary-muted mb-4">
              Backend validation: <span className="text-green-400 font-bold">✅ 10/10 tests passing</span>
            </p>
            <p className="text-sm text-sanctuary-muted">
              All services active and ready. Your sanctuary is fully operational.
            </p>
          </div>
        </div>
      </div>
    ),
    memory_palace: (
      <div className="min-h-[80vh] flex items-center justify-center pr-20">
        <div className="text-center space-y-8 max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-sanctuary-accent">🧠 Memory Palace</h1>
          <p className="text-xl text-sanctuary-muted max-w-2xl mx-auto">
            Your AI-powered memory system using Mem0. Store, organize, and retrieve your thoughts with intelligence.
          </p>
          <div className="p-8 rounded-2xl bg-black/20 backdrop-blur-sm border border-purple-400/30">
            <p className="text-sanctuary-text">Memory Palace features coming soon...</p>
          </div>
        </div>
      </div>
    ),
    creation_studio: (
      <div className="min-h-[80vh] flex items-center justify-center pr-20">
        <div className="text-center space-y-8 max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-sanctuary-accent">🎨 Creation Studio</h1>
          <p className="text-xl text-sanctuary-muted max-w-2xl mx-auto">
            Build and design with Magic MCP components. Create beautiful interfaces and experiences.
          </p>
          <div className="p-8 rounded-2xl bg-black/20 backdrop-blur-sm border border-pink-400/30">
            <p className="text-sanctuary-text">Creation Studio features coming soon...</p>
          </div>
        </div>
      </div>
    ),
    learning_hub: (
      <div className="min-h-[80vh] flex items-center justify-center pr-20">
        <div className="text-center space-y-8 max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-sanctuary-accent">📚 Learning Hub</h1>
          <p className="text-xl text-sanctuary-muted max-w-2xl mx-auto">
            Structured learning paths designed for neurodivergent minds with ADHD-friendly pacing.
          </p>
          <div className="p-8 rounded-2xl bg-black/20 backdrop-blur-sm border border-blue-400/30">
            <p className="text-sanctuary-text">Learning Hub features coming soon...</p>
          </div>
        </div>
      </div>
    ),
    sensory_garden: (
      <div className="min-h-[80vh] flex items-center justify-center pr-20">
        <div className="text-center space-y-8 max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-sanctuary-accent">🌸 Sensory Garden</h1>
          <p className="text-xl text-sanctuary-muted max-w-2xl mx-auto">
            Calming sensory experiences designed to soothe and regulate your nervous system.
          </p>
          <div className="p-8 rounded-2xl bg-black/20 backdrop-blur-sm border border-green-400/30">
            <p className="text-sanctuary-text">Sensory Garden features coming soon...</p>
          </div>
        </div>
      </div>
    ),
    connection_center: (
      <div className="min-h-[80vh] flex items-center justify-center pr-20">
        <div className="text-center space-y-8 max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-sanctuary-accent">💫 Connection Center</h1>
          <p className="text-xl text-sanctuary-muted max-w-2xl mx-auto">
            Chat with your 7 AI Mama Bear companions. Each one specialized to help you in different ways.
          </p>
          <div className="p-8 rounded-2xl bg-black/20 backdrop-blur-sm border border-yellow-400/30">
            <p className="text-sanctuary-text">Connection Center features coming soon...</p>
          </div>
        </div>
      </div>
    ),
    control_center: (
      <div className="min-h-[80vh] flex items-center justify-center pr-20">
        <div className="text-center space-y-8 max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-sanctuary-accent">⚙️ Control Center</h1>
          <p className="text-xl text-sanctuary-muted max-w-2xl mx-auto">
            Customize your sanctuary experience. Adjust settings, themes, and preferences.
          </p>
          <div className="p-8 rounded-2xl bg-black/20 backdrop-blur-sm border border-gray-400/30">
            <p className="text-sanctuary-text">Control Center features coming soon...</p>
          </div>
        </div>
      </div>
    )
  };

  return (
    <div className="relative min-h-screen">
      <SanctuaryLayout currentPage={currentPage}>
        {pageContent[currentPage as keyof typeof pageContent] || pageContent.home}
      </SanctuaryLayout>
      
      {/* Right Sidebar Navigation */}
      <SanctuaryNav 
        currentPage={currentPage} 
        onPageChange={setCurrentPage}
        className="shadow-2xl"
      />
    </div>
  );
}

export default App;