#!/bin/env/python3

import json


def main():
    with open("kod.brno.cz.json", encoding="utf-8") as f:
        data = json.loads(f.read())["data"]
    
    with open("load_data.cypher") as f:
        for voting in data:
            # Node for subject of voting
            subj_str =  'MERGE (subject:Subject {name:' + voting["subject"] + '})' + \
                        'ON CREATE SET subject.result = ' + voting["result"] + "\n"
            f.write(subj_str)

            # Nodes for parties
            for party in voting["parties"]:
                party_str = 'MERGE (party:Party {name:' + party["name"] + "})\n"
                f.write(party_str)

                # Nodes for voters
                for voter in party["votes"]:
                    voter_str = 'MERGE (voter:Voter {name:' + voter["voter"] + '})'

                    # Relationships for voters
                    # TBD

                



if __name__ == "__main__":
    main()