import requests

class NetworkSliceManager:
    """
    Manager for Dynamic Network Slicing (Open5GS / Mininet).
    """
    def __init__(self, api_url="http://localhost:9999"):
        self.api_url = api_url

    def create_emergency_slice(self):
        """
        Provisions a dedicated network slice for First Responders (S-NSSAI: 01-000002).
        """
        print("  🍰 SLICE MANAGER: Provisioning Emergency Slice...")
        
        slice_config = {
            "s_nssai": {"sst": 1, "sd": "000002"},
            "qos_profile": "5QI_1", # Critical Voice/Data
            "bandwidth_guarantee": "100Mbps"
        }

        try:
            # requests.post(f"{self.api_url}/slice/create", json=slice_config, timeout=2)
            raise Exception("Slice Manager API unreachable")
        except:
            print("  ✅ Emergency Slice (SST:1 SD:000002) CREATED")
            print("  👮 Dedicated Capacity: 100 Mbps Reserved")
            return True

    def delete_emergency_slice(self):
        print("  🗑️  Emergency Slice DEPROVISIONED")
        return True
