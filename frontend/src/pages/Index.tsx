import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Leaf } from "lucide-react";
import InputPanel from "@/components/InputPanel";
import WorkloadPredictionChart from "@/components/WorkloadPredictionChart";
import EnergySimulation from "@/components/EnergySimulation";
import OptimizationPanel from "@/components/OptimizationPanel";
import BeforeAfterDashboard from "@/components/BeforeAfterDashboard";
import { generateSummaryPdf } from "@/lib/pdf";
import {
  type WorkloadConfig,
  type SimulationResult,
  type OptimizedResult,
  type WorkloadPrediction,
  simulateAsync,
  optimizeAsync,
  predictWorkloadAsync,
} from "@/lib/simulation";

const Index = () => {
  const [config, setConfig] = useState<WorkloadConfig | null>(null);
  const [before, setBefore] = useState<SimulationResult | null>(null);
  const [optimized, setOptimized] = useState<OptimizedResult | null>(null);
  const [predictions, setPredictions] = useState<WorkloadPrediction[]>([]);
  const [backendSource, setBackendSource] = useState(false);
  const [visiblePanel, setVisiblePanel] = useState<"none" | "all" | "recommendations" | "before-after">("none");

  const handleSubmit = async (cfg: WorkloadConfig) => {
    setConfig(cfg);
    setBackendSource(false);
    const beforeRes = await simulateAsync(cfg);
    const optimizedRes = await optimizeAsync(cfg);
    const preds = await predictWorkloadAsync(cfg);
    setBefore(beforeRes);
    setOptimized(optimizedRes);
    setPredictions(preds);
    // mark that results came from backend models
    setBackendSource(true);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-primary/20 flex items-center justify-center eco-glow">
              <Leaf className="h-5 w-5 text-primary" />
            </div>
            <h1 className="text-xl font-bold">
              <span className="eco-gradient-text">EcoScale</span>
              <span className="text-muted-foreground font-normal text-sm ml-2">Cloud Optimizer</span>
            </h1>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-muted-foreground font-mono">v1.0</span>
            {backendSource && (
              <span className="text-xs text-emerald-700 bg-emerald-100/60 border border-emerald-200 px-2 py-0.5 rounded">
                Results from backend model
              </span>
            )}

            {/* Quick panel buttons: show only recommendations or before/after */}
            {config && before && optimized && (
              <>
                <button
                  onClick={() => setVisiblePanel("recommendations")}
                  className={`ml-3 inline-flex items-center gap-2 rounded-md px-3 py-1 text-sm font-medium ${
                    visiblePanel === "recommendations" ? "bg-primary text-white" : "bg-transparent text-primary border border-primary/20"
                  }`}
                  type="button"
                >
                  Recommendations
                </button>

                <button
                  onClick={() => setVisiblePanel("before-after")}
                  className={`ml-2 inline-flex items-center gap-2 rounded-md px-3 py-1 text-sm font-medium ${
                    visiblePanel === "before-after" ? "bg-primary text-white" : "bg-transparent text-primary border border-primary/20"
                  }`}
                  type="button"
                >
                  Before vs After
                </button>
                {visiblePanel !== "all" && (
                  <button
                    onClick={() => setVisiblePanel("all")}
                    className="ml-2 inline-flex items-center gap-2 rounded-md bg-muted px-2 py-1 text-xs font-medium text-foreground"
                    type="button"
                  >
                    Show All
                  </button>
                )}
              </>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left: Input */}
          <div className="lg:col-span-4">
            <InputPanel onSubmit={handleSubmit} />
          </div>

          {/* Right: Results */}
          <div className="lg:col-span-8 space-y-6">
            <AnimatePresence mode="wait">
              {!config && (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="eco-card p-12 flex flex-col items-center justify-center text-center min-h-[400px]"
                >
                  <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center mb-4 animate-pulse-glow">
                    <Leaf className="h-8 w-8 text-primary" />
                  </div>
                  <h2 className="text-xl font-semibold text-foreground mb-2">Configure Your Workload</h2>
                  <p className="text-sm text-muted-foreground max-w-md">
                    Set your cloud parameters on the left, then hit <strong className="text-primary">Analyze & Optimize</strong> to see energy savings, CO₂ reduction, and smart recommendations.
                  </p>
                </motion.div>
              )}

              {config && before && optimized && (
                <motion.div
                  key="results"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="space-y-6"
                >
                  {before && optimized && (
                    <WorkloadPredictionChart
                      key={`pred-${predictions.length}-${predictions[0]?.predicted ?? 0}`}
                      predictions={predictions}
                    />
                  )}

                  {before && optimized && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <EnergySimulation result={before} label="⚡ Current Metrics" />
                      <EnergySimulation result={optimized.result} label="🌱 Optimized Metrics" />
                    </div>
                  )}

                  {/* When visiblePanel is "none" we intentionally render no result panels until user clicks a header button */}

                  {visiblePanel === "all" && <OptimizationPanel original={config} optimized={optimized} />}

                  {visiblePanel === "all" && (
                    <BeforeAfterDashboard
                      key={optimized ? `beforeafter-${optimized.result.energyKwh}-${optimized.result.co2Kg}` : "beforeafter-empty"}
                      before={before}
                      after={optimized}
                    />
                  )}

                  {visiblePanel === "before-after" && (
                    <BeforeAfterDashboard
                      key={optimized ? `beforeafter-${optimized.result.energyKwh}-${optimized.result.co2Kg}` : "beforeafter-empty"}
                      before={before}
                      after={optimized}
                    />
                  )}

                  {visiblePanel === "recommendations" && <OptimizationPanel original={config} optimized={optimized} />}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
