#!/bin/bash
#
# Pick a mutually installable set of nginx / Phusion Passenger versions.
#
# Phusion publishes several builds of libnginx-mod-http-passenger per Ubuntu
# release. Older builds depend on "nginx-common" with no version, newer ones
# depend on one exact nginx revision, e.g. on noble:
#
#   1:6.1.6-1~noble1       Depends: nginx-common
#   1:6.2.0-1~noble1       Depends: nginx-common (= 1.24.0-2ubuntu7.15)
#   1:6.2.0-1~noble1build1 Depends: nginx-common (= 1.24.0-2ubuntu7.16)
#
# Installing the newest build unconditionally fails with "held broken packages"
# whenever the Ubuntu archive has not published the nginx revision that build
# was compiled against. This script prefers the Passenger version pinned in
# vars/<release>.yml and only falls back to another build when that version is
# not installable, so deploys keep working when either side moves.
#
# Usage: resolve_passenger_versions.sh [pinned_passenger_version] [pinned_nginx_version]
# Output: one JSON object on stdout.

set -uo pipefail

want_passenger="${1:-}"
want_nginx="${2:-}"

nginx_candidate="$(apt-cache policy nginx-common | awk '/Candidate:/ {print $2}')"
if [ -z "$nginx_candidate" ] || [ "$nginx_candidate" = "(none)" ]; then
  echo "no installation candidate for nginx-common; is the apt cache up to date?" >&2
  exit 1
fi

nginx_available="$(apt-cache show nginx-common 2>/dev/null | awk '/^Version: / {print $2}' | sort -u)"

nginx_installable() {
  printf '%s\n' "$nginx_available" | grep -Fxq "$1"
}

# One line per module build: "<module version> <required nginx version|-> <required passenger version|->"
builds="$(apt-cache show libnginx-mod-http-passenger 2>/dev/null | awk '
  /^Version: / { version = $2; next }
  /^Depends: / {
    nginx = "-"
    if (match($0, /nginx-(common|core) \(= [^)]+\)/)) {
      dep = substr($0, RSTART, RLENGTH)
      gsub(/nginx-(common|core) \(= |\)/, "", dep)
      nginx = dep
    }
    passenger = "-"
    if (match($0, /passenger \(= [^)]+\)/)) {
      dep = substr($0, RSTART, RLENGTH)
      gsub(/passenger \(= |\)/, "", dep)
      passenger = dep
    }
    if (version != "") { print version, nginx, passenger }
    version = ""
  }')"

if [ -z "$builds" ]; then
  echo "no libnginx-mod-http-passenger builds found; is the Phusion repository configured?" >&2
  exit 1
fi

# Newest build that is installable now; when a Passenger version is requested,
# only builds belonging to that Passenger release are considered.
select_build() {
  local require_passenger="$1"
  local module nginx passenger
  local sel="" sel_nginx="" sel_passenger=""

  while read -r module nginx passenger; do
    [ -n "$module" ] || continue
    if [ -n "$require_passenger" ] && [ "$passenger" != "$require_passenger" ]; then
      continue
    fi
    # a build pinned to an nginx revision apt cannot install is unusable
    if [ "$nginx" != "-" ] && ! nginx_installable "$nginx"; then
      continue
    fi
    if [ -n "$sel" ] && ! dpkg --compare-versions "$module" gt "$sel"; then
      continue
    fi
    sel="$module"
    sel_nginx="$nginx"
    sel_passenger="$passenger"
  done <<< "$builds"

  [ -n "$sel" ] || return 1
  printf '%s\t%s\t%s\n' "$sel" "$sel_nginx" "$sel_passenger"
}

pinned="true"
result=""
if [ -n "$want_passenger" ]; then
  result="$(select_build "$want_passenger")" || result=""
fi
if [ -z "$result" ]; then
  pinned="false"
  result="$(select_build "")" || {
    echo "no libnginx-mod-http-passenger build is compatible with the available nginx ($nginx_candidate)" >&2
    exit 1
  }
fi

IFS=$'\t' read -r module nginx_required passenger <<< "$result"

# Pin nginx when the chosen module demands an exact revision, or when the
# revision recorded for this release is still installable. Otherwise install
# whatever the archive currently offers.
nginx_pin=""
if [ "$nginx_required" != "-" ]; then
  nginx_pin="$nginx_required"
elif [ -n "$want_nginx" ] && nginx_installable "$want_nginx"; then
  nginx_pin="$want_nginx"
fi

[ "$passenger" != "-" ] || passenger=""

printf '{"module":"%s","passenger":"%s","nginx":"%s","nginx_candidate":"%s","pinned":%s}\n' \
  "$module" "$passenger" "$nginx_pin" "$nginx_candidate" "$pinned"
