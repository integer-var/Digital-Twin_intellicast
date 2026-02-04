# Digital-Twin_intellicast
IntelliCast_real is an AI-native closed-loop 5G network proof-of-concept that demonstrates how artificial intelligence can sense, predict, decide, and reconfigure a live network in real time.

# 🧠 IntelliCast: AI-Native Network Orchestration System

## Overview

IntelliCast is a complete AI-native closed-loop orchestration system that combines:
- **LSTM Neural Network** for disaster prediction
- **Rule-based logic** for safety validation
- **Digital Twin** for action verification
- **Real-time dashboard** for monitoring
- **Closed-loop control** for network reconfiguration

This system replaces the Edge Impulse model with a production-ready LSTM implementation while maintaining full integration with the orchestrator and digital twin.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  IntelliCast Architecture                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📡 Network Telemetry (network_scenario.py)                 │
│       │                                                      │
│       ├──→ network_state.json                               │
│       │                                                      │
│       ↓                                                      │
│  🧠 LSTM AI Brain (lstm_ai_runner.py)                       │
│       │                                                      │
│       ├──→ sensor_trigger.json                              │
│       │                                                      │
│       ↓                                                      │
│  🎯 Orchestrator (orchestrator.py)                          │
│       │                                                      │
│       ├──→ AI Trigger Check                                 │
│       ├──→ Rule-based Check                                 │
│       │                                                      │
│       ↓                                                      │
│  🔬 Digital Twin Validation                                 │
│       │                                                      │
│       ├──→ Simulate Action                                  │
│       ├──→ Verify Safety                                    │
│       │                                                      │
│       ↓                                                      │
│  🚀 Network Reconfiguration                                 │
│       │                                                      │
│       ├──→ Update network_state.json                        │
│       ├──→ Log decision_log.json                            │
│       │                                                      │
│       ↓                                                      │
│  📊 Streamlit Dashboard (dashboard.py)                      │
│       │                                                      │
│       └──→ Real-time Visualization                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Python 3.8+
- pip3

### Step 1: Install Dependencies

```bash
# Install Python packages
pip3 install -r requirements.txt

# If you encounter issues, install with --break-system-packages flag
pip3 install tensorflow numpy scikit-learn streamlit plotly pandas --break-system-packages
```

### Step 2: Train LSTM Model

```bash
# Train the LSTM model (one-time setup)
python3 train_lstm.py
```

This will:
- Generate synthetic training data (2000 samples)
- Train LSTM model with 50 timesteps
- Save model to `intelli_lstm_model.h5`
- Create `model_config.json`
- Display training accuracy

Expected output:
```
✅ Test Accuracy: 95%+
💾 Model saved to: intelli_lstm_model.h5
```

---

## 🚀 Running the System

The system requires **4 terminals** running simultaneously:

### Terminal 1: Network Telemetry Simulator
```bash
python3 network_scenario.py
```
**Purpose**: Generates realistic network KPIs (load, latency, jitter)  
**Output**: Updates `network_state.json` at 5Hz  
**Scenario**: AUTO_CYCLE (Normal → Increasing → Emergency → Recovery)

### Terminal 2: Orchestrator
```bash
python3 orchestrator.py
```
**Purpose**: Makes orchestration decisions based on AI + rules  
**Reads**: `network_state.json`, `sensor_trigger.json`  
**Writes**: `network_state.json`, `decision_log.json`  
**Features**: Digital twin validation, closed-loop control

### Terminal 3: Dashboard
```bash
streamlit run dashboard.py
```
**Purpose**: Real-time visualization  
**Access**: Open browser to `http://localhost:8501`  
**Shows**: Network metrics, AI confidence, decisions, gauges

### Terminal 4: LSTM AI Brain
```bash
python3 lstm_ai_runner.py
```
**Purpose**: Real-time disaster prediction  
**Reads**: `network_state.json`  
**Writes**: `sensor_trigger.json`  
**Model**: LSTM with 50-timestep sliding window

---

## 📊 System Files

| File | Purpose | Updated By |
|------|---------|------------|
| `network_state.json` | Current network KPIs | Simulator, Orchestrator |
| `sensor_trigger.json` | AI predictions | LSTM AI Brain |
| `decision_log.json` | Orchestration history | Orchestrator |
| `model_config.json` | LSTM configuration | Training script |
| `intelli_lstm_model.h5` | Trained LSTM model | Training script |
| `scenario_config.json` | Simulation scenario | Simulator |

---

## 🧠 Key Features

### 1. LSTM AI Brain
- **Input**: 50 timesteps × 3 features (load, latency, jitter)
- **Output**: Emergency confidence score (0.0 - 1.0)
- **Sampling**: 5Hz (200ms interval)
- **Trigger**: Confidence > 0.90

