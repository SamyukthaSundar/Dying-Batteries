import { motion } from "framer-motion";
import { useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { Leaf, TrendingDown, Award } from "lucide-react";
import { generateSummaryPdf } from "@/lib/pdf";
import type { SimulationResult, OptimizedResult } from "@/lib/simulation";

interface Props {
  before: SimulationResult;
  after: OptimizedResult;
}

const GreenScoreMeter = ({ score }: { score: number }) => {
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="relative w-36 h-36 mx-auto">
      <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r="54" fill="none" stroke="hsl(160, 10%, 10%)" strokeWidth="8" />
        <motion.circle
          cx="60"
          cy="60"
          r="54"
          fill="none"
          stroke="url(#scoreGrad)"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
        />
        <defs>
          <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsl(152, 76%, 44%)" />
            <stop offset="100%" stopColor="hsl(82, 85%, 55%)" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span
          className="text-3xl font-mono font-bold eco-gradient-text"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          {score}
        </motion.span>
        <span className="text-xs text-muted-foreground">Green Score</span>
      </div>
    </div>
  );
};

const BeforeAfterDashboard = ({ before, after }: Props) => {
  // Use `generateSummaryPdf` in the shared lib instead of inline jsPDF here
  const chartData = [
    {
      name: "Energy (kWh/h)",
      Before: Number((before.energyKwh * 1000).toFixed(2)),
      After: Number((after.result.energyKwh * 1000).toFixed(2)),
    },
    {
      name: "CO₂ (g/h)",
      Before: Number((before.co2Kg * 1000).toFixed(2)),
      After: Number((after.result.co2Kg * 1000).toFixed(2)),
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      id="before-after-dashboard"
      className="eco-card p-6"
    >
      {/* trigger resize so Recharts ResponsiveContainer recalculates when `after` updates */}
      <ResizeOnUpdate after={after} />
      <div className="flex items-center gap-2 mb-6">
        <Award className="h-5 w-5 text-accent" />
        <h2 className="text-lg font-semibold text-foreground">Before vs After</h2>
        <div className="ml-auto">
          <button
            onClick={() => generateSummaryPdf(before, after)}
            className="inline-flex items-center gap-2 rounded-md bg-primary px-3 py-1 text-sm font-medium text-white hover:opacity-90"
            type="button"
          >
            Download Summary
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Green Score */}
        <div className="flex flex-col items-center justify-center">
          <GreenScoreMeter score={after.greenScore} />
          <div className="mt-3 flex items-center gap-1 text-sm text-primary">
            <Leaf className="h-4 w-4" />
            <span className="font-medium">
              {after.greenScore >= 70 ? "Excellent" : after.greenScore >= 40 ? "Good" : "Needs Work"}
            </span>
          </div>
        </div>

        {/* Bar Chart */}
        <div className="md:col-span-2 h-56">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} barGap={8} margin={{ top: 5, right: 5, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(160, 12%, 14%)" />
              <XAxis dataKey="name" tick={{ fill: "hsl(155, 8%, 50%)", fontSize: 11 }} stroke="hsl(160, 12%, 14%)" />
              <YAxis tick={{ fill: "hsl(155, 8%, 50%)", fontSize: 11 }} stroke="hsl(160, 12%, 14%)" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(160, 15%, 7%)",
                  border: "1px solid hsl(160, 12%, 14%)",
                  borderRadius: "8px",
                  color: "hsl(145, 10%, 90%)",
                  fontSize: 12,
                }}
              />
              <Bar dataKey="Before" radius={[4, 4, 0, 0]} maxBarSize={40}>
                <Cell fill="hsl(0, 60%, 45%)" />
                <Cell fill="hsl(0, 60%, 45%)" />
              </Bar>
              <Bar dataKey="After" radius={[4, 4, 0, 0]} maxBarSize={40}>
                <Cell fill="hsl(152, 76%, 44%)" />
                <Cell fill="hsl(152, 76%, 44%)" />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Reduction Stats */}
      <div className="grid grid-cols-2 gap-4 mt-6">
        <div className="bg-primary/10 border border-primary/20 rounded-lg p-4 text-center">
          <TrendingDown className="h-5 w-5 text-primary mx-auto mb-1" />
          <div className="text-2xl font-mono font-bold text-primary">{after.energyReduction}%</div>
          <div className="text-xs text-muted-foreground">Energy Reduction</div>
        </div>
        <div className="bg-accent/10 border border-accent/20 rounded-lg p-4 text-center">
          <TrendingDown className="h-5 w-5 text-accent mx-auto mb-1" />
          <div className="text-2xl font-mono font-bold text-accent">{after.co2Reduction}%</div>
          <div className="text-xs text-muted-foreground">CO₂ Reduction</div>
        </div>
      </div>

      {/* Explainable AI */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="mt-4 p-3 rounded-lg bg-secondary/50 border border-border text-xs text-muted-foreground"
      >
        💡 <strong className="text-secondary-foreground">Why these savings?</strong>{" "}
        {after.energyReduction > 0
          ? `Energy reduced by removing ${after.energyReduction}% idle compute capacity. `
          : "Configuration is already near-optimal. "}
        {after.recommendations[0] && after.recommendations[0]}
      </motion.div>
    </motion.div>
  );
};

export default BeforeAfterDashboard;

function ResizeOnUpdate({ after }: { after: any }) {
  useEffect(() => {
    // small delay to allow layout to settle
    const t = setTimeout(() => {
      try {
        window.dispatchEvent(new Event("resize"));
      } catch (e) {
        // ignore
      }
    }, 120);
    return () => clearTimeout(t);
  }, [after]);

  return null;
}
