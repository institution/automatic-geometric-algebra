from sympy.galgebra.ga import *
from sympy import *
import operator as op
import sympy, numpy, sys
from math import factorial as _factorial
import operator 
from string import join
import sys

"""
from sympy.galgebra.ga import *
from sympy import *

x0,x1,x2 = symbols('x0 x1 x2')
e0,e1,e2,grad = MV.setup('e0 e1 e2',metric='[1,1,1]',coords=(x0,x1,x2))
"""

if len(sys.argv) != 2:
	print "Usage: python sc.py 2 > aga2.hpp && astyle aga2.hpp"
	sys.exit(0)

prec = 'float'

n = int(sys.argv[1])
N = 2**n

def get_metric(ms):
	""" Return metric passable to setup proc	
	ex.
	n=2 -> "[1,1]"
	n=3 -> "[1,1,1]"
	"""
	return '['+','.join(str(m) for m in ms)+']'


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
ms = n*['1']
e = MV.setup(get_basis(n), get_metric(ms))



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
		'#include "safe_cast.h"',
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



def produce_obj(name, grades, wrap_scalar=True):
	""" Return sympy mv object with symbolic coeffs
	name
	grades

	name[0]*e1 + name[1]*e2

	
	"""
		
	
	mv = ZERO
	
	i = 0
	for g in grades:
		for base_mv in bases[g]:
			if not wrap_scalar and g == 0:
				coef = symbols('{}'.format(name))  # name
			else:
				coef = symbols('{}[{}]'.format(name, i))  # name[i]
			mv += coef * base_mv			
			i += 1	
	
	return mv
		


def _comb(n,k):
	return _factorial(n) / (_factorial(n-k) * _factorial(k))
	


def name_cls(grades, template_args=(), wrap_scalar=True):
	""" Return c++ multivector template class name 
	
	ex rotor inst.
		grades = (0,2), template_args = 'float' -> "Mv02<float>"
	
	ex rotor default inst.
		grades = (0,2), template_args = '' -> "Mv02<>"
	
	ex vector decl.
		grades = (1,) -> "Mv1"
	"""
	assert isinstance(template_args, (tuple, list))
	
	if not wrap_scalar and grades == [0]:
		return 'R'
	
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
	

	
"""
k,i -- grade, index inside grade
d -- index inside our multi-vector

n = 3

k:[i]
	0:[0]
	1:[0 1 2]
	2:[0 1 2]
	3:[0]

Mv02 d: (k,i)
	0: (0,0) 
	1: (2,0)
	2: (2,1)
	3: (2,2)

0 <= d < csize(gs)	

d_ki(gs,k,i) -- index inside Mv containing all grades from gs
ki_d(gs,d) -- k,i from d
"""

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
	
	# constructor args,body
	cargs = []
	cbody = []
	
	for k in gs:
		l = _comb(n,k)
		for i in range(l):
			k,i	
			
			# k -- grade
			# i -- index inside grade
			# d_ki(gs,k,i) -- index inside Mv containing all grades from gs
			cargs.append('R const& a{}{}'.format(k,i))
			cbody.append('arr[{}] = a{}{};'.format(d_ki(gs, k,i), k, i))
	
	# casting constructor body
	ccbody_lines = []
	for d in range(csize(gs)):				
		ccbody_lines.append('arr[{d}] = R(other[{d}]);'.format(d=d))
	ccbody = '\n'.join(ccbody_lines)

	if gs == [0]:
		# implicit cast to R from scalar
		mod = ''
		cast = [
			mod+'operator R() const { return arr[0]; }',
			'',
		]
	elif gs == [n]:
		# explicit cast to R from pseudoscalar
		mod = 'explicit '
		cast = [
			mod+'operator R() const { return arr[0]; }',
			'',
		]
	
	else: 
		mod = ''
		cast = []

	class_name = name_cls(gs)



	assigment = []
	assigment.append('// operator=')
	
	
	assigment.extend(p_func_wrap(
		name = 'operator=', 
		ret_type = 'void', 
		arg_types = [name_cls(gs,['A'])],
		arg_mods = ['const&'],
		arg_names = ['x'],
		body = '\n'.join(['(*this)[{i}] = x[{i}];'.format(i=i) for i in range(len(gs))]),
		template = "template <class A,\ntypename enable_if_safe_cast<A,R>::type* = nullptr>",
	))


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
			'using scalar_type = R;',
			'',
			'Array arr;',
			'',
			'// cast constructor from scalar type',
			'{} {}({}) {{'.format(mod, name_cls(gs, ['R']), ', '.join(cargs)),
			cbody,
			'}',
			'',
			'// null constructor',
			'{}() '.format(name_cls(gs, ['R'])) + '{',
			'}',
			'',
			#'// implicit cast constructor',
			#'template<class SrcType,',
			#'	typename enable_if_safe_cast<SrcType, R>::type* = nullptr',
			#'>',
			#'{ClassName}({ClassName}<SrcType> const& other) {{'.format(ClassName = class_name),
			#'	{ccbody}'.format(ccbody = ccbody),
			#'}',
			#'',
			'// explicit cast constructor',
			'template<class SrcType>',
			'explicit',
			'{ClassName}({ClassName}<SrcType> const& other) {{'.format(ClassName = class_name),
			'	{ccbody}'.format(ccbody = ccbody),
			'}',
			'',			
		] +	cast + [
			'R& operator[](uint const& d) {',
			'	assert(d < size());',
			'	return arr[d];',
			'}',
			'',
			'const R& operator[](uint const& d) const {',
			'	assert(d < size());',
			'	return arr[d];',
			'}',
			'',
			'uint size() const {',
			'	return {};'.format(csize(gs)),
			'}',	
			'',
		] + assigment + [			
			p_op('norm2', lambda x: x.norm2(), [gs], gen = p_meth_wrap_inline)[1],
			'',
			p_op('rev', lambda x: x.rev(), [gs], gen = p_meth_wrap_inline)[1],
			'',			
			p_op('inv', lambda x: x.rev()/x.norm2(), [gs], gen = p_meth_wrap_inline)[1],
			'',			
			p_op('operator-', lambda x: -x, [gs], gen = p_meth_wrap_inline)[1],
			'',			
			'R const* data() const {',
				['return arr.data();'],
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
		# 'template<class R = {}> class {};'.format(prec, name_cls(gs)),
	]



