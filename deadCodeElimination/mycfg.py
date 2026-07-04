import json
import sys
from collections import OrderedDict

TERMINATORS = [ 'jmp', 'br', 'ret']

def form_blocks(func):
    curr_block = []
    for instr in func:
        if 'op' in instr:
            curr_block.append(instr)
            if instr['op'] in TERMINATORS:
                yield curr_block
                curr_block = []
        else:
            if curr_block:
                yield curr_block
            curr_block = [instr]
    if curr_block:
        yield curr_block



def mycfg():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        name2blocks = block_map(form_blocks(func['instrs']))
        print(name2blocks)
        myCfg = get_cfg(name2blocks)
        print(myCfg)

def get_cfg(name2blocks):
    out = {}

    for i,(name,block) in  enumerate(name2blocks.items()):

        last = block[-1]
        if last['op'] in ('jmp','br'):
            succ = last['labels']
        elif last['op'] == 'ret':
            succ = []
        else:
            if i+1<= (len(name2blocks)-1):
                succ = [list(name2blocks.keys())[i+1]]
            else:
                succ = []

        out[name] = succ
    return out


def block_map(blocks):

    out = OrderedDict()
    for block in blocks:
        if 'label' in block[0]:
            name = block[0]['label']
            block = block[1:]
        else:
            name = f"b{len(out)}"

        out[name] = block
    
    return out


if __name__ == '__main__':
    mycfg()
