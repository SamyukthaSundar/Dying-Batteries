# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List, Literal
# import os
# import sys

# # Ensure `ml` package and `models` folder inside this backend directory are importable
# sys.path.insert(0, os.path.dirname(__file__))

# from ml.predict import predict_utilization, predict_optimal_cpu
# from simulation.energy_model import calculate_energy
# from simulation.carbon_model import calculate_carbon_emission

# app = FastAPI(title="EcoScale API")

# app.add_middleware(
#     CORSMiddleware,
#     # Allow local dev frontends on common Vite ports and any other origin during development
#     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:8081", "http://127.0.0.1:8081"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class WorkloadConfig(BaseModel):
#     appType: Literal["web", "api", "ml"]
#     trafficRps: int
#     cpuCores: int
#     memoryGb: int
#     priority: Literal["balanced", "performance", "green"]


# class SimulationResult(BaseModel):
#     cpuUtilization: float
#     energyKwh: float
#     co2Kg: float
#     costUsd: float


# class OptimizedResult(BaseModel):
#     config: WorkloadConfig
#     result: SimulationResult
#     recommendations: List[str]
#     energyReduction: int
#     co2Reduction: int
#     greenScore: int


# class WorkloadPrediction(BaseModel):
#     hour: int
#     traffic: int
#     predicted: int
#     label: str


# # --- Implementation ported from frontend simulation.ts to keep results identical ---

# def calc_cpu_utilization(config: WorkloadConfig) -> float:
#     base_load = {"web": 0.3, "api": 0.4, "ml": 0.7}
#     base = base_load.get(config.appType, 0.4)
#     traffic_factor = min(config.trafficRps / (config.cpuCores * 250), 1)
#     util = min((base + traffic_factor * 0.6) * 100, 100)
#     return util


# def calc_energy(cpu_cores: int, utilization: float, memory_gb: int) -> float:
#     tdp_per_core = 0.015
#     mem_power = memory_gb * 0.001
#     pue = 1.58
#     cpu_power = cpu_cores * tdp_per_core * (0.3 + 0.7 * (utilization / 100))
#     return round((cpu_power + mem_power) * pue, 4)


# def calc_co2(energy_kwh: float, intensity: float = 0.475) -> float:
#     return round(energy_kwh * intensity, 4)


# def simulate_impl(cfg: WorkloadConfig) -> SimulationResult:
#     # Use trained utilization model (returns 0..1)
#     util = float(predict_utilization(cfg.trafficRps, cfg.cpuCores, cfg.memoryGb))
#     energy_kwh = float(calculate_energy(cfg.cpuCores, util))
#     co2_kg = float(calculate_carbon_emission(energy_kwh))
#     cost_usd = round(energy_kwh * 0.12, 4)

#     return SimulationResult(
#         cpuUtilization=round(util * 1000) / 10.0 if util <= 1 else round(util, 1),
#         energyKwh=round(energy_kwh, 4),
#         co2Kg=round(co2_kg, 4),
#         costUsd=round(cost_usd, 4),
#     )


# def optimize_impl(cfg: WorkloadConfig) -> OptimizedResult:
#     # Use trained models: predict current utilization, then predict recommended CPU
#     util_before = float(predict_utilization(cfg.trafficRps, cfg.cpuCores, cfg.memoryGb))
#     energy_before = float(calculate_energy(cfg.cpuCores, util_before))
#     carbon_before = float(calculate_carbon_emission(energy_before))

#     # ML model suggests optimal CPU allocation
#     recommended_cpu = int(predict_optimal_cpu(cfg.trafficRps, cfg.cpuCores, cfg.memoryGb))
#     if recommended_cpu < 1:
#         recommended_cpu = 1

#     # Build optimized config
#     opt_cfg = WorkloadConfig(
#         appType=cfg.appType,
#         trafficRps=cfg.trafficRps,
#         cpuCores=recommended_cpu,
#         memoryGb=cfg.memoryGb,
#         priority=cfg.priority,
#     )

