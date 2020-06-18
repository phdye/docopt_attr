# -*- coding: utf-8 -*-

import sys

from docopt import docopt

from collections.abc import Mapping

#------------------------------------------------------------------------------

class AttributeConfig(Mapping):

    def __init__(self, *args, **kwargs):
        # self.attr = [ ]
        for key, value in kwargs.items() :
            setattr(self, key, value)
            # self.attr.append(key)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    def __str__(self):
        return ( "AttributeConfig(" +
                 ", ".join([ f'{k}={repr(v)}' for k,v in self.__dict__.items() ]) +
                 ")" )

    def __repr__(self):
        return self.__str__()

#------------------------------------------------------------------------------

def docattr(doc, argv=None, help=True, version=None, options_first=False):

    """docopt with options in attributes rather than dictionary elements

           args['--verbose']  =>  args.verbose

           args['<file>']     =>  arg.file

       All else remains the same.  Attributes are single values or lists
       as appropriate.

       <docopt-doc>
    """

    args = docopt(doc, argv, help, version, options_first)

    clean = { }

    for key in args :
        value = args[key]
        if key.startswith('--') :
            key = key[2:]
            # print(f": -- {key:<16s} : {repr(value)}")
        elif key.startswith('<') and key.endswith('>') :
            key = key[1:][:-1]
            # print(f": -- {key:<16s} : {repr(value)}")
        else :
            raise ValueError("Unrecognized option name '{key}'")
        key = key.replace('-', '_')
        clean [ key ] = value

    return AttributeConfig(**clean)
        
docattr.__doc__ = docattr.__doc__.replace('<docopt-doc>', docopt.__doc__ )

# ------------------------------------------------------------------------------
