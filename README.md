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

**out-quads** - CodeGen output

**quads.smo** - Sample object file .smo

Input examples: */ej*
