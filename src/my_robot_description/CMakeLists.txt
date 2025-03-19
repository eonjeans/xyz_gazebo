cmake_minimum_required(VERSION 3.8)
project(my_robot_description)

# ==========================================
# 컴파일 옵션
# ==========================================
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ==========================================
# 패키지 의존성
# ==========================================
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(gazebo_dev REQUIRED)
find_package(gazebo_msgs REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)
find_package(Protobuf REQUIRED)
find_package(TBB REQUIRED)

# ==========================================
# C++ 표준 설정
# ==========================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ==========================================
# include 경로 (추후 헤더 파일 대비)
# ==========================================
include_directories(
  include
  ${Boost_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
)

link_directories(
  ${GAZEBO_LIBRARY_DIRS}
)

# ==========================================
# animated_box 플러그인 라이브러리 빌드
# ==========================================
# animated_box_1
add_library(animated_box_1 SHARED src/animated_box_plugin/animated_box_1.cc)
ament_target_dependencies(animated_box_1
  rclcpp
  gazebo_dev
  Boost
)
target_link_libraries(animated_box_1 ${GAZEBO_LIBRARIES})

# animated_box_2
add_library(animated_box_2 SHARED src/animated_box_plugin/animated_box_2.cc)
ament_target_dependencies(animated_box_2
  rclcpp
  gazebo_dev
  Boost
)
target_link_libraries(animated_box_2 ${GAZEBO_LIBRARIES})

# animated_box_3
add_library(animated_box_3 SHARED src/animated_box_plugin/animated_box_3.cc)
ament_target_dependencies(animated_box_3
  rclcpp
  gazebo_dev
  Boost
)
target_link_libraries(animated_box_3 ${GAZEBO_LIBRARIES})

# animated_box_4
add_library(animated_box_4 SHARED src/animated_box_plugin/animated_box_4.cc)
ament_target_dependencies(animated_box_4
  rclcpp
  gazebo_dev
  Boost
)
target_link_libraries(animated_box_4 ${GAZEBO_LIBRARIES})

# ==========================================
# 실행 노드 빌드 (옵션)
# ==========================================
add_executable(integrated_main src/animated_box_plugin/integrated_main.cc)
ament_target_dependencies(integrated_main
  rclcpp
  gazebo_msgs
  gazebo_dev
  Boost
  Protobuf
  TBB
)

# ==========================================
# 설치 파일 및 폴더
# ==========================================
install(
  DIRECTORY rviz urdf launch meshes config worlds models
  DESTINATION share/${PROJECT_NAME}
)

install(TARGETS
  animated_box_1
  animated_box_2
  animated_box_3
  animated_box_4
  integrated_main
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY include/
  DESTINATION include/
)

# ==========================================
# 라이브러리 export (다른 패키지가 쓸 경우)
# ==========================================
ament_export_libraries(
  animated_box_1
  animated_box_2
  animated_box_3
  animated_box_4
)

# ==========================================
# 패키지 정의
# ==========================================
ament_package()
