// Simulation & optimization logic for Green Cloud Optimizer

export interface WorkloadConfig {
  appType: "web" | "api" | "ml";
  trafficRps: number;
  cpuCores: number;
  memoryGb: number;
  priority: "balanced" | "performance" | "green";
  // Optional forecast length in hours for workload prediction (default 24)
  forecastHours?: number;
}

export interface SimulationResult {
  cpuUtilization: number; // 0-100%
  energyKwh: number;
  co2Kg: number;
  costUsd: number;
}

export interface OptimizedResult {
  config: WorkloadConfig;
  result: SimulationResult;
  recommendations: string[];
  energyReduction: number; // %
  co2Reduction: number; // %
  greenScore: number; // 0-100
  explanation?: Record<string, number>; // SHAP values {traffic, cpu, memory}
}

export interface ExplanationResponse {
  feature_importance: Record<string, number>;
  utilization_explanation: Record<string, number>;
  optimal_cpu_explanation: Record<string, number>;
}

export interface WorkloadPrediction {
  hour: number;
  traffic: number;
  predicted: number;
  label: string;
}

// CPU utilization based on workload
function calcCpuUtilization(config: WorkloadConfig): number {
  const baseLoad: Record<string, number> = { web: 0.3, api: 0.4, ml: 0.7 };
  const base = baseLoad[config.appType] || 0.4;
  const trafficFactor = Math.min(config.trafficRps / (config.cpuCores * 250), 1);
  return Math.min((base + trafficFactor * 0.6) * 100, 100);
}

// Energy in kWh per hour
function calcEnergy(cpuCores: number, utilization: number, memoryGb: number): number {
  const tdpPerCore = 0.015; // kW per core at full load
  const memPower = memoryGb * 0.001; // kW per GB
  const pue = 1.58; // Power Usage Effectiveness
  const cpuPower = cpuCores * tdpPerCore * (0.3 + 0.7 * (utilization / 100));
  return (cpuPower + memPower) * pue;
}

// CO2 in kg per hour (global average ~0.475 kg CO2/kWh)
function calcCo2(energyKwh: number, intensity = 0.475): number {
  return energyKwh * intensity;
}

export function simulate(config: WorkloadConfig): SimulationResult {
  throw new Error("simulate() is now async and must call the backend API. Use simulateAsync().");
}

export function optimize(config: WorkloadConfig): OptimizedResult {
  throw new Error("optimize() is now async and must call the backend API. Use optimizeAsync().");
}

export function predictWorkload(config: WorkloadConfig): WorkloadPrediction[] {
  throw new Error("predictWorkload() is now async and must call the backend API. Use predictWorkloadAsync().");
}

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "http://localhost:8000";

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API error ${res.status}: ${res.statusText}`);
  return res.json();
}

export async function simulateAsync(config: WorkloadConfig): Promise<SimulationResult> {
  return postJson<SimulationResult>("/api/simulate", config);
}

export async function optimizeAsync(config: WorkloadConfig): Promise<OptimizedResult> {
  return postJson<OptimizedResult>("/api/optimize", config);
}

export async function predictWorkloadAsync(config: WorkloadConfig): Promise<WorkloadPrediction[]> {
  return postJson<WorkloadPrediction[]>("/api/predict", config);
}

export async function explainAsync(config: WorkloadConfig): Promise<ExplanationResponse> {
  return postJson<ExplanationResponse>("/api/explain", config);
}
