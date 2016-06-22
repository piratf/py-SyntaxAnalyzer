
class TrieNode(object):
    """node of trie tree"""
    def __init__(self):
        super(TrieNode, self).__init__()
        self.ch = 0
        self.branch = 0
        self.times = 0
        self.child = {}

def init_trie():
    root = TrieNode()
    return root

def insert_trie(root, strs):
    slen = len(strs)
    if slen == 0:
        root.times += 1
        return
    i = 0
    idx = 0
    p = root
    p.times += 1
    while (i < slen):
        idx = strs[i]
        if idx in p.child:
            p = p.child[idx]
            p.times += 1
            i += 1
        else:
            tmp = TrieNode()
            tmp.ch = strs[i]
            tmp.times = 1
            p.branch += 1
            p.child[idx] = tmp
            p = tmp
            i += 1

def longest_common_prefix(contents):
    n = len(contents)
    if n == 0:
        return ''

    ret = ''
    root = init_trie()
    for x in contents:
        if len(x) < 2:
            break;
        print (x)
        insert_trie(root, x)
        i = 0
        p = root
        while i < len(contents[0]) and p.branch == 1 and p.times == n:
            p = p.child[contents[0][i]]
            i += 1
        if p.times < n:
            i -= 1
        print (contents[0][0: i])
        if i > len(ret):
            ret = contents[0][0: i]

    return ret



print (longest_common_prefix(sorted([['i', 'C', 't', 'S'], ['i', 'C', 't', 'S', 'e', 'S'], ['a']])))



