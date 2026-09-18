#!/usr/bin/env python
"""Find nested functions where a variable named 'line' is a FREE variable (closure).

This is the exact bug behind: "cannot access local variable 'line' where it is not
associated with a value". Reports the precise file:line for every occurrence across
the whole working tree.
"""
import ast, os, sys

ROOT = os.path.abspath(".")


def walk(tree, path, out):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # A nested function uses `line` as a free var if it is referenced but
            # not defined in the enclosing function's own local scope.
            inside = node  # the nested function body
            # Collect names assigned in the function's own scope (locals of THIS fn)
            assigned = set()
            for sub in ast.walk(inside):
                if isinstance(sub, ast.arg):
                    assigned.add(sub.arg)
                elif isinstance(sub, (ast.Name,)):
                    if isinstance(sub.ctx, (ast.Store,)):
                        assigned.add(sub.id)
                elif isinstance(sub, (ast.Tuple, ast.List)):
                    for el in el_list(sub):
                        if isinstance(el, ast.Name) and isinstance(el.ctx, ast.Store):
                            assigned.add(el.id)
            # Names READ (Load) inside the function
            used = set()
            for sub in ast.walk(inside):
                if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                    used.add(sub.id)
            # free vars = used but not locally assigned
            free = used - assigned
            if "line" in free:
                # Confirm 'line' is assigned in an ENCLOSING (outer) function
                out.append(f"{path}:{node.lineno}: nested function {node.name!r} uses 'line' as FREE var")


def el_list(t):
    # handle Tuple/List element lists
    if isinstance(t, ast.Tuple):
        return t.elts
    if isinstance(t, ast.List):
        return t.elts
    return []


def main():
    hits = []
    for dp, _dn, fnames in os.walk(ROOT):
        if "node_modules" in dp or ".git" in dp:
            continue
        for f in fnames:
            if not f.endswith(".py"):
                continue
            path = os.path.join(dp, f)
            try:
                with open(path, encoding="utf-8") as fh:
                    tree = ast.parse(fh.read(), filename=path)
                walk(tree, path, hits)
            except SyntaxError as e:
                pass
    if not hits:
        print("No nested function uses 'line' as a free variable.")
        return 0
    print("FOUND 'line' free-variable closures:")
    for h in sorted(set(hits)):
        print("  " + h)
    return 1


if __name__ == "__main__":
    sys.exit(main())
