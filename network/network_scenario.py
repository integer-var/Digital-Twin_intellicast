"""
IntelliCast Network Telemetry Simulator
Generates realistic network KPI streams for testing
Simulates: Normal → Gradual Increase → Emergency → Recovery
"""
import time
import json
import random
import math
from datetime import datetime

print("=" * 60)
print("📡 IntelliCast Network Telemetry Simulator")
print("=" * 60)

STATE_FILE = "network_state.json"
SCENARIO_FILE = "scenario_config.json"

class NetworkSimulator:
    """Simulates realistic network behavior"""
    
    def __init__(self):
        self.time_step = 0
        self.scenario = "NORMAL"
        self.load_base = 30.0
        self.scenario_start_time = time.time()
        
        # Load scenario configuration
        self.load_scenario()
    
    def load_scenario(self):
        """Load or create scenario configuration"""
        try:
            with open(SCENARIO_FILE, "r") as f:
                config = json.load(f)
            print(f"✅ Loaded scenario: {config.get('type', 'NORMAL')}")
        except:
            # Default scenario
            config = {
                "type": "AUTO_CYCLE",
                "phases": [
                    {"name": "NORMAL", "duration": 30, "load_range": [30, 50]},
                    {"name": "INCREASING", "duration": 20, "load_range": [50, 85]},
                    {"name": "EMERGENCY", "duration": 15, "load_range": [85, 95]},
                    {"name": "RECOVERY", "duration": 25, "load_range": [60, 40]}
                ]
            }
            with open(SCENARIO_FILE, "w") as f:
                json.dump(config, f, indent=4)
            print("✅ Created default scenario configuration")
    
    def get_current_phase(self):
        """Determine current scenario phase"""
        elapsed = time.time() - self.scenario_start_time
        
        # Cycle through phases
        total_duration = 30 + 20 + 15 + 25  # 90 seconds total cycle
        phase_time = elapsed % total_duration
        
        if phase_time < 30:
            return "NORMAL", phase_time / 30
        elif phase_time < 50:
            return "INCREASING", (phase_time - 30) / 20
        elif phase_time < 65:
            return "EMERGENCY", (phase_time - 50) / 15
        else:
            return "RECOVERY", (phase_time - 65) / 25
    
    def generate_telemetry(self):
        """Generate realistic network telemetry"""
        self.time_step += 1
        
        # Get current phase
        phase, progress = self.get_current_phase()
        
        # Generate load based on phase
        if phase == "NORMAL":
            load = 30 + random.uniform(0, 20) + 5 * math.sin(self.time_step * 0.1)
        elif phase == "INCREASING":
            # Gradual increase
            load = 50 + progress * 35 + random.uniform(-5, 5)
        elif phase == "EMERGENCY":
            # High load with spikes
            load = 85 + random.uniform(0, 10) + 5 * math.sin(self.time_step * 0.5)
        else:  # RECOVERY
            # Gradual decrease
            load = 60 - progress * 20 + random.uniform(-3, 3)
        
        # Clamp load
        load = max(10, min(95, load))
        
        # Calculate dependent metrics
        latency = 10 + (load ** 1.5) / 100 + random.uniform(-2, 3)
        jitter = 3 + (load / 20) + random.uniform(0, 5)
        
        # Calculate packet loss (increases with load)
        packet_loss = max(0, (load - 60) / 40) * random.uniform(0.5, 2.0)
        
        return {
            "live_load": round(load, 2),
            "latency": round(latency, 2),
            "jitter": round(jitter, 2),
            "packet_loss": round(packet_loss, 3),
            "phase": phase,
            "timestamp": time.time(),
            "timestamp_human": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def run(self):
        """Main simulation loop"""
        print("\n🚀 Starting network simulation...")
        print("   Update rate: 5 Hz (0.2s interval)")
        print("   Scenario: AUTO_CYCLE (Normal → Increasing → Emergency → Recovery)")
        print("\n" + "-" * 60 + "\n")
        
        last_phase = None
        
        try:
            while True:
                # Generate telemetry
                telemetry = self.generate_telemetry()
                
                # Detect phase change
                if telemetry["phase"] != last_phase:
                    print(f"\n{'='*60}")
                    print(f"🔄 PHASE CHANGE: {telemetry['phase']}")
                    print(f"{'='*60}\n")
                    last_phase = telemetry["phase"]
                
                # Display telemetry
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Phase: {telemetry['phase']:12s} | "
                      f"Load: {telemetry['live_load']:5.1f}% | "
                      f"Latency: {telemetry['latency']:5.1f}ms | "
                      f"Jitter: {telemetry['jitter']:4.1f}ms | "
                      f"Loss: {telemetry['packet_loss']:4.2f}%")
                
                # Read existing state to preserve orchestrator data
                try:
                    with open(STATE_FILE, "r") as f:
                        existing_state = json.load(f)
                    
                    # Preserve offload status and AI confidence
                    telemetry["offload_active"] = existing_state.get("offload_active", False)
                    telemetry["ai_confidence"] = existing_state.get("ai_confidence", 0.0)
                except:
                    telemetry["offload_active"] = False
                    telemetry["ai_confidence"] = 0.0
                
                # Write state
                with open(STATE_FILE, "w") as f:
                    json.dump(telemetry, f, indent=4)
                
                # Wait for next update
                time.sleep(0.2)  # 5 Hz
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Simulator stopped by user")
            print(f"   Total updates: {self.time_step}")
            print("=" * 60)

if __name__ == "__main__":
    simulator = NetworkSimulator()
    simulator.run()