from sympy.core.power import Pow
from sympy.core.numbers import Integer,NegativeOne, Zero
from sympy.core.symbol import Symbol
from sympy.core.add import Add
from sympy.core.mul import Mul

def conv_expr(root):
	if root.func == Pow:
		ls = map(conv_expr, root.args)
		assert len(ls) == 2
		return 'pow({}, {})'.format(*ls)
	elif root.func == Integer:
		return str(root)
	elif root.func == NegativeOne:
		return str(root)
	elif root.func == Symbol:
		return str(root)
	elif root.func == Add:
		# subexpressions
		ls = list(map(conv_expr, root.args))
				
		# "{} + {} + ..."
		pat = ' + '.join(['{}']*len(ls))    
		
		
		
		# <subexpr1> + <subexpr2> + ...
		return ('('+pat+')').format(*ls)
				
	elif root.func == Mul:
		if len(root.args) == 2 and root.args[0] == -1:
			return	'(-{})'.format(conv_expr(root.args[1]))
		elif len(root.args) == 2 and root.args[0] == 1:
			return	'({})'.format(conv_expr(root.args[1]))		
		else:
			# subexpressions
			ls = list(map(conv_expr, root.args))
					
			# {} * {} * ...
			pat = ' * '.join(['{}']*len(ls))    
			
			# <subexpr1> + <subexpr2> + ...
			return ('('+pat+')').format(*ls)
	elif root.func == Zero:
		return '0'
	else:
		import ipdb; ipdb.set_trace()
		assert 0
	


	

	
# symbol -> base type
#        -> struct



def p_meth_wrap_inline(name, ret_type, arg_types, arg_mods, arg_names, body, assert_ = '',
		template = ''
	):
	"""	
	<ret_type> <func_name>(<arg_lst[1:]>) <first_arg_mod> {
		<first_arg_name> = *this;
		<body>
	}
	"""		
	
	decl_args = []	
	for arg_type, arg_mod, arg_name in zip(arg_types[1:], arg_mods[1:], arg_names[1:]):
		decl_args.append(format('{} {} {}', arg_type, arg_mod, arg_name))
		
	return [(
		'{template}\n'
		'{ret_type} {func_name}({arg_lst}) {f_arg_mod} {{\n'
		'{assert_}\n'	
		'auto& {f_arg_name} = *this;\n'
		'{body}\n'
		'}}\n'
	).format(
		f_arg_type = arg_types[0],
		f_arg_mod = 'const' if 'const' in arg_mods[0] else '',
		f_arg_name = arg_names[0],
		assert_ = assert_,
		ret_type = ret_type, 		
		func_name = name, 
		arg_lst = join(decl_args, ', '),
		body = body,
		template = template,		
	)]
	
