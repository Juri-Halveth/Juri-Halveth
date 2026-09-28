"""Finite rewriting example. Iterations are not seconds or a physical-history claim."""
import argparse
import hashlib
import json

RULES = {'five': 'F[+F]F[-F]F', 'four': 'F[+F]F[-F]'}

def model(depth):
    if type(depth) is not int or not 0 <= depth <= 4:
        raise ValueError('depth must be an integer from 0 to 4')
    branches = {}
    for name, rule in RULES.items():
        state = 'F'
        steps = []
        for step in range(depth + 1):
            steps.append({'step': step, 'segments': state.count('F'),
                          'symbols': len(state), 'sha256': hashlib.sha256(state.encode('ascii')).hexdigest()})
            if step < depth:
                state = state.replace('F', rule)
        branches[name] = {'rule': rule, 'steps': steps}
    first = next((i for i in range(depth + 1)
                  if branches['five']['steps'][i]['sha256'] != branches['four']['steps'][i]['sha256']), None)
    return {'schema': 'halveth.finite-branches.v1', 'depth': depth, 'branches': branches,
            'first_divergence_step': first, 'time_unit': 'iteration',
            'physical_measurement': False, 'game_mutation': False}

def self_check():
    for depth in range(5):
        result = model(depth)
        assert result['branches']['five']['steps'][-1]['segments'] == 5 ** depth
        assert result['branches']['four']['steps'][-1]['segments'] == 4 ** depth
        assert result['first_divergence_step'] == (None if depth == 0 else 1)
        assert result == model(depth)
    for invalid in (-1, 5, 1.5, True, '4', None):
        try:
            model(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')
    return {'depths_checked': 5, 'rejected_invalid_inputs': 6, 'deterministic': True}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--depth', type=int, default=4, choices=range(5))
    parser.add_argument('--self-check', action='store_true')
    args = parser.parse_args()
    print(json.dumps(self_check() if args.self_check else model(args.depth), indent=2))
