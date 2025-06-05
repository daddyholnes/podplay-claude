
import React, { useState } from 'react';
import { useMamaBear } from '../hooks/useMamaBear';
import { useTheme } from '../hooks/useTheme';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import { MagnifyingGlassCircleIcon, DocumentTextIcon, PlayIcon, PauseIcon, StopIcon } from '../components/icons';
import LoadingSpinner from '../components/ui/LoadingSpinner';

interface ScoutTask {
  id: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'paused';
  progress: number;
  filesGenerated: string[];
  consoleOutput: string[];
}

const ScoutAgentPage: React.FC = () => {
  const { sendUserMessage, currentVariant } = useMamaBear();
  const { theme } = useTheme();
  const [taskDescription, setTaskDescription] = useState('');
  const [activeTask, setActiveTask] = useState<ScoutTask | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleStartTask = async () => {
    if (!taskDescription.trim()) return;
    setIsLoading(true);
    await sendUserMessage(`Mama Bear Scout, please start this task: ${taskDescription}`);
    
    const newTask: ScoutTask = {
      id: `task-${Date.now()}`,
      description: taskDescription,
      status: 'running',
      progress: 0,
      filesGenerated: [],
      consoleOutput: [`Task started: ${taskDescription}`],
    };
    setActiveTask(newTask);
    
    // Simulate task progress
    const interval = setInterval(() => {
      setActiveTask(prev => {
        if (!prev || prev.status !== 'running') {
          clearInterval(interval);
          return prev;
        }
        const newProgress = Math.min(prev.progress + 10, 100);
        const newOutput = [...prev.consoleOutput, `Progress: ${newProgress}%...`];
        let newFiles = prev.filesGenerated;
        if (newProgress > 30 && newProgress < 45 && newFiles.length === 0) newFiles = ['report_draft_v1.txt'];
        if (newProgress > 70 && newProgress < 85 && newFiles.length === 1) newFiles = [...newFiles, 'results_summary.md'];

        if (newProgress === 100) {
          clearInterval(interval);
          setIsLoading(false);
          return { ...prev, status: 'completed', progress: 100, consoleOutput: [...newOutput, 'Task completed successfully!'], filesGenerated: newFiles.length === 0 ? ['final_report.pdf', 'data_analysis.csv'] : newFiles };
        }
        return { ...prev, progress: newProgress, consoleOutput: newOutput, filesGenerated: newFiles };
      });
    }, 1000);
    // Do not set setIsLoading(false) here as progress simulation handles it
  };

  const handlePauseResumeTask = () => {
    if (!activeTask) return;
    setActiveTask(prev => prev ? ({ ...prev, status: prev.status === 'running' ? 'paused' : 'running' }) : null);
    sendUserMessage(`Mama Bear Scout, ${activeTask.status === 'running' ? 'pause' : 'resume'} current task.`);
  };

  const handleStopTask = () => {
    setActiveTask(prev => prev ? ({ ...prev, status: 'failed', progress: prev.progress }) : null); // or 'stopped'
    setIsLoading(false);
    sendUserMessage(`Mama Bear Scout, stop current task.`);
  };

  return (
    <div className="p-6 flex flex-col h-full">
      <header className="mb-6">
        <h1 className={`text-3xl font-bold ${theme.accent} flex items-center`}>
          <MagnifyingGlassCircleIcon className="w-8 h-8 mr-2" /> Mama Bear Scout - Autonomous Explorer
        </h1>
        <p className={`${theme.text}/70`}>Delegate long-running tasks to your autonomous AI agent.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-grow">
        {/* Task Input & Controls */}
        <Card className="lg:col-span-1 flex flex-col">
          <h2 className="text-xl font-semibold mb-3">New Scout Task</h2>
          <textarea
            value={taskDescription}
            onChange={(e) => setTaskDescription(e.target.value)}
            placeholder="Describe the task for Mama Bear Scout... e.g., 'Research market trends for sustainable energy and generate a report.'"
            rows={6}
            className={`w-full p-2 rounded-md ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/30 focus:ring-1 focus:${theme.accent.replace('text-','ring-')} outline-none mb-3 resize-none`}
            style={{ scrollbarWidth: 'thin' }}
          />
          {/* Mock File Upload */}
          <div className="mb-4">
            <label className={`block text-sm font-medium mb-1 ${theme.text}/80`}>Attach Files (optional)</label>
            <Input type="file" multiple disabled={isLoading} />
          </div>
          <Button onClick={handleStartTask} isLoading={isLoading && activeTask?.status === 'running'} disabled={isLoading || !taskDescription.trim()} className="w-full" leftIcon={<PlayIcon className="w-5 h-5"/>}>
            {activeTask && activeTask.status !== 'completed' && activeTask.status !== 'failed' ? 'Task In Progress' : 'Start Autonomous Task'}
          </Button>
          
          {activeTask && (activeTask.status === 'running' || activeTask.status === 'paused') && (
            <div className="mt-4 flex space-x-2">
              <Button onClick={handlePauseResumeTask} variant="secondary" className="flex-1" leftIcon={activeTask.status === 'running' ? <PauseIcon className="w-5 h-5"/> : <PlayIcon className="w-5 h-5"/>}>
                {activeTask.status === 'running' ? 'Pause' : 'Resume'}
              </Button>
              <Button onClick={handleStopTask} variant="danger" className="flex-1" leftIcon={<StopIcon className="w-5 h-5"/>}>
                Stop
              </Button>
            </div>
          )}
        </Card>

        {/* Task Progress & Output */}
        <Card className="lg:col-span-2 flex flex-col">
          {!activeTask && (
            <div className="flex-grow flex flex-col items-center justify-center text-center p-6">
              <MagnifyingGlassCircleIcon className={`w-16 h-16 ${theme.text}/30 mb-4`} />
              <h3 className="text-xl font-semibold mb-2">No Active Task</h3>
              <p className={`${theme.text}/60`}>Describe a task and click "Start Autonomous Task" to begin.</p>
            </div>
          )}
          {activeTask && (
            <>
              <h2 className="text-xl font-semibold mb-1">Active Task: <span className="font-normal text-base truncate" title={activeTask.description}>{activeTask.description.substring(0,50)}{activeTask.description.length > 50 ? '...' : ''}</span></h2>
              <div className="mb-3">
                <div className="flex justify-between text-sm mb-1">
                  <span>Status: <span className={`font-medium ${
                    activeTask.status === 'completed' ? 'text-green-500' :
                    activeTask.status === 'failed' ? 'text-red-500' :
                    activeTask.status === 'paused' ? 'text-yellow-500' :
                    theme.accent
                  }`}>{activeTask.status}</span></span>
                  <span>Progress: {activeTask.progress}%</span>
                </div>
                <div className={`w-full ${theme.chatBubbleBg} rounded-full h-2.5 border ${theme.accent.replace('text-','border-')}/30`}>
                  <div className={`h-full rounded-full ${theme.accent.replace('text-','bg-')} transition-all duration-500 ease-out`} style={{ width: `${activeTask.progress}%` }}></div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-grow">
                {/* Console Output */}
                <div className="flex flex-col">
                  <h3 className="text-md font-semibold mb-2">Console Output</h3>
                  <div className={`flex-grow p-2 rounded-md ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/20 font-mono text-xs overflow-y-auto h-48 md:h-auto`} style={{ scrollbarWidth: 'thin' }}>
                    {activeTask.consoleOutput.map((line, idx) => (
                      <p key={idx} className="whitespace-pre-wrap">{`> ${line}`}</p>
                    ))}
                    {isLoading && activeTask.status === 'running' && <LoadingSpinner size="sm" />}
                  </div>
                </div>

                {/* Files Generated */}
                <div className="flex flex-col">
                  <h3 className="text-md font-semibold mb-2">Files Generated</h3>
                  <div className={`flex-grow p-2 rounded-md ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/20 text-xs overflow-y-auto h-32 md:h-auto`} style={{ scrollbarWidth: 'thin' }}>
                    {activeTask.filesGenerated.length === 0 && <p className="italic opacity-60">No files generated yet.</p>}
                    {activeTask.filesGenerated.map((file, idx) => (
                      <div key={idx} className="flex items-center p-1 hover:bg-gray-500/10 rounded">
                        <DocumentTextIcon className="w-4 h-4 mr-2 opacity-70" />
                        <span>{file}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </>
          )}
        </Card>
      </div>
    </div>
  );
};

export default ScoutAgentPage;