def p_meth_wrap(name, ret_type, arg_types, arg_mods, arg_names, body, assert_ = '',
		template = 'template <class R>'
	):
	"""
	template <class R>
	<ret_type> <first_arg_type>::<func_name>(<arg_lst[1:]>) <first_arg_mod> {
		<first_arg_name> = *this;
		<body>
	}	
	"""	
	
	
	decl_args = []	
	for arg_type, arg_mod, arg_name in zip(arg_types[1:], arg_mods[1:], arg_names[1:]):
		decl_args.append(format('{} {} {}', arg_type, arg_mod, arg_name))
		
	return [(
		'{template}\n'
		'{ret_type} {f_arg_type}::{func_name}({arg_lst}) {f_arg_mod} {{\n'
		'{assert_}\n'	
		'auto& {f_arg_name} = *this;\n'
		'{body}\n'
		'}}\n'
	).format(
		f_arg_type = arg_types[0],
		f_arg_mod = arg_mods[0],
		f_arg_name = arg_names[0],
		assert_ = assert_,
		ret_type = ret_type, 		
		func_name = name, 
		arg_lst = join(decl_args, ', '),
		body = body,
		template = template,	
	)]


def p_func_wrap(name, ret_type, arg_types, arg_mods, arg_names, body, assert_ = '', 
		template = 'template <class R>'
	):
	"""
	template <class R>
	<ret_type> <func_name>(<arg_lst>) {
		<assert_>
		<body>
	}	
	"""	
	
	decl_args = []	
	for arg_type, arg_mod, arg_name in zip(arg_types, arg_mods, arg_names):
		decl_args.append(format('{} {} {}', arg_type, arg_mod, arg_name))
		
	return [(
		'{template}\n'
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
		template = template,
	)]

