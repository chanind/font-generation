#!/usr/bin/env bash

# MS fonts downloader
# based on https://salsa.debian.org/debian/msttcorefonts/-/blob/master/update-ms-fonts

cd "$(dirname "${BASH_SOURCE[0]}")"
FONTDIR=../fonts
mkdir -p $FONTDIR
cd $FONTDIR

URLROOTS="https://downloads.sourceforge.net/corefonts/
	https://jaist.dl.sourceforge.net/sourceforge/corefonts/
	https://nchc.dl.sourceforge.net/sourceforge/corefonts/
	https://ufpr.dl.sourceforge.net/sourceforge/corefonts/
	https://internode.dl.sourceforge.net/sourceforge/corefonts/
	https://netcologne.dl.sourceforge.net/sourceforge/corefonts/
	https://vorboss.dl.sourceforge.net/sourceforge/corefonts/
	https://netix.dl.sourceforge.net/sourceforge/corefonts/"


cat <<EOF > msfonts.info
48d9bc613917709d3b0e0f4a6d4fe33a5c544c5035dffe9e90bc11e50e822071	Andale_Mono.ttf		andale32.exe	andalemo.ttf
dad7c04acb26e23dfe4780e79375ca193ddaf68409317e81577a30674668830e	Arial_Black.ttf		arialb32.exe	ariblk.ttf
35c0f3559d8db569e36c31095b8a60d441643d95f59139de40e23fada819b833	Arial.ttf		arial32.exe	arial.ttf
4044aa6b5bebbc36980206b45b0aaaaa5681552a48bcadb41746d5d1d71fd7b4	Arial_Bold.ttf		arial32.exe	arialbd.ttf
2f371cd9d96b3ac544519d85c16dc43ceacdfcea35090ee8ddf3ec5857c50328	Arial_Bold_Italic.ttf	arial32.exe	arialbi.ttf
70ade233175a6a6675e4501461af9326e6f78b1ffdf787ca0da5ab0fc8c9cfd6	Arial_Italic.ttf	arial32.exe	ariali.ttf
b82c53776058f291382ff7e008d4675839d2dc21eb295c66391f6fb0655d8fc0	Comic_Sans_MS.ttf	comic32.exe	comic.ttf
873361465d994994762d0b9845c99fc7baa2a600442ea8db713a7dd19f8b0172	Comic_Sans_MS_Bold.ttf	comic32.exe	comicbd.ttf
6715838c52f813f3821549d3f645db9a768bd6f3a43d8f85a89cb6875a546c61	Courier_New.ttf		courie32.exe	cour.ttf
edf8a7c5bfcac2e1fe507faab417137cbddc9071637ef4648238d0768c921e02	Courier_New_Bold.ttf	courie32.exe	courbd.ttf
f3f6b09855b6700977e214aab5eb9e5be6813976a24f894bd7766e92c732fbe1	Courier_New_Italic.ttf	courie32.exe	couri.ttf
66dbfa20b534fba0e203da140fec7276a45a1069e424b1b9c35547538128bbe8	Courier_New_Bold_Italic.ttf	courie32.exe	courbi.ttf
7d0bb20c632bb59e81a0885f573bd2173f71f73204de9058feb68ce032227072	Georgia.ttf		georgi32.exe	georgia.ttf
82d2fbadb88a8632d7f2e8ad50420c9fd2e7d3cbc0e90b04890213a711b34b93	Georgia_Bold.ttf	georgi32.exe	georgiab.ttf
1523f19bda6acca42c47c50da719a12dd34f85cc2606e6a5af15a7728b377b60	Georgia_Italic.ttf	georgi32.exe	georgiai.ttf
c983e037d8e4e694dd0fb0ba2e625bca317d67a41da2dc81e46a374e53d0ec8a	Georgia_Bold_Italic.ttf	georgi32.exe	georgiaz.ttf
00f1fc230ac99f9b97ba1a7c214eb5b909a78660cb3826fca7d64c3af5a14848	Impact.ttf		impact32.exe	impact.ttf
4e98adeff8ccc8ef4e3ece8d4547e288ff85fdc9c7ca711a4599c234874bbe86	Times_New_Roman.ttf	times32.exe	times.ttf
4357b63cef20c01661a53c5dae70ffd20cb4765503aaed6d38b17a57c5a90bff	Times_New_Roman_Bold.ttf	times32.exe	timesbd.ttf
192e1b0d18e90334e999a99f8c32808d6a2e74b3698b8cd90c943c2249a46549	Times_New_Roman_Bold_Italic.ttf	times32.exe	timesbi.ttf
c25ae529b4cecdbca148b6ccb862ee0abad770af8b1fd29c8dba619d1b8da78a	Times_New_Roman_Italic.ttf	times32.exe	timesi.ttf
ec3ffb302488251e1b67fb09dd578b364c5339e27c1cfb26eb627666236453d0	Trebuchet_MS.ttf	trebuc32.exe	trebuc.ttf
f65941f9487c0a0a3b7445996ecbbd24466d7ae76ea2a597ced55f438fa63838	Trebuchet_MS_Bold.ttf	trebuc32.exe	trebucbd.ttf
db56fdac7d3ba20b7aededcb6ee86c46687489d17b759e1708ea4e2d21e38410	Trebuchet_MS_Italic.ttf	trebuc32.exe	trebucit.ttf
c0a6bdf31f9f2953b2f08a0c1734c892bc825f0fb17c604d420f7acf203a213b	Trebuchet_MS_Bold_Italic.ttf	trebuc32.exe	trebucbi.ttf
96ed14949ca4b7392cff235b9c41d55c125382abbe0c0d3c2b9dd66897cae0cb	Verdana.ttf		verdan32.exe	verdana.ttf
c8f5065ba91680f596af3b0378e2c3e713b95a523be3d56ae185ca2b8f5f0b23	Verdana_Bold.ttf	verdan32.exe	verdanab.ttf
91b59186656f52972531a11433c866fd56e62ec4e61e2621a2dba70c8f19a828	Verdana_Italic.ttf	verdan32.exe	verdanai.ttf
698e220f48f4a40e77af7eb34958c8fd02f1e18c3ba3f365d93bfa2ed4474c80	Verdana_Bold_Italic.ttf	verdan32.exe	verdanaz.ttf
10d099c88521b1b9e380b7690cbe47b54bb19396ca515358cfdc15ac249e2f5d	Webdings.ttf		webdin32.exe	webdings.ttf
EOF