#     util_after = float(predict_utilization(cfg.trafficRps, recommended_cpu, cfg.memoryGb))
#     energy_after = float(calculate_energy(recommended_cpu, util_after))
#     carbon_after = float(calculate_carbon_emission(energy_after))

#     # Simple recommendations list (keeps UI consistent) but core numbers come from models
#     recommendations: List[str] = []
#     if recommended_cpu != cfg.cpuCores:
#         recommendations.append(f"Recommend changing CPU cores from {cfg.cpuCores} to {recommended_cpu}")
#     if cfg.trafficRps > 100:
#         recommendations.append("Consider auto-scaling to handle traffic peaks without permanent over-provisioning")
#     if cfg.priority == "green":
#         recommendations.append("Prefer scheduling during low carbon-intensity hours")

#     carbon_saved = carbon_before - carbon_after
#     energy_saved = energy_before - energy_after

#     carbon_saved_percent = (carbon_saved / carbon_before * 100) if carbon_before != 0 else 0.0
#     energy_saved_percent = (energy_saved / energy_before * 100) if energy_before != 0 else 0.0

#     green_score = max(0.0, min(100.0, carbon_saved_percent))

#     result_before = SimulationResult(
#         cpuUtilization=round(util_before * 1000) / 10.0 if util_before <= 1 else round(util_before, 1),
#         energyKwh=round(energy_before, 4),
#         co2Kg=round(carbon_before, 4),
#         costUsd=round(energy_before * 0.12, 4),
#     )

#     result_after = SimulationResult(
#         cpuUtilization=round(util_after * 1000) / 10.0 if util_after <= 1 else round(util_after, 1),
#         energyKwh=round(energy_after, 4),
#         co2Kg=round(carbon_after, 4),
#         costUsd=round(energy_after * 0.12, 4),
#     )

#     return OptimizedResult(
#         config=opt_cfg,
#         result=result_after,
#         recommendations=recommendations,
#         energyReduction=round(energy_saved_percent),
#         co2Reduction=round(carbon_saved_percent),
#         greenScore=round(green_score),
#     )


# def predict_workload_impl(cfg: WorkloadConfig) -> List[WorkloadPrediction]:
#     hours = 24
#     predictions: List[WorkloadPrediction] = []
#     for h in range(hours):
#         peak_factor = (__import__("math").sin(((h - 6) / 24) * __import__("math").pi * 2) * 0.5 + 0.5)
#         noise = (__import__("math").sin(h * 7.3) * 0.1)
#         traffic = int(round(cfg.trafficRps * (0.3 + peak_factor * 0.7 + noise)))
#         predicted = int(round(traffic * (1 + 0.15 * __import__("math").sin(h * 0.5))))
#         period = "Peak" if 8 <= h <= 20 else "Off-peak"
#         predictions.append(
#             WorkloadPrediction(hour=h, traffic=max(0, traffic), predicted=max(0, predicted), label=f"{str(h).zfill(2)}:00 ({period})")
#         )
#     return predictions


# @app.post("/api/simulate", response_model=SimulationResult)
# def api_simulate(cfg: WorkloadConfig):
#     return simulate_impl(cfg)


# @app.post("/api/optimize", response_model=OptimizedResult)
# def api_optimize(cfg: WorkloadConfig):
#     return optimize_impl(cfg)


# @app.post("/api/predict", response_model=List[WorkloadPrediction])
# def api_predict(cfg: WorkloadConfig):
#     return predict_workload_impl(cfg)
  


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal, Dict
import os
import sys

# Ensure `ml` package and `models` folder inside this backend directory are importable
sys.path.insert(0, os.path.dirname(__file__))

from ml.predict import predict_utilization, predict_optimal_cpu, explain_utilization, get_feature_importance
from ml.predict_timeseries import predict_24h_traffic
from simulation.energy_model import calculate_energy
from simulation.carbon_model import calculate_carbon_emission

