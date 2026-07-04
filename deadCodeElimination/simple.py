import json
import sys


def eliminate(data):

    #print(func)
    res = {'functions':[] }
    for func in data['functions']:

        used = set()
        for instr in func['instrs']:
            if 'args' in instr:
                for a in instr['args']:
                    used.add(a)

        for instr in func['instrs']:
            if 'dest' in instr and instr['dest'] not in used:
                func['instrs'].remove(instr)
        res['functions'].append(func)
    
    return res


if __name__ == '__main__':

    data = json.load(sys.stdin)
    curr = data

    while True:
        new = eliminate(curr)
        if new == curr:
            break
        curr = new

    print(json.dumps(curr))
