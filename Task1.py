import json
import unittest
import datetime
with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)
def convertFromFormat1(jsonObject):
    convertedObject = {}
    convertedObject["deviceID"] = jsonObject["deviceID"]
    convertedObject["deviceType"] = jsonObject["deviceType"]
    convertedObject["timestamp"] = jsonObject["timestamp"]
    location = jsonObject["location"].split("/")
    convertedObject["location"] = {
        "country": location[0],
        "city": location[1],
        "area": location[2],
        "factory": location[3],
        "section": location[4]
    }
    convertedObject["data"] = {
        "status": jsonObject["operationStatus"],
        "temperature": jsonObject["temp"]
    }
    return convertedObject
def convertFromFormat2(jsonObject):
    convertedObject = {}
    device = jsonObject["device"]
    convertedObject["deviceID"] = device["id"]
    convertedObject["deviceType"] = device["type"]
    timestamp = datetime.datetime.fromisoformat(jsonObject["timestamp"].replace("Z", ""))
    convertedObject["timestamp"] = int(timestamp.timestamp() * 1000)
    convertedObject["location"] = {
        "country": jsonObject["country"],
        "city": jsonObject["city"],
        "area": jsonObject["area"],
        "factory": jsonObject["factory"],
        "section": jsonObject["section"]
    }
    data = jsonObject["data"]
    convertedObject["data"] = {
        "status": data["status"],
        "temperature": data["temperature"]
    }
    return convertedObject
def main(jsonObject):
    result = {}
    if jsonObject.get('device') is None:
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)
    return result
class TestSolution(unittest.TestCase):
    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 1 failed')
    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 2 failed')
if __name__ == '__main__':
    unittest.main()
