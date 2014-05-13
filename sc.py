from sympy.galgebra.ga import *
from sympy import *
import operator as op
import sympy, numpy, sys
from math import factorial as _factorial
import operator 
from string import join
import sys

if len(sys.argv) != 2:
	print "Usage: python sc.py 2 > aga2.hpp && astyle aga2.hpp"
	sys.exit(0)

prec = 'float'

n = int(sys.argv[1])
N = 2**n

def get_metric(n):
	""" Return metric passable to setup proc	
	ex.
	n=2 -> "[1,1]"
	n=3 -> "[1,1,1]"
	"""
	return '['+','.join(['1']*n)+']'


def get_basis(n):
	""" Return basis passable to setup proc
	ex.
	n=2 -> "e0 e1"
	n=3 -> "e0 e1 e2"
	"""
	return ' '.join('e{}'.format(i) for i in range(n))


def get_bases():
	""" Return mv base grouped by grades
	ex.
	n = 2 -> ((ONE,), (e0, e1), (e0*e1,))
	"""
	return ((MV.ONE,),) + MV.blades[1:]
	# return ((MV.ONE,),) + MV.bases[1:]

def get_flat_bases():
	""" Return mv base grouped by grades
	ex.
	n = 2 -> ((ONE,), (e0, e1), (e0*e1,))
	"""
	rs = []
	for bs in get_bases():
		for b in bs:
			rs.append(b)
	return rs



# get basis multivectors
e = MV.setup(get_basis(n), get_metric(n))


def get_bases():
	""" Return mv base grouped by grades
	ex.
	n = 2 -> ((ONE,), (e0, e1), (e0*e1,))
	"""
	bss = []
	for es in MV.index:
		bs = []
		if es == ():
			bs.append(_1)
		else:
			for js in es:
				bmv = reduce(operator.mul, map(lambda j: e[j], js))
				bs.append(bmv)
				
		bss.append(bs)
	
	return bss






_1 = e[0]*e[0]
_I = _1.dual()


ZERO = MV.ONE - MV.ONE

bases = get_bases()
flat_bases = get_flat_bases()

def get_base_coefs(mv):
	"""
	ex.
	1 + 2*e0 + 4*e0*e1 (with n=2) -> [[1],[1,0],[4]]
	"""
	rs = []
	for bs in bases:
		t = []
		for b in bs:
			t.append(mv.coef(b))
					
		rs.append(t)		
	return rs
	
	

# MV.index = ((),((0,),(1,),(2,)),((0,1),(0,2),(1,2)),((0,1,2)))



# A = A_0*MV.bases[0][0]+A__1*MV.bases[1][0]+A__2*MV.bases[1][1]+A__12*MV.bases[2][0]



def get_base_elems():
	MV.bases





def prelude():
	""" Return c++ prelude """
	bs = map(len, MV.index)

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
		'using uint = unsigned int;',
		'',
		'uint const n = {n};'.format(n = n),
	]
	

def ending():
	""" Return c++ ending """
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


def csize(grades):
	""" Return size of c++ Mv(grades) object
	ex.
	n = 3
	(0,3) -> 2
	(1) -> 3
	(1,3) -> 4
	"""
	p = 0
	for k in grades:
		l = _comb(n,k)
		p += l
	return p



def produce_obj(name, grades):
	""" Return sympy mv object with symbolic coeffs
	name
	grades

	name[0]*e1 + name[1]*e2

	
	"""
	mv = ZERO
	
	i = 0
	for g in grades:
		for base_mv in bases[g]:			
			coef = symbols('{}[{}]'.format(name, i))  # name[i]
			mv += coef * base_mv			
			i += 1	
	
	return mv
		


def _comb(n,k):
	return _factorial(n) / (_factorial(n-k) * _factorial(k))
	


def name_cls(grades, *template_args):
	""" Return c++ multivector template class name 
	
	ex rotor inst.
		grades = (0,2), template_args = 'float' -> "Mv02<float>"
	
	ex vector decl.
		grades = (1,) -> "Mv1"
	"""
	if template_args:
		targs = '<{}>'.format(join(template_args, ', '))
	else:
		targs = ''

	return 'Mv'+''.join(map(str,grades)) + targs



def build(xs, j = 0):
	for x in xs:
		if isinstance(x, (list,tuple)):
			for _ in build(x, j+1):
				yield _
		else:
			yield '\t'*j + x
			



def csize(grades):
	""" Return size of c++ Mv(grades) object
	ex.
	n = 3
	(0,3) -> 2
	(1) -> 3
	(1,3) -> 4
	"""
	p = 0
	for k in grades:
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

