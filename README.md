ProjectSAMPLE
=============

A graphical-output compiler that receives input commands, displaying drawing and figures. Uses *PLY* as lexical-syntax analysis; *Python* language for virtual machine.

**/ply** - Python module which contains lex and yacc.

**parsetable.py** - Includes parse table and productions.

**parser.out** - Debug file for S/R, R/R conflicts.

**sample_ly.py** - Lex/Yacc analysis, including table/directory construction activities.

**cube_sem.py** - Operator comparisson analysis

**tabvars.py** - Python class TabVar, retains all variables found.

**out-tabla_vars** - TabVar output

**tabconst.py** - Python class TabConst, retains all constants found.

**out-tabla_const** - TabConst output

**dirmods.py** - Python class DirMods, retains all modules found.

**out-dir_mods** - DirMods output

**codegen.py** - Python class CodeGen, retains all generated quadruples.

**error.py** - Python file, includes error statements while compiling a Sample input.

**out-quads** - CodeGen output

**quads.smo** - Sample quads file .smo

**sample.smo** - Sample object file .smo, includes module directory, constants and quads.

**run_sample.py** - Sample runtime file, read and executes .smo file.

**memory.py** - Python class Memory, serves as virtual memory for runtime procedures.

**error_exec.py** - Python file, includes error statements while running a Sample input.

**tabdims.py** - Python class TabDims, retains dimension values for arrays and matrices.

**tabpointers.py** - Python class TabPointer, saves memory value for a certain array/matrix index location.

Input examples: */ej*
