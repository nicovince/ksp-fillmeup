#!/usr/bin/env python3

import sfsutils

import argparse
import shutil


def fill(resource):
    resource['amount'] = resource['maxAmount']


def fill_resources(resources, resource_types):
    """Fill all resources of the specified resource type to the max."""
    if type(resources) == list:
        resources_list = resources
    else:
        resources_list = [resources]
    for r in resources_list:
        if r['name'] in resource_types:
            fill(r)


def fill_vessel(vessel, resource_types):
    print(f"Process {vessel['name']}")
    parts_list = get_vessel_parts(vessel)
    for p in parts_list:
        if 'RESOURCE' in p.keys():
            fill_resources(p['RESOURCE'], resource_types)


def find_vessel(vessels, name):
    if type(vessels) == list:
        vessels_list = vessels
    else:
        vessels_list = [vessels]
    for v in vessels_list:
        if v['name'] == name:
            return v
    return None


def patch_sfs(sfs_file, ship_name, resource_types):
    shutil.copy2(sfs_file, f"{sfs_file}.old")
    data = sfsutils.parse_savefile(sfs_file)
    vessel = find_vessel(data['GAME']['FLIGHTSTATE']['VESSEL'], ship_name)
    fill_vessel(vessel, resource_types)
    sfsutils.writeout_savefile(data, destination_file=f"{sfs_file}")


def list_vessels(sfs_file, show_debris):
    data = sfsutils.parse_savefile(sfs_file)
    if type(data['GAME']['FLIGHTSTATE']['VESSEL']) == list:
        vessels = data['GAME']['FLIGHTSTATE']['VESSEL']
    else:
        vessels = list(data['GAME']['FLIGHTSTATE']['VESSEL'])
    print("Vessels list:")
    for v in vessels:
        if v['type'] == 'Debris' and not show_debris:
            continue
        print(f"- {v['name']} ({v['type']})")

def get_vessel_parts(vessel):
    if type(vessel['PART']) == list:
        parts_list = vessel['PART']
    else:
        parts_list = [vessel]
    return parts_list

def list_vessel_parts(vessel):
    parts = get_vessel_parts(vessel)
    resources_parts = [p for p in parts if 'RESOURCE' in p.keys()]
    for rp in resources_parts:
        print(rp['name'])
        if type(rp['RESOURCE']) != list:
            resources = [rp['RESOURCE']]
        else:
            resources = rp['RESOURCE']
        for r in resources:
            print(f" - {r['name']}")


def main_fill(args):
    patch_sfs(args.save_file, args.ship_name, args.resources)


def main_list(args):
    list_vessels(args.save_file, args.show_debris)

def main_parts(args):
    ship_name = args.ship_name
    sfs_file = args.save_file
    data = sfsutils.parse_savefile(sfs_file)
    vessel = find_vessel(data['GAME']['FLIGHTSTATE']['VESSEL'], ship_name)
    list_vessel_parts(vessel)

def main():
    parser = argparse.ArgumentParser(description="Fill Up Ships")
    parser.add_argument('--save-file', default='persistent.sfs',
                        help='Save file to use')
    sub_parsers = parser.add_subparsers(help='sub parser help')
    parser_fill = sub_parsers.add_parser('fill', help='Fill vessels')
    parser_fill.add_argument('ship_name', metavar='ship-name')
    parser_fill.add_argument('--resources', type=str, nargs='*', default=['LiquidFuel', 'Oxidizer'])
    parser_fill.set_defaults(func=main_fill)

    parser_list = sub_parsers.add_parser('list', help='List vessels')
    parser_list.add_argument('--show-debris', action='store_true', default=False,
                             help='List debris as well')
    parser_list.set_defaults(func=main_list)

    parser_parts = sub_parsers.add_parser('parts', help='List parts of vessel')
    parser_parts.add_argument('ship_name', metavar='ship-name')
    parser_parts.set_defaults(func=main_parts)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
