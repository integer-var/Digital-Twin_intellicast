# orchestrator.py  (patched: decision latency + PDR placeholders)
import time
import json
import os
from datetime import datetime

from atsc_gateway import ATSCGateway
from upf_router import UPFRouter
from slice_manager import NetworkSliceManager
from zone_classifier import ZoneClassifier

STATE_FILE = "network_state.json"
TRIGGER_FILE = "sensor_trigger.json"
DECISION_LOG = "decision_log.json"

LOAD_THRESHOLD = 80.0
LATENCY_THRESHOLD = 50.0
CHECK_INTERVAL = 1.0  # seconds

class DigitalTwin:
    def __init__(self):
        self.validation_count = 0

    def validate_action(self, state, proposed_action):
        self.validation_count += 1
        current_load = state.get("live_load", 50.0)
        current_latency = state.get("latency", 10.0)

        # project improvements (conservative)
        if proposed_action == "OFFLOAD":
            projected_load = current_load * 0.6
            projected_latency = current_latency * 0.7

            # return tuple for logging
            success = (projected_load < LOAD_THRESHOLD and projected_latency < LATENCY_THRESHOLD) or state.get("disaster_intent", False)
            return {
                "validated": bool(success),
                "projected_load": round(projected_load,2),
                "projected_latency": round(projected_latency,2)
            }
        return {"validated": True, "projected_load": current_load, "projected_latency": current_latency}

class IntelliCastOrchestrator:
    def __init__(self):
        self.digital_twin = DigitalTwin()
        self.decision_count = 0
        self.decisions_log = []
        self.atsc = ATSCGateway()
        self.upf = UPFRouter()
        self.slicer = NetworkSliceManager()
        self.gis = ZoneClassifier()

        if not os.path.exists(STATE_FILE):
            self._init_state_file()
        # load existing decision log if present
        if os.path.exists(DECISION_LOG):
            try:
                with open(DECISION_LOG, "r") as f:
                    self.decisions_log = json.load(f)
            except:
                self.decisions_log = []

    def _init_state_file(self):
        initial_state = {
            "live_load": 50.0,
            "latency": 15.0,
            "jitter": 5.0,
            "offload_active": False,
            "ai_confidence": 0.0,
            "packet_loss": 0.0,
            "last_update": time.time()
        }
        with open(STATE_FILE, "w") as f:
            json.dump(initial_state, f, indent=4)

    def read_network_state(self):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except:
            return {"live_load":50.0,"latency":15.0,"jitter":5.0,"offload_active":False,"ai_confidence":0.0,"packet_loss":0.0}

    def read_ai_trigger(self):
        try:
            with open(TRIGGER_FILE, "r") as f:
                return json.load(f)
        except:
            return {"disaster_intent": False, "ai_confidence": 0.0, "timestamp": 0}

    def update_network_state(self, state):
        state["last_update"] = time.time()
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)

    def _log_decision(self, record):
        self.decisions_log.append(record)
        try:
            with open(DECISION_LOG, "w") as f:
                json.dump(self.decisions_log, f, indent=4)
        except Exception as e:
            print("⚠️ Failed to write decision log:", e)

    def estimate_pdr_improvement(self, state):
        # Placeholder physics: PDR improves as load reduces; use packet_loss from state if present
        packet_loss = state.get("packet_loss", 0.0)
        baseline_pdr = round(max(0.0, 100.0 - packet_loss*100), 2)  # crude
        projected_pdr = min(100.0, baseline_pdr + 10.0)  # assume +10% PDR after offload
        return {"baseline_pdr": baseline_pdr, "projected_pdr": projected_pdr}

    def make_decision(self, state, trigger):
        self.decision_count += 1
        current_load = state.get("live_load", 50.0)
        ai_confidence = trigger.get("ai_confidence", 0.0)
        ai_disaster = trigger.get("disaster_intent", False)
        state["ai_confidence"] = ai_confidence

        print(f"\n=== Decision Cycle #{self.decision_count} ===")
        print(f"Network Load: {current_load:.1f}%  AI Confidence: {ai_confidence:.3f}  AI Flag: {ai_disaster}")

        ai_trigger = ai_disaster and (ai_confidence > 0.90)
        load_trigger = current_load > LOAD_THRESHOLD
        should_offload = ai_trigger or load_trigger

        trigger_source = "NONE"
        if ai_trigger:
            trigger_source = "AI"
        elif load_trigger:
            trigger_source = "RULE"

        decision_record = {
            "timestamp": time.time(),
            "timestamp_human": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "network_load": current_load,
            "ai_confidence": ai_confidence,
            "trigger_source": trigger_source,
            "action": None,
            "validated": False,
            "decision_latency_ms": None,
            "baseline_pdr": None,
            "projected_pdr": None
        }

        if should_offload and not state.get("offload_active", False):
            t0 = time.time()
            # Digital Twin validation (returns dict)
            vt = self.digital_twin.validate_action(state, "OFFLOAD")
            t1 = time.time()
            decision_latency_ms = (t1 - t0) * 1000.0

            decision_record["decision_latency_ms"] = round(decision_latency_ms,2)
            decision_record["validated"] = bool(vt.get("validated", False))
            decision_record["projected_load"] = vt.get("projected_load")
            decision_record["projected_latency"] = vt.get("projected_latency")

            if vt.get("validated", False):
                print("✅ Digital Twin validated action. Executing OFFLOAD sequence...")
                zones = self.gis.classify_zones(state)
                self.slicer.create_emergency_slice()
                alert = "EMERGENCY ALERT: Please follow instructions."
                self.atsc.activate_emergency_broadcast(alert, zones)
                self.upf.redirect_public_traffic_to_atsc()

                state["offload_active"] = True
                state["live_load"] = round(state["live_load"] * 0.6,2)
                state["latency"] = round(state.get("latency",15.0) * 0.7,2)
                state["current_phase"] = "OFFLOADED"

                # estimate PDR effect
                pdr = self.estimate_pdr_improvement(state)
                decision_record["baseline_pdr"] = pdr["baseline_pdr"]
                decision_record["projected_pdr"] = pdr["projected_pdr"]

                decision_record["action"] = "OFFLOAD_ATSC_3.0"
                print("✅ Offload executed.")
            else:
                print("❌ Digital Twin rejected proposed action.")
                decision_record["action"] = "REJECTED_BY_TWIN"

        elif not should_offload and state.get("offload_active", False):
            print("🔄 Conditions recovered. Restoring normal operation.")
            t0 = time.time()
            self.atsc.deactivate_broadcast()
            self.upf.restore_normal_routing()
            self.slicer.delete_emergency_slice()
            t1 = time.time()
            decision_record["decision_latency_ms"] = round((t1 - t0) * 1000.0,2)
            state["offload_active"] = False
            state["current_phase"] = "NORMAL"
            decision_record["action"] = "RESTORE_NORMAL"

        else:
            print("— No action required this cycle.")
            decision_record["action"] = "NO_ACTION"

        # log & persist
        self._log_decision(decision_record)
        return state

    def run(self):
        print("🚀 Orchestrator: starting loop (ctrl-c to stop).")
        try:
            while True:
                state = self.read_network_state()
                trigger = self.read_ai_trigger()
                state = self.make_decision(state, trigger)
                self.update_network_state(state)

                print(f"Stats: decisions={self.decision_count}  validation_count={self.digital_twin.validation_count}")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("Orchestrator stopped by user.")

if __name__ == "__main__":
    orchestrator = IntelliCastOrchestrator()
    orchestrator.run()
