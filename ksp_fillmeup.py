#!/usr/bin/env python3

import sfsutils

import argparse


def fill(resource):
    print("set resource to max")
    resource['amount'] = resource['maxAmount']



def fill_resources(resources, resource_types):
    """Fill all resources of the specified resource type to the max."""
    if type(resources) == list:
        for r in resources:
            if r['name'] in resource_types:
                fill(r)
    else:
        if resources['name'] in resource_types:
            fill(resources)


def fill_vessel(vessel, resource_types):
    print(f"Process {vessel['name']}")
    for p in vessel['PART']:
        print(f"process part {p['name']}")
        if 'RESOURCE' in p.keys():
            fill_resources(p['RESOURCE'], resource_types)


def find_vessel(vessels, name):
    if type(vessels) == list:
        for v in vessels:
            if v['name'] == name:
                return v
    else:
        if vessels['name'] == name:
            return vessels
    return None


def find_fill_vessel(vessels, ship_name, resource_types):
    """Find vessel with requested name and fill resources requested."""
    for v in vessels:
        if v['name'] == ship_name:
            pass


def patch_sfs(sfs_file, ship_name, resource_types):
    data = sfsutils.parse_savefile(sfs_file)
    vessel = find_vessel(data['GAME']['FLIGHTSTATE']['VESSEL'], ship_name)
    fill_vessel(vessel, resource_types)
    sfsutils.writeout_savefile(data, destination_file=f"{sfs_file}.new")


def main():
    parser = argparse.ArgumentParser(description="Fill Up Ships")
    parser.add_argument('ship_name', metavar='ship-name')
    parser.add_argument('--resources', type=str, nargs='*', default=['LiquidFuel', 'Oxidizer'])
    parser.add_argument('--save-file', default="persistent.sfs",
                       help="Save file to modify")
    args = parser.parse_args()
    patch_sfs(args.save_file, args.ship_name, args.resources)

if __name__ == "__main__":
    main()
