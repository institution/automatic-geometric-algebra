#ifndef AGA3_HPP
#define AGA3_HPP
#include <cassert>
#include <array>
#include <cmath>
#include <iostream>

namespace aga3 {

const uint n = 3;

template <class R>
class Mv0 {
public:
    std::array<R,1> arr;

    Mv0<R>(const R& a00) {
        arr[0] = a00;
    }

    operator R() {
        return arr[0];
    }

    R& operator[](const uint d) {
        assert(d < size());
        return arr[d];
    }

    template<class F>
    Mv0<F> cast<F>() {
        return Mv0<F>(arr[0]);
    }

    const R& operator[](const uint d) const {
        assert(d < size());
        return arr[d];
    }

    uint size() const {
        return 1;
    }
};

template<class R = float> class Mv0;

template <class R>
class Mv1 {
public:
    std::array<R,3> arr;

    Mv1<R>(const R& a10, const R& a11, const R& a12) {
        arr[0] = a10;
        arr[1] = a11;
        arr[2] = a12;
    }

    R& operator[](const uint d) {
        assert(d < size());
        return arr[d];
    }

    template<class F>
    Mv1<F> cast<F>() {
        return Mv1<F>(arr[0], arr[1], arr[2]);
    }

    const R& operator[](const uint d) const {
        assert(d < size());
        return arr[d];
    }

    uint size() const {
        return 3;
    }
};

template<class R = float> class Mv1;

template <class R>
class Mv2 {
public:
    std::array<R,3> arr;

    Mv2<R>(const R& a20, const R& a21, const R& a22) {
        arr[0] = a20;
        arr[1] = a21;
        arr[2] = a22;
    }

    R& operator[](const uint d) {
        assert(d < size());
        return arr[d];
    }

    template<class F>
    Mv2<F> cast<F>() {
        return Mv2<F>(arr[0], arr[1], arr[2]);
    }

    const R& operator[](const uint d) const {
        assert(d < size());
        return arr[d];
    }

    uint size() const {
        return 3;
    }
};

template<class R = float> class Mv2;

template <class R>
class Mv02 {
public:
    std::array<R,4> arr;

    Mv02<R>(const R& a00, const R& a20, const R& a21, const R& a22) {
        arr[0] = a00;
        arr[1] = a20;
        arr[2] = a21;
        arr[3] = a22;
    }

    R& operator[](const uint d) {
        assert(d < size());
        return arr[d];
    }

    template<class F>
    Mv02<F> cast<F>() {
        return Mv02<F>(arr[0], arr[1], arr[2], arr[3]);
    }

    const R& operator[](const uint d) const {
        assert(d < size());
        return arr[d];
    }

    uint size() const {
        return 4;
    }
};

template<class R = float> class Mv02;

// mul
template <class R>
Mv0<R> operator*(const Mv0<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv0<R>((x[0] * y[0]));
}

template <class R>
Mv1<R> operator*(const Mv0<R> &x, const Mv1<R> &y) {
    assert(&x != &y);
    return Mv1<R>((x[0] * y[0]), (x[0] * y[1]), (x[0] * y[2]));
}

template <class R>
Mv2<R> operator*(const Mv0<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv2<R>((x[0] * y[0]), (x[0] * y[1]), (x[0] * y[2]));
}

template <class R>
Mv02<R> operator*(const Mv0<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>((x[0] * y[0]), (x[0] * y[1]), (x[0] * y[2]), (x[0] * y[3]));
}

template <class R>
Mv1<R> operator*(const Mv1<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv1<R>((x[0] * y[0]), (x[1] * y[0]), (x[2] * y[0]));
}

template <class R>
Mv02<R> operator*(const Mv1<R> &x, const Mv1<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((x[2] * y[2]) + (x[1] * y[1])), ((-x[1]) + (x[0] * y[1])), ((x[0] * y[2]) + (-x[2])), ((x[1] * y[2]) + (-x[2])));
}

template <class R>
Mv2<R> operator*(const Mv2<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv2<R>((x[0] * y[0]), (x[1] * y[0]), (x[2] * y[0]));
}

template <class R>
Mv02<R> operator*(const Mv2<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-x[0]) + (-x[1])), ((-x[1]) + (x[2] * y[1])), ((x[0] * y[2]) + (-x[2])), ((-x[0]) + (x[1] * y[0])));
}

template <class R>
Mv02<R> operator*(const Mv2<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-x[1]) + (-x[0])), ((x[2] * y[2]) + (-x[1])), ((-x[2]) + (x[0] * y[3])), ((-x[0]) + (x[2] * y[0])));
}

