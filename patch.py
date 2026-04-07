from pathlib import Path
from typing import List
from patch_utils import *

with open('Version.txt', 'r') as f:
    data = f.readlines()
    version_major = int(data[0].split('=')[1])
    version_minor = int(data[1].split('=')[1])
newer_than_v9_12 = (version_major, version_minor) >= (9, 12)
newer_than_v9_13 = (version_major, version_minor) >= (9, 13)

additions: List[Addition] = []
replacements: List[Addition] = []

# add the USE_SIRIUS configuration flag in CMakeLists.txt
additions.append(Addition(
    Path.cwd()/'CMakeLists.txt',
    '''option(USE_CPLEX "Use the CPLEX solver" OFF)
message(STATUS "CPLEX support: ${USE_CPLEX}")

''',
    '''option(USE_SIRIUS "Build and use SIRIUS interface" OFF)
message(STATUS "SIRIUS support: ${USE_SIRIUS}")

'''))

# add the USE_SIRIUS configuration flag in cpp.cmake

additions.append(
    Addition(
        Path.cwd()/'cmake'/'cpp.cmake',
        '  ${SCIP_DEPS}\n' if newer_than_v9_12 else '  $<$<BOOL:${USE_SCIP}>:libscip>\n',
        '  $<$<BOOL:${USE_SIRIUS}>:sirius_solver>\n'))
additions.append(Addition(
    Path.cwd()/'cmake'/'cpp.cmake',
    '''
if(USE_CPLEX)
  list(APPEND OR_TOOLS_COMPILE_DEFINITIONS "USE_CPLEX")
endif()
''',
    '''
if(USE_SIRIUS)
  list(APPEND OR_TOOLS_COMPILE_DEFINITIONS "USE_SIRIUS")
endif()
'''))

# add the USE_SIRIUS configuration flag in deps.cmake
lookup = '''
if(USE_CPLEX)
  if(NOT TARGET CPLEX::CPLEX)
    find_package(CPLEX REQUIRED)
  endif()
endif()
''' if newer_than_v9_13 else '''
if(USE_CPLEX)
  find_package(CPLEX REQUIRED)
endif()
'''
additions.append(Addition(
    Path.cwd()/'cmake'/'system_deps.cmake',
    lookup,
    '''
#add SIRIUS
if (USE_SIRIUS)
  include(cmake_patches/sirius.cmake)
  if(POLICY CMP0074)
    cmake_policy(SET CMP0074 NEW)
  endif()
  find_package(sirius_solver CONFIG REQUIRED)
endif(USE_SIRIUS)
'''))

# add the USE_SIRIUS configuration flag in ortoolsConfig.cmake.in
lookup = '''
if(@USE_SCIP@)
  if(NOT TARGET SCIP::libscip)
    find_dependency(SCIP REQUIRED)
  endif()
endif()
''' if newer_than_v9_13 else '''
if(@USE_SCIP@)
  if(NOT TARGET libscip)
    find_dependency(SCIP REQUIRED)
  endif()
endif()
'''
additions.append(Addition(
    Path.cwd()/'cmake'/'ortoolsConfig.cmake.in',
    lookup,
    '''
if(@USE_SIRIUS@)
  if(POLICY CMP0074)
	  cmake_policy(SET CMP0074 NEW)
	endif()
  if(NOT sirius_solver_FOUND AND NOT TARGET sirius_solver)
    find_dependency(sirius_solver REQUIRED ${CONFIG_FLAG})
  endif()
endif()
'''))

additions.append(Addition(
    Path.cwd()/'examples'/'java'/'LinearProgramming.java',
    '''    runLinearProgrammingExample("CLP", false);
''',
    '''    System.out.println("---- Linear programming example with Sirius ----");
    runLinearProgrammingExample("SIRIUS_LP", false);
'''))

additions.append(Addition(
    Path.cwd()/'examples'/'python'/'linear_programming.py',
    '    RunLinearExampleCppStyleAPI("XPRESS_LP")\n',
    '    RunLinearExampleCppStyleAPI("SIRIUS_LP")\n'))

