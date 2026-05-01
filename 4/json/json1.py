import json

with open("sample-data.json") as f:
    data = json.load(f)
print("Interface Status")
print("=" * 70)
print(f"{'DN':45} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 70)

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    
    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")
    
    print(f"{dn:45} {descr:20} {speed:8} {mtu:6}")