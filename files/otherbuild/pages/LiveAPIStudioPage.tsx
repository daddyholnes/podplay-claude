import React, { useState, useRef, useEffect } from 'react';
import { useTheme } from '../hooks/useTheme';
import { useMamaBear } from '../hooks/useMamaBear';
import { useToast } from '../hooks/useToast';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import { MicrophoneIcon, VideoCameraIcon, PlayIcon, StopIcon, Cog6ToothIcon, CodeBracketIcon } from '../components/icons';
import { LIVE_API_GEMINI_MODELS } from '../constants';
import LoadingSpinner from '../components/ui/LoadingSpinner';

// Mock Gemini Service
const mockGeminiService = {
  startSession: async (modelId: string, config: any) => {
    console.log(`Starting session with ${modelId}`, config);
    return { sessionId: `sess_${Date.now()}`, message: "Session started successfully." };
  },
  sendAudioChunk: async (sessionId: string, chunk: Blob) => {
    console.log(`Sending audio chunk to ${sessionId}`, chunk);
    // Simulate transcription
    return { transcript: `Mock transcript: ...some spoken words... (${Math.random().toString(36).substring(7)})`, isFinal: Math.random() > 0.5 };
  },
  sendVideoFrame: async (sessionId: string, frame: string) => { // frame as base64 string
    console.log(`Sending video frame to ${sessionId}`);
    // Simulate some video processing ack
    return { ack: true };
  },
  callFunction: async (sessionId: string, functionCall: any) => {
    console.log(`Calling function for ${sessionId}`, functionCall);
    return { result: `Mock function result for ${functionCall.name}` };
  },
  stopSession: async (sessionId: string) => {
    console.log(`Stopping session ${sessionId}`);
    return { message: "Session stopped." };
  }
};


