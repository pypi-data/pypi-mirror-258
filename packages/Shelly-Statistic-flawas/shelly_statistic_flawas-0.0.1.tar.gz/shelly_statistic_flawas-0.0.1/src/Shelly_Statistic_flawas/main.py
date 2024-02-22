import requests, json
# "https://shelly-21-eu.shelly.cloud/device/status"
def checkCloudStatus(url, devid, authkey):
    j = json.loads(getData(url, devid, authkey))
    if (j["data"]["online"] == True):
        return True
    else:
        return False


def getData(url, devid, authkey):
    data = {'id': devid, 'auth_key': authkey}
    reply = requests.post(url, data=data)
    return reply.content


def getEnergyTotal(devid, authkey):
    j = json.loads(getData(devid, authkey))
    return j["data"]["device_status"]["switch:0"]["aenergy"]["total"]
