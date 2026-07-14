import { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Camera, Wand2, Zap, Brain, ChevronRight, Settings, Image as ImageIcon, Info, Power, Video } from 'lucide-react';

const API_BASE = (import.meta.env.VITE_API_BASE as string) ?? "http://localhost:8000";
const WS_URL = API_BASE.replace(/^http/, 'ws') + "/ws";

function App() {
  const [currentPage, setCurrentPage] = useState<'landing' | 'dashboard'>('landing');

  return (
    <div className="min-h-screen bg-[#0B1120] text-white selection:bg-[#00E5FF]/30">
      <AnimatePresence mode="wait">
        {currentPage === 'landing' ? (
          <LandingPage key="landing" onStart={() => setCurrentPage('dashboard')} />
        ) : (
          <Dashboard key="dashboard" onExit={() => setCurrentPage('landing')} />
        )}
      </AnimatePresence>
    </div>
  );
}

// --- LANDING PAGE ---
function LandingPage({ onStart }: { onStart: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0, y: -50 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen relative overflow-hidden"
    >
      {/* Magical Particles Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute bg-[#00E5FF] rounded-full opacity-30 blur-sm"
            style={{
              width: Math.random() * 6 + 2 + 'px',
              height: Math.random() * 6 + 2 + 'px',
              left: Math.random() * 100 + '%',
              top: Math.random() * 100 + '%',
            }}
            animate={{
              y: [0, -100, 0],
              opacity: [0.1, 0.5, 0.1],
              scale: [1, 1.5, 1],
            }}
            transition={{
              duration: Math.random() * 10 + 5,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
        ))}
      </div>

      {/* Navbar */}
      <nav className="w-full p-6 flex justify-between items-center relative z-10 glass-card border-b-0 rounded-none bg-[#0B1120]/50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full border-2 border-[#00E5FF] flex items-center justify-center glow-cyan">
            <span className="font-poppins font-bold text-[#00E5FF]">CV</span>
          </div>
          <span className="font-poppins text-xl font-semibold tracking-wide">CloakVision</span>
        </div>
        <div className="hidden md:flex gap-8 text-[#8B9BB4] text-sm">
          <a href="#" className="hover:text-white transition-colors">Home</a>
          <a href="#" className="hover:text-white transition-colors">Features</a>
          <a href="#" className="hover:text-[#00E5FF] transition-colors">Demo</a>
        </div>
        <button 
          onClick={onStart}
          className="bg-[#7C4DFF] hover:bg-[#00E5FF] transition-colors duration-300 px-6 py-2 rounded-full font-medium glow-purple hover:glow-cyan"
        >
          Start Application
        </button>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-6 pt-20 pb-32 flex flex-col lg:flex-row items-center relative z-10">
        <div className="lg:w-1/2 mt-10">
          <motion.h1 
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="text-5xl lg:text-7xl font-poppins font-bold leading-tight mb-6"
          >
            Become <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#00E5FF] to-[#7C4DFF] glow-cyan">Invisible</span><br/>
            Using AI Vision.
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="text-lg text-[#8B9BB4] mb-10 max-w-lg"
          >
            Inspired by Harry Potter's Invisible Cloak, CloakVision uses real-time Computer Vision and OpenCV to make white cloth disappear instantly into thin air.
          </motion.p>
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="flex gap-4"
          >
            <button onClick={onStart} className="flex items-center gap-2 bg-[#00E5FF] text-[#0B1120] px-8 py-3 rounded-full font-semibold glow-cyan hover:scale-105 transition-transform">
              Enter Dashboard <ChevronRight size={20} />
            </button>
            <button className="flex items-center gap-2 border-2 border-[#16213E] hover:border-[#00E5FF] px-8 py-3 rounded-full font-semibold transition-colors">
              Watch Demo
            </button>
          </motion.div>
        </div>
        
        {/* Magic Graphic */}
        <div className="lg:w-1/2 mt-20 lg:mt-0 flex justify-center">
          <motion.div 
            animate={{ y: [0, -20, 0] }} 
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
            className="relative w-80 h-80 lg:w-96 lg:h-96"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-[#00E5FF]/20 to-[#7C4DFF]/20 rounded-full blur-3xl"></div>
            <div className="absolute inset-4 glass-card rounded-3xl flex items-center justify-center flex-col overflow-hidden border-[#00E5FF]/30">
               <Wand2 size={80} className="text-[#00E5FF] mb-4 drop-shadow-[0_0_15px_rgba(0,229,255,0.8)]" />
               <span className="font-poppins text-xl tracking-widest text-[#00E5FF]/80">MAGIC ENGAGED</span>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Features */}
      <div className="container mx-auto px-6 pb-20 relative z-10">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <FeatureCard icon={<Camera className="text-[#00E5FF]" size={32}/>} title="Real-Time Webcam" desc="Process every frame instantly with 0 latency." delay={0.2}/>
          <FeatureCard icon={<Wand2 className="text-[#7C4DFF]" size={32}/>} title="Invisible Cloak" desc="Detects white cloth and replaces it seamlessly." delay={0.4}/>
          <FeatureCard icon={<Zap className="text-yellow-400" size={32}/>} title="30 FPS Processing" desc="Highly optimized OpenCV pipeline." delay={0.6}/>
          <FeatureCard icon={<Brain className="text-[#00E676]" size={32}/>} title="AI Vision" desc="Morphological ops & color segmentation." delay={0.8}/>
        </div>
      </div>
    </motion.div>
  );
}

