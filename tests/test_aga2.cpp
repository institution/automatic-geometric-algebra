#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"

#include "../aga2.hpp"
#include "../dual.hpp"

using aga2::Mv0;  // scalar, _1
using aga2::Mv1;  // vector
using aga2::Mv2;  // plane, I
using aga2::Mv02; // rotor

using dual::Dual;

// template<class = decltype(Mv1<float>::Mv1<int>)
// check





TEST_CASE( "conversions2", "" ) {
	
	
	// implicit conversion int -> float
	Mv1<float> x;
	x = Mv1<int>(1,2);
	
	//Mv1<int>(Mv1<float>(1,2));
	
    REQUIRE( float(Mv0<float>(1)) == 1.0f );
	
	REQUIRE( Mv0<float>(1) == 1.0f );
	
	REQUIRE( (Mv0<float>(1) * 2.0f) == 2.0f );
	
	REQUIRE( (Mv1<float>(1,2) * 2.0f) == Mv1<float>(2,4) );
	
	// explicit safe conversion
	REQUIRE_NOTHROW( Mv1<float>(Mv1<int>(1,2)) );
	
	// explicit unsafe conv
	REQUIRE_NOTHROW( Mv1<int>(Mv1<float>(1,2)) );
	
	
	REQUIRE_NOTHROW( Mv1<float>(1,2) );
    
    // implicit safe conversion
	//REQUIRE_NOTHROW( (Mv1<int>(1,2) * 2.0f) );
    
}


TEST_CASE( "dual", "" ) {
	
	
	Dual<float> x;
	
	x = Dual<float>(1.0f, 1.0f);
	
	// f(x) = x*x
	auto f = x*x;
	
	// f(x) and df(x)/dx
	REQUIRE( f[0] == 1.0f );
	REQUIRE( f[1] == 2.0f );   
	
}

TEST_CASE( "dual and vect", "" ) {
	/*
	using T = Dual<float>;
	
	Mv1<T> v;
	
	// gradient
	float g[2] = {1,1};
	
	v[0] = T(2.0f, 1.0f);
	v[1] = T(3.0f);
		
	// f(x) = x|x	
	auto f = T(v|v);
	
	// f(x) and df(x)/dx1
	REQUIRE( f[0] == 13.0f );
	REQUIRE( f[1] == 4.0f );
	*/
	
}



TEST_CASE( "vector mul num", "" ) {
	auto x = 3 * Mv1<int>(1,2);
    REQUIRE( x[0] == 3 );
    REQUIRE( x[1] == 6 );    
}

TEST_CASE( "vector add", "" ) {
	auto x = Mv1<int>(1,2) + Mv1<int>(2,3);
    REQUIRE( x[0] == 3 );
    REQUIRE( x[1] == 5 );    
}

TEST_CASE( "vector sub", "" ) {
	auto x = Mv1<int>(1,-8) - Mv1<int>(2,3);
    REQUIRE( x[0] == -1 );
    REQUIRE( x[1] == -11 );    
}

TEST_CASE( "vector inner product", "" ) {
	auto x = Mv1<int>(1,-8) | Mv1<int>(2,3);
    REQUIRE( x == (1*2-8*3) );
}

/*TEST_CASE( "vector outer product", "" ) {
	auto x = Mv1<>(1,-8) ^ Mv1<>(2,3);
    REQUIRE( x == (1*2-8*3) );
}*/

TEST_CASE( "vector neq", "" ) {	
    REQUIRE( Mv1<int>(1,2) != Mv1<int>(1,3) );
    REQUIRE( Mv1<int>(2,1) != Mv1<int>(3,1) );
	REQUIRE( Mv1<int>(1,2) != Mv1<int>(3,4) );
	REQUIRE( !(Mv1<int>(1,2) != Mv1<int>(1,2)) );
}

TEST_CASE( "vector eq", "" ) {
	REQUIRE( Mv1<int>(1,2) == Mv1<int>(1,2) );
	REQUIRE( !(Mv1<int>(1,3) == Mv1<int>(1,2)) );
	REQUIRE( !(Mv1<int>(3,1) == Mv1<int>(2,1)) );
	REQUIRE( !(Mv1<int>(1,2) == Mv1<int>(3,4)) );
}
