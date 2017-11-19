from distutils.core import setup, Extension


quaternionC = Extension('demo',
                    sources = ['quaternion_sim/geometry.cpp'])

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='quaternion_sim',
    version='0.1',
    packages=['quaternion_sim'],
    url='https://github.com/sylvaus/quaternion-sim',
    license='',
    author='Py',
    author_email='',
    description='',
    long_description=readme(),
    requires=['numpy', 'PyQt4', "PyOpenGL_accelerate"],
    install_requires=['numpy', "PyOpenGL", "PyOpenGL_accelerate"],
    python_requires='>=3',
    ext_modules = [quaternionC]
)
