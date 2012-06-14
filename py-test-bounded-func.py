#!/usr/bin/python

# discussion: http://stackoverflow.com/questions/11036815/implicitely-bound-callable-objects-to-instance

import itertools
import random

def bound(f):
	def dummy(*args, **kwargs):
		return f(*args, **kwargs)
	return dummy

class LFSeq: # lazy infinite sequence with new elements from func
	def __init__(self, func):
		self.evaluated = []
		self.func = func

	def fillUpToLen(self, n):
		self.evaluated += [self.func() for i in range(len(self.evaluated), n)]
		
	@bound
	class __iter__:
		def __init__(self, seq):
			self.index = 0
			self.seq = seq
		def next(self):
			self.index += 1
			return self.seq[self.index]

	def __getitem__(self, i):
		self.fillUpToLen(i + 1)
		return self.evaluated[i]

	def __getslice__(self, i, k):
		assert k is not None, "inf not supported here"
		if i is None: i = 0
		assert i >= 0, "LFSeq has no len"
		assert k >= 0, "LFSeq has no len"
		self.fillUpToLen(k)
		return self.evaluated[i:k]
		
LRndSeq = lambda: LFSeq(lambda: chr(random.randint(0,255)))

def test():
	f = itertools.count(0).next	
	s = LFSeq(f)
	print s.__iter__
	# LFSeq.__iter__(s) == s.__iter__() ?
	i = iter(s)
	#i = s.__iter__()
	#i = LFSeq.__iter__(s)
	print i
	for c in range(10):
		print next(i)
		
def test2():
	s = LRndSeq()
	print repr("".join(s[:10]))
	
if __name__ == '__main__':
	test()
	test2()