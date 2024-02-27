#!/usr/bin/env python3
import sys
import json
from pathlib import Path
import hashlib
import argparse
import random

def make_nodes_noloop(jlog, filename, id, result):
    filename=Path(filename).name
    self_id=id
    result.append(f"    id{self_id}[{filename}]")
    if "dependencies" in jlog:
        for name, dep in jlog["dependencies"].items():
            dep_id=id+1
            id=make_nodes(dep, name, dep_id, result)
            progamname=Path(jlog["program"]).name
            result.append(f"    id{dep_id} --> |{progamname}| id{self_id}")
    return id

def _hash_name(name):
    return hashlib.md5(name.encode()).hexdigest()

def make_nodes(jlog, filename, result):
    self_hash=_hash_name(filename)
    filename=Path(filename).name
    result.append(f"    id_{self_hash}[{filename}]")
    if set(['text'])==set(jlog.keys()): #legacy: text based logs are included in json logs as "text"
        return #no further evaluation of text based logs possible
    if "dependencies" in jlog and len(jlog["dependencies"])>0:
        for name, dep in jlog["dependencies"].items():
            dep_hash=_hash_name(name)
            make_nodes(dep, name, result)
            progamname=Path(jlog["program"]).name
            result.append(f"    id_{dep_hash} --> |{progamname}| id_{self_hash}")
    else: #no dependencies: create a unique dummy node "No Dependencies"
        dep_hash=_hash_name(jlog["program"]) #every call of this program depends on the same 'no-dependency' node
        result.append(f"    id_{dep_hash}[No Dependencies]")
        progamname=Path(jlog["program"]).name
        result.append(f"    id_{dep_hash} --> |{progamname}| id_{self_hash}")

def main():
    parser = argparse.ArgumentParser(description='Generate mermaid flowchart from jlog')
    parser.add_argument('jlog', type=str, help='log file in json format')
    args = parser.parse_args()

    jlog={}
    with open(args.jlog, 'r') as f:
        jlog.update(json.load(f))

    mermaid_code=["%% The following lines are code for the mermaid charting application."]
    mermaid_code.append("%% Paste them into the mermaid live editor at https://mermaid.live to see the flowchart.")
    mermaid_code.append("flowchart TD")
    # make_nodes_noloop(jlog, args.jlog, 1)
    make_nodes(jlog, args.jlog, mermaid_code)
    mermaid_code=list(dict.fromkeys(mermaid_code)) #remove duplicates
    print("\n".join(mermaid_code))

if __name__ == "__main__":
    main()