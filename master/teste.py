import curses

def render_tree(results, tree, level=0, prefix=[], node='/'):
    # Exit condition
    if node not in tree:
        return

    # Iteration
    for i, line in enumerate(tree[node]):
        cgroup = line['cgroup']

        # Build name
        if i == len(tree[node]) - 1:
            line['_tree'] = prefix + [curses.ACS_LLCORNER, curses.ACS_HLINE, ' ']
            _child_prefix = prefix + [' ', ' ', ' ']
        else:
            line['_tree'] = prefix + [curses.ACS_LTEE, curses.ACS_HLINE, ' ']
            _child_prefix = prefix + [curses.ACS_VLINE, ' ', ' ']

        # Commit, fold or recurse
        results.append(line)
        if cgroup not in CONFIGURATION['fold']:
            render_tree(results, tree, level+1, _child_prefix, cgroup)
        else:
            line['_tree'] [-2] = '+' 