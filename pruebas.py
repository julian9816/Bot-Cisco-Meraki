from meraki_sdk import *
from meraki_sdk.meraki_sdk_client import MerakiSdkClient
from meraki_sdk.exceptions.api_exception import APIException

x_cisco_meraki_api_key = "1833bcc16a027bf707548bdce8a978e7c517153e"
meraki = MerakiSdkClient(x_cisco_meraki_api_key)
# controladores
networkid = "L_635570497412679705"
ssid_controller = meraki.ssids
update_network_ssid = {"name": "Prueba", "enabled": False, "authMode": "8021x-radius", "encryptionMode": "wpa",
                        "wpaEncryptionMode": "WPA2 only",
                        "radiusEnabled": True, "ipAssignmentMode": "Bridge mode",
                        "useVlanTagging": True, "defaultVlanId": 123, "minBitrate": 11, "bandSelection": "5 GHz band only",
                        "perClientBandwidthLimitUp": 0, "perClientBandwidthLimitDown": 0, "availableOnAllAps": True, "visible": True,
                        "lanIsolationEnabled": False, "splashPage": "None"}
radiusServers={"host": "192.168.1.1", "port": "3000", "secret":"null"}
update_network_ssid["radiusServers"] = [radiusServers]
collect = {}
collect["network_id"] = networkid
collect["number"] = 6
collect["update_network_ssid"] = update_network_ssid
try:
    ssid_controller.update_network_ssid(collect)
    print("Bien")
except APIException as e:
    print(e)

