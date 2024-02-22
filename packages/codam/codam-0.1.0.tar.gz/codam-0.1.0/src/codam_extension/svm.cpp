#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(svm_extension, m) {
    m.def("add", &add, "A function that adds two numbers");
}
