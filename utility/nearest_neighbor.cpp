/**
 * This file defines an analogous algorithm to call in C++ as the one defined
 * in the Python counterpart in order to boost efficiency.
*/

/** Environment Setup **/
#include <iostream>             // I/O for coordinates, etc.
#include <vector>               // storing matrices
#include <utility>              // coordinates

using namespace std;            // I ain't typing std:: 50000 times bruh


/** Auxiliary Functions **/
float distance(pair<float, float> p1, pair<float, float> p2)
{
    // return distance //
    return sqrt(pow(p1.first - p2.first, 2) + pow(p1.second - p2.second, 2));
}



