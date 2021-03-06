# Settings passed on the command line:
#
# PROJECT_LIBS_DIR = the directory which all external libraries may be referenced from.
# PROJECT_ARCH = the build architecture
# PROJECT_LINK = whether to build a static or dynamic library.

##############################
# General Settings
##############################

cmake_minimum_required (VERSION 2.8.9)
project (boss)

set (BOSS_SRC   "${CMAKE_SOURCE_DIR}/src/backend/metadata.cpp"
                "${CMAKE_SOURCE_DIR}/src/backend/game.cpp"
                "${CMAKE_SOURCE_DIR}/src/backend/helpers.cpp"
                "${CMAKE_SOURCE_DIR}/src/backend/network.cpp"
                "${CMAKE_SOURCE_DIR}/src/backend/globals.cpp"
                "${CMAKE_SOURCE_DIR}/src/backend/graph.cpp"
                "${PROJECT_LIBS_DIR}/pugixml/src/pugixml.cpp")

set (BOSS_GUI_SRC ${BOSS_SRC}
                  "${CMAKE_SOURCE_DIR}/src/gui/ids.cpp"
                  "${CMAKE_SOURCE_DIR}/src/gui/main.cpp"
                  "${CMAKE_SOURCE_DIR}/src/gui/settings.cpp"
                  "${CMAKE_SOURCE_DIR}/src/gui/editor.cpp"
                  "${CMAKE_SOURCE_DIR}/src/gui/viewer.cpp"
                  "${CMAKE_SOURCE_DIR}/src/gui/misc.cpp"
                  "${CMAKE_SOURCE_DIR}/src/resource.rc")

set (BOSS_API_SRC ${BOSS_SRC}
                  "${CMAKE_SOURCE_DIR}/src/api/api.cpp")

# Include source and library directories.
include_directories ("${CMAKE_SOURCE_DIR}/src"
                     "${PROJECT_LIBS_DIR}/alphanum"
                     "${PROJECT_LIBS_DIR}/boost"
                     "${PROJECT_LIBS_DIR}/yaml-cpp/include"
                     "${PROJECT_LIBS_DIR}/libloadorder/src"
                     "${PROJECT_LIBS_DIR}/libespm"
                     "${PROJECT_LIBS_DIR}/zlib"
                     "${PROJECT_LIBS_DIR}/pugixml/src"
                     "${PROJECT_LIBS_DIR}/libgit2/include"
                     "${PROJECT_LIBS_DIR}/wxWidgets/include")

link_directories ("${PROJECT_LIBS_DIR}/libloadorder/build"
                  "${PROJECT_LIBS_DIR}/zlib/build"
                  "${PROJECT_LIBS_DIR}/libgit2/build"
                  "${PROJECT_LIBS_DIR}/yaml-cpp/build"
                  "${PROJECT_LIBS_DIR}/boost/stage-${PROJECT_ARCH}/lib")


##############################
# System-Specific Settings
##############################

# Settings when compiling for Windows. Since it's a Windows-only app this is always true, but useful to check for copy/paste into other projects.
IF (CMAKE_SYSTEM_NAME MATCHES "Windows")
    add_definitions (-DUNICODE -D_UNICODE -D__WXMSW__ -DNDEBUG -DLIBLO_STATIC -DWIN32 -D_WINDOWS)
    IF (${PROJECT_LINK} MATCHES "STATIC")
        add_definitions (-DBOSS_STATIC)
    ELSE ()
        add_definitions (-DBOSS_EXPORT)
    ENDIF ()
ENDIF ()

