import { motion } from "framer-motion";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { TrendingUp } from "lucide-react";
import type { WorkloadPrediction } from "@/lib/simulation";

interface Props {
  predictions: WorkloadPrediction[];
}

const WorkloadPredictionChart = ({ predictions }: Props) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="eco-card p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp className="h-5 w-5 text-primary" />
        <h2 className="text-lg font-semibold text-foreground">Workload Prediction ({predictions.length}h)</h2>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={predictions} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <defs>
              <linearGradient id="trafficGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(152, 76%, 44%)" stopOpacity={0.4} />
                <stop offset="95%" stopColor="hsl(152, 76%, 44%)" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="predictedGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(82, 85%, 55%)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="hsl(82, 85%, 55%)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(160, 12%, 14%)" />
            <XAxis
              dataKey="hour"
              tick={{ fill: "hsl(155, 8%, 50%)", fontSize: 11 }}
              tickFormatter={(v) => `${v}:00`}
              stroke="hsl(160, 12%, 14%)"
            />
            <YAxis
              tick={{ fill: "hsl(155, 8%, 50%)", fontSize: 11 }}
              stroke="hsl(160, 12%, 14%)"
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(160, 15%, 7%)",
                border: "1px solid hsl(160, 12%, 14%)",
                borderRadius: "8px",
                color: "hsl(145, 10%, 90%)",
                fontSize: 12,
              }}
              labelFormatter={(v) => `${v}:00`}
            />
            <Area
              type="monotone"
              dataKey="traffic"
              stroke="hsl(152, 76%, 44%)"
              fill="url(#trafficGrad)"
              strokeWidth={2}
              name="Current"
            />
            <Area
              type="monotone"
              dataKey="predicted"
              stroke="hsl(82, 85%, 55%)"
              fill="url(#predictedGrad)"
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Predicted"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div className="flex gap-4 mt-3 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <span className="w-3 h-0.5 bg-primary inline-block rounded" /> Current Traffic
        </span>
        <span className="flex items-center gap-1">
          <span className="w-3 h-0.5 bg-accent inline-block rounded border-dashed" /> Predicted
        </span>
      </div>
    </motion.div>
  );
};

export default WorkloadPredictionChart;
