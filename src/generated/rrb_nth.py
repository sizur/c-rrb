#!/usr/bin/env python

# Copyright (c) 2013 Jean Niklas L'orange. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import sys

def max_height(bits, total_bits):
    '''Returns maximal height of the rrb-vector'''
    i = 1
    bit_count = bits
    while total_bits > bit_count:
        i += 1
        bit_count += bits
    return i


if __name__ == '__main__':
    rrb_bits = int(sys.argv[1])
    print """// Autogenerated
void* rrb_nth(const RRB *rrb, uint32_t index) {
  if (index >= rrb->cnt) {
    return NULL;
  }
  else {
    const InternalNode *current = (const InternalNode *) rrb->root;
    switch (RRB_SHIFT(rrb)) {"""
    for n in range(max_height(rrb_bits, 32) - 1, 0, -1):
        print '    case (RRB_BITS * {}):'.format(n)
        print '      if (current->size_table == NULL) {'
        print '        current = current->child[(index >> (RRB_BITS * {})) & RRB_MASK];'.format(n)
        print '      }'
        print '      else {'
        print '        current = sized(current, &index, RRB_BITS * {});'.format(n)
        print '      }'
    print """    case 0:
      return ((const LeafNode *)current)->child[index & RRB_MASK];
    default:
      return NULL;
    }
  }
}"""
