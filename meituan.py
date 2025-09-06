import sys
from collections import defaultdict


def main():
    n, m = map(int, input().split())
    values = [0] + list(map(int, input().split()))

    graph = defaultdict(list)
    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    children = defaultdict(list)
    parent = [0] * (n + 1)

    def build_tree(node, par):
        parent[node] = par
        for neighbor in graph[node]:
            if neighbor != par:
                children[node].append(neighbor)
                build_tree(neighbor, node)

    build_tree(1, -1)

    weight_cache = {}
    subtree_cache = {}

    def get_weight(node):
        if node in weight_cache:
            return weight_cache[node]

        if not children[node]:
            weight_cache[node] = values[node]
        else:
            max_xor = 0
            for child in children[node]:
                max_xor = max(max_xor, values[node] ^ values[child])
            weight_cache[node] = max_xor
        return weight_cache[node]

    def invalidate_cache(node):
        if node in weight_cache:
            del weight_cache[node]
        if node in subtree_cache:
            del subtree_cache[node]
        if parent[node] != -1:
            invalidate_cache(parent[node])

    def get_subtree_max(node):
        if node in subtree_cache:
            return subtree_cache[node]

        max_weight = get_weight(node)
        for child in children[node]:
            max_weight = max(max_weight, get_subtree_max(child))
        subtree_cache[node] = max_weight
        return max_weight

    for _ in range(m):
        operation = list(map(int, input().split()))

        if operation[0] == 1:
            x, y = operation[1], operation[2]
            values[x] = y
            invalidate_cache(x)
        elif operation[0] == 2:
            x, y = operation[1], operation[2]
            max_weight = 0
            for i in range(x, min(y + 1, n + 1)):
                max_weight = max(max_weight, get_weight(i))
            print(max_weight)
        else:
            x = operation[1]
            print(get_subtree_max(x))


main()
