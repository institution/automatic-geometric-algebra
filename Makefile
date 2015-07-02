# $@ -- The file name of the target of the rule.
# $* -- The stem with which an implicit rule matches
# $< -- The name of the first prerequisite.
# $^ -- The names of all the prerequisites
# $(VARS:%.cpp=%.o) -- pattern replace

CC:=g++-4.9

OPTS:=-std=c++14 -fmax-errors=5 -g -O0 -Wsign-compare -Wreturn-type -Wparentheses -Wpedantic -Wconversion-null


test_aga2: tests/test_aga2.cpp aga2.hpp
	${CC} -o test_aga2 tests/test_aga2.cpp ${OPTS}

clean:
	rm -rf b/* bin/*