template <class R>
Mv02<R> operator*(const Mv02<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv02<R>((x[0] * y[0]), (x[1] * y[0]), (x[2] * y[0]), (x[3] * y[0]));
}

template <class R>
Mv02<R> operator*(const Mv02<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-x[3]) + (-x[1])), ((x[3] * y[1]) + (x[0] * y[0])), ((x[1] * y[2]) + (x[0] * y[1])), ((-x[1]) + (x[2] * y[0])));
}

template <class R>
Mv02<R> operator*(const Mv02<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-x[1]) + (x[0] * y[0])), ((x[3] * y[2]) + (x[0] * y[1])), ((x[1] * y[3]) + (x[2] * y[0])), ((-x[1]) + (x[3] * y[0])));
}

// inn
template <class R>
Mv0<R> operator|(const Mv0<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv0<R>((x[0] * y[0]));
}

template <class R>
Mv1<R> operator|(const Mv0<R> &x, const Mv1<R> &y) {
    assert(&x != &y);
    return Mv1<R>((x[0] * y[0]), (x[0] * y[1]), (x[0] * y[2]));
}

template <class R>
Mv2<R> operator|(const Mv0<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv2<R>((x[0] * y[0]), (x[0] * y[1]), (x[0] * y[2]));
}

template <class R>
Mv02<R> operator|(const Mv0<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>((x[0] * y[0]), (x[0] * y[1]), (x[0] * y[2]), (x[0] * y[3]));
}

template <class R>
Mv1<R> operator|(const Mv1<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv1<R>((x[0] * y[0]), (x[1] * y[0]), (x[2] * y[0]));
}

template <class R>
Mv0<R> operator|(const Mv1<R> &x, const Mv1<R> &y) {
    assert(&x != &y);
    return Mv0<R>(((x[2] * y[2]) + (x[1] * y[1])));
}

template <class R>
Mv1<R> operator|(const Mv1<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv1<R>(((-x[1]) + (-x[2])), ((x[0] * y[0]) + (-x[2])), ((x[1] * y[2]) + (x[0] * y[1])));
}

template <class R>
Mv1<R> operator|(const Mv1<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv1<R>(((-x[1]) + (x[0] * y[0])), ((x[0] * y[1]) + (-x[2])), ((x[1] * y[3]) + (x[2] * y[0])));
}

template <class R>
Mv2<R> operator|(const Mv2<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv2<R>((x[0] * y[0]), (x[1] * y[0]), (x[2] * y[0]));
}

template <class R>
Mv1<R> operator|(const Mv2<R> &x, const Mv1<R> &y) {
    assert(&x != &y);
    return Mv1<R>(((x[1] * y[2]) + (x[0] * y[1])), ((-x[0]) + (x[2] * y[2])), ((-x[1]) + (-x[2])));
}

template <class R>
Mv0<R> operator|(const Mv2<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv0<R>(((-x[0]) + (-x[1])));
}

template <class R>
Mv02<R> operator|(const Mv2<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-x[1]) + (-x[0])), (x[0] * y[0]), (x[1] * y[0]), (x[2] * y[0]));
}

template <class R>
Mv02<R> operator|(const Mv02<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv02<R>((x[0] * y[0]), (x[1] * y[0]), (x[2] * y[0]), (x[3] * y[0]));
}

template <class R>
Mv1<R> operator|(const Mv02<R> &x, const Mv1<R> &y) {
    assert(&x != &y);
    return Mv1<R>(((x[2] * y[2]) + (x[1] * y[1])), ((-x[1]) + (x[3] * y[2])), ((-x[3]) + (x[0] * y[2])));
}

template <class R>
Mv02<R> operator|(const Mv02<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-x[3]) + (-x[1])), (x[0] * y[0]), (x[0] * y[1]), (x[0] * y[2]));
}

template <class R>
Mv02<R> operator|(const Mv02<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-x[1]) + (x[0] * y[0])), ((x[0] * y[1]) + (x[1] * y[0])), ((x[2] * y[0]) + (x[0] * y[2])), ((x[3] * y[0]) + (x[0] * y[3])));
}

// inn2
template <class R>
Mv0<R> inn2(const Mv0<R> &x) {
    return Mv0<R>(pow(x[0], 2));
}

template <class R>
Mv0<R> inn2(const Mv1<R> &x) {
    return Mv0<R>((pow(x[0], 2) + pow(x[2], 2)));
}

template <class R>
Mv0<R> inn2(const Mv2<R> &x) {
    return Mv0<R>(((-pow(x[2], 2)) + (-pow(x[1], 2))));
}

