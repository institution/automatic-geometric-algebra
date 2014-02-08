from sympy.galgebra.GA import *
from sympy.galgebra.latex_ex import *
from sympy import *
import operator as op
import sympy, numpy, sys
from math import factorial as _factorial
import operator 
from string import join

set_main(sys.modules[__name__])

import sys


n = int(sys.argv[1])

metric = (
	'1 0 0,'
	'0 1 0,'
	'0 0 1')

base = MV.setup(' '.join('e{}'.format(i) for i in range(n)), metric)
_1 = base[0] * base[0]
basis = base[0].basis
prec = 'float'



def prelude():
	bs = map(len,basis)
	bs[0] = 1
	return [
		'#ifndef AGA{n}_HPP'.format(n = n),
		'#define AGA{n}_HPP'.format(n = n),
		'#include <cassert>',
		'#include <array>',
		'#include <cmath>',
		'#include <iostream>',
		'',
		'namespace aga{n} {{'.format(n = n),
		'',
		'const uint n = {n};'.format(n = n),
	]
	

def ending():
	return [
		'}} // aga{n}'.format(n = n),
		'',
		'#endif // AGA{}_HPP'.format(n),
	]


def lacomb(cs, bs):
	return reduce(op.add, map(op.mul, cs, bs))
	
def fname(gs, key, k, i):
	#return '{}[{}{}]'.format(key, k, i)
	return '{}[{}]'.format(key, d_ki(gs, k, i))

def produce_obj(key, n, ks):
	if ks == [0]:
		return MV(symbols(key+'[0]'), 'scalar')

	cs,bs = [],[]
	if 0 in ks:
		bs.append(1)
		
	for k in ks:
		l = _comb(n, k)
		symbs = []
		for i in range(l):
			symbs.append(fname(ks, key, k, i))
			
		for ds in basis[k]:
			bs.append(reduce(lambda a,b: a^b, map(lambda j: base[j], ds)))
		
		cs.extend(map(symbols, symbs))

	return lacomb(cs, bs)
	
	

def _comb(n,k):
	return _factorial(n) / (_factorial(n-k) * _factorial(k))
	


def name_cls(gs, *ts):
	if ts:
		targs = '<{}>'.format(join(ts, ', '))
	else:
		targs = ''

	#if gs == [0]:
	#	return 'R'
	#else:
	return 'Mv'+''.join(map(str,gs)) + targs



def build(xs, j = 0):
	for x in xs:
		if isinstance(x, (list,tuple)):
			for _ in build(x, j+1):
				yield _
		else:
			yield '\t'*j + x
			

def csize(gs):
	p = 0
	for k in gs:
		l = _comb(n,k)
		p += l
	return p

def d_ki(gs, k, i):
	""" d -> k,i """
	p = 0
	for g in gs:
		l = _comb(n,g)
		if g == k:
			assert i < l
			return p + i
		p += l
	assert 0
	
	
def ki_d(gs, d):
	""" k,i <- d """
	p = 0
	for k in gs:
		l = _comb(n,k)
		if d - p < l:
			return k,d - p			
		p += l
	assert 0
	
def p_alias_func(fname, aname):
	return [
		'// forward "{}" to "{}"'.format(aname, fname),
		'template <typename... Args>',
		'auto {}(Args&&... args) -> decltype({}(std::forward<Args>(args)...)) {{'.format(aname, fname),
		'\treturn {}(std::forward<Args>(args)...);'.format(fname),
		'}'
	]

def p_cls(gs):
	
	cargs = []
	cbody = []
	for k in gs:
		l = _comb(n,k)
		for i in range(l):
			k,i	
			cargs.append('const R& a{}{}'.format(k,i))
			cbody.append('arr[{}] = a{}{};'.format(d_ki(gs, k,i), k, i))

	if gs == [0]:
		mod = ''
		cast = [
			mod+'operator R() { return arr[0]; }',
			'',
		]
	elif gs == [n]:
		mod = 'explicit '
		cast = [
			mod+'operator R() { return arr[0]; }',
			'',
		]
	
	else: 
		mod = ''
		cast = []

	

	return [
		'template <class R>',
		'class {} '.format(name_cls(gs)) + '{',
		'public:',
		[
			'using Array = std::array<R,{}>;'.format(csize(gs)),
			'',			
			'using Iter = typename Array::iterator;'.format(csize(gs)),
			'',			
			'Array arr;'.format(csize(gs)),
			'',
			mod+'{}({}) '.format(name_cls(gs, 'R'), ', '.join(cargs)) + '{',
			cbody,
			'}',
			'',
		] +	cast + [
			'R& operator[](const uint d) {',
			[
				'assert(d < size());',
				'return arr[d];',
			],
			'}',
			'',
			'template<class F>',
			'{} cast() {{'.format(name_cls(gs, 'F')),
			[
				'return {}({});'.format(
					name_cls(gs, 'F'),
					join(['F(arr[{}])'.format(i) for i in range(csize(gs))], ', '),
				),
			],
			'}',
			'',
			'const R& operator[](const uint d) const {',
			[
				'assert(d < size());',
				'return arr[d];',
			],
			'}',
			'',
			'uint size() const {',
				['return {};'.format(csize(gs))],
			'}',			
			'',
			'Iter begin() {',
				['return arr.begin();'],
			'}',			
			'',
			'Iter end() {',
				['return arr.end();'],
			'}',
		],
		'};',
		'',
		'template<class R = {}> class {};'.format(prec, name_cls(gs)),
	]