def p_op(opname, opfunc, kss, nargs = 'xyz', nbtypes='ABCD', gen = p_func_wrap, wrap_scalar=True):
	"""
	
	template <class R>
	Mv02<R> operator*(Mv0<R> const& x, Mv02<R> const& y) {
		return Mv02<R>((x[0] * y[0]), (x[0] * y[1]));
	}
	
	"""
	args = []
	arg_types = []
	for ks, narg, btype in zip(kss, nargs, nbtypes):
		args.append(produce_obj(narg, ks, wrap_scalar=wrap_scalar))
		
		if len(kss) == 1:
			btype = 'R'
			
		if not wrap_scalar and ks == [0]:
			arg_types.append(btype)
		else:
			arg_types.append(name_cls(ks,[btype]))
	
	
				
	if len(kss) == 1:
		arg_btypes = ['R']
		ret_btype = 'R'
		
		if gen == p_func_wrap:
			template = 'template <class R>'
		else:
			template = ''
		
	else:
		arg_btypes = nbtypes[:len(kss)]
		ret_btype = nbtypes[len(kss)]
		
		arg_btypes_lst1 = ', '.join('class {}'.format(X) for X in arg_btypes)
		arg_btypes_lst2 = ', '.join('{}'.format(X) for X in arg_btypes)
		
		ret_type_decl = 'class {} = typename std::common_type<{}>::type'.format(ret_btype, arg_btypes_lst2)
		template = 'template<{}, \n{}>\n'.format(arg_btypes_lst1, ret_type_decl)
		
		
	arg_names = nargs[:len(kss)]
			
	r = opfunc(*args)
		
	
	if (isinstance(r, MV)):
		# result is multivector
		bss = get_base_coefs(r)
		
		# non zero result grades	
		nz_grades = []		
		
		for g,bs in enumerate(bss):
			if any([b != ZERO for b in bs]):		
				nz_grades.append(g)
				
		
		ret_type = name_cls(nz_grades,[ret_btype], wrap_scalar=wrap_scalar)
				
		ces = []
		for g in nz_grades:
			for coef in bss[g]:
				ces.append(conv_expr(coef))
		
		coe = ', '.join(ces)
		
		body = format('return {}({});', ret_type, coe)
		#import ipdb; ipdb.set_trace()
		
	else:
		# result is scalar
		nz_grades = [0];
		ret_type = 'R'
		coe = conv_expr(r)
		
		body = format('return {};', coe)


		
	if len(kss) == 2 and kss[0] == kss[1]:
		# assert_ = 'assert(&{} != &{});\n'.format(nargs[0], nargs[1])
		assert_ = ''
	else:
		assert_ = ''
				
				
	return nz_grades, gen(
		name = opname, 
		ret_type = ret_type, 
		arg_types = arg_types, 
		arg_mods = ['const&'] * len(arg_types),
		arg_names = arg_names, 
		body = body, 
		assert_=assert_,
		template = template,
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
			ncls = name_cls(ks,['R']),
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
		arg_types = [name_cls(grades,['R']), name_cls(grades,['R'])],
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
	
	xs.append('// mul when one arg is Scalar')
	for c1 in [[0]]:
		for c2 in cs:
			if c1 != c2: # disable mul(R,R)
				rk, func = p_op('operator*', operator.mul, (c1, c2), wrap_scalar=False)
				if rk in cs:
					xs.extend(func)
		
	for c1 in cs:
		for c2 in [[0]]:
			if c1 != c2: # disable mul(R,R)
				rk, func = p_op('operator*', operator.mul, (c1, c2), wrap_scalar=False)
				if rk in cs:
					xs.extend(func)
					
			
	xs.append('// inner product')
	for c1 in cs:
		for c2 in cs:
			rk, func = p_op('operator|', operator.or_, (c1, c2))
			if rk in cs:
				xs.extend(func)
	
	xs.append('// outer product')
	for c1 in cs:
		for c2 in cs:
			rk, func = p_op('operator^', operator.xor, (c1, c2))
			if rk in cs:
				xs.extend(func)
	
	
	#xs.extend(p_alias_func('operator|', 'inn'))
	#xs.append('')
			
	xs.append('// inn2')
	for c1 in cs:
		rk, func = p_op('inn2', lambda x: (x|x), [c1])
		if rk in cs:
			xs.extend(func)
	
	'''
	xs.append('// reverse (operator~)')
	for c1 in cs:
		rk, func = p_op('operator~', lambda x: x.rev(), [c1])
		if rk in cs:
			xs.extend(func)	
	'''
	
	
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
						arg_types = [name_cls(c1,['A']), name_cls(c2,['B'])],
						arg_mods = ['&', 'const&'],
						arg_names = ['x', 'y'],
						body = 'x = x + y;', 
						template = "template <class A, class B,\ntypename enable_if_safe_cast<B,A>::type* = nullptr>",
					))

	xs.append('// sub')
	for c1 in cs:
		for c2 in cs:
			rk, func = p_op('operator-', operator.sub, [c1, c2])
			if rk in cs:
				xs.extend(func)

				if rk == c1:				
					xs.extend(p_func_wrap(
						name = 'operator-=', 
						ret_type = 'void', 
						arg_types = [name_cls(c1,['A']), name_cls(c2,['B'])],
						arg_mods = ['&', 'const&'],
						arg_names = ['x', 'y'],
						body = 'x = x - y;', 
						template = "template <class A, class B,\ntypename enable_if_safe_cast<B,A>::type* = nullptr>",						
					))
	
	xs.append('// rotated')	
	rk, func = p_op('rotated', lambda x,R: (R * x * R.rev()), [[1], [0,2]])
	if rk in cs:
		xs.extend(func)

	
	xs.append('// ostream')
	for c in cs:
		xs.extend(p_print(c)); xs.append('')
		
	xs.append('// const')
	
	# GEN:: auto const _1 = Mv0<>(1);
	xs.append('auto const _1 = {}(1);'.format(
		name_cls([0], ['float'])
	))
	
	# GEN:: auto const e1 = Mv1<>(1,0,0);
	# GEN:: auto const e2 = Mv1<>(0,1,0);
	# GEN:: auto const e3 = Mv1<>(0,0,1);
	for i in range(n):
		args = [0]*n
		args[i] = 1
		xs.append('auto const e{} = {}({});'.format(			
			str(i), 
			name_cls([1], ['float']), 
			join(map(str,args), ',')
		))
		
	# GEN:: auto const I = Mv3<>(1);
	xs.append('auto const I = {}(1);'.format(
		name_cls([n], ['float'])
	))
	xs.append('')
	
	
	xs.append('// misc')
	# GEN:: Mv02<R> rotor(Mv2<R> const& nplane, R const& angle);
	
	xs.extend((
		'/*\n'
		'nplane -- normal plane\n',
		'angle -- angle [1]\n',
		'return -- rotor\n'
		'*/\n'
	))
	
	func = p_func_wrap(
		name='rotor', 
		ret_type = name_cls([0,2], ['R']), 
		arg_types = [name_cls([2], ['R']), 'R'], 
		arg_mods = ['const&', 'const&'], 
		arg_names = ['nplane', 'angle'], 
		body = (
			'return Mv0<R>(cos(angle/2.0)) - nplane * Mv0<R>(sin(angle/2.0));'		
		), 
		#assert_ = 'assert(nplane.norm_r2() - 1.0 <= 0.0000001);'
	)

	xs.extend(func)
	
	
	# close namespace ect.
	xs.extend(ending())
	
	print '\n'.join(build(xs))
	
	
	

if __name__ == '__main__':
	main()