for ttf in `awk '{print $2}' msfonts.info` ; do
    if [ ! -e $FONTDIR/$ttf ] || \
        [ `sha256sum $FONTDIR/$ttf | awk '{print $1}'` != `awk "/$ttf/ {print \\$1 }" msfonts.info` ]
        then
        THISFILE=`grep $ttf msfonts.info | awk '{print $3}'`
        if ! echo $FONTFILES | grep -q $THISFILE ; then
            FONTFILES="$FONTFILES $THISFILE"
        fi
    fi
done


FFDONE=""
FFFAILED=""
if [ -n "$FONTFILES" ] ; then 
    for ff in $FONTFILES; do
        for URLROOT in $URLROOTS ; do
						if ! wget --continue --tries=1 --connect-timeout=60 --read-timeout=300 $QUIET_ARG --directory-prefix . --no-directories --no-background --progress=dot:default $URLROOT$ff ; then
								continue 1
						fi
						break
        done
        if [ -e "$ff" ]; then
            FFDONE="$FFDONE $ff"
        else 
            FFFAILED="$FFFAILED $ff"
            EXITCODE=1
        fi   
    done

    for ff in $FONTFILES; do
        cabextract $ff 1>&2
        rm $ff
    done
fi

rm *.exe
rm msfonts.info
rm *.DLL
rm Webdings.TTF