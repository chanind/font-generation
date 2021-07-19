#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"
FONTDIR=../fonts
mkdir -p $FONTDIR
cd $FONTDIR

# arphic
wget -O ukai.ttc https://salsa.debian.org/fonts-team/fonts-arphic-ukai/-/raw/master/ukai.ttc
wget -O gbsn00lp.ttf https://salsa.debian.org/fonts-team/fonts-arphic-gbsn00lp/-/raw/master/gbsn00lp.ttf 
wget -O bsmi00lp.ttf https://salsa.debian.org/fonts-team/fonts-arphic-bsmi00lp/-/raw/master/bsmi00lp.ttf
wget -O bkai00mp.ttf https://salsa.debian.org/fonts-team/fonts-arphic-bkai00mp/-/raw/master/bkai00mp.ttf
wget -O gkai00mp.ttf https://salsa.debian.org/fonts-team/fonts-arphic-gkai00mp/-/raw/master/gkai00mp.ttf
# wget -O uming.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/uming.ttf

# babelstone
wget -O BabelStoneHan.ttf https://salsa.debian.org/fonts-team/fonts-babelstone-han/-/raw/master/BabelStoneHan.ttf
wget -O BabelStoneModern.ttf https://salsa.debian.org/fonts-team/fonts-babelstone-modern/-/raw/debian/sid/BabelStoneModern.ttf
# cmu
wget -O cmunbbx.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbbx.ttf
wget -O cmunbi.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbi.ttf
wget -O cmunbl.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbl.ttf
wget -O cmunbmo.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbmo.ttf
wget -O cmunbmr.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbmr.ttf
wget -O cmunbso.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbso.ttf
wget -O cmunbsr.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbsr.ttf
wget -O cmunbtl.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbtl.ttf
wget -O cmunbto.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbto.ttf
wget -O cmunbx.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbx.ttf
wget -O cmunbxo.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunbxo.ttf
wget -O cmunci.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunci.ttf
wget -O cmunit.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunit.ttf
wget -O cmunobi.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunobi.ttf
wget -O cmunobx.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunobx.ttf
wget -O cmunorm.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunorm.ttf
wget -O cmunoti.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunoti.ttf
wget -O cmunrb.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunrb.ttf
wget -O cmunrm.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunrm.ttf
wget -O cmunsi.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunsi.ttf
wget -O cmunsl.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunsl.ttf
wget -O cmunso.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunso.ttf
wget -O cmunss.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunss.ttf
wget -O cmunssdc.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunssdc.ttf
wget -O cmunst.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunst.ttf
wget -O cmunsx.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunsx.ttf
wget -O cmuntb.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmuntb.ttf
wget -O cmunti.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunti.ttf
wget -O cmuntt.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmuntt.ttf
wget -O cmuntx.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmuntx.ttf
wget -O cmunui.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunui.ttf
wget -O cmunvi.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunvi.ttf
wget -O cmunvt.ttf https://salsa.debian.org/fonts-team/fonts-cmu/-/raw/master/cmunvt.ttf

# fonts-cns
wget -O TW-Kai-98_1.ttf https://salsa.debian.org/fonts-team/fonts-cns11643/-/raw/master/TW-Kai-98_1.ttf

# comfortaa
wget -O Comfortaa-Bold.ttf https://salsa.debian.org/fonts-team/fonts-comfortaa/-/raw/master/Comfortaa-Bold.ttf
wget -O Comfortaa-Light.ttf https://salsa.debian.org/fonts-team/fonts-comfortaa/-/raw/master/Comfortaa-Light.ttf
wget -O Comfortaa-Regular.ttf https://salsa.debian.org/fonts-team/fonts-comfortaa/-/raw/master/Comfortaa-Regular.ttf

# comicneue
wget -O ComicNeue-Regular.ttf https://github.com/crozynski/comicneue/raw/master/Fonts/TTF/ComicNeue/ComicNeue-Regular.ttf
wget -O ComicNeue-Italic.ttf https://github.com/crozynski/comicneue/raw/master/Fonts/TTF/ComicNeue/ComicNeue-Italic.ttf
wget -O ComicNeue-Light.ttf https://github.com/crozynski/comicneue/raw/master/Fonts/TTF/ComicNeue/ComicNeue-Light.ttf
wget -O ComicNeue-Bold.ttf https://github.com/crozynski/comicneue/raw/master/Fonts/TTF/ComicNeue/ComicNeue-Bold.ttf