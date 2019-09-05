# Install script for directory: /home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-build")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/samples" TYPE FILE FILES
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/MQTTClient_subscribe.c"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/MQTTAsync_subscribe.c"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/paho_c_sub.c"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/MQTTClient_publish_async.c"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/paho_cs_pub.c"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/paho_c_pub.c"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/pubsub_opts.c"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/MQTTAsync_publish.c"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/paho_cs_sub.c"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/src/samples/MQTTClient_publish.c"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/." TYPE FILE FILES
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/CONTRIBUTING.md"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/epl-v10"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/edl-v10"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/README.md"
    "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/paho-src/notice.html"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/pahomqtt-prefix/src/pahomqtt-build/src/cmake_install.cmake")
  include("/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/pahomqtt-prefix/src/pahomqtt-build/test/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/u26213/Reference-samples/iot-devcloud/cpp/restricted_zone_notifier/build/pahomqtt-prefix/src/pahomqtt-build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
