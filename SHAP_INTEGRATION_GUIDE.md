# SHAP Explainability Integration Guide

## Overview
The backend now integrates SHAP (SHapley Additive exPlanations) for explainable AI, providing feature importance and SHAP value explanations for model predictions. This helps users understand WHY the models make specific recommendations.

## Backend Changes

### 1. **Enhanced OptimizedResult** (`main.py`)
Added an `explanation` field to the OptimizedResult response:
```python
class OptimizedResult(BaseModel):
    ...
    explanation: Dict[str, float] = {}  # SHAP value explanations (traffic, cpu, memory)
```

### 2. **SHAP-Enhanced Recommendations**
The `/api/optimize` endpoint now generates contextual recommendations based on SHAP feature importance:
- ⭐ **CPU Impact**: Shows if CPU allocation strongly influences utilization
- 🚀 **Traffic Impact**: Indicates if traffic is a major utilization driver
- 💾 **Memory Impact**: Shows memory allocation's impact on efficiency
- 🌱 **Green Priority**: Carbon-aware scheduling recommendations

Example output:
```
"⭐ CPU cores strongly influence utilization (impact: 0.42). Recommend changing from 4 to 8 cores"
"🚀 Traffic is a major utilization driver (impact: 0.38). Consider auto-scaling to handle peaks"
"💾 Memory allocation has moderate impact (impact: 0.15). Optimize memory usage for better efficiency"
```

### 3. **New Explanation Endpoint** (`/api/explain`)
```bash
POST /api/explain
{
  "appType": "web",
  "trafficRps": 150,
  "cpuCores": 4,
  "memoryGb": 8,
  "priority": "balanced"
}
```

Response:
```json
{
  "feature_importance": {
    "traffic": 0.45,
    "cpu": 0.35,
    "memory": 0.20
  },
  "utilization_explanation": {
    "traffic": 0.38,
    "cpu": 0.42,
    "memory": -0.05
  },
  "optimal_cpu_explanation": {
    "traffic": 0.50,
    "cpu": 0.25,
    "memory": 0.10
  }
}
```

## Frontend Integration

### 1. **Display SHAP Values in OptimizationPanel**
The explanation data is already included in the `/api/optimize` response:

```typescript
interface OptimizedResult {
  config: WorkloadConfig;
  result: SimulationResult;
  recommendations: string[];
  energyReduction: number;
  co2Reduction: number;
  greenScore: number;
  explanation?: Record<string, number>;  // Add this
}
```

### 2. **Render Recommendations with Insights**
The recommendations already include emojis and impact values. Display them as-is in the UI:

```typescript
recommendations.map((rec, i) => (
  <div key={i} className="flex items-start gap-2 p-2 bg-blue-50 rounded">
    <span className="text-lg">{rec}</span>
  </div>
))
```

### 3. **Create Explanation Visualization Component** (Optional)
Add a feature importance chart for better UX:

```typescript
// In ExplanationChart component
async function fetchExplanation(config: WorkloadConfig) {
  const response = await fetch('http://localhost:8000/api/explain', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config)
  });
  const data = await response.json();
  return data;
}
```

Then visualize:
- **Feature Importance Bar Chart**: Global importance across all predictions
- **SHAP Value Heatmap**: Per-feature contribution to specific prediction
- **Waterfall Plot**: How each feature pushes prediction up/down from base value

### 4. **Example Feature Card**
```typescript
<div className="p-4 border rounded-lg">
  <h3 className="font-bold">Why This Recommendation?</h3>
  
  <div className="mt-3 space-y-2">
    <FeatureImpact 
      name="Traffic"
      shapValue={explanation.traffic}
      importance={0.45}
    />
    <FeatureImpact 
      name="CPU Cores"
      shapValue={explanation.cpu}
      importance={0.35}
    />
    <FeatureImpact 
      name="Memory"
      shapValue={explanation.memory}
      importance={0.20}
    />
  </div>
</div>
```

## How to Use in Frontend

### Method 1: Parse Emoji-Enhanced Recommendations (Simple)
Already working! Just render the `recommendations` array as-is. The SHAP insights are baked into the text.

### Method 2: Use Raw SHAP Values (Advanced)
Fetch explanations separately for visualization:

```typescript
// In OptimizationPanel.tsx
const [explanation, setExplanation] = useState<ExplanationResponse>();

const handleOptimize = async (config: WorkloadConfig) => {
  const result = await optimizeAsync(config);
  
  // Fetch explanation data
  const explData = await fetch('/api/explain', {
    method: 'POST',
    body: JSON.stringify(config)
  }).then(r => r.json());
  
  setExplanation(explData);
};

// Then render explanation data as bar chart or table
```

## API Response Fields Explained

- **feature_importance**: Global importance of each feature across all predictions
  - Sum ~1.0
  - Higher = more influential to model decisions

- **utilization_explanation**: SHAP values for this specific workload
  - Positive = pushes utilization UP
  - Negative = pushes utilization DOWN

- **optimal_cpu_explanation**: SHAP values for CPU recommendation
  - Shows why model recommends specific CPU allocation

## Benefits

✅ **Transparency**: Users understand why recommendations are made  
✅ **Trust**: ML decisions backed by explainable insights  
✅ **Optimization**: Users can identify which factors to focus on  
✅ **Debugging**: Data team can validate model behavior  

## Testing

```bash
# Test the optimization endpoint with SHAP
curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "appType": "api",
    "trafficRps": 200,
    "cpuCores": 4,
    "memoryGb": 8,
    "priority": "balanced"
  }'

# Test the explanation endpoint
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{
    "appType": "api",
    "trafficRps": 200,
    "cpuCores": 4,
    "memoryGb": 8,
    "priority": "balanced"
  }'
```

## Next Steps

1. **Update frontend simulation.ts** to include explanation field in OptimizedResult interface
2. **Display recommendations** with their emoji/impact indicators
3. **Optional: Build visualization component** for feature importance charts
4. **Test end-to-end** with various workload configurations
