#!/bin/bash
set -e -u -x

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT" -w /io/wheelhouse/
    fi
}


# Install a system package required by our library
yum install -y atlas-devel

ls -al /opt/python
# Compile wheels
for PYBIN in /opt/python/cp36-cp36m/bin /opt/python/cp37-cp37m/bin /opt/python/cp38-cp38/bin; do
    cd /io
    "${PYBIN}/pip" install -e .
    "${PYBIN}/pip" wheel /io/ --no-deps -w wheelhouse/${PYBIN}
done

ls -alR wheelhouse
# Bundle external shared libraries into the wheels
basepath=/io/wheelhouse/opt/python
wheelname=pylogging-0.3.0-py3-none-any.whl

for whl in ${basepath}/cp36-cp36m/bin/${wheelname} ${basepath}/cp37-cp37m/bin/${wheelname} ${basepath}/cp38-cp38/bin/${wheelname}; do
    repair_wheel "$whl"
done

# Install packages and test
for PYBIN in /opt/python/cp36-cp36m/bin /opt/python/cp37-cp37m/bin /opt/python/cp38-cp38/bin; do
    # "${PYBIN}/pip" install pylogging-py3-none-any.whl --no-index -f /io/wheelhouse${PYBIN}
    "${PYBIN}/pip" install --no-index /io/wheelhouse${PYBIN}/${wheelname}
done