### 2. Hybrid Decision Logic
```python
ai_trigger = (ai_confidence > 0.90) and disaster_intent
rule_trigger = (network_load > 80%)
should_offload = ai_trigger OR rule_trigger
```

### 3. Digital Twin Validation
- Simulates network behavior after proposed action
- Projects load and latency changes
- Validates safety before execution
- Prevents harmful decisions

### 4. Closed-Loop Control
- Continuous monitoring
- Automatic decision making
- State feedback
- Adaptive response

---

## 🎓 Research Significance

This system demonstrates:

1. **ITU-T Y.3172 Compliance**: AI-native closed-loop orchestration
2. **ML-Physical Hybrid**: Neural networks + physics-based validation
3. **Production-Ready**: Digital twin safety, real-time monitoring
4. **Publishable Architecture**: Novel integration of AI, DT, and control theory

### Paper Keywords
- AI-native networking
- LSTM time-series prediction
- Digital twin validation
- Closed-loop orchestration
- 5G network intelligence
- Smart city infrastructure

---

## 📈 Performance Metrics

### LSTM Model
- **Training Accuracy**: ~95%
- **Inference Time**: <10ms per prediction
- **Window Size**: 50 timesteps (10 seconds at 5Hz)
- **Features**: 3 (load, latency, jitter)

### System Latency
- **AI Prediction**: 5Hz (200ms cycle)
- **Orchestrator Decision**: 1Hz (1s cycle)
- **Dashboard Update**: Configurable (0.5-5s)
- **End-to-end**: ~1.2s (trigger to action)

---

## 🔧 Customization

### Change AI Confidence Threshold
Edit `lstm_ai_runner.py`:
```python
if prob_emergency > 0.90:  # Change to 0.85, 0.95, etc.
```

### Change Load Threshold
Edit `orchestrator.py`:
```python
LOAD_THRESHOLD = 80.0  # Change to 70.0, 85.0, etc.
```

### Change Scenario
Edit `scenario_config.json` or modify `network_scenario.py` phases.

### Retrain Model
Modify `train_lstm.py` to use your own dataset:
```python
X = np.load("your_dataset.npy")
y = np.load("your_labels.npy")
```

---

## 🐛 Troubleshooting

### Model not found
```
❌ Error loading model: intelli_lstm_model.h5
💡 Please run train_lstm.py first!
```
**Solution**: Run `python3 train_lstm.py`

### No data in dashboard
```
⚠️ No data available. Please start network_scenario.py first.
```
**Solution**: Start `python3 network_scenario.py` in Terminal 1

### TensorFlow import error
```
ModuleNotFoundError: No module named 'tensorflow'
```
**Solution**: `pip3 install tensorflow --break-system-packages`

---

## 📝 Quick Start (All-in-One)

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Train model
python3 train_lstm.py

# 3. Open 4 terminals and run:
# Terminal 1:
python3 network_scenario.py

# Terminal 2:
python3 orchestrator.py

# Terminal 3:
streamlit run dashboard.py

# Terminal 4:
python3 lstm_ai_runner.py
```

---

## 🎯 Expected Behavior

1. **Normal Phase (0-30s)**:
   - Load: 30-50%
   - AI Confidence: <0.5
   - Status: Normal ✅

2. **Increasing Phase (30-50s)**:
   - Load: 50-85%
   - AI Confidence: Rising
   - Status: Warning ⚠️

3. **Emergency Phase (50-65s)**:
   - Load: 85-95%
   - AI Confidence: >0.90 🔴
   - Action: Orchestrator triggers offload
   - Digital Twin: Validates action
   - Result: Load drops to ~60%

4. **Recovery Phase (65-90s)**:
   - Load: 40-60%
   - AI Confidence: Decreasing
   - Status: Returning to normal

---

## 🌟 Advantages Over Edge Impulse

| Feature | Edge Impulse | LSTM (This System) |
|---------|--------------|-------------------|
| Training | Cloud-based GUI | Local Python script |
| Customization | Limited | Full control |
| Model Type | NN classifier | LSTM time-series |
| Deployment | .eim binary | Standard .h5 format |
| Integration | External tool | Native Python |
| Research | Proprietary | Open, publishable |

---

## 📚 Next Steps

1. **Real Network Integration**: Replace `network_scenario.py` with Mininet/Open5GS telemetry
2. **Model Enhancement**: Train on real network data
3. **Advanced Features**: Add GRU, Transformer, or attention mechanisms
4. **ROS2 Integration**: Convert to ROS2 nodes for robotic systems
5. **Paper Writing**: Document methodology for IEEE/ACM publication

---

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Examine the log files (`decision_log.json`)

---

## 🏆 Achievements

✅ **LSTM-based AI prediction**  
✅ **Digital twin validation**  
✅ **Closed-loop control**  
✅ **Real-time dashboard**  
✅ **Production-ready architecture**  
✅ **Research-grade implementation**  

---

**Built with ❤️ for AI-Native Networking Research**
