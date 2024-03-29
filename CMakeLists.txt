cmake_minimum_required (VERSION 2.8)


# possible values: Release, Debug, RelWithDebugInfo
set(CMAKE_BUILD_TYPE RelWithDebugInfo)

project(ladspa.m.proto)
set(PROJECT_VERSION "1")

# set(CMAKE_INSTALL_PREFIX /usr)

set(CPACK_PACKAGE_VERSION 1)
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Florian Paul Schmidt (mista.tapas@gmx.net)")
set(CPACK_GENERATOR "DEB" "TGZ")
set(CPACK_DEBIAN_PACKAGE_DEPENDS "ladspamm-1-dev, libboost-timer-dev")
set(CPACK_DEBIAN_PACKAGE_NAME "ladspa.m.proto-${PROJECT_VERSION}-dev")
include(CPack)

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE Native CACHE STRING
      "Choose the type of build, options are: None Debug Release RelWithDebInfo MinSizeRel Native."
      FORCE)
ENDIF(NOT CMAKE_BUILD_TYPE)

enable_testing()

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake-modules")


find_package(Protobuf REQUIRED)

set(PYTHON "python")
execute_process (COMMAND ${PYTHON} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(prefix='')" OUTPUT_VARIABLE PYTHON_SITE_PACKAGES OUTPUT_STRIP_TRAILING_WHITESPACE)

set(CMAKE_VERBOSE_MAKEFILE off)

configure_file(ladspam.proto.in ${PROJECT_SOURCE_DIR}/ladspam${PROJECT_VERSION}.proto @ONLY)
configure_file(ladspa.m.proto.pc.in ${PROJECT_SOURCE_DIR}/ladspa.m.proto-${PROJECT_VERSION}.pc @ONLY)
configure_file(ladspam_pb2_util.py.in ${PROJECT_SOURCE_DIR}/ladspam${PROJECT_VERSION}_pb2_util.py)

# configure_file(ladspa.m/synth.h.in ladspa.m-${PROJECT_VERSION}/synth.h)

# configure_file(ladspa.m.test.synth.cc.in ladspa.m.test.synth.cc)

include_directories(${PROJECT_BINARY_DIR})

add_definitions(-DPROJECT_VERSION=\"${PROJECT_VERSION}\")

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wconversion -Wall -pthread -fmax-errors=1")

if(CMAKE_BUILD_TYPE MATCHES Debug)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0 -pg")
endif()

if (CMAKE_BUILD_TYPE MATCHES Release)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")
    add_definitions("-DNDEBUG")
endif()

if (CMAKE_BUILD_TYPE MATCHES RelWithDebugInfo)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -g")
    add_definitions("-DNDEBUG")
endif()

if (CMAKE_BUILD_TYPE MATCHES Native)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=native -mtune=native -mfpmath=sse")
    add_definitions("-DNDEBUG")
endif()

if (CMAKE_BUILD_TYPE MATCHES NativeKvm)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=native -mtune=native -mfpmath=sse -mno-avx")
    add_definitions("-DNDEBUG")
endif()

message(STATUS "The build type is: " ${CMAKE_BUILD_TYPE})

SET(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)


#
# BUILD DEPENDENCIES:
#

#find_package(PkgConfig REQUIRED)
#pkg_check_modules(LADSPAMM REQUIRED ladspamm-1)

#find_package(Boost COMPONENTS timer REQUIRED)

#
# TARGETS
# 

protobuf_generate_cpp(LADSPAM_PROTOBUF_SOURCES LADSPAM_PROTOBUF_HEADERS ladspam${PROJECT_VERSION}.proto)
add_library(ladspa.m.proto-${PROJECT_VERSION} SHARED ${LADSPAM_PROTOBUF_SOURCES})
set_target_properties(ladspa.m.proto-${PROJECT_VERSION} PROPERTIES COMPILE_FLAGS "-Wno-conversion")

protobuf_generate_python(LADSPAM_PROTOBUF_PYTHON_SOURCES ladspam${PROJECT_VERSION}.proto)
add_custom_target(py DEPENDS ${LADSPAM_PROTOBUF_PYTHON_SOURCES})
add_dependencies(ladspa.m.proto-${PROJECT_VERSION} py)

#add_executable(ladspa.m.test.synth-${PROJECT_VERSION} ${PROJECT_BINARY_DIR}/ladspa.m.test.synth.cc)
#target_link_libraries(ladspa.m.test.synth-${PROJECT_VERSION} ${LADSPAMM_LIBRARIES} ${Boost_LIBRARIES})

# 
# INSTALLATION
# 

#install(DIRECTORY ${PROJECT_BINARY_DIR}/ladspa.m-${PROJECT_VERSION}  DESTINATION include)
#install(FILES ${PROJECT_BINARY_DIR}/ladspam DESTINATION lib/pkgconfig)

install(TARGETS ladspa.m.proto-${PROJECT_VERSION} LIBRARY DESTINATION lib)
install(FILES ladspa.m.proto-${PROJECT_VERSION}.pc  DESTINATION lib/pkgconfig)
install(FILES ${PROJECT_BINARY_DIR}/ladspam${PROJECT_VERSION}.pb.h DESTINATION include/ladspa.m.proto-${PROJECT_VERSION})
install(FILES ${LADSPAM_PROTOBUF_PYTHON_SOURCES} DESTINATION ${PYTHON_SITE_PACKAGES}/)
install(FILES ladspam${PROJECT_VERSION}_pb2_util.py DESTINATION ${PYTHON_SITE_PACKAGES}/)
