# from ml.predict import predict_utilization, predict_optimal_cpu
# from simulation.energy_model import calculate_energy
# from simulation.carbon_model import calculate_carbon_emission


# def run_pipeline(traffic: int, cpu: int, memory: int):
#     """
#     Full ML-based carbon optimization pipeline.
#     Returns structured before vs after results.
#     """

#     # -------------------------
#     # STEP 1: CURRENT STATE
#     # -------------------------

#     current_utilization = predict_utilization(traffic, cpu, memory)

#     energy_before = calculate_energy(cpu, current_utilization)
#     carbon_before = calculate_carbon_emission(energy_before)

#     # -------------------------
#     # STEP 2: ML OPTIMIZATION
#     # -------------------------

#     recommended_cpu = predict_optimal_cpu(traffic, cpu, memory)

#     # Safety check
#     if recommended_cpu < 1:
#         recommended_cpu = 1

#     # Predict utilization after optimization
#     optimized_utilization = predict_utilization(
#         traffic, recommended_cpu, memory
#     )

#     energy_after = calculate_energy(recommended_cpu, optimized_utilization)
#     carbon_after = calculate_carbon_emission(energy_after)

#     # -------------------------
#     # STEP 3: METRICS
#     # -------------------------

#     carbon_reduction = carbon_before - carbon_after

#     if carbon_before != 0:
#         reduction_percent = (carbon_reduction / carbon_before) * 100
#     else:
#         reduction_percent = 0

#     # -------------------------
#     # FINAL RESPONSE
#     # -------------------------

#     return {
#         "input": {
#             "traffic": traffic,
#             "cpu": cpu,
#             "memory": memory
#         },
#         "before": {
#             "utilization": round(current_utilization, 4),
#             "energy_kwh": round(energy_before, 4),
#             "carbon_kg": round(carbon_before, 4)
#         },
#         "after": {
#             "recommended_cpu": recommended_cpu,
#             "utilization": round(optimized_utilization, 4),
#             "energy_kwh": round(energy_after, 4),
#             "carbon_kg": round(carbon_after, 4)
#         },
#         "impact": {
#             "carbon_saved_kg": round(carbon_reduction, 4),
#             "carbon_saved_percent": round(reduction_percent, 2)
#         }
#     }



"""
ML Optimization Integrator (B2) - Carbon Minimization Version
-------------------------------------------------------------
Uses ML ONLY to predict utilization.

Then performs an optimization search over CPU choices (1..16) to
select the CPU that minimizes carbon emissions (with safety constraints).

Outputs a clean before/after JSON-style dict.
"""

from ml.predict import predict_utilization
from simulation.energy_model import calculate_energy
from simulation.carbon_model import calculate_carbon_emission


def _clamp_int(x: int, lo: int, hi: int) -> int:
    return max(lo, min(int(x), hi))


def run_pipeline(
    traffic: int,
    cpu: int,
    memory: int,
    region: str = "default",
    cpu_min: int = 1,
    cpu_max: int = 16,
    util_sla_max: float = 0.85,   # performance safety: keep util <= this
):
    """
    Args:
        traffic, cpu, memory: input configuration
        region: used by carbon model (region-aware intensity)
        cpu_min/cpu_max: search range
        util_sla_max: if utilization exceeds this, config is considered "risky"
                     and we penalize it (so optimizer avoids it)

    Returns:
        dict with before/after + impact metrics.
    """

    # ---------
    # Validate
    # ---------
    traffic = _clamp_int(traffic, 1, 1_000_000)
    cpu = _clamp_int(cpu, cpu_min, cpu_max)
    memory = _clamp_int(memory, 1, 2048)

    cpu_min = _clamp_int(cpu_min, 1, cpu_max)
    cpu_max = _clamp_int(cpu_max, cpu_min, 128)  # allow higher if you want later

    # -------------------------
    # STEP 1: CURRENT (BEFORE)
    # -------------------------
    util_before = float(predict_utilization(traffic, cpu, memory))
    energy_before = float(calculate_energy(cpu, util_before))
    carbon_before = float(calculate_carbon_emission(energy_before, region=region))

    # -----------------------------------
    # STEP 2: SEARCH BEST CPU (OPTIMIZE)
    # -----------------------------------
    best_cpu = cpu
    best_util = util_before
    best_energy = energy_before
    best_carbon = carbon_before

    # penalty for violating SLA (keeps it realistic)
    # if util is too high -> carbon score becomes worse so it won't be chosen
    SLA_PENALTY_MULTIPLIER = 1.25

    for test_cpu in range(cpu_min, cpu_max + 1):
        test_util = float(predict_utilization(traffic, test_cpu, memory))
        test_energy = float(calculate_energy(test_cpu, test_util))
        test_carbon = float(calculate_carbon_emission(test_energy, region=region))

        # Apply SLA penalty if too risky
        score = test_carbon
        if test_util > util_sla_max:
            score = test_carbon * SLA_PENALTY_MULTIPLIER

        # Minimize score
        if score < best_carbon:
            best_cpu = test_cpu
            best_util = test_util
            best_energy = test_energy
            best_carbon = test_carbon

    # -------------------------
    # STEP 3: IMPACT METRICS
    # -------------------------
    carbon_saved = carbon_before - best_carbon
    energy_saved = energy_before - best_energy

    carbon_saved_percent = (carbon_saved / carbon_before * 100) if carbon_before != 0 else 0.0
    energy_saved_percent = (energy_saved / energy_before * 100) if energy_before != 0 else 0.0

    # Simple green score (optional): higher = better
    green_score = max(0.0, min(100.0, carbon_saved_percent))

    # -------------------------
    # FINAL RESPONSE
    # -------------------------
    return {
        "input": {
            "traffic": traffic,
            "cpu": cpu,
            "memory": memory,
            "region": region,
            "util_sla_max": util_sla_max,
            "cpu_search_range": [cpu_min, cpu_max],
        },
        "before": {
            "utilization": round(util_before, 4),
            "energy_kwh": round(energy_before, 4),
            "carbon_kg": round(carbon_before, 4),
        },
        "after": {
            "recommended_cpu": int(best_cpu),
            "utilization": round(best_util, 4),
            "energy_kwh": round(best_energy, 4),
            "carbon_kg": round(best_carbon, 4),
        },
        "impact": {
            "energy_saved_kwh": round(energy_saved, 4),
            "energy_saved_percent": round(energy_saved_percent, 2),
            "carbon_saved_kg": round(carbon_saved, 4),
            "carbon_saved_percent": round(carbon_saved_percent, 2),
            "green_score": round(green_score, 2),
        },
    }