from sympy.core.power import Pow
from sympy.core.numbers import Integer,NegativeOne
from sympy.core.symbol import Symbol
from sympy.core.add import Add
from sympy.core.mul import Mul

def conv_expr(root):
	if root.func == Pow:
		return 'pow({}, {})'.format(*map(conv_expr, root.args))
	elif root.func == Integer:
		return str(root)
	elif root.func == NegativeOne:
		return str(root)
	elif root.func == Symbol:
		return str(root)
	elif root.func == Add:
		return '({} + {})'.format(*map(conv_expr, root.args))
	elif root.func == Mul:
		if root.args[0] == -1:
			return	'(-{})'.format(conv_expr(root.args[1]))
		else:
			return '({} * {})'.format(*map(conv_expr, root.args))
	else:
		import ipdb; ipdb.set_trace()
		assert 0
	


	

	
# symbol -> base type
#        -> struct





def p_op(opname, opfunc, kss, nargs = 'xyz'):
	
	args = []
	decl_args = []
	for ks, narg in zip(kss, nargs):
		args.append(produce_obj(narg, n, ks))
		decl_args.append('const {} &{}'.format(name_cls(ks,'R'), narg))
			
	r = opfunc(*args)
	
	# import ipdb; ipdb.set_trace()
	nzr = list(nz_grades(r))
	tr = name_cls(nzr,'R')
	
	coeffs = []				
	for k in nzr:
		for i,expr in enumerate(r.mv[k]):
			coeffs.append(conv_expr(expr))    #//'+fname(zgs, 'z', k, i))
	
	if len(kss) == 2 and kss[0] == kss[1]:
		assert_ = 'assert(&{} != &{});\n'.format(nargs[0], nargs[1])
	else:
		assert_ = ''
		
	return nzr, [(
		'template <class R>\n'
		'{ret_type} {op_name}({arg_lst}) {{\n'
		'    {assert_}'	
		'    return {ret_type}({coe_lst});\n'
		'}}\n'
	).format(
		assert_ = assert_,
		ret_type = tr, 
		op_name = opname, 
		arg_lst = join(decl_args, ', '),
		coe_lst = join(coeffs, ', '),
	)]
	
	

def nz_grades(x):
	for k,exprs in enumerate(x.mv):
		if exprs is not 0 and any(e != 0 for e in exprs):
			yield k


	
def p_print(ks):		
	return [(
		'template <class R>\n'
		'std::ostream& operator<<(std::ostream& t, const {ncls}& x) {{'
		'    t << "{ncls}(" << {out_args} << ")";'
		'}}').format(
			ncls = name_cls(ks,'R'),
			out_args = join(['x[{}]'.format(i) for i in range(csize(ks))], ' << "," << '),
	)]
	

def main():
	if n == 3:
		cs = [[0], [1], [2], [0,2], [1,3], [3]]
	else:
		cs = [[0], [1], [2], [0,2]]

	xs = []
	xs.extend(prelude())
	xs.append('')
	
	for c in cs:
		xs.extend(p_cls(c)); xs.append('')
		
	xs.append('// mul')
	for c1 in cs:
		for c2 in cs:
			rk, func = p_op('operator*', operator.mul, (c1, c2))
			if rk in cs:
				xs.extend(func)
			
	xs.append('// inn')
	for c1 in cs:
		for c2 in cs:
			rk, func = p_op('operator|', operator.or_, (c1, c2))
			if rk in cs:
				xs.extend(func)
	
	#xs.extend(p_alias_func('operator|', 'inn'))
	#xs.append('')
			
	xs.append('// inn2')
	for c1 in cs:
		rk, func = p_op('inn2', lambda x: (x|x), [c1])
		if rk in cs:
			xs.extend(func)
			
	xs.append('// add')
	for c1 in cs:
		for c2 in cs:
			rk, func = p_op('operator+', operator.add, [c1, c2])
			if rk in cs:
				xs.extend(func)
	
	xs.append('// sub')
	for c1 in cs:
		for c2 in cs:
			rk, func = p_op('operator-', operator.sub, [c1, c2])
			if rk in cs:
				xs.extend(func)
	
	xs.append('// ostream')
	for c in cs:
		xs.extend(p_print(c)); xs.append('')
		
	xs.append('// const')
	for i in range(n):
		args = [0]*n
		args[i] = 1
		xs.append('const {} e{}({});'.format(
			name_cls([1], prec), 
			str(i), 
			join(map(str,args), ',')
		))
		
	xs.append('const {} I(1);'.format(
		name_cls([n], prec)
	))
	xs.append('')
	
	xs.extend(ending())
	
	print '\n'.join(build(xs))

if __name__ == '__main__':
	main()