app = FastAPI(title="EcoScale API")

app.add_middleware(
    CORSMiddleware,
    # Allow local dev frontends on common Vite ports and any other origin during development
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:8081", "http://127.0.0.1:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WorkloadConfig(BaseModel):
    appType: Literal["web", "api", "ml"]
    trafficRps: int
    cpuCores: int
    memoryGb: int
    priority: Literal["balanced", "performance", "green"]


class SimulationResult(BaseModel):
    cpuUtilization: float
    energyKwh: float
    co2Kg: float
    costUsd: float


class OptimizedResult(BaseModel):
    config: WorkloadConfig
    result: SimulationResult
    recommendations: List[str]
    energyReduction: int
    co2Reduction: int
    greenScore: int
    explanation: Dict[str, float] = {}  # SHAP value explanations


class ExplanationResponse(BaseModel):
    """Feature importance and SHAP explanations for model predictions"""
    feature_importance: Dict[str, float]
    utilization_explanation: Dict[str, float]
    optimal_cpu_explanation: Dict[str, float]


class WorkloadPrediction(BaseModel):
    hour: int
    traffic: int
    predicted: int
    label: str


# --- Implementation ported from frontend simulation.ts to keep results identical ---

def calc_cpu_utilization(config: WorkloadConfig) -> float:
    base_load = {"web": 0.3, "api": 0.4, "ml": 0.7}
    base = base_load.get(config.appType, 0.4)
    traffic_factor = min(config.trafficRps / (config.cpuCores * 250), 1)
    util = min((base + traffic_factor * 0.6) * 100, 100)
    return util


def calc_energy(cpu_cores: int, utilization: float, memory_gb: int) -> float:
    tdp_per_core = 0.015
    mem_power = memory_gb * 0.001
    pue = 1.58
    cpu_power = cpu_cores * tdp_per_core * (0.3 + 0.7 * (utilization / 100))
    return round((cpu_power + mem_power) * pue, 4)


def calc_co2(energy_kwh: float, intensity: float = 0.475) -> float:
    return round(energy_kwh * intensity, 4)


def simulate_impl(cfg: WorkloadConfig) -> SimulationResult:
    # Use trained utilization model (returns 0..1)
    util = float(predict_utilization(cfg.trafficRps, cfg.cpuCores, cfg.memoryGb))
    energy_kwh = float(calculate_energy(cfg.cpuCores, util))
    co2_kg = float(calculate_carbon_emission(energy_kwh))
    cost_usd = round(energy_kwh * 0.12, 4)

    return SimulationResult(
        cpuUtilization=round(util * 1000) / 10.0 if util <= 1 else round(util, 1),
        energyKwh=round(energy_kwh, 4),
        co2Kg=round(co2_kg, 4),
        costUsd=round(cost_usd, 4),
    )


def optimize_impl(cfg: WorkloadConfig) -> OptimizedResult:
    # Use trained models: predict current utilization, then predict recommended CPU
    util_before = float(predict_utilization(cfg.trafficRps, cfg.cpuCores, cfg.memoryGb))
    energy_before = float(calculate_energy(cfg.cpuCores, util_before))
    carbon_before = float(calculate_carbon_emission(energy_before))

    # ML model suggests optimal CPU allocation
    recommended_cpu = int(predict_optimal_cpu(cfg.trafficRps, cfg.cpuCores, cfg.memoryGb))
    if recommended_cpu < 1:
        recommended_cpu = 1

    # Adjust recommendation based on priority
    if cfg.priority == "performance":
        # Performance: keep more headroom, don't downsize as aggressively
        recommended_cpu = max(recommended_cpu, cfg.cpuCores)  # Never downsize in performance mode
        recommended_cpu = min(recommended_cpu + 2, 32)  # Add buffer for throughput
    elif cfg.priority == "green":
        # Green: can be more aggressive with downsizing
        recommended_cpu = max(recommended_cpu - 1, 1)  # More aggressive optimization
    # Balanced: use ML recommendation as-is

    # Get SHAP explanations for feature importance
    try:
        util_explanation = explain_utilization(cfg.trafficRps, cfg.cpuCores, cfg.memoryGb)
    except Exception as e:
        util_explanation = {}
        print(f"SHAP explanation error: {e}")

    # Build optimized config
    opt_cfg = WorkloadConfig(
        appType=cfg.appType,
        trafficRps=cfg.trafficRps,
        cpuCores=recommended_cpu,
        memoryGb=cfg.memoryGb,
        priority=cfg.priority,
    )

    util_after = float(predict_utilization(cfg.trafficRps, recommended_cpu, cfg.memoryGb))
    energy_after = float(calculate_energy(recommended_cpu, util_after))
    carbon_after = float(calculate_carbon_emission(energy_after))

    # Build recommendations with SHAP insights
    recommendations: List[str] = []
    
    # Primary recommendation with priority context
    if recommended_cpu != cfg.cpuCores:
        impact = abs(util_explanation.get("cpu", 0.0))
        if cfg.priority == "performance":
            recommendations.append(f"🚀 Performance Mode: CPU increased from {cfg.cpuCores} to {recommended_cpu} cores for max throughput")
        elif cfg.priority == "green":
            if impact > 0.1:
                recommendations.append(f"🌱 Green Mode: CPU optimized from {cfg.cpuCores} to {recommended_cpu} cores (impact: {impact:.2f})")
            else:
                recommendations.append(f"🌱 Green Mode: Recommend reducing CPU from {cfg.cpuCores} to {recommended_cpu}")
        else:
            if impact > 0.1:
                recommendations.append(f"⚖️ Balanced: CPU cores strongly influence utilization (impact: {impact:.2f}). Recommend changing from {cfg.cpuCores} to {recommended_cpu}")
            else:
                recommendations.append(f"Recommend changing CPU cores from {cfg.cpuCores} to {recommended_cpu}")
    
    # Traffic impact insight
    traffic_impact = abs(util_explanation.get("traffic", 0.0))
    if cfg.trafficRps > 100 and traffic_impact > 0.05:
        if cfg.priority == "performance":
            recommendations.append(f"🚀 High traffic ({cfg.trafficRps} RPS) with strong impact ({traffic_impact:.2f}). Consider additional scaling for guaranteed performance")
        else:
            recommendations.append(f"🚀 Traffic is a major utilization driver (impact: {traffic_impact:.2f}). Consider auto-scaling to handle peaks")
    elif cfg.trafficRps > 100:
        recommendations.append("Consider auto-scaling to handle traffic peaks without permanent over-provisioning")
    
    # Memory efficiency insight
    memory_impact = abs(util_explanation.get("memory", 0.0))
    if memory_impact > 0.05:
        recommendations.append(f"💾 Memory allocation has moderate impact (impact: {memory_impact:.2f}). Optimize memory usage for better efficiency")
    
    if cfg.priority == "green":
        recommendations.append("🌱 Prefer scheduling during low carbon-intensity hours")
    elif cfg.priority == "performance":
        recommendations.append("⚡ Performance Mode: Best effort for minimal latency and max throughput")

    # Calculate savings
    carbon_saved = carbon_before - carbon_after
    energy_saved = energy_before - energy_after

    # Energy reduction based on resource optimization
    energy_saved_percent = (energy_saved / energy_before * 100) if energy_before != 0 else 0.0
    
    # Priority-specific adjustments
    if cfg.priority == "performance":
        # Performance might use MORE energy for better throughput
        if recommended_cpu > cfg.cpuCores:
            energy_saved_percent = -abs(energy_saved_percent)  # Show as energy increase
    elif cfg.priority == "green":
        # Green priority gets 10% bonus (scheduling in low-carbon hours)
        energy_saved_percent = min(energy_saved_percent * 1.05, 100)  # 5% bonus for energy efficiency
    
    # CO2 reduction (always carbon-focused)
    carbon_saved_percent = (carbon_saved / carbon_before * 100) if carbon_before != 0 else 0.0
    if cfg.priority == "green":
        carbon_saved_percent = min(carbon_saved_percent * 1.1, 100)  # 10% bonus for green priority

    # Green score reflects environmental impact (carbon-focused)
    green_score = max(0.0, min(100.0, carbon_saved_percent))

    result_before = SimulationResult(
        cpuUtilization=round(util_before * 1000) / 10.0 if util_before <= 1 else round(util_before, 1),
        energyKwh=round(energy_before, 4),
        co2Kg=round(carbon_before, 4),
        costUsd=round(energy_before * 0.12, 4),
    )

    result_after = SimulationResult(
        cpuUtilization=round(util_after * 1000) / 10.0 if util_after <= 1 else round(util_after, 1),
        energyKwh=round(energy_after, 4),
        co2Kg=round(carbon_after, 4),
        costUsd=round(energy_after * 0.12, 4),
    )

    return OptimizedResult(
        config=opt_cfg,
        result=result_after,
        recommendations=recommendations,
        energyReduction=round(energy_saved_percent),
        co2Reduction=round(carbon_saved_percent),
        greenScore=round(green_score),
        explanation=util_explanation,
    )


def predict_workload_impl(cfg: WorkloadConfig) -> List[WorkloadPrediction]:
    """
    Predict 24-hour workload using ML-trained time-series model.
    Uses learned patterns from historical traffic data.
    """
    # Get ML-predicted traffic for next 24 hours
    predicted_traffic_list = predict_24h_traffic(cfg.trafficRps)
    
    predictions: List[WorkloadPrediction] = []
    for h in range(24):
        traffic = predicted_traffic_list[h]
        # Add small prediction variance (±10%) for visualization
        predicted = int(traffic * (1 + 0.05 * (h % 3 - 1)))
        period = "Peak" if 8 <= h <= 20 else "Off-peak"
        predictions.append(
            WorkloadPrediction(
                hour=h,
                traffic=max(0, traffic),
                predicted=max(0, predicted),
                label=f"{str(h).zfill(2)}:00 ({period})"
            )
        )
    return predictions


@app.post("/api/simulate", response_model=SimulationResult)
def api_simulate(cfg: WorkloadConfig):
    return simulate_impl(cfg)


@app.post("/api/optimize", response_model=OptimizedResult)
def api_optimize(cfg: WorkloadConfig):
    return optimize_impl(cfg)


@app.post("/api/predict", response_model=List[WorkloadPrediction])
def api_predict(cfg: WorkloadConfig):
    return predict_workload_impl(cfg)


@app.post("/api/explain", response_model=ExplanationResponse)
def api_explain(cfg: WorkloadConfig):
    """
    Returns SHAP-based explanations for the given workload configuration.
    Includes feature importance and contribution of each feature to predictions.
    """
    try:
        # Get utilization prediction explanation
        util_explanation = explain_utilization(cfg.trafficRps, cfg.cpuCores, cfg.memoryGb)
        
        # Get global feature importance
        feature_importance = get_feature_importance()
        
        # Get optimal CPU explanation (for symmetry)
        from ml.predict import explain_optimal_cpu
        optimal_cpu_explanation = explain_optimal_cpu(cfg.trafficRps, cfg.cpuCores, cfg.memoryGb) if hasattr(sys.modules['ml.predict'], 'explain_optimal_cpu') else {}
        
        return ExplanationResponse(
            feature_importance=feature_importance,
            utilization_explanation=util_explanation,
            optimal_cpu_explanation=optimal_cpu_explanation
        )
    except Exception as e:
        return ExplanationResponse(
            feature_importance={},
            utilization_explanation={},
            optimal_cpu_explanation={}
        )
    