function FeatureCard({ icon, title, desc, delay }: any) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="glass-card p-6 rounded-2xl hover:-translate-y-2 transition-transform duration-300"
    >
      <div className="bg-[#0B1120] w-14 h-14 rounded-xl flex items-center justify-center mb-6">
        {icon}
      </div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-[#8B9BB4] text-sm leading-relaxed">{desc}</p>
    </motion.div>
  );
}

// --- DASHBOARD ---
function Dashboard({ onExit }: { onExit: () => void }) {
  const [activeTab, setActiveTab] = useState('camera');
  const [invisibilityActive, setInvisibilityActive] = useState(false);
  const [bgReady, setBgReady] = useState(false);
  const [logs, setLogs] = useState<string[]>(["[SYSTEM] CloakVision initialized..."]);
  const [hsv, setHsv] = useState({ h: 180, s: 40, v: 180 });
  const [isConnected, setIsConnected] = useState(false);

  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const displayCanvasRef = useRef<HTMLCanvasElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const isCapturingBgRef = useRef(false);

  const addLog = useCallback((msg: string) => {
    setLogs(prev => [...prev.slice(-10), `[${new Date().toLocaleTimeString()}] ${msg}`]);
  }, []);

  useEffect(() => {
    // 1. Setup Camera
    async function setupCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { width: 640, height: 480, facingMode: "user" } 
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
        addLog("Camera access granted.");
      } catch (err) {
        addLog("Error accessing camera.");
        console.error(err);
      }
    }
    setupCamera();

    // 2. Setup WebSocket
    const ws = new WebSocket(WS_URL);
    ws.binaryType = "arraybuffer";

    ws.onopen = () => {
      setIsConnected(true);
      addLog("Connected to backend engine.");
      wsRef.current = ws;
    };

    ws.onmessage = (event) => {
      if (typeof event.data === "string") {
        try {
          const data = JSON.parse(event.data);
          if (data.type === "status") {
            setInvisibilityActive(data.active);
            setBgReady(data.bg_ready);
            if (data.bg_ready && isCapturingBgRef.current) {
              addLog("Background captured successfully.");
              isCapturingBgRef.current = false;
            }
          }
        } catch (e) {}
      } else if (event.data instanceof ArrayBuffer) {
        // Binary frame
        const bytes = new Uint8Array(event.data);
        if (bytes.length > 1 && bytes[0] === 2) {
          const imgBytes = bytes.slice(1);
          const blob = new Blob([imgBytes], { type: "image/jpeg" });
          const url = URL.createObjectURL(blob);
          const img = new Image();
          img.onload = () => {
            if (displayCanvasRef.current) {
              const ctx = displayCanvasRef.current.getContext("2d");
              if (ctx) {
                // Flip horizontally and draw
                ctx.save();
                ctx.scale(-1, 1);
                ctx.drawImage(img, -displayCanvasRef.current.width, 0, displayCanvasRef.current.width, displayCanvasRef.current.height);
                ctx.restore();
              }
            }
            URL.revokeObjectURL(url);
          };
          img.src = url;
        }
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      addLog("Disconnected from backend engine.");
      wsRef.current = null;
    };

    return () => {
      ws.close();
      if (videoRef.current?.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream;
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [addLog]);

  // Capture loop
  useEffect(() => {
    let animationId: number;

    const captureFrame = () => {
      if (videoRef.current && canvasRef.current && wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");

        if (ctx && video.videoWidth > 0) {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          
          canvas.toBlob((blob) => {
            if (blob) {
              blob.arrayBuffer().then(buffer => {
                const imgBytes = new Uint8Array(buffer);
                const packet = new Uint8Array(imgBytes.length + 1);
                // 1 if capturing bg, 0 otherwise
                packet[0] = isCapturingBgRef.current ? 1 : 0;
                packet.set(imgBytes, 1);
                
                try {
                  wsRef.current?.send(packet);
                } catch(e) {}
              });
            }
          }, "image/jpeg", 0.6); // Slightly lower quality for better fps over network
        }
      }
      animationId = requestAnimationFrame(captureFrame);
    };

    animationId = requestAnimationFrame(captureFrame);

    return () => cancelAnimationFrame(animationId);
  }, []);


  const captureBackground = () => {
    if (!isConnected) return addLog("Cannot capture: Not connected.");
    addLog("Initiating background capture (5s)...");
    
    // Simulate delay
    setTimeout(() => {
      isCapturingBgRef.current = true;
    }, 5000);
  };

  const toggleInvisibility = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ command: "toggle_invisibility" }));
      addLog("Toggling cloak...");
    }
  };
  
  const updateHSV = (newHsv: any) => {
    setHsv(newHsv);
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ 
        command: "update_hsv",
        h: newHsv.h,
        s: newHsv.s,
        v: newHsv.v
      }));
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen flex"
    >
      {/* Hidden elements for capture */}
      <video ref={videoRef} autoPlay playsInline muted className="hidden" />
      <canvas ref={canvasRef} className="hidden" />

      {/* Sidebar */}
      <div className="w-64 glass-card border-r border-white/5 flex flex-col p-6 z-20">
        <div className="flex items-center gap-3 mb-12">
          <div className="w-8 h-8 rounded-full border border-[#00E5FF] flex items-center justify-center glow-cyan">
            <span className="font-poppins text-xs font-bold text-[#00E5FF]">CV</span>
          </div>
          <span className="font-poppins font-semibold">CloakVision</span>
        </div>
        
        <div className="flex flex-col gap-2 flex-grow">
          <NavBtn icon={<Video size={18}/>} label="Dashboard" active={activeTab==='camera'} onClick={()=>setActiveTab('camera')} />
          <NavBtn icon={<Settings size={18}/>} label="Settings" active={activeTab==='settings'} onClick={()=>setActiveTab('settings')} />
          <NavBtn icon={<ImageIcon size={18}/>} label="Gallery" active={activeTab==='gallery'} onClick={()=>setActiveTab('gallery')} />
          <NavBtn icon={<Info size={18}/>} label="About" active={activeTab==='about'} onClick={()=>setActiveTab('about')} />
        </div>
        
        <button onClick={onExit} className="flex items-center gap-3 text-red-400 hover:text-red-300 p-3 rounded-xl transition-colors">
          <Power size={18} /> Exit
        </button>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 p-8 flex flex-col h-screen overflow-hidden relative">
        {/* Header Stats */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          <StatCard label="Connection" value={isConnected ? "CONNECTED" : "OFFLINE"} color={isConnected ? "text-[#00E676]" : "text-red-500"} />
          <StatCard label="Status" value={invisibilityActive ? "INVISIBLE" : "VISIBLE"} color={invisibilityActive ? "text-[#00E5FF]" : "text-white"} />
          <StatCard label="Background" value={bgReady ? "READY" : "NOT CAPTURED"} color={bgReady ? "text-[#00E676]" : "text-yellow-400"} />
          <StatCard label="Engine" value="WebSocket" />
        </div>
        
        <div className="flex-1 flex gap-8 min-h-0">
          {/* Camera Feed */}
          <div className="flex-1 glass-card rounded-2xl overflow-hidden flex flex-col relative border-[#00E5FF]/20 shadow-[0_0_30px_rgba(0,229,255,0.05)]">
            <div className="p-4 border-b border-white/5 flex justify-between items-center bg-[#0B1120]/50">
              <span className="font-semibold text-sm tracking-widest text-[#00E5FF]">LIVE FEED</span>
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
              </span>
            </div>
            <div className="flex-1 bg-black relative flex items-center justify-center">
              <canvas 
                ref={displayCanvasRef} 
                className="max-h-full object-contain"
                width={640}
                height={480}
              />
              <div className="absolute inset-0 pointer-events-none shadow-[inset_0_0_50px_rgba(0,0,0,0.8)]"></div>
            </div>
          </div>
          
          {/* Right Panel */}
          <div className="w-80 flex flex-col gap-6">
            <div className="glass-card p-6 rounded-2xl flex flex-col gap-4">
              <h3 className="font-poppins font-semibold text-[#00E5FF] mb-2">Controls</h3>
              
              <button 
                onClick={captureBackground}
                disabled={!isConnected}
                className="bg-[#16213E] hover:bg-[#1a284c] border border-white/10 p-3 rounded-xl transition-all disabled:opacity-50"
              >
                Capture Background
              </button>
              
              <button 
                onClick={toggleInvisibility}
                disabled={!bgReady || !isConnected}
                className={`p-3 rounded-xl font-semibold transition-all ${
                  bgReady && isConnected
                    ? invisibilityActive 
                      ? 'bg-red-500/20 text-red-400 border border-red-500/50 hover:bg-red-500/30' 
                      : 'bg-[#7C4DFF] hover:bg-[#8d63ff] glow-purple text-white'
                    : 'bg-[#16213E] text-white/30 cursor-not-allowed'
                }`}
              >
                {invisibilityActive ? "Stop Invisibility" : "Start Invisibility"}
              </button>
            </div>
            
            <div className="glass-card p-6 rounded-2xl flex-1 flex flex-col min-h-0">
              <h3 className="font-poppins font-semibold text-[#7C4DFF] mb-4">HSV Tuning</h3>
              <div className="flex-1 overflow-y-auto pr-2 space-y-6">
                <div>
                  <div className="flex justify-between text-xs text-[#8B9BB4] mb-2">
                    <span>Hue Upper</span><span>{hsv.h}</span>
                  </div>
                  <input type="range" min="0" max="180" value={hsv.h} 
                    onChange={e => updateHSV({...hsv, h: parseInt(e.target.value)})}
                    className="w-full accent-[#00E5FF]" />
                </div>
                <div>
                  <div className="flex justify-between text-xs text-[#8B9BB4] mb-2">
                    <span>Sat Upper</span><span>{hsv.s}</span>
                  </div>
                  <input type="range" min="0" max="255" value={hsv.s} 
                    onChange={e => updateHSV({...hsv, s: parseInt(e.target.value)})}
                    className="w-full accent-[#00E5FF]" />
                </div>
                <div>
                  <div className="flex justify-between text-xs text-[#8B9BB4] mb-2">
                    <span>Val Lower</span><span>{hsv.v}</span>
                  </div>
                  <input type="range" min="0" max="255" value={hsv.v} 
                    onChange={e => updateHSV({...hsv, v: parseInt(e.target.value)})}
                    className="w-full accent-[#00E5FF]" />
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Terminal Status */}
        <div className="mt-8 h-32 bg-black/80 rounded-xl border border-white/10 p-4 font-mono text-xs overflow-y-auto flex flex-col justify-end">
          {logs.map((log, i) => (
            <div key={i} className="text-[#00E676] mb-1 opacity-80">{log}</div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function NavBtn({ icon, label, active, onClick }: any) {
  return (
    <button 
      onClick={onClick}
      className={`flex items-center gap-3 p-3 rounded-xl transition-all ${
        active ? 'bg-[#00E5FF]/10 text-[#00E5FF] border border-[#00E5FF]/30' : 'text-[#8B9BB4] hover:bg-white/5 hover:text-white'
      }`}
    >
      {icon} <span className="font-medium text-sm">{label}</span>
    </button>
  );
}

function StatCard({ label, value, color = "text-white" }: any) {
  return (
    <div className="glass-card p-4 rounded-xl flex flex-col justify-center border-l-4 border-[#00E5FF]/50">
      <span className="text-[#8B9BB4] text-xs font-semibold uppercase tracking-wider mb-1">{label}</span>
      <span className={`font-poppins text-2xl font-bold ${color}`}>{value}</span>
    </div>
  );
}

export default App;
