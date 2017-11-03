#include <Python.h>
#include <stdio.h>
#include <math.h>

//Actual module method definition - this is the code that will be called by
//demo.print_hello_world
static PyObject* demo_print_hello_world(PyObject *self, PyObject *args)
{
   float a;
   float b;
   float c;

   if (!PyArg_ParseTuple(args, "ff", &a, &b)) {
      return NULL;
   }

   c = sin(a)*cos(b)*tan(a*b);

   return Py_BuildValue("f", c);
}

//Method definition object for this extension, these argumens mean:
//ml_name: The name of the method
//ml_meth: Function pointer to the method implementation
//ml_flags: Flags indicating special features of this method, such as
//          accepting arguments, accepting keyword arguments, being a
//          class method, or being a static method of a class.
//ml_doc:  Contents of this method's docstring
static PyMethodDef demo_methods[] = {
    {
        "print_hello_world",
        demo_print_hello_world,
        METH_VARARGS,
        "Print 'hello world' from a method defined in a C extension."
    },
    {NULL, NULL, 0, NULL}
};

//Module definition
//The arguments of this structure tell Python what to call your extension,
//what it's methods are and where to look for it's method definitions
static struct PyModuleDef demo_definition = {
    PyModuleDef_HEAD_INIT,
    "demo",
    "A Python module that prints 'hello world' from C code.",
    -1,
    demo_methods
};

//Module initialization
//Python calls this function when importing your extension. It is important
//that this function is named PyInit_[[your_module_name]] exactly, and matches
//the name keyword argument in setup.py's setup() call.
PyMODINIT_FUNC PyInit_demo(void)
{
    Py_Initialize();

    return PyModule_Create(&demo_definition);
}