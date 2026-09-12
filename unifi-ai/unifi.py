import os
import http.client
import json
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


key = os.getenv('UNIFI_KEY', None)


def network_request_setup():
    host = http.client.HTTPSConnection("api.ui.com")
    payload = ''
    headers = {
      'Accept': 'application/json',
      'X-API-Key': key
    }

    return host, payload, headers

def get_id():
    base, payload, headers = network_request_setup()
    base.request("GET", "/v1/sites", payload, headers)
    res = base.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    hostid = (json_data["data"][0]["hostId"])

    return hostid

def get_site_id(hostid):
    base, payload, headers = network_request_setup()
    base.request("GET", "/v1/connector/consoles/{}/proxy/network/integration/v1/sites".format(hostid), payload, headers)
    res = base.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    if __name__ == '__main__':
        print(json.dumps(json_data))

    siteid = (json_data["data"][0]["id"])
    return siteid 

def get_devices(hostid):
    base, payload, headers = network_request_setup()
    base.request("GET", "/v1/devices?hostIds%5B%5D={}".format(hostid), payload, headers)
    res = base.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    if __name__ == '__main__':
        print(json.dumps(json_data))

    return json.dumps(json_data)

def get_clients(siteid, hostid):
    base, payload, headers = network_request_setup()
    base.request("GET", "/v1/connector/consoles/{}/proxy/network/integration/v1/sites/{}/clients".format(hostid, siteid), payload, headers)
    res = base.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    if __name__ == '__main__':
        print(json.dumps(json_data))

    return json.dumps(json_data)

def get_host_by_id(hostid):
    base, payload, headers = network_request_setup()
    base.request("GET", "/v1/hosts/{}".format(hostid), payload, headers)
    res = base.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))

    return json.dumps(json_data["data"])


def get_acls(siteid, hostid):
    base, payload, headers = network_request_setup()
    base.request("GET", "/v1/connector/consoles/{}/proxy/network/integration/v1/sites/{}/acl-rules".format(hostid, siteid), payload, headers)
    res = base.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    if __name__ == '__main__':
        print(json.dumps(json_data))

    return json.dumps(json_data)

def get_firewall_policies(siteid, hostid):
    base, payload, headers = network_request_setup()
    base.request("GET", "/v1/connector/consoles/{}/proxy/network/integration/v1/sites/{}/firewall/policies".format(hostid, siteid), payload, headers)
    res = base.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    if __name__ == '__main__':
        print(json.dumps(json_data))

    return json.dumps(json_data["data"])

def get_traffic_matching_lists(siteid, hostid):
    base, payload, headers = network_request_setup()
    base.request("GET", "/v1/connector/consoles/{}/proxy/network/integration/v1/sites/{}/traffic-matching-lists".format(hostid, siteid), payload, headers)
    res = base.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    if __name__ == '__main__':
        print(json.dumps(json_data))

    return json.dumps(json_data["data"])

def get_wifi_broadcasts(siteid, hostid):
    base, payload, headers = network_request_setup()
    base.request("GET", "/v1/connector/consoles/{}/proxy/network/integration/v1/sites/{}/wifi/broadcasts".format(hostid, siteid), payload, headers)
    res = base.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    if __name__ == '__main__':
        print(json.dumps(json_data))

    return json.dumps(json_data["data"])

if __name__ == '__main__':
    hostid = get_id()
    #get_devices(hostid)
    siteid = get_site_id(hostid)
    #get_clients(siteid, hostid)
    #get_acls(siteid, hostid)
    #get_firewall_policies(siteid, hostid)
    get_traffic_matching_lists(siteid, hostid)
    get_wifi_broadcasts(siteid, hostid)
