#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"
FONTDIR=../fonts
mkdir -p $FONTDIR
cd $FONTDIR

# zh fonts
wget -O LongCang-Regular.ttf https://github.com/google/fonts/raw/main/ofl/longcang/LongCang-Regular.ttf
wget -O LiuJianMaoCao-Regular.ttf https://github.com/google/fonts/raw/main/ofl/liujianmaocao/LiuJianMaoCao-Regular.ttf
wget -O ZhiMangXing-Regular.ttf https://github.com/google/fonts/raw/main/ofl/zhimangxing/ZhiMangXing-Regular.ttf
wget -O ZCOOLKuaiLe-Regular.ttf https://github.com/google/fonts/raw/main/ofl/zcoolkuaile/ZCOOLKuaiLe-Regular.ttf
wget -O MaShanZheng-Regular.ttf https://github.com/google/fonts/raw/main/ofl/mashanzheng/MaShanZheng-Regular.ttf
wget -O ZCOOLQingKeHuangYou-Regular.ttf https://github.com/google/fonts/raw/main/ofl/zcoolqingkehuangyou/ZCOOLQingKeHuangYou-Regular.ttf
wget -O ZCOOLXiaoWei-Regular.ttf https://github.com/google/fonts/raw/main/ofl/zcoolxiaowei/ZCOOLXiaoWei-Regular.ttf