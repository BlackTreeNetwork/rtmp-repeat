# -*- coding: utf-8 -*-
import os
import sys

def is_argument_value(v):
    return v.startswith('-')
	

def isnumber(obj):
    try:
        int(obj)
        return True
    except:
        return False


def has_args_filter(value, f):
    try:
        if isinstance(f, dict) is True:
            do = f[value]
        else:
            f.index(value)
        return True
    except:
        return False


def argv_dict(it, current):
    try:
        if is_argument_value(it[current + 1]) is True:
            return None
        else:
            return it[current + 1]
    except IndexError:
        return None

def define_argument_value(argv, name, default=None, flag=None):
    target = None
    try:
        if has_args_filter(name, argv) is True:
            target = argv.get(name)

        if target is None:
            if flag is not None:
                target = argv.get(flag)
        else:
            return target
        
        if target is None:
            return default
        else:
            return target

    except Exception as e:
        return default

def disting_args(args, *it, path_ignored=True):
    kv = {}
    unknown = []
    for i, v in enumerate(args):
        if i == 0:
            if is_argument_value(v) is False:
                unknown.append(v)
            else:
                if has_args_filter(v, it) is True:
                    kv[v] = True
                else:
                    kv[v] = argv_dict(args, i)
        else:
            if is_argument_value(v) is True:
                if has_args_filter(v, it) is True:
                    kv[v] = True
                else:
                    kv[v] = argv_dict(args, i)
            else:
                if kv.get(args[i - 1]) is v:
                    continue
                else:
                    unknown.append(v)
                    
    if path_ignored is False:
        unknown = sys.argv[:1] + unknown
    return kv, unknown