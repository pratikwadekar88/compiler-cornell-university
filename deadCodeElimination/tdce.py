import sys
import json
from mycfg import form_blocks
from util import flatten

def trivial_dce(func):
    while trivial_dce_pass(func):
        pass

def trivial_dce_pass(func):
    blocks =  list(form_blocks(func['instrs']))

    used = set()

    for block in blocks:
        for instr in block:
            used.update(instr.get("args",[]))

    changed = False
    for block in blocks:
        new_block = [i for i in block if 'dest' not in i or i['dest'] in used]

        changed |= len(new_block) != len(block)

        block[:] = new_block

    func['instrs']= flatten(blocks)

    return changed

def drop_killed_local(block):
    last_def = {}
    
    to_drop = set()
    # Check for uses
    for i, instr in enumerate(block):
        for var in instr.get("args",[]):
            if var in last_def:
                del last_def[val]

        if 'dest' in instr:
            dest = instr['dest']
            if dest in last_def:
                to_drop.add(last_def[dest])
            last_def[dest] = instr

    new_block = [instr for i,instr in enumerate(block) if i not in to_drop]
    changed  = len(new_block) != len(block)
    block[:] = new_block
    return changed


def drop_killed_pass(func):
    blocks = list(form_blocks(func['instrs']))
    changed = False
    for block in blocks:
        changed |= drop_killed_local(block)
    func["instrs"] = flatten(blocks)
    return changed
    
def trivial_dce_plus():
    while trivial_dce_pass(func) or drop_killed_pass(func):
        pass 


MODES = {
        "tdce": trivial_dce,
        "tdcep": trivial_dce_pass,
        "dkp" : drop_killed_pass,
        "tdce+" : trivial_dce_plus
        }

def localopt():
    if len(sys.argv) > 1:
        modify_func = MODES[sys.argv[1]]
    else:
        modify_func = trivial_dce

    bril  = json.load(sys.stdin)
    for func in bril['functions']:
        modify_func(func)
    json.dump(bril,sys.stdout,indent=2,sort_keys=True)

if __name__ == '__main__':
    localopt()
