from time import sleep
from datetime import datetime

from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
from devices.device import refresh_list


def main(devices):
    devices_codes = []
    for device in devices:
        res_str = str(datetime.now()) + "\n" + device[0]["device"] + "\n" + device[0]["model"] + "\n"
        mibs = [i for i in device[0]["mibs"]]
        res = [int(i) for i in get_info([item["mib"] for item in mibs], device[1])]

        res_arr = list(zip(res, mibs))
        error_exist = False
        for item in res_arr:
            code = item[0]
            mib = item[1]
            if code != 0 and mib["value_type"] == "error":
                error_exist = True
            res_str += mib["name"] + ": "
            if mib["value_type"] == "error":
                res_str += mib["codes"][str(code)].capitalize() + "\n"
            else:
                res_str += str(code) + "\n"

        print(res_str)
        devices_codes.append((device[0]["model"], error_exist))

        with open(device[0]["model"].replace(" ", "_") + ".html", "w") as file:
            template = open("template.html", "r").read()
            arr = ["<p>" + item + "</p>" for item in res_str.split("\n")]

            file.write(template)
            file.write("<body>")
            file.writelines(arr)
            file.write("</body>")

    with open("index.html", "w") as file:
        template = open("template.html", "r").read()
        arr = ["<p>"
               + f'<a style="color:{"#FF0000" if item[1] else "#008000"}"' \
                 f' href="{item[0].replace(" ", "_") + ".html"}";>'
               + item[0]
               + "</a>"
               + "</p>" for item in devices_codes]

        file.write(template)
        file.write("<body>")
        file.writelines(arr)
        file.write("</body>")


def get_info(codes, ip):
    code_arr = []

    for item in codes:
        try:
            error_indication, error_status, error_index, var_bind_table = cmdgen.CommandGenerator().nextCmd(
                cmdgen.CommunityData('public'),
                cmdgen.UdpTransportTarget((ip, 161)),
                item
            )
            for i in var_bind_table[0]:
                code_arr.append(i[1])
        except Exception as ex:
            print(ex)
    return code_arr


if __name__ == "__main__":
    while True:
        try:
            main(refresh_list())
        except Exception as ex:
            print(ex)

        sleep(10)