template <class R>
Mv02<R> inn2(const Mv02<R> &x) {
    return Mv02<R>((pow(x[0], 2) + (-pow(x[2], 2))), (2 * x[0]), (2 * x[0]), (2 * x[0]));
}

// add
template <class R>
Mv0<R> operator+(const Mv0<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv0<R>((x[0] + y[0]));
}

template <class R>
Mv02<R> operator+(const Mv0<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv02<R>(x[0], y[0], y[1], y[2]);
}

template <class R>
Mv02<R> operator+(const Mv0<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>((x[0] + y[0]), y[1], y[2], y[3]);
}

template <class R>
Mv1<R> operator+(const Mv1<R> &x, const Mv1<R> &y) {
    assert(&x != &y);
    return Mv1<R>((x[0] + y[0]), (x[1] + y[1]), (y[2] + x[2]));
}

template <class R>
Mv02<R> operator+(const Mv2<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv02<R>(y[0], x[0], x[1], x[2]);
}

template <class R>
Mv2<R> operator+(const Mv2<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv2<R>((x[0] + y[0]), (x[1] + y[1]), (y[2] + x[2]));
}

template <class R>
Mv02<R> operator+(const Mv2<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>(y[0], (x[0] + y[1]), (x[1] + y[2]), (y[3] + x[2]));
}

template <class R>
Mv02<R> operator+(const Mv02<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv02<R>((x[0] + y[0]), x[1], x[2], x[3]);
}

template <class R>
Mv02<R> operator+(const Mv02<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv02<R>(x[0], (x[1] + y[0]), (y[1] + x[2]), (x[3] + y[2]));
}

template <class R>
Mv02<R> operator+(const Mv02<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>((x[0] + y[0]), (x[1] + y[1]), (y[2] + x[2]), (x[3] + y[3]));
}

// sub
template <class R>
Mv0<R> operator-(const Mv0<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv0<R>(((-y[0]) + x[0]));
}

template <class R>
Mv02<R> operator-(const Mv0<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv02<R>(x[0], (-y[0]), (-y[1]), (-y[2]));
}

template <class R>
Mv02<R> operator-(const Mv0<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-y[0]) + x[0]), (-y[1]), (-y[2]), (-y[3]));
}

template <class R>
Mv1<R> operator-(const Mv1<R> &x, const Mv1<R> &y) {
    assert(&x != &y);
    return Mv1<R>(((-y[0]) + x[0]), ((-y[1]) + x[1]), ((-y[2]) + x[2]));
}

template <class R>
Mv02<R> operator-(const Mv2<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv02<R>((-y[0]), x[0], x[1], x[2]);
}

template <class R>
Mv2<R> operator-(const Mv2<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv2<R>(((-y[0]) + x[0]), ((-y[1]) + x[1]), ((-y[2]) + x[2]));
}

template <class R>
Mv02<R> operator-(const Mv2<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>((-y[0]), ((-y[1]) + x[0]), (x[1] + (-y[2])), ((-y[3]) + x[2]));
}

template <class R>
Mv02<R> operator-(const Mv02<R> &x, const Mv0<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-y[0]) + x[0]), x[1], x[2], x[3]);
}

template <class R>
Mv02<R> operator-(const Mv02<R> &x, const Mv2<R> &y) {
    assert(&x != &y);
    return Mv02<R>(x[0], ((-y[0]) + x[1]), ((-y[1]) + x[2]), (x[3] + (-y[2])));
}

template <class R>
Mv02<R> operator-(const Mv02<R> &x, const Mv02<R> &y) {
    assert(&x != &y);
    return Mv02<R>(((-y[0]) + x[0]), ((-y[1]) + x[1]), ((-y[2]) + x[2]), (x[3] + (-y[3])));
}

// ostream
template <class R>
std::ostream& operator<<(std::ostream& t, const Mv0<R>& x) {
    t << "Mv0<R>(" << x[0] << ")";
}

template <class R>
std::ostream& operator<<(std::ostream& t, const Mv1<R>& x) {
    t << "Mv1<R>(" << x[0] << "," << x[1] << "," << x[2] << ")";
}

template <class R>
std::ostream& operator<<(std::ostream& t, const Mv2<R>& x) {
    t << "Mv2<R>(" << x[0] << "," << x[1] << "," << x[2] << ")";
}

template <class R>
std::ostream& operator<<(std::ostream& t, const Mv02<R>& x) {
    t << "Mv02<R>(" << x[0] << "," << x[1] << "," << x[2] << "," << x[3] << ")";
}

// const
const Mv1<float> e0(1,0,0);
const Mv1<float> e1(0,1,0);
const Mv1<float> e2(0,0,1);
const Mv3<float> I(1);

} // aga3

#endif // AGA3_HPP