# add the USE_SIRIUS configuration flag in ortools/linear_solver/CMakeLists.txt
lookup = '  $<$<BOOL:${USE_SCIP}>:SCIP::libscip>\n' if newer_than_v9_13 else '  $<$<BOOL:${USE_SCIP}>:libscip>\n'
additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'CMakeLists.txt',
    lookup,
    '  $<$<BOOL:${USE_SIRIUS}>:sirius_solver>\n'))

additions.append(Addition(
    Path.cwd() / 'ortools' / 'linear_solver' / 'CMakeLists.txt',
    '''if(USE_XPRESS)
  list(APPEND _SRCS xpress_interface.cc)
endif()
''',
    '''
if(USE_SIRIUS)
  list(APPEND _SRCS sirius_interface.cc)
endif()
'''
))

additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'CMakeLists.txt',
    '''  add_test(NAME cxx_unittests_xpress_interface COMMAND test_xprs_interface)
''',
    '''  endif()

  if (USE_SIRIUS)
    add_executable(test_sirius_interface sirius_interface_test.cc)
    target_compile_features(test_sirius_interface PRIVATE cxx_std_17)
    target_link_libraries(test_sirius_interface PRIVATE ortools::ortools GTest::gtest_main)

    add_test(NAME cxx_unittests_sirius_interface COMMAND test_sirius_interface)
'''))

# add the SIRIUS support in ortools/linear_solver/linear_solver.cc & .h

additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'linear_solver.cc',
    '''case MPModelRequest::CPLEX_LINEAR_PROGRAMMING:
      return false;
''',
    '''#ifdef USE_SIRIUS
    case MPModelRequest::SIRIUS_LINEAR_PROGRAMMING:
      return false;
#endif
'''))
additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'linear_solver.cc',
    '''case MPModelRequest::CPLEX_MIXED_INTEGER_PROGRAMMING:
      return true;
''',
    '''#ifdef USE_SIRIUS
    case MPModelRequest::SIRIUS_MIXED_INTEGER_PROGRAMMING:
      return false;
#endif
'''))

additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'linear_solver.cc',
    '''        {MPSolver::XPRESS_MIXED_INTEGER_PROGRAMMING, "xpress"},
''',
    '''        {MPSolver::SIRIUS_LINEAR_PROGRAMMING, "sirius_lp"},
        {MPSolver::SIRIUS_MIXED_INTEGER_PROGRAMMING, "sirius"},
'''))

additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'linear_solver.h',
    '''    COPT_MIXED_INTEGER_PROGRAMMING = 104,
''',
    '''    SIRIUS_LINEAR_PROGRAMMING = 105,
    SIRIUS_MIXED_INTEGER_PROGRAMMING = 106,
'''))

additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'linear_solver.h',
    '  friend class XpressInterface;\n',
    '  friend class SiriusInterface;\n'))

additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'linear_solver.proto',
    'HIGHS_LINEAR_PROGRAMMING = 15;\n',
    '''    SIRIUS_LINEAR_PROGRAMMING = 110;
    SIRIUS_MIXED_INTEGER_PROGRAMMING = 111;
    '''
))

# enable xpress for mathopt-python (to remove starting v9.16)
additions.append(Addition(
    Path.cwd()/'ortools'/'math_opt'/'python'/'parameters.py',
    'SANTORINI = math_opt_parameters_pb2.SOLVER_TYPE_SANTORINI\n',
    '    XPRESS = math_opt_parameters_pb2.SOLVER_TYPE_XPRESS\n'
))

replacements.append(
    Addition(
    Path.cwd()/'cmake'/'dependencies'/'CMakeLists.txt',
    'set(BUILD_TESTING OFF)\n',
    ''
))

# run patch
for a in additions:
    add_in_file(a.filepath, a.search, a.search+a.add)
for a in replacements:
    replace_in_file(a.filepath, a.search, a.add)
