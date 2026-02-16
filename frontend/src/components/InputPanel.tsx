import { useState } from "react";
import { motion } from "framer-motion";
import { Cpu, Gauge, MemoryStick, Zap, Leaf } from "lucide-react";
import type { WorkloadConfig } from "@/lib/simulation";

interface InputPanelProps {
  onSubmit: (config: WorkloadConfig) => void;
}

const appTypes = [
  { value: "web" as const, label: "Web App", icon: "🌐" },
  { value: "api" as const, label: "API Service", icon: "⚡" },
  { value: "ml" as const, label: "ML Pipeline", icon: "🧠" },
];

const priorities = [
  { value: "balanced" as const, label: "Balanced", icon: "⚖️", desc: "Cost & performance" },
  { value: "performance" as const, label: "High Perf", icon: "🚀", desc: "Max throughput" },
  { value: "green" as const, label: "Green", icon: "🌱", desc: "Min carbon" },
];

const InputPanel = ({ onSubmit }: InputPanelProps) => {
  const [appType, setAppType] = useState<WorkloadConfig["appType"]>("web");
  const [trafficRps, setTrafficRps] = useState(500);
  const [cpuCores, setCpuCores] = useState(8);
  const [memoryGb, setMemoryGb] = useState(16);
  const [priority, setPriority] = useState<WorkloadConfig["priority"]>("balanced");
  const [forecastHours, setForecastHours] = useState(24);

  const handleSubmit = () => {
    onSubmit({ appType, trafficRps, cpuCores, memoryGb, priority, forecastHours });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="eco-card p-6 space-y-6"
    >
      <div className="flex items-center gap-2 mb-2">
        <Cpu className="h-5 w-5 text-primary" />
        <h2 className="text-lg font-semibold text-foreground">Configure Workload</h2>
      </div>

      {/* App Type */}
      <div className="space-y-2">
        <label className="text-sm text-muted-foreground">Application Type</label>
        <div className="grid grid-cols-3 gap-2">
          {appTypes.map((t) => (
            <button
              key={t.value}
              onClick={() => setAppType(t.value)}
              className={`p-3 rounded-lg border text-sm font-medium transition-all ${
                appType === t.value
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-border bg-secondary/50 text-muted-foreground hover:border-primary/50"
              }`}
            >
              <span className="text-lg block mb-1">{t.icon}</span>
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* Traffic */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <label className="text-muted-foreground flex items-center gap-1">
            <Gauge className="h-3.5 w-3.5" /> Traffic (req/s)
          </label>
          <span className="text-primary font-mono">{trafficRps}</span>
        </div>
        <input
          type="range"
          min={10}
          max={5000}
          step={10}
          value={trafficRps}
          onChange={(e) => setTrafficRps(Number(e.target.value))}
          className="w-full accent-primary h-1.5 bg-secondary rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
        />
      </div>

      {/* CPU */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <label className="text-muted-foreground flex items-center gap-1">
            <Cpu className="h-3.5 w-3.5" /> CPU Cores
          </label>
          <span className="text-primary font-mono">{cpuCores}</span>
        </div>
        <input
          type="range"
          min={1}
          max={64}
          value={cpuCores}
          onChange={(e) => setCpuCores(Number(e.target.value))}
          className="w-full accent-primary h-1.5 bg-secondary rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
        />
      </div>

      {/* Memory */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <label className="text-muted-foreground flex items-center gap-1">
            <MemoryStick className="h-3.5 w-3.5" /> Memory (GB)
          </label>
          <span className="text-primary font-mono">{memoryGb}</span>
        </div>
        <input
          type="range"
          min={1}
          max={128}
          value={memoryGb}
          onChange={(e) => setMemoryGb(Number(e.target.value))}
          className="w-full accent-primary h-1.5 bg-secondary rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
        />
      </div>

      {/* Priority */}
      <div className="space-y-2">
        <label className="text-sm text-muted-foreground">Performance Priority</label>
        <div className="grid grid-cols-3 gap-2">
          {priorities.map((p) => (
            <button
              key={p.value}
              onClick={() => setPriority(p.value)}
              className={`p-3 rounded-lg border text-sm transition-all ${
                priority === p.value
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-border bg-secondary/50 text-muted-foreground hover:border-primary/50"
              }`}
            >
              <span className="text-lg block mb-1">{p.icon}</span>
              <span className="font-medium">{p.label}</span>
              <span className="block text-xs opacity-60">{p.desc}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Forecast hours */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <label className="text-muted-foreground flex items-center gap-1">Run Time (hours)</label>
          <span className="text-primary font-mono">{forecastHours}h</span>
        </div>
        <input
          type="range"
          min={1}
          max={168}
          value={forecastHours}
          onChange={(e) => setForecastHours(Number(e.target.value))}
          className="w-full accent-primary h-1.5 bg-secondary rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
        />
      </div>

      {/* Submit */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={handleSubmit}
        className="w-full py-3 rounded-lg bg-primary text-primary-foreground font-semibold text-sm flex items-center justify-center gap-2 eco-glow transition-shadow hover:shadow-lg"
      >
        <Zap className="h-4 w-4" />
        Analyze & Optimize
        <Leaf className="h-4 w-4" />
      </motion.button>
    </motion.div>
  );
};

export default InputPanel;
