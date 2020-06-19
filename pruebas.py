from meraki_sdk import *
from meraki_sdk.meraki_sdk_client import MerakiSdkClient
from meraki_sdk.exceptions.api_exception import APIException

x_cisco_meraki_api_key = "1833bcc16a027bf707548bdce8a978e7c517153e"
meraki = MerakiSdkClient(x_cisco_meraki_api_key)
organization_id={"id":"921480"}
networks=meraki.networks.get_organization_networks({"organization_id":"921480"})
print(networks)
# controladores
networkid = "L_635570497412679705"
ssid_controller = meraki.ssids
update_network_ssid = {"name": "Prueba_radius", "enabled": True, "radiusEnabled": True,
"radiusAttributeForGroupPolicies": "Filter-Id", "authMode": "8021x-meraki", "encryptionMode": "wpa",
"wpaEncryptionMode": "WPA2 only", "useVlanTagging": True, "defaultVlanId": 123, "lanIsolationEnabled": False,
"minBitrate": 11, "bandSelection": "Dual band operation", "perClientBandwidthLimitUp": 0,
 "perClientBandwidthLimitDown": 0, "availableOnAllAps": True, "visible": True, "splashPage": "None",
 "ipAssignmentMode" : "Bridge mode"}
collect = {}
collect["network_id"] = networkid
collect["number"] = 6
collect["update_network_ssid"] = update_network_ssid
try:
    ssid_controller.update_network_ssid(collect)
    print("Bien")
except APIException as e:
    print(e)

