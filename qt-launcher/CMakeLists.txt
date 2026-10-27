cmake_minimum_required(VERSION 3.20)
project(vde-launcher LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS
    Core
    Gui
    Quick
    DBus
    Network
    Concurrent
)

# Source files
set(SOURCES
    src/main.cpp
    src/AppIndexer.h
    src/AppIndexer.cpp
    src/FileSearcher.h
    src/FileSearcher.cpp
    src/LocalAiClient.h
    src/LocalAiClient.cpp
    src/LauncherManager.h
    src/LauncherManager.cpp
    src/LauncherAdaptor.h
    src/LauncherAdaptor.cpp
)

# Executable target
add_executable(vde-launcher ${SOURCES})

# Qt QML module registration
qt_add_qml_module(vde-launcher
    URI Vde
    VERSION 1.0
    QML_FILES
        qml/Main.qml
        qml/AcrylicSurface.qml
        qml/PinnedGrid.qml
        qml/AllAppsList.qml
        qml/SearchResultsView.qml
        tokens/ThemeTokens.qml
)

target_link_libraries(vde-launcher PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Quick
    Qt6::DBus
    Qt6::Network
    Qt6::Concurrent
)

install(TARGETS vde-launcher RUNTIME DESTINATION bin)
