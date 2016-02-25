# To improve
# * dependency items are declared at different places
#   - This file two places 
#     - CPACK_DEBIAN_PACKAGE_DEPENDS: all deb pkgs needed during install
#     - DOCKER_PKGING_DEPS_DEB: all deb pkgs needed in building
#   - File rpm.spec.in
# * rpm and deb releases are treated differently:
#   - rpm: source rpm
#   - deb: binary deb
# * upload-<> should also upload to github release site

cmake_minimum_required (VERSION 2.6)
project (mcvine-resources)

set(PROJECT_NAME "mcvine-resources")
set(VERSION "0.1")
set(AUTHOR "Jiao Lin")
set(AUTHOR_EMAILE "jiao.lin@gmail.com")
set(VENDOR "DANSE")
set(SUMMARY "MCViNE data files")
set(LICENSE "BSD")
set(RPM_APP_GROUP "Development/Tools")
set(GITHUB_URL "https://github.com/mcvine/resources")

# package repository at packagecloud
set (PKGCLOUD_USERNAME "danse")
set (PKGCLOUD_REPO "ins")
# debian
set(DOCKER_PKGING_DEB_DIST_NAME "ubuntu")
set(DOCKER_PKGING_DEB_DIST_VERSION "14.04")
# dependencies
set (DOCKER_PKGING_DEPS_DEB "danse.ins")
set (DOCKER_PKGING_DEPS_RPM "danse.ins")
set (DOCKER_PKGING_TEST_SRPM "ls /opt/danse/share/mcvine/resources")
set (DOCKER_PKGING_TEST_RPM ${DOCKER_PKGING_TEST_SRPM})
set (DOCKER_PKGING_TEST_DEB ${DOCKER_PKGING_TEST_SRPM})

# variables
set (PKG_NAME "${PROJECT_NAME}")

# subdirs
install(
  DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/instruments
  DESTINATION share/mcvine/resources
  USE_SOURCE_PERMISSIONS
  )
install(
  DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/samples
  DESTINATION share/mcvine/resources
  USE_SOURCE_PERMISSIONS
  )

# packaging
# CPACK
set(CPACK_PACKAGE_VERSION ${VERSION})
# set(CPACK_GENERATOR  "RPM")
set(CPACK_GENERATOR  "DEB")
set(CPACK_PACKAGE_NAME ${PKG_NAME})
set(CPACK_PACKAGE_SUMMARY ${SUMMARY})
set(CPACK_PACKAGE_LICENSE ${LICENSE})
set(CPACK_PACKAGE_RELEASE 0)
set(CPACK_PACKAGE_APP_GROUP ${RPM_APP_GROUP})
set(CPACK_PACKAGE_CONTACT ${AUTHOR})
set(CPACK_PACKAGE_VENDOR ${VENDOR})
set(CPACK_PACKAGING_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX})
set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-${CPACK_PACKAGE_RELEASE}.${CMAKE_SYSTEM_PROCESSOR}")
set(CPACK_RPM_PACKAGE_REQUIRES "cmake")
set(CPACK_DEBIAN_PACKAGE_DEPENDS "")
include(CPack)

# source tar ball
add_custom_command(
  OUTPUT ${PKG_NAME}-${CPACK_PACKAGE_VERSION}.tar.gz
  COMMAND git archive --format=tar --prefix=${PKG_NAME}-${CPACK_PACKAGE_VERSION}/ HEAD | gzip -c > ${CMAKE_CURRENT_BINARY_DIR}/${PKG_NAME}-${CPACK_PACKAGE_VERSION}.tar.gz
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  )
add_custom_target( 
  src_tgz
  DEPENDS ${PKG_NAME}-${CPACK_PACKAGE_VERSION}.tar.gz 
  )

# CPack does not have a rule for source rpm
# the following is a way to do that
#
set(RPM_BUILD_DIR rpm_build)
# rpm spec file
configure_file( ${CMAKE_CURRENT_SOURCE_DIR}/rpm.spec.in
  ${CMAKE_CURRENT_BINARY_DIR}/${RPM_BUILD_DIR}/SPECS/${PKG_NAME}.spec )
# rules to build src rpm
set(SRC_RPM ${PKG_NAME}-${CPACK_PACKAGE_VERSION}-${CPACK_PACKAGE_RELEASE}.src.rpm)
add_custom_command(
  OUTPUT ${SRC_RPM}
  COMMAND ${CMAKE_COMMAND} -E make_directory ${RPM_BUILD_DIR}
  COMMAND ${CMAKE_COMMAND} -E make_directory ${RPM_BUILD_DIR}/BUILD
  COMMAND ${CMAKE_COMMAND} -E make_directory ${RPM_BUILD_DIR}/BUILDROOT
  COMMAND ${CMAKE_COMMAND} -E make_directory ${RPM_BUILD_DIR}/RPMS
  COMMAND ${CMAKE_COMMAND} -E make_directory ${RPM_BUILD_DIR}/SOURCES
  COMMAND ${CMAKE_COMMAND} -E make_directory ${RPM_BUILD_DIR}/SPECS
  COMMAND ${CMAKE_COMMAND} -E make_directory ${RPM_BUILD_DIR}/SRPMS
  COMMAND ${CMAKE_COMMAND} -E make_directory ${RPM_BUILD_DIR}/tmp
  COMMAND ${CMAKE_COMMAND} -E copy ${PKG_NAME}-${CPACK_PACKAGE_VERSION}.tar.gz ${RPM_BUILD_DIR}/SOURCES
  COMMAND rpmbuild -bs --define=\"_topdir ${RPM_BUILD_DIR}\" --buildroot=${RPM_BUILD_DIR}/tmp  ${RPM_BUILD_DIR}/SPECS/${PKG_NAME}.spec
  COMMAND ${CMAKE_COMMAND} -E copy ${RPM_BUILD_DIR}/SRPMS/${SRC_RPM} ${SRC_RPM}
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
  DEPENDS src_tgz
  )
add_custom_target( 
  srpm
  DEPENDS ${SRC_RPM}
  )

# docker folder for build and test packaging artifacts
execute_process(
  COMMAND rm -rf docker
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  )
execute_process(
  COMMAND git clone https://github.com/danse-inelastic/packaging-use-docker docker
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  )
add_subdirectory(docker)
