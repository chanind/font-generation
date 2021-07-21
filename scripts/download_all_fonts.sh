#!/usr/bin/env bash
set -e

cd "$(dirname "${BASH_SOURCE[0]}")"

./download_deb_fonts.sh
./download_google_fonts.sh
./download_ms_fonts.sh
./download_noto_fonts.sh
./download_misc_zh_fonts.sh