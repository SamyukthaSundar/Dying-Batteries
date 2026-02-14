import { motion } from "framer-motion";
import { Lightbulb, ArrowRight } from "lucide-react";
import type { OptimizedResult, WorkloadConfig } from "@/lib/simulation";

interface Props {
  original: WorkloadConfig;
  optimized: OptimizedResult;
}

const OptimizationPanel = ({ original, optimized }: Props) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="eco-card p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="h-5 w-5 text-accent" />
        <h2 className="text-lg font-semibold text-foreground">Optimization Recommendations</h2>
      </div>

      {/* Config comparison */}
      <div className="bg-secondary/50 rounded-lg p-4 border border-border mb-4">
        <div className="text-xs text-muted-foreground mb-2">Configuration Change</div>
        <div className="flex items-center gap-3 text-sm font-mono">
          <span className="text-destructive">
            {original.cpuCores} cores / {original.memoryGb}GB
          </span>
          <ArrowRight className="h-4 w-4 text-primary" />
          <span className="text-primary">
            {optimized.config.cpuCores} cores / {optimized.config.memoryGb}GB
          </span>
        </div>
      </div>

      {/* Recommendations */}
      <div className="space-y-2">
        {optimized.recommendations.map((rec, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 + i * 0.08 }}
            className="flex gap-3 text-sm p-3 rounded-lg bg-primary/5 border border-primary/10"
          >
            <span className="text-primary mt-0.5 shrink-0">●</span>
            <span className="text-secondary-foreground">{rec}</span>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default OptimizationPanel;
