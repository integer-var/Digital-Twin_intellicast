"""
IntelliCast LSTM AI Runner
Real-time network disaster prediction and orchestrator triggering
Replaces Edge Impulse model.eim script
"""
import time
import json
import random
import numpy as np
from tensorflow.keras.models import load_model
from datetime import datetime
import os

print("=" * 60)
print("🧠 IntelliCast LSTM AI Brain")
print("=" * 60)

# Configuration
MODEL_FILE = "intelli_lstm_model.h5"
CONFIG_FILE = "model_config.json"
TRIGGER_FILE = "sensor_trigger.json"
STATE_FILE = "network_state.json"

# Load model configuration
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
    WINDOW_SIZE = config["window_size"]
    FEATURES = config["features"]
    print(f"✅ Loaded config: Window={WINDOW_SIZE}, Features={FEATURES}")
else:
    WINDOW_SIZE = 50
    FEATURES = 3
    print("⚠️  No config found, using defaults")

# Load model
print(f"📦 Loading LSTM model from {MODEL_FILE}...")
try:
    model = load_model(MODEL_FILE)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("💡 Please run train_lstm.py first!")
    exit(1)

# Initialize sliding window buffer
buffer = []
prediction_count = 0

def read_live_telemetry():
    """Read live network telemetry from network_state.json"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
            
            load = state.get("live_load", 50.0)
            latency = state.get("latency", 10.0)
            jitter = state.get("jitter", 5.0)
            
            return [load, latency, jitter]
    except:
        pass
    
    # Fallback to simulation if no live data
    return generate_simulated_data()

def generate_simulated_data():
    """Generate simulated network telemetry for demo"""
    load = random.uniform(10, 90)
    latency = 10 + (load ** 1.5) / 100 + random.uniform(-2, 2)
    jitter = random.uniform(2, 15)
    return [load, latency, jitter]

def write_trigger(confidence, disaster=True):
    """Write trigger file for orchestrator"""
    trigger_data = {
        "disaster_intent": disaster,
        "ai_confidence": float(confidence),
        "timestamp": time.time(),
        "timestamp_human": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prediction_source": "LSTM_AI"
    }
    
    with open(TRIGGER_FILE, "w") as f:
        json.dump(trigger_data, f, indent=4)
    
    print(f"📝 Trigger file updated: disaster={disaster}, confidence={confidence:.3f}")

def main():
    global prediction_count
    
    print("\n🚀 Starting real-time prediction loop...")
    print(f"   Sampling rate: 5 Hz (0.2s interval)")
    print(f"   Window size: {WINDOW_SIZE} timesteps")
    print(f"   Emergency threshold: 0.90 confidence")
    print("\n" + "-" * 60)
    
    try:
        while True:
            # Get live or simulated data
            data = read_live_telemetry()
            
            # Add to sliding window buffer
            buffer.append(data)
            
            # Maintain window size
            if len(buffer) > WINDOW_SIZE:
                buffer.pop(0)
            
            # Only predict when buffer is full
            if len(buffer) == WINDOW_SIZE:
                # Prepare input for LSTM
                X = np.array(buffer).reshape(1, WINDOW_SIZE, FEATURES)
                
                # Make prediction
                pred = model.predict(X, verbose=0)[0]
                
                prob_normal = float(pred[0])
                prob_emergency = float(pred[1])
                
                prediction_count += 1
                
                # Display status
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Load:{data[0]:5.1f}% Lat:{data[1]:5.1f}ms Jit:{data[2]:4.1f}ms | "
                      f"AI: Normal={prob_normal:.3f} 🔥Emergency={prob_emergency:.3f}")
                
                # Check for emergency trigger
                if prob_emergency > 0.90:
                    print("\n" + "=" * 60)
                    print("🔴 AI DETECTED EMERGENCY → TRIGGERING ORCHESTRATOR")
                    print("=" * 60)
                    print(f"   Emergency Confidence: {prob_emergency:.3f}")
                    print(f"   Load: {data[0]:.1f}%")
                    print(f"   Latency: {data[1]:.1f}ms")
                    print(f"   Jitter: {data[2]:.1f}ms")
                    print("=" * 60 + "\n")
                    
                    # Write trigger file
                    write_trigger(prob_emergency, disaster=True)
                    
                    # Optional: Stop after first trigger (like original script)
                    # break
                    
                    # Wait before next check
                    time.sleep(2)
                else:
                    # Update trigger with normal status
                    write_trigger(prob_emergency, disaster=False)
            
            else:
                # Still filling buffer
                print(f"📊 Filling buffer... {len(buffer)}/{WINDOW_SIZE}")
            
            # Sleep for 5Hz sampling (0.2 seconds)
            time.sleep(0.2)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  AI Brain stopped by user")
        print(f"   Total predictions made: {prediction_count}")
        print("=" * 60)

if __name__ == "__main__":
    main()
