from devices.CDM570 import cdm570
from devices.CDM570L import cdm570L

device_list = [cdm570, cdm570L]


def refresh_list():
    with open("devices/config.txt", "r") as config:
        lines = [line.replace("\n", "").split(" ") for line in config.readlines()]
        nums = [int(line[0]) for line in lines]
        ips = [line[1] for line in lines]
        devices = [device_list[i - 1] for i in nums]

        return list(zip(devices, ips))


device = {
    "device": "type",
    "model": "model",
    "mibs": [
        {
            "mib": "mib num",
            "name": "name",
            "value_type": "error",
            "codes": {
                "0" : ""
            }
        },
        {
            "mib": "mib num",
            "name": "name",
            "value_type": "value",
        }
    ],
}