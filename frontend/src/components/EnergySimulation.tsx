import { motion } from "framer-motion";
import { Battery, Flame, DollarSign, Cpu } from "lucide-react";
import type { SimulationResult } from "@/lib/simulation";

interface Props {
  result: SimulationResult;
  label: string;
}

const stats = [
  { key: "cpuUtilization" as const, label: "CPU Utilization", unit: "%", icon: Cpu, color: "text-primary" },
  { key: "energyKwh" as const, label: "Energy Usage", unit: " kWh/h", icon: Battery, color: "text-accent" },
  { key: "co2Kg" as const, label: "CO₂ Emissions", unit: " kg/h", icon: Flame, color: "text-warning" },
  { key: "costUsd" as const, label: "Est. Cost", unit: " $/h", icon: DollarSign, color: "text-muted-foreground" },
];

const EnergySimulation = ({ result, label }: Props) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="eco-card p-6"
    >
      <h2 className="text-lg font-semibold text-foreground mb-4">{label}</h2>
      <div className="grid grid-cols-2 gap-4">
        {stats.map((s) => {
          const Icon = s.icon;
          const value = result[s.key];
          return (
            <div key={s.key} className="bg-secondary/50 rounded-lg p-4 border border-border">
              <div className="flex items-center gap-2 mb-2">
                <Icon className={`h-4 w-4 ${s.color}`} />
                <span className="text-xs text-muted-foreground">{s.label}</span>
              </div>
              <div className="text-2xl font-mono font-bold text-foreground">
                {typeof value === "number" && value < 1 ? value.toFixed(4) : value}
                <span className="text-sm text-muted-foreground font-normal">{s.unit}</span>
              </div>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
};

export default EnergySimulation;
