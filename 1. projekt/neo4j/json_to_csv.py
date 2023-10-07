#!/bin/env/python3

import json


def main():
    with open("kod.brno.cz.json", encoding="utf-8") as f:
        data = json.loads(f.read())["data"]

    with open("data.csv", "w", encoding="utf-8") as f:
        f.write("id,subject,time,result,party,name,vote\n")
        for voting in data:
            for party in voting["parties"]:
                for voter in party["votes"]:
                    # Skip invalid - cant vote for no subject
                    if voting['subject'] == "": continue 

                    # When missing code, insert ??? as placeholder
                    if str(voting['code']) == "": voting['code'] = "???"

                    # Parse subject string to csv-compliant format
                    subject = str(voting['subject']).replace('"', '""')

                    # Write to file
                    f.write(f"{voting['code'] + '-' + str(voting['number'])},\"{subject}\",{voting['datetime']},{voting['result']},{party['name']},{voter['voter']},{voter['option']}\n")

if __name__ == "__main__":
    main()