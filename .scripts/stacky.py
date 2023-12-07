import argparse
import json
import os
import re

parser = argparse.ArgumentParser(
    description="A little script that makes managing my docker containers a bit easier"
)
parser.add_argument(
    "-a",
    "--all",
    action="store_true",
    help="for deploying all stacks in all categories",
)
parser.add_argument(
    "-c", "--category", nargs=1, help="for deploying all stacks in a category"
)
parser.add_argument(
    "-s", "--stack", nargs=1, help="for deploying a stack in a category"
)
args = parser.parse_args()

compost = {}


def build_manifest():
    global compost
    re_is_service_line = re.compile(r"  [a-z0-9-.]+:\n")
    re_is_service = re.compile(r"[a-z0-9-.]+")
    directories = os.listdir(os.path.join(os.getcwd(), os.pardir))
    for directory in directories:
        if re.match(r"^[^.].+", directory):
            compost[directory] = {}
            files = os.listdir(os.path.join(os.getcwd(), os.pardir, directory))
            for file in files:
                if re.match(r"^[^.].*\.yml$", file):
                    fp = os.path.abspath(
                        os.path.join(os.getcwd(), os.pardir, directory, file)
                    )
                    services = []
                    with open(fp, "r") as f:
                        for line in f:
                            if re_is_service_line.fullmatch(line):
                                services.append(re_is_service.search(line).group(0))
                    services.remove('compost-bin')
                    compost[directory][file[:-4]] = services
    manifest = "manifest.json"
    with open(manifest, "w") as f:
        json.dump(compost, f)


# sn : stack name
def retrieve_stack_category(sn):
    for cn in list(compost.keys()):
        if sn in list(compost[cn].keys()):
            return cn


# sn : stack name
# cn : category name
def stack_deploy(sn, cn):
    path_yaml = os.path.abspath(os.path.join(os.getcwd(), os.pardir, cn, sn + ".yml"))
    path_env = os.path.abspath(os.path.join(os.getcwd(), os.pardir, cn, ".env." + sn))
    command_deploy = " ".join(
        [
            "sudo docker compose --file",
            path_yaml,
            "--env-file",
            path_env,
            "up --detach --force-recreate",
        ]
    )
    # os.system(command_deploy)
    print("~ ", command_deploy)


# l : list
# pn : parent
# t : type : e.g. all, category
def list_deploy(l, pn, t):
    if t == "all":
        for category in list(l.keys()):
            list_deploy(l[category], category, "category")
    elif t == "category":
        for stack in list(l.keys()):
            stack_deploy(stack, pn)


# s : stack
def stack_stop(s):
    services = s.copy()
    services.reverse()
    services.insert(0, "sudo docker stop")
    command_stop = " ".join(services)
    # os.system(command_stop)
    print("~ ", command_stop)


# l : list
# t : type : e.g. all, category
def list_stop(l, t):
    if t == "all":
        for category in list(l.keys()):
            list_stop(l[category], "category")
    elif t == "category":
        for stack in list(l.keys()):
            stack_stop(l[stack])


# l : list
def print_list_items(l):
    count = len(l)
    for item in l:
        if count > 1 and count != len(l) and len(l) != 1:
            print(" ", end="")
        print(item, end="")
        if count > 1 and len(l) > 2:
            print(",", end="")
        if count == 2:
            print(" and ", end="")
        count -= 1


# l : list
# p : parent
# t : type : e.g. all, category, stack
# g : category : e.g. category, stack, service
# a : action : e.g. start, stop, exists
def print_list_msg(l, p, t, g, a):
    if t == "all" and g != "category":
        for category in list(l.keys()):
            print_list_msg(l[category], category, "category", g, a)
    elif t == "category" and g != "stack":
        for stack in list(l.keys()):
            print_list_msg(l[stack], stack, "stack", g, a)
    else:
        if a == "exists":
            print("there ", end="")
            if g == "service":
                if len(list(l)) > 1:
                    print("are", end="")
                else:
                    print("is", end="")
            else:
                if len(list(l.keys())) > 1:
                    print("are", end="")
                else:
                    print("is", end="")
        elif a == "start":
            print("starting", end="")
        elif a == "stop":
            print("stopping", end="")
        print(" ", end="")
        if g == "service":
            print(str(len(list(l))), end="")
        else:
            print(str(len(list(l.keys()))), end="")
        print(" ", end="")
        if a == "exists":
            print("available ", end="")
        if g == "category":
            print(g[:-1], end="")
            if len(list(l.keys())) > 1:
                print("ies", end="")
        elif g == "stack" or g == "service":
            print(g, end="")
            if g == "stack":
                if len(list(l.keys())) > 1:
                    print("s", end="")
            elif g == "service":
                if len(list(l)) > 1:
                    print("s", end="")
        print(" (", end="")
        print_list_items(list(l))
        print(") ", end="")
        if t != "all":
            print("from", t, p, end="")
        print()


def main():
    build_manifest()

    if args.all:
        print_list_msg(compost, None, "all", "service", "stop")
        list_stop(compost, "all")
        print_list_msg(compost, None, "all", "service", "start")
        list_deploy(compost, None, "all")

    if args.category:
        _categories = [i for i in list(compost.keys())]
        if args.category[0] in _categories:
            print_list_msg(
                compost[args.category[0]],
                args.category[0],
                "category",
                "service",
                "stop",
            )
            list_stop(compost[args.category[0]], "category")
            print_list_msg(
                compost[args.category[0]],
                args.category[0],
                "category",
                "service",
                "start",
            )
            list_deploy(compost[args.category[0]], args.category[0], "category")
        else:
            print("invalid category")
            print_list_msg(compost, None, "all", "category", "exists")

    if args.stack:
        _stacks = [j for i in list(compost.keys()) for j in list(compost[i].keys())]
        if args.stack[0] in _stacks:
            print_list_msg(
                compost[retrieve_stack_category(args.stack[0])][args.stack[0]],
                args.stack[0],
                "stack",
                "service",
                "stop",
            )
            stack_stop(compost[retrieve_stack_category(args.stack[0])][args.stack[0]])
            print_list_msg(
                compost[retrieve_stack_category(args.stack[0])][args.stack[0]],
                args.stack[0],
                "stack",
                "service",
                "start",
            )
            stack_deploy(args.stack[0], retrieve_stack_category(args.stack[0]))
        else:
            print("invalid stack")
            print_list_msg(compost, None, "all", "stack", "exists")


if __name__ == "__main__":
    main()