# MinGW settings.
IF (MINGW)
    include_directories("${PROJECT_LIBS_DIR}/wxWidgets/lib/wx/include/${COMPILER_PREFIX}-msw-unicode-static-3.0")
    link_directories("${PROJECT_LIBS_DIR}/openssl"
                     "${PROJECT_LIBS_DIR}/wxWidgets/lib")
    set (CMAKE_C_FLAGS  "-m${PROJECT_ARCH} -O3")
    set (CMAKE_CXX_FLAGS "-m${PROJECT_ARCH} -O3")
    set (CMAKE_EXE_LINKER_FLAGS "-static-libstdc++ -static-libgcc -Wl,--subsystem,windows")
    set (CMAKE_SHARED_LINKER_FLAGS "-static-libstdc++ -static-libgcc -Wl,--subsystem,windows")
    set (CMAKE_MODULE_LINKER_FLAGS "-static-libstdc++ -static-libgcc -Wl,--subsystem,windows")
    set (BOSS_LIBS ${BOSS_LIBS}
                   yaml-cpp
                   boost_log_setup
                   boost_log
                   boost_locale
                   boost_thread_win32
                   boost_chrono
                   boost_date_time
                   boost_filesystem
                   boost_system
                   boost_regex
                   version
                   git2
                   zlibstatic
                   loadorder${PROJECT_ARCH}
                   ssl
                   crypto
                   ws2_32)
    set (BOSS_GUI_LIBS ${BOSS_LIBS}
                       wx_mswu_webview-3.0-${COMPILER_PREFIX}
                       wx_mswu_core-3.0-${COMPILER_PREFIX}
                       wx_baseu-3.0-${COMPILER_PREFIX}
                       wx_mswu_adv-3.0-${COMPILER_PREFIX}
                       wxpng-3.0-${COMPILER_PREFIX}
                       wxzlib-3.0-${COMPILER_PREFIX}
                       comctl32)
ELSEIF (MSVC)
    #IF (MSVC_VERSION EQUAL 1800) 
        set (CMAKE_GENERATOR_TOOLSET "v120_xp" CACHE STRING "Platform Toolset" FORCE)
    #ENDIF ()
    include_directories("${PROJECT_LIBS_DIR}/wxWidgets/lib/vc_lib/mswu")
    link_directories("${PROJECT_LIBS_DIR}/wxWidgets/lib/vc_lib")
	set (CMAKE_CXX_FLAGS "/EHsc")
    set (CMAKE_EXE_LINKER_FLAGS "/SUBSYSTEM:WINDOWS")
    set (BOOST_SUFFIX "-vc120-mt-1_55")
    set (BOSS_LIBS ${BOSS_LIBS}
                   libyaml-cppmd
                   libboost_log_setup${BOOST_SUFFIX}
                   libboost_log${BOOST_SUFFIX}
                   libboost_locale${BOOST_SUFFIX}
                   libboost_thread${BOOST_SUFFIX}
                   libboost_chrono${BOOST_SUFFIX}
                   libboost_date_time${BOOST_SUFFIX}
                   libboost_filesystem${BOOST_SUFFIX}
                   libboost_system${BOOST_SUFFIX}
                   libboost_regex${BOOST_SUFFIX}
                   version
                   git2
                   zlibstatic
                   loadorder${PROJECT_ARCH}
                   ws2_32)
    set (BOSS_GUI_LIBS ${BOSS_LIBS}
                       wxmsw30u_webview
                       wxmsw30u_adv
                       wxmsw30u_core
                       wxbase30u
                       wxpng
                       wxzlib
                       comctl32)
ENDIF ()


##############################
# Actual Building
##############################

# Build API.
add_library           (boss${PROJECT_ARCH} ${PROJECT_LINK} ${BOSS_API_SRC})
target_link_libraries (boss${PROJECT_ARCH} ${BOSS_LIBS})

# Build application.
add_executable        (BOSS ${BOSS_GUI_SRC})
target_link_libraries (BOSS ${BOSS_GUI_LIBS})

# Build converter.
add_executable        (masterlist-converter ${BOSS_SRC} "${CMAKE_SOURCE_DIR}/src/converter.cpp")
target_link_libraries (masterlist-converter ${BOSS_LIBS})

