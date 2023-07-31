#!/bin/bash
if [ -d "build" ]; then
  rm -rf build dist
fi
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --target all -- -j 8
