cmake_minimum_required(VERSION 3.3)
project(__CODINGAME__)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    FACILE/Le_pouvoir_de_Thor/C++/solution_avec_template_v1.cpp
    FACILE/Temperatures/C++/solution_std.cpp
    MOYEN/Indiana_-_Niveau_1/C++/solution_IA_simple.cpp
    TRES_DIFFICILE/Nintendo_Sponsored_Challenge/encode.cpp
    TRES_DIFFICILE/Nintendo_Sponsored_Challenge/solution.cpp
    TUTORIEL/Onboarding/C++/solution.cpp)

add_executable(__CODINGAME__ ${SOURCE_FILES})