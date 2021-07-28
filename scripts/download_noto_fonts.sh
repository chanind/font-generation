#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"
FONTDIR=../fonts
mkdir -p $FONTDIR
cd $FONTDIR

wget -O NotoSansMonoCJKsc-Regular.otf https://github.com/googlefonts/noto-cjk/raw/main/Sans/Mono/NotoSansMonoCJKsc-Regular.otf
wget -O NotoSansMonoCJKsc-Bold.otf https://github.com/googlefonts/noto-cjk/raw/main/Sans/Mono/NotoSansMonoCJKsc-Bold.otf

# these don't seem to work :/
# wget -O NotoSansCJKsc-Black.otf https://github.com/googlefonts/noto-cjk/blob/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Black.otf
# wget -O NotoSansCJKsc-Bold.otf https://github.com/googlefonts/noto-cjk/blob/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf
# wget -O NotoSansCJKsc-Light.otf https://github.com/googlefonts/noto-cjk/blob/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Light.otf
# wget -O NotoSansCJKsc-Regular.otf https://github.com/googlefonts/noto-cjk/blob/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf

wget -O NotoSansCJK-Black.ttc https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK-Black.ttc
wget -O NotoSansCJK-Bold.ttc https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK-Bold.ttc
wget -O NotoSansCJK-DemiLight.ttc https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK-DemiLight.ttc
wget -O NotoSansCJK-Light.ttc https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK-Light.ttc
wget -O NotoSansCJK-Medium.ttc https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK-Medium.ttc
wget -O NotoSansCJK-Regular.ttc https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK-Regular.ttc
wget -O NotoSansCJK-Thin.ttc https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK-Thin.ttc

wget -O NotoSerifCJKsc-Black.otf https://github.com/googlefonts/noto-cjk/raw/main/Serif/NotoSerifCJKsc-Black.otf
wget -O NotoSerifCJKsc-Bold.otf https://github.com/googlefonts/noto-cjk/raw/main/Serif/NotoSerifCJKsc-Bold.otf
wget -O NotoSerifCJKsc-Light.otf https://github.com/googlefonts/noto-cjk/raw/main/Serif/NotoSerifCJKsc-Light.otf
wget -O NotoSerifCJKsc-ExtraLight.otf https://github.com/googlefonts/noto-cjk/raw/main/Serif/NotoSerifCJKsc-ExtraLight.otf
wget -O NotoSerifCJKsc-Medium.otf https://github.com/googlefonts/noto-cjk/raw/main/Serif/NotoSerifCJKsc-Medium.otf
wget -O NotoSerifCJKsc-Regular.otf https://github.com/googlefonts/noto-cjk/raw/main/Serif/NotoSerifCJKsc-Regular.otf
wget -O NotoSerifCJKsc-SemiBold.otf https://github.com/googlefonts/noto-cjk/raw/main/Serif/NotoSerifCJKsc-SemiBold.otf