const LiveAPIStudioPage: React.FC = () => {
  const { theme } = useTheme();
  const { currentVariant, sendUserMessage } = useMamaBear();
  const { addToast } = useToast();

  const [selectedModel, setSelectedModel] = useState(LIVE_API_GEMINI_MODELS[0].id);
  const [isSessionActive, setIsSessionActive] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isRecordingAudio, setIsRecordingAudio] = useState(false);
  const [isSharingVideo, setIsSharingVideo] = useState(false);
  const [transcript, setTranscript] = useState<string[]>([]);
  const [functionLogs, setFunctionLogs] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const localStreamRef = useRef<MediaStream | null>(null);
  
  // Mock voice selection
  const voices = ["Alloy (Default)", "Echo", "Fable", "Onyx", "Nova", "Shimmer"];
  const [selectedVoice, setSelectedVoice] = useState(voices[0]);

  const handleStartSession = async () => {
    setIsLoading(true);
    addToast(`Starting session with ${selectedModel}...`, 'info');
    sendUserMessage(`Mama Bear, prepare Live API session with ${selectedModel}.`);
    try {
      const response = await mockGeminiService.startSession(selectedModel, { voice: selectedVoice });
      setSessionId(response.sessionId);
      setIsSessionActive(true);
      setTranscript([`Session started with ${selectedModel} (ID: ${response.sessionId})`]);
      addToast(response.message, 'success');
    } catch (error) {
      console.error("Error starting session:", error);
      addToast('Failed to start session.', 'error');
    }
    setIsLoading(false);
  };

  const handleStopSession = async () => {
    if (!sessionId) return;
    setIsLoading(true);
    addToast('Stopping session...', 'info');
    try {
      await mockGeminiService.stopSession(sessionId);
      setIsSessionActive(false);
      setSessionId(null);
      setIsRecordingAudio(false);
      setIsSharingVideo(false);
      if (localStreamRef.current) {
        localStreamRef.current.getTracks().forEach(track => track.stop());
        localStreamRef.current = null;
      }
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
        mediaRecorderRef.current.stop();
      }
      setTranscript(prev => [...prev, "Session stopped."]);
      addToast('Session stopped successfully.', 'success');
    } catch (error) {
      console.error("Error stopping session:", error);
      addToast('Failed to stop session.', 'error');
    }
    setIsLoading(false);
  };

  const toggleAudioRecording = async () => {
    if (!isSessionActive) {
      addToast('Start a session first to record audio.', 'warning');
      return;
    }
    if (isRecordingAudio) {
      // Stop recording
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
        mediaRecorderRef.current.stop();
      }
      setIsRecordingAudio(false);
      setTranscript(prev => [...prev, "Audio recording stopped."]);
    } else {
      // Start recording
      try {
        if (!localStreamRef.current) { // Get stream if not already active (e.g. from video)
             localStreamRef.current = await navigator.mediaDevices.getUserMedia({ audio: true, video: isSharingVideo });
        } else if (!localStreamRef.current.getAudioTracks().find(t=>t.enabled && t.readyState === 'live')) { // if stream exists but audio is not active
            const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            if (localStreamRef.current) { // Check if still exists
                localStreamRef.current.addTrack(audioStream.getAudioTracks()[0]);
            } else { // If it became null somehow
                 localStreamRef.current = audioStream;
            }
        } else if (!localStreamRef.current) { // Fallback if it's null
             localStreamRef.current = await navigator.mediaDevices.getUserMedia({ audio: true, video: isSharingVideo });
        }


        const recorder = new MediaRecorder(localStreamRef.current);
        mediaRecorderRef.current = recorder;
        recorder.ondataavailable = async (event) => {
          if (event.data.size > 0 && sessionId) {
            const { transcript: newText, isFinal } = await mockGeminiService.sendAudioChunk(sessionId, event.data);
            setTranscript(prev => {
              const lastIndex = prev.length -1;
              // If last message was partial and this one is too, append. Otherwise, new line.
              if (prev.length > 0 && !prev[lastIndex].startsWith("Final:") && !isFinal && prev[lastIndex].startsWith("Partial: ")) {
                const updatedTranscript = [...prev];
                updatedTranscript[lastIndex] = prev[lastIndex].replace("Partial: ", "") + " " + newText.replace("Mock transcript: ", "");
                return isFinal ? [...updatedTranscript.slice(0, lastIndex), `Final: ${updatedTranscript[lastIndex]}`] : [...updatedTranscript.slice(0, lastIndex), `Partial: ${updatedTranscript[lastIndex]}`];
              }
              return [...prev, `${isFinal ? 'Final' : 'Partial'}: ${newText}`];
            });
          }
        };
        recorder.start(1000); // Slice into 1s chunks
        setIsRecordingAudio(true);
        setTranscript(prev => [...prev, "Audio recording started..."]);
      } catch (error) {
        console.error("Error accessing microphone:", error);
        addToast('Could not access microphone. Check permissions.', 'error');
      }
    }
  };
  
  const toggleVideoSharing = async () => {
    if (!isSessionActive) {
      addToast('Start a session first to share video.', 'warning');
      return;
    }
    if (isSharingVideo) {
      // Stop video
      if (localStreamRef.current) {
        localStreamRef.current.getVideoTracks().forEach(track => track.stop());
        // If audio is not recording, stop the whole stream
        if (!isRecordingAudio && localStreamRef.current) { // Check again if still exists
            localStreamRef.current.getTracks().forEach(track => track.stop());
            localStreamRef.current = null;
        }
      }
      if (videoRef.current) videoRef.current.srcObject = null;
      setIsSharingVideo(false);
      setTranscript(prev => [...prev, "Video sharing stopped."]);
    } else {
      // Start video
      try {
         if (!localStreamRef.current) { // Get stream if not already active (e.g. from audio)
            localStreamRef.current = await navigator.mediaDevices.getUserMedia({ video: true, audio: isRecordingAudio });
        } else if (!localStreamRef.current.getVideoTracks().find(t=>t.enabled && t.readyState === 'live')) { // if stream exists but video is not active
            const videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
             if (localStreamRef.current) { // Check if still exists
                localStreamRef.current.addTrack(videoStream.getVideoTracks()[0]);
            } else { // If it became null somehow
                 localStreamRef.current = videoStream;
            }
        } else if (!localStreamRef.current) { // Fallback if it's null
            localStreamRef.current = await navigator.mediaDevices.getUserMedia({ video: true, audio: isRecordingAudio });
        }


        if (videoRef.current && localStreamRef.current) {
          videoRef.current.srcObject = localStreamRef.current;
        }
        setIsSharingVideo(true);
        setTranscript(prev => [...prev, "Video sharing started."]);
        // Mock sending frames
        // setInterval(() => { if (isSharingVideo && sessionId) mockGeminiService.sendVideoFrame(sessionId, "base64_image_data"); }, 1000);
      } catch (error) {
        console.error("Error accessing camera:", error);
        addToast('Could not access camera. Check permissions.', 'error');
      }
    }
  };

  const handleMockFunctionCall = async () => {
    if (!sessionId) {
        addToast('Start a session first.', 'warning');
        return;
    }
    const funcCall = { name: "getWeather", params: { city: "London" } };
    setFunctionLogs(prev => [...prev, `Calling function: ${funcCall.name}(${JSON.stringify(funcCall.params)})`]);
    const result = await mockGeminiService.callFunction(sessionId, funcCall);
    setFunctionLogs(prev => [...prev, `Result: ${result.result}`]);
    addToast(`Function ${funcCall.name} call simulated.`, 'info');
  };
  
  const renderPanel = (title: string, children: React.ReactNode) => (
    <Card className="flex-grow flex flex-col">
      <h3 className={`text-md font-semibold mb-2 border-b pb-2 ${theme.accent.replace('text-','border-')}/20`}>{title}</h3>
      <div className="flex-grow overflow-y-auto text-xs" style={{ scrollbarWidth: 'thin' }}>{children}</div>
    </Card>
  );

  return (
    <div className="p-6 flex flex-col h-full">
      <header className="mb-6">
        <h1 className={`text-3xl font-bold ${theme.accent} flex items-center`}>
          <MicrophoneIcon className="w-8 h-8 mr-2" /> Live API Studio
        </h1>
        <p className={`${theme.text}/70`}>Experiment with Gemini Live API for voice and video interactions. Mama Bear: {currentVariant}</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Controls */}
        <Card className="lg:col-span-1">
          <h2 className="text-xl font-semibold mb-3 flex items-center"><Cog6ToothIcon className="w-5 h-5 mr-2"/>Controls & Settings</h2>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium opacity-80 mb-1">Select Model:</label>
              <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)} disabled={isSessionActive || isLoading}
                className={`w-full p-2 rounded-lg ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/50 focus:ring-1 focus:${theme.accent.replace('text-','ring-')} outline-none text-sm transition-colors duration-200`}>
                {LIVE_API_GEMINI_MODELS.map(model => <option key={model.id} value={model.id}>{model.name}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium opacity-80 mb-1">Select Voice (TTS):</label>
              <select value={selectedVoice} onChange={(e) => setSelectedVoice(e.target.value)} disabled={isSessionActive || isLoading}
                 className={`w-full p-2 rounded-lg ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/50 focus:ring-1 focus:${theme.accent.replace('text-','ring-')} outline-none text-sm transition-colors duration-200`}>
                {voices.map(voice => <option key={voice} value={voice}>{voice}</option>)}
              </select>
            </div>
            <div className="flex space-x-2">
              {!isSessionActive ? (
                <Button onClick={handleStartSession} isLoading={isLoading} disabled={isLoading} leftIcon={<PlayIcon className="w-5 h-5"/>} className="flex-1">Start Session</Button>
              ) : (
                <Button onClick={handleStopSession} isLoading={isLoading} disabled={isLoading} variant="danger" leftIcon={<StopIcon className="w-5 h-5"/>} className="flex-1">Stop Session</Button>
              )}
            </div>
            <div className="flex space-x-2">
              <Button onClick={toggleAudioRecording} disabled={!isSessionActive || isLoading} leftIcon={<MicrophoneIcon className="w-5 h-5"/>} className="flex-1" variant={isRecordingAudio ? "primary" : "secondary"}>
                {isRecordingAudio ? 'Stop Audio' : 'Start Audio'}
              </Button>
              <Button onClick={toggleVideoSharing} disabled={!isSessionActive || isLoading} leftIcon={<VideoCameraIcon className="w-5 h-5"/>} className="flex-1" variant={isSharingVideo ? "primary" : "secondary"}>
                {isSharingVideo ? 'Stop Video' : 'Share Video'}
              </Button>
            </div>
            <Button onClick={handleMockFunctionCall} disabled={!isSessionActive || isLoading} leftIcon={<CodeBracketIcon className="w-5 h-5"/>} variant="secondary" className="w-full">
              Call Mock Function (getWeather)
            </Button>
          </div>
        </Card>
        
        {/* Video Preview */}
        <Card className="lg:col-span-2 flex items-center justify-center">
           {isSharingVideo && videoRef.current?.srcObject ? (
            <video ref={videoRef} autoPlay playsInline muted className={`w-full h-full max-h-64 object-contain rounded-xl ${theme.chatBubbleBg}`}></video>
          ) : (
            <div className="text-center opacity-50">
              <VideoCameraIcon className="w-16 h-16 mx-auto mb-2"/>
              <p>{isSessionActive ? "Video sharing is off. Click 'Share Video' to start." : "Start a session to enable video."}</p>
            </div>
          )}
          {isLoading && isSessionActive && <div className="absolute inset-0 bg-white/50 dark:bg-black/50 flex items-center justify-center rounded-xl"><LoadingSpinner size="md"/></div>}
        </Card>
      </div>

      {/* Output Panels */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 flex-grow min-h-[200px]">
         {renderPanel("Real-time Transcription", 
          <div className="space-y-1.5 whitespace-pre-wrap">
            {transcript.map((line, i) => <p key={i} className={`${line.startsWith("Final:") ? 'font-semibold' : ''} ${line.startsWith("Session") || line.startsWith("Audio") || line.startsWith("Video") ? 'italic opacity-70' : ''}`}>{line}</p>)}
          </div>
        )}
        {renderPanel("Function Call Logs", 
          <div className="space-y-1.5 whitespace-pre-wrap">
            {functionLogs.map((log, i) => <p key={i}>{log}</p>)}
             {functionLogs.length === 0 && <p className="italic opacity-60">No function calls yet.</p>}
          </div>
        )}
      </div>
       {/* Audio Waveform (placeholder) */}
        {isRecordingAudio && (
            <div className={`mt-4 p-3 rounded-xl ${theme.chatBubbleBg} border ${theme.accent.replace('text-','border-')}/20`}>
                <p className="text-sm text-center opacity-70">Mock Audio Waveform Visualizer</p>
                <div className="h-10 w-full flex items-center justify-center space-x-1">
                    {[...Array(20)].map((_, i) => (
                        <div key={i} className={`w-1 rounded-full ${theme.accent.replace('text-','bg-')}`} style={{height: `${Math.random()*80+10}%`, animation: `pulseNeon ${0.5 + Math.random()}s ease-in-out infinite alternate`}}></div>
                    ))}
                </div>
            </div>
        )}
    </div>
  );
};

export default LiveAPIStudioPage;