def p_cls(grades):
	""" Return c++ code for Mv class """
	
	gs = grades
	
	cargs = []
	cbody = []
	for k in gs:
		l = _comb(n,k)
		for i in range(l):
			k,i	
			cargs.append('R const& a{}{}'.format(k,i))
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
			'using {0} = typename Array::{0};'.format('iterator'),
			'using {0} = typename Array::{0};'.format('const_iterator'),
			'using {0} = typename Array::{0};'.format('value_type'),
			'using {0} = typename Array::{0};'.format('reference'),
			'using {0} = typename Array::{0};'.format('const_reference'),
			'using {0} = typename Array::{0};'.format('pointer'),
			'using {0} = typename Array::{0};'.format('difference_type'),
			'using {0} = typename Array::{0};'.format('size_type'),
			'',			
			'Array arr;'.format(csize(gs)),
			'',
			mod+'{}({}) '.format(name_cls(gs, 'R'), ', '.join(cargs)) + '{',
			cbody,
			'}',
			'',
			# null constructor
			'{}() '.format(name_cls(gs, 'R')) + '{',
			'}',
			'',
		] +	cast + [
			'R& operator[](uint const& d) {',
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
			'const R& operator[](uint const& d) const {',
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
			'bool empty() const { return false; }',
			'',
			'iterator begin() {',
				['return arr.begin();'],
			'}',			
			'',
			'iterator end() {',
				['return arr.end();'],
			'}',			
			'',
			'const_iterator begin() const {',
				['return arr.begin();'],
			'}',			
			'',
			'const_iterator end() const {',
				['return arr.end();'],
			'}',			
			'',			
			'void swap({}& b) {{'.format(name_cls(gs)),
				['assert(false);'],
			'}',			
			'',			
			'template<class A>',
			'void serialize(A & ar, unsigned int const version) {',
				'for (auto& c: *this) {',
					'ar & c;',
				'}',
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



def p_func_wrap(name, ret_type, arg_types, arg_mods, arg_names, body, assert_ = ''):
	decl_args = []	
	for arg_type, arg_mod, arg_name in zip(arg_types, arg_mods, arg_names):
		decl_args.append(format('{} {} {}', arg_type, arg_mod, arg_name))
		
	return [(
		'template <class R>\n'
		'{ret_type} {func_name}({arg_lst}) {{\n'
		'{assert_}\n'	
		'{body}\n'
		'}}\n'
	).format(
		assert_ = assert_,
		ret_type = ret_type, 		
		func_name = name, 
		arg_lst = join(decl_args, ', '),
		body = body,		
	)]





def p_op(opname, opfunc, kss, nargs = 'xyz'):
	"""
	
	template <class R>
	Mv02<R> operator*(Mv0<R> const& x, Mv02<R> const& y) {
		return Mv02<R>((x[0] * y[0]), (x[0] * y[1]));
	}
	
	"""
	args = []
	arg_types = []
	for ks, narg in zip(kss, nargs):
		args.append(produce_obj(narg, ks))
		arg_types.append(name_cls(ks,'R'))
		
	arg_names = nargs[:len(kss)]
			
	r = opfunc(*args)
	
	bss = get_base_coefs(r)
	
	# non zero result grades	
	nz_grades = []
	
	
	for g,bs in enumerate(bss):
		if any([b != ZERO for b in bs]):		
			nz_grades.append(g)
			
	ret_type = name_cls(nz_grades,'R')
		
	
	ces = []
	for g in nz_grades:
		for coef in bss[g]:
			ces.append(conv_expr(coef))
	
	if len(kss) == 2 and kss[0] == kss[1]:
		assert_ = 'assert(&{} != &{});\n'.format(nargs[0], nargs[1])
	else:
		assert_ = ''
	
	coe = ', '.join(ces)
				
	return nz_grades, p_func_wrap(
		name = opname, 
		ret_type = ret_type, 
		arg_types = arg_types, 
		arg_mods = ['const&'] * len(arg_types),
		arg_names = arg_names, 
		body = format('return {}({});', ret_type, coe), 
		assert_=assert_
	)
	
	

def nz_grades(x):
	# non zero grades - list of int
	return x.get_grades().keys()

	#for k,exprs in enumerate(x.mv):
	#	if exprs is not 0 and any(e != 0 for e in exprs):
	#		yield k


	
	
def p_print(ks):		
	return [(
		'template <class R>\n'
		'std::ostream& operator<<(std::ostream& t, const {ncls}& x) {{'
		'    t << "{ncls}(" << {out_args} << ")";'
		'    return t;'
		'}}').format(
			ncls = name_cls(ks,'R'),
			out_args = join(['x[{}]'.format(i) for i in range(csize(ks))], ' << "," << '),
	)]
	
def format(x, *args, **kwargs):
	return x.format(*args, **kwargs)
	
def par(x):
	return format('({})', x)

def oper_join(xs, o1, o2):
	ys = [par(o1.join(x)) for x in xs]
	return o2.join(ys)

	

def p_xeq_func(grades, name, opers):
	""" Return c++ same-obj comparsion function in the form of:
	
	bool eq(Mv1<R> const& x, Mv1<R> const& y) {
		return x[0] == y[0] and x[1] == y[1];
	}
	
	"""

	# body
	pairs = []
	for i in range(csize(grades)):
		pairs.append([
			format('x[{}]', i), format('y[{}]', i)
		])
		
	return p_func_wrap(
		name = name,
		ret_type = 'bool',
		arg_types = [name_cls(grades,'R'), name_cls(grades,'R')],
		arg_mods = ['const&'] * 2,
		arg_names = ['x', 'y'],
		body = format('return {};', oper_join(pairs, *opers))
	)
	
			
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
		
	
	xs.append('// eq')
	for c in cs:
		x =  p_xeq_func(c, 
			name = 'operator==',
			opers = (' == ', ' && '),
		)
		xs.extend(x)
			

	xs.append('// neq')
	for c in cs:
		x =  p_xeq_func(c,
			name = 'operator!=',
			opers = (' != ', ' || '),
		)
		xs.extend(x)
				
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

				if rk == c1:				
					xs.extend(p_func_wrap(
						name = 'operator+=', 
						ret_type = 'void', 
						arg_types = [name_cls(c1,'R'), name_cls(c2,'R')],
						arg_mods = ['&', 'const&'],
						arg_names = ['x', 'y'],
						body = 'x = x + y;', 
					))

	
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
		xs.append('{} const e{}({});'.format(
			name_cls([1], prec), 
			str(i), 
			join(map(str,args), ',')
		))
		
	xs.append('{} const I(1);'.format(
		name_cls([n], prec)
	))
	xs.append('')
	
	xs.extend(ending())
	
	print '\n'.join(build(xs))

if __name__ == '__main__':
	main()


