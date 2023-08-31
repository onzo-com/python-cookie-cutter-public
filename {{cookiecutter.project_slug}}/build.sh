#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

cd "$(dirname "$0")"

# This version relates to the build version of https://github.com/onzo-com/atlas-build-lib-script. It currently needs to
# be updated manually, when changes are made to the above repository that are required in this project.
scriptversion="2.0.29"

ensure-present() {
  if [ -f "${1}" ]; then
    grep -c "script version  ${scriptversion}" "${1}" > /dev/null 2>&1 && echo "${1} already exists therefore not downloading from Artifactory" && return 0
  fi

  echo "Downloading ${1}"
  curl --connect-timeout 5 -s "https://artifactory.dev.onzo.cloud/artifactory/int-files/atlas-build-lib-script/${scriptversion}-${1}" -o "${1}"
  chmod u+x "${1}"
}

ensure-present Rakefile
ensure-present operatingsystem.rb
ensure-present utilities.rb
ensure-present localbuild.sh
ensure-present integration_testing.rb
ensure-present fix_pytest_xml.py
ensure-present pylint-report.sh
ensure-present flake8-report.sh

#if no cmd line params
if [ -z "$1" ]; then
  rake default
  exit $?
fi

rake $1
exit $?
