#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"
FONTDIR=../fonts
mkdir -p $FONTDIR
cd $FONTDIR

# found via https://www.freechinesefont.com/

# misc senty http://sentyfont.com/download.htm
wget -O HanyiSentyMarshmallow.ttf http://sentyfont.com/index_htm_files/HanyiSentyMarshmallow.ttf
wget -O HanyiSentySuciTablet.ttf http://sentyfont.com/index_htm_files/HanyiSentySuciTablet.ttf
wget -O HanyiSentyScholar.ttf http://sentyfont.com/index_htm_files/HanyiSentyScholar.ttf
wget -O HanyiSentyBubbleTea.ttf http://sentyfont.com/index_htm_files/HanyiSentyBubbleTea.ttf
wget -O HanyiSentyFoundation.ttf http://sentyfont.com/index_htm_files/HanyiSentyFoundation.ttf
wget -O HanyiSentyPailouArch.ttf http://sentyfont.com/index_htm_files/HanyiSentyPailouArch.ttf
wget -O OzCaramel.ttf http://sentyfont.com/index_htm_files/OzCaramel.ttf
wget -O HanyiSentyJoy.ttf http://sentyfont.com/index_htm_files/HanyiSentyJoy.ttf
wget -O HanyiSentyCrayon-non-color.ttf http://sentyfont.com/index_htm_files/HanyiSentyCrayon-non-color.ttf
wget -O HanyiSentyPine.ttf http://sentyfont.com/index_htm_files/HanyiSentyPine.ttf
wget -O HanyiSentyCHALK_2018.ttf http://sentyfont.com/index_htm_files/HanyiSentyChalk%202018.ttf
wget -O SentyTea.ttf http://sentyfont.com/index_htm_files/SentyTEA-20190904.ttf
wget -O SentyMaruko.ttf http://sentyfont.com/index_htm_files/SentyMARUKO.ttf
wget -O SentyCreamPuff.ttf http://sentyfont.com/index_htm_files/SentyCreamPuff.ttf
wget -O SentyWen2017.ttf http://sentyfont.com/index_htm_files/HanyiSentyWEN.ttf
wget -O Hanyi_Senty_Lingfei_Scroll.ttf http://sentyfont.com/index_htm_files/Hanyi%20Senty%20Lingfei%20Scroll.ttf
wget -O HanyiSentyTang.ttf http://sentyfont.com/index_htm_files/HanyiSentyTang.ttf
wget -O HanyiSentyJournal.ttf http://sentyfont.com/index_htm_files/HanyiSentyJournal.ttf
wget -O HanyiSentySIlkRoad.ttf http://sentyfont.com/index_htm_files/HanyiSentySIlkRoad.ttf
wget -O HanyiSentyGarden.ttf http://sentyfont.com/index_htm_files/HanyiSentyGarden.ttf

# benmo http://www.benmo.biz/index.html
wget -O BenmoJunsong.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E9%92%A7%E5%AE%8B.ttf
wget -O BenmoLiuyuan.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E5%AD%97%E9%80%A0%E7%90%89%E5%9C%86.ttf
wget -O BenmoSanyue.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E5%AD%97%E9%80%A0%E4%B8%89%E6%9C%88.ttf
wget -O BenmoBeijia.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E5%AD%97%E9%80%A0%E8%B4%9D%E5%98%89.ttf
wget -O BenmoBeiyuan.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E5%AD%97%E9%80%A0%E8%B4%9D%E5%9C%86.ttf
wget -O BenmoRuiyi.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E5%AD%97%E9%80%A0%E9%94%90%E9%80%B8.ttf
wget -O BenmoZhuhei.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E9%93%B8%E9%BB%91.ttf
wget -O BenmoJinsong.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E4%BB%8A%E5%AE%8B.ttf
wget -O BenmoYouyuan.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E6%82%A0%E5%9C%86.ttf
wget -O BenmoJinhei.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E6%B4%A5%E9%BB%91.ttf
wget -O BenmoZiyu.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E5%AD%97%E8%AF%AD.ttf
wget -O BenmoYonghei.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E5%92%8F%E9%BB%91.ttf
wget -O BenmoChenhei.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E9%99%88%E9%BB%91.ttf
wget -O BenmoJingyuan.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E7%AB%9E%E5%9C%86-%E5%B8%B8%E8%A7%84.ttf
wget -O BenmoJinhei.ttf http://www.benmo.biz/fonts/%E6%9C%AC%E5%A2%A8%E6%B4%A5%E9%BB%91.ttf

# adobe and google
# wget -O DroidSansFallback.ttf https://github.com/aosp-mirror/platform_frameworks_base/raw/master/data/fonts/DroidSansFallback.ttf

wget -O SourceHanSerifSC-Medium.otf https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SimplifiedChinese/SourceHanSerifSC-Medium.otf
wget -O SourceHanSerifSC-Regular.otf https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf
wget -O SourceHanSerifSC-Heavy.otf https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SimplifiedChinese/SourceHanSerifSC-Heavy.otf
wget -O SourceHanSerifSC-ExtraLight.otf https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SimplifiedChinese/SourceHanSerifSC-ExtraLight.otf

wget -O SourceHanMonoSC-Normal.otf https://github.com/adobe-fonts/source-han-mono/raw/master/Normal/OTC/SourceHanMonoSC-Normal.otf
wget -O SourceHanMonoSC-Medium.otf https://github.com/adobe-fonts/source-han-mono/raw/master/Medium/OTC/SourceHanMonoSC-Medium.otf
wget -O SourceHanMonoSC-Regular.otf https://github.com/adobe-fonts/source-han-mono/raw/master/Regular/OTC/SourceHanMonoSC-Regular.otf
wget -O SourceHanMonoSC-Heavy.otf https://github.com/adobe-fonts/source-han-mono/raw/master/Heavy/OTC/SourceHanMonoSC-Heavy.otf
wget -O SourceHanMonoSC-ExtraLight.otf https://github.com/adobe-fonts/source-han-mono/raw/master/ExtraLight/OTC/SourceHanMonoSC-ExtraLight.otf
wget -O SourceHanMonoSC-Bold.otf https://github.com/adobe-fonts/source-han-mono/raw/master/Bold/OTC/SourceHanMonoSC-Bold.otf
wget -O SourceHanMonoSC-Light.otf https://github.com/adobe-fonts/source-han-mono/raw/master/Light/OTC/SourceHanMonoSC-Light.otf

# yegenyou
wget -O yegenyouTangKaiJian.ttf http://yegenyou.com/upload/font/35.ttf
wget -O yegenyouWeiYingTi.ttf http://yegenyou.com/upload/font/36.ttf
