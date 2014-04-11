#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"

#include "../aga2.hpp"

using aga2::Mv0;  // scalar, _1
using aga2::Mv1;  // vector
using aga2::Mv2;  // plane, I
using aga2::Mv02; // rotor

TEST_CASE( "vector addition", "" ) {
	auto x = Mv1<>(1,2) + Mv1<>(2,3);
    REQUIRE( x[0] == 3 );
    REQUIRE( x[1] == 5 );    
}

TEST_CASE( "vector neq", "" ) {	
    REQUIRE( Mv1<>(1,2) != Mv1<>(1,3) );
    REQUIRE( Mv1<>(2,1) != Mv1<>(3,1) );
	REQUIRE( Mv1<>(1,2) != Mv1<>(3,4) );
	REQUIRE( !(Mv1<>(1,2) != Mv1<>(1,2)) );
}

TEST_CASE( "vector eq", "" ) {
	REQUIRE( Mv1<>(1,2) == Mv1<>(1,2) );
	REQUIRE( !(Mv1<>(1,3) == Mv1<>(1,2)) );
	REQUIRE( !(Mv1<>(3,1) == Mv1<>(2,1)) );
	REQUIRE( !(Mv1<>(1,2) == Mv1<>(3,4)) );
}