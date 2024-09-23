from pathlib import Path
from typing import List
from patch_utils import *

additions: List[Addition] = []
replacements: List[Replacement] = []

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
    '  $<$<BOOL:${USE_SCIP}>:libscip>\n',
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
additions.append(Addition(
    Path.cwd()/'cmake'/'system_deps.cmake',
    '''
if(USE_CPLEX)
  find_package(CPLEX REQUIRED)
endif()
''',
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
additions.append(Addition(
    Path.cwd()/'cmake'/'ortoolsConfig.cmake.in',
    '''
if(@USE_SCIP@)
  if(NOT scip_FOUND AND NOT TARGET libscip)
    find_dependency(SCIP REQUIRED)
  endif()
endif()
''',
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

# add SIRIUS execution in example files
additions.append(Addition(
    Path.cwd()/'examples'/'cpp'/'linear_programming.cc',
    '  RunLinearProgrammingExample("XPRESS_LP");\n',
    '  RunLinearProgrammingExample("SIRIUS_LP");\n'
    ))

additions.append(Addition(
    Path.cwd()/'examples'/'dotnet'/'cslinearprogramming.cs',
    '        RunLinearProgrammingExample("XPRESS_LP");\n',
    '        RunLinearProgrammingExample("SIRIUS_LP");\n'
    ))

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
additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'CMakeLists.txt',
    '  $<$<BOOL:${USE_SCIP}>:libscip>\n',
    '  $<$<BOOL:${USE_SIRIUS}>:sirius_solver>\n'))

additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'CMakeLists.txt',
    '''  add_test(NAME cxx_unittests_xpress_interface COMMAND test_xprs_interface)
''',
    '''  if (USE_SIRIUS)
    add_executable(test_sirius_interface sirius_interface_test.cc)
    target_compile_features(test_sirius_interface PRIVATE cxx_std_17)
    target_link_libraries(test_sirius_interface PRIVATE ortools::ortools GTest::gtest_main)

    add_test(NAME cxx_unittests_sirius_interface COMMAND test_sirius_interface)
  endif()
'''))

# add the SIRIUS support in ortools/linear_solver/linear_solver.cc & .h
additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'linear_solver.cc',
    '''extern MPSolverInterface* BuildXpressInterface(bool mip,
                                               MPSolver* const solver);
''',
    '''#if defined(USE_SIRIUS)
extern MPSolverInterface* BuildSiriusInterface(bool mip, MPSolver* const solver);
#endif
'''))

additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'linear_solver.cc',
    '''      return BuildXpressInterface(false, solver);
''',
    '''#if defined(USE_SIRIUS)
	case MPSolver::SIRIUS_LINEAR_PROGRAMMING:
		return BuildSiriusInterface(false, solver);
	case MPSolver::SIRIUS_MIXED_INTEGER_PROGRAMMING:
		return BuildSiriusInterface(true, solver);
#endif
'''))

additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'linear_solver.cc',
    '''#ifdef USE_CPLEX
  if (problem_type == CPLEX_LINEAR_PROGRAMMING ||
      problem_type == CPLEX_MIXED_INTEGER_PROGRAMMING) {
    return true;
  }
#endif
''',
    '''#ifdef USE_SIRIUS
  if (problem_type == SIRIUS_MIXED_INTEGER_PROGRAMMING) return true;
  if (problem_type == SIRIUS_LINEAR_PROGRAMMING) return true;
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

# add temporary patch for XPressInterface
additions.append(Addition(
    Path.cwd()/'ortools'/'linear_solver'/'xpress_interface.cc',
    '''#include "absl/strings/str_format.h"
#include "ortools/base/logging.h"''',
    '''#include "absl/strings/numbers.h"
#include "absl/strings/str_format.h"
#include "ortools/base/logging.h"'''))

replacements.append(Replacement(
    Path.cwd()/'ortools'/'linear_solver'/'xpress_interface.cc',
    '''  }
}

const char* stringToCharPtr(std::string& var) { return var.c_str(); }

// Save the existing locale, use the "C" locale to ensure that
// string -> double conversion is done ignoring the locale.
struct ScopedLocale {
  ScopedLocale() {
    oldLocale = std::setlocale(LC_NUMERIC, nullptr);
    auto newLocale = std::setlocale(LC_NUMERIC, "C");
    CHECK_EQ(std::string(newLocale), "C");
  }
  ~ScopedLocale() { std::setlocale(LC_NUMERIC, oldLocale); }
+bool stringToCharPtr(const std::string& var, const char** out) {
 
 private:
  const char* oldLocale;
};

#define setParamIfPossible_MACRO(target_map, setter, converter)          \
  {                                                                      \
    auto matchingParamIter = (target_map).find(paramAndValuePair.first); \
    if (matchingParamIter != (target_map).end()) {                       \
      const auto convertedValue = converter(paramAndValuePair.second);   \
      VLOG(1) << "Setting parameter " << paramAndValuePair.first         \
              << " to value " << convertedValue << std::endl;            \
      setter(mLp, matchingParamIter->second, convertedValue);            \
      continue;                                                          \
    }''',
    '''  }
}

bool stringToCharPtr(const std::string& var, const char** out) {
  *out = var.c_str();
  return true;
}

#define setParamIfPossible_MACRO(target_map, setter, converter, type)    \
  {                                                                      \
    auto matchingParamIter = (target_map).find(paramAndValuePair.first); \
    if (matchingParamIter != (target_map).end()) {                       \
      type convertedValue;                                               \
      bool ret = converter(paramAndValuePair.second, &convertedValue);   \
      if (ret) {                                                         \
        VLOG(1) << "Setting parameter " << paramAndValuePair.first       \
                << " to value " << convertedValue << std::endl;          \
      }                                                                  \
      setter(mLp, matchingParamIter->second, convertedValue);            \
      continue;                                                          \
    }'''
))

replacements.append(Replacement(
    Path.cwd()/'ortools'/'linear_solver'/'xpress_interface.cc',
    '''    }
  }

  ScopedLocale locale;
  for (auto& paramAndValuePair : paramAndValuePairList) {
    setParamIfPossible_MACRO(mapIntegerControls_, XPRSsetintcontrol, std::stoi);
    setParamIfPossible_MACRO(mapDoubleControls_, XPRSsetdblcontrol, std::stod);
    setParamIfPossible_MACRO(mapStringControls_, XPRSsetstrcontrol,
                             stringToCharPtr);
    setParamIfPossible_MACRO(mapInteger64Controls_, XPRSsetintcontrol64,
                             std::stoll);
    LOG(ERROR) << "Unknown parameter " << paramName << " : function "
               << __FUNCTION__ << std::endl;
    return false;
''',
    '''    }
  }

  for (auto& paramAndValuePair : paramAndValuePairList) {
    setParamIfPossible_MACRO(mapIntegerControls_, XPRSsetintcontrol,
                             absl::SimpleAtoi<int>, int);
    setParamIfPossible_MACRO(mapDoubleControls_, XPRSsetdblcontrol,
                             absl::SimpleAtod, double);
    setParamIfPossible_MACRO(mapStringControls_, XPRSsetstrcontrol,
                             stringToCharPtr, const char*);
    setParamIfPossible_MACRO(mapInteger64Controls_, XPRSsetintcontrol64,
                             absl::SimpleAtoi<int64_t>, int64_t);
    LOG(ERROR) << "Unknown parameter " << paramName << " : function "
               << __FUNCTION__ << std::endl;
    return false;
'''
))


# run patch
for a in additions:
    replace_in_file(a.filepath, a.search, a.search+a.add)
for r in replacements:
    replace_in_file(r.filepath, r.search, r.replace)