# inspired by https://github.com/hologerry/Attr2Font/blob/master/model.py

import torch
import torch.nn as nn
import torch.nn.functional as F


def tile_like(x, img):
    x = x.view(x.size(0), x.size(1), 1, 1)
    x = x.repeat(1, 1, img.size(2), img.size(3))
    return x


def get_model_parameters(model):
    total_parameters = 0
    for layer in list(model.parameters()):
        layer_parameter = 1
        for dim in list(layer.size()):
            layer_parameter *= dim
        total_parameters += layer_parameter
    return total_parameters


class ResidualBlock(nn.Module):
    def __init__(self, in_channel, kernel_size=3):
        super().__init__()

        conv_block = [
            nn.Conv2d(
                in_channel,
                in_channel,
                kernel_size,
                stride=1,
                padding=(kernel_size - 1) // 2,
                bias=False,
            ),
            nn.InstanceNorm2d(in_channel),
            nn.ReLU(inplace=True),
            nn.Conv2d(
                in_channel,
                in_channel,
                kernel_size,
                stride=1,
                padding=(kernel_size - 1) // 2,
                bias=False,
            ),
            nn.InstanceNorm2d(in_channel),
            nn.ReLU(inplace=True),
        ]

        self.conv_block = nn.Sequential(*conv_block)

    def forward(self, x):
        return x + self.conv_block(x)


class Down(nn.Module):
    def __init__(
        self,
        in_channel,
        out_channel,
        normalize=True,
        attention=False,
        lrelu=False,
        dropout=0.0,
        bias=False,
        kernel_size=4,
        stride=2,
        padding=1,
    ):
        super().__init__()
        layers = [
            nn.Conv2d(
                in_channel,
                out_channel,
                kernel_size=kernel_size,
                stride=stride,
                padding=padding,
                bias=bias,
            )
        ]
        if attention:
            layers.append(SelfAttention(out_channel))
        if normalize:
            layers.append(nn.InstanceNorm2d(out_channel))
        if lrelu:
            layers.append(nn.LeakyReLU(0.2, inplace=True))
        else:
            layers.append(nn.ReLU(inplace=True))
        if dropout:
            layers.append(nn.Dropout(dropout))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)


class Up(nn.Module):
    def __init__(
        self,
        in_channel,
        out_channel,
        dropout=0.0,
        bias=False,
        attention=True,
    ):
        super().__init__()
        img_layers = [nn.ConvTranspose2d(in_channel, out_channel, 4, 2, 1, bias=bias)]
        if attention:
            img_layers.append(SelfAttention(out_channel))
        img_layers.append(nn.InstanceNorm2d(out_channel))
        img_layers.append(nn.ReLU(inplace=True))
        if dropout:
            img_layers.append(nn.Dropout(dropout))
        img_layers += [
            nn.Conv2d(
                out_channel,
                out_channel,
                3,
                stride=1,
                padding=1,
                bias=False,
            ),
            nn.InstanceNorm2d(out_channel),
            nn.ReLU(inplace=True),
            SelfAttention(out_channel),
            nn.ReLU(inplace=True),
        ]
        self.img_layer = nn.Sequential(*img_layers)

    def forward(self, x, skip_input):
        # assert len(attr_feature.size()) == 3
        x = self.img_layer(x)
        out = torch.cat([x, skip_input], 1)
        return out


# Self Attention module from self-attention gan
class SelfAttention(nn.Module):
    """Self attention Layer"""

    def __init__(self, in_dim, activation=None):
        super().__init__()
        self.chanel_in = in_dim
        self.activation = activation

        self.query_conv = nn.Conv2d(
            in_channels=in_dim, out_channels=in_dim // 8, kernel_size=1
        )
        self.key_conv = nn.Conv2d(
            in_channels=in_dim, out_channels=in_dim // 8, kernel_size=1
        )
        self.value_conv = nn.Conv2d(
            in_channels=in_dim, out_channels=in_dim, kernel_size=1
        )
        self.gamma = nn.Parameter(torch.zeros(1))

        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        """
        inputs :
            x : input feature maps( B X C X W X H)
        returns :
            out : self attention value + input feature
            attention: B X N X N (N is Width*Height)
        """
        m_batchsize, C, width, height = x.size()
        proj_query = (
            self.query_conv(x).view(m_batchsize, -1, width * height).permute(0, 2, 1)
        )  # B X C X (N)
        proj_key = self.key_conv(x).view(
            m_batchsize, -1, width * height
        )  # B X C X (W*H)
        energy = torch.bmm(proj_query, proj_key)  # transpose check
        attention = self.softmax(energy)  # B X (N) X (N)
        proj_value = self.value_conv(x).view(
            m_batchsize, -1, width * height
        )  # B X C X N

        out = torch.bmm(proj_value, attention.permute(0, 2, 1))
        out = out.view(m_batchsize, C, width, height)

        out = self.gamma * out + x
        return out


class ImageEncoder(nn.Module):
    def __init__(self, in_channel=1, n_images=4, style_out_channel=256, n_res_blocks=8):
        super().__init__()
        layers = []
        # Initial Conv
        layers += [
            nn.Conv2d(in_channel * n_images, 64, 7, stride=1, padding=3, bias=False),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True),
        ]

        # Down scale
        layers += [Down(64, 128)]
        layers += [Down(128, 256)]
        layers += [Down(256, 512)]
        layers += [Down(512, 512, dropout=0.5)]
        layers += [Down(512, 512, dropout=0.5)]
        layers += [Down(512, style_out_channel, normalize=False, dropout=0.5)]
        self.down = nn.Sequential(*layers)

        # Style transform
        # res_blks = []
        # res_channel = style_out_channel
        # for _ in range(n_res_blocks):
        #     # 64x64 images turn into 1px here, so it seems dumb to use a 3x3 kernel on 1 px. Also pytorch errors
        #     # This all just seems pretty silly tbh...
        #     res_blks.append(ResidualBlock(res_channel))
        # self.res_layer = nn.Sequential(*res_blks)

    def forward(self, style):
        return self.down(style)
        # return self.res_layer(x)
        # source_style = source_style.view(source_style.size(0), source_style.size(1), 1)
        # attr_intensity = attr_intensity.view(attr_intensity.size(0),  attr_intensity.size(1), 1)
        # feature = torch.cat([source_style, attr_intensity], 1)
        # feature = feature.view(feature.size(0), feature.size(1), 1, 1)
        # target_style = self.res_layer(feature)
        # return feature


class Generator(nn.Module):
    def __init__(
        self,
        in_channel=1,
        n_style=4,
        n_content=4,
        style_out_channel=256,
        out_channel=1,
        n_res_blocks=8,
        attention=True,
    ):
        """Generator with style transform"""
        super().__init__()

        self.style_enc = ImageEncoder(
            in_channel=in_channel,
            n_images=n_style,
            style_out_channel=style_out_channel,
            n_res_blocks=n_res_blocks,
        )

        # Initial Conv
        self.conv = nn.Sequential(
            nn.Conv2d(n_content * in_channel, 64, 7, stride=1, padding=3, bias=False),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True),
        )

        self.down1 = Down(64, 64)
        self.down2 = Down(64, 128)
        self.down3 = Down(128, 256)
        self.down4 = Down(256, 512, dropout=0.5)
        self.down5 = Down(512, 512, dropout=0.5)
        self.down6 = Down(512, 512, normalize=False, dropout=0.5)

        self.up1 = Up(512 + style_out_channel, 512, dropout=0.5)
        self.up2 = Up(1024, 512, dropout=0.5, attention=attention)
        self.up3 = Up(1024, 256, attention=attention)
        self.up4 = Up(512, 128, attention=attention)
        self.up5 = Up(256, 64)

        self.skip_conv1 = nn.Sequential(
            nn.Conv2d(512 + style_out_channel, 512, 3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(512),
            nn.ReLU(inplace=True),
        )
        self.skip_conv2 = nn.Sequential(
            nn.Conv2d(512 + style_out_channel, 512, 3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(512),
            nn.ReLU(inplace=True),
        )
        self.skip_conv3 = nn.Sequential(
            nn.Conv2d(256 + style_out_channel, 256, 3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(256),
            nn.ReLU(inplace=True),
        )
        self.skip_conv4 = nn.Sequential(
            nn.Conv2d(128 + style_out_channel, 128, 3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(128),
            nn.ReLU(inplace=True),
        )
        self.skip_conv5 = nn.Sequential(
            nn.Conv2d(64 + style_out_channel, 64, 3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(64),
            nn.ReLU(inplace=True),
        )

        self.final = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.ZeroPad2d((1, 0, 1, 0)),
            nn.Conv2d(128, out_channel, 4, padding=1),
            nn.Tanh(),
        )

    def forward(self, content_imgs, target_styles):
        # Forward style

        # stack images along the channel dim
        squeezed_content_imgs = content_imgs.view(
            (content_imgs.shape[0], -1, *content_imgs.shape[-2:])
        )
        squeezed_target_styles = target_styles.view(
            (target_styles.shape[0], -1, *target_styles.shape[-2:])
        )
        target_style = self.style_enc(squeezed_target_styles)
        style_feature = target_style

        # Forward content
        conv = self.conv(squeezed_content_imgs)
        d1 = self.down1(conv)
        d2 = self.down2(d1)
        d3 = self.down3(d2)
        d4 = self.down4(d3)
        d5 = self.down5(d4)
        d6 = self.down6(d5)

        d6_ = torch.cat([d6, style_feature], dim=1)

        skip_style_feature = style_feature

        style1 = tile_like(skip_style_feature, d5)
        skip1 = torch.cat([d5, style1], 1)
        skip1 = self.skip_conv1(skip1)
        u1 = self.up1(d6_, skip1)

        atyle2 = tile_like(skip_style_feature, d4)
        skip2 = torch.cat([d4, atyle2], 1)
        skip2 = self.skip_conv2(skip2)
        u2 = self.up2(u1, skip2)

        style3 = tile_like(skip_style_feature, d3)
        skip3 = torch.cat([d3, style3], 1)
        skip3 = self.skip_conv3(skip3)
        u3 = self.up3(u2, skip3)

        style4 = tile_like(skip_style_feature, d2)
        skip4 = torch.cat([d2, style4], 1)
        skip4 = self.skip_conv4(skip4)
        u4 = self.up4(u3, skip4)

        style5 = tile_like(skip_style_feature, d1)
        skip5 = torch.cat([d1, style5], 1)
        skip5 = self.skip_conv5(skip5)
        u5 = self.up5(u4, skip5)

        out = self.final(u5)
        return out


class Discriminator(nn.Module):
    def __init__(
        self,
        in_channel: int = 1,
        n_style: int = 4,
        n_content: int = 4,
        n_res_blocks=8,
    ):
        super().__init__()

        def discriminator_block(in_filters, out_filters, normalize=True):
            layers = [nn.Conv2d(in_filters, out_filters, 4, 2, 1)]
            if normalize:
                layers.append(nn.InstanceNorm2d(out_filters))
            layers.append(nn.LeakyReLU(0.1))
            return layers

        res_blks = []
        for _ in range(n_res_blocks):
            res_blks.append(ResidualBlock(256))

        self.model = nn.Sequential(
            *discriminator_block(
                in_channel * (1 + n_content + n_style), 64, normalize=False
            ),
            *discriminator_block(64, 128),
            *discriminator_block(128, 256),
            *discriminator_block(256, 256),
            *res_blks,
            nn.ZeroPad2d((1, 0, 1, 0)),
            nn.Conv2d(256, 1, 4, padding=1, bias=False),
        )

    def forward(self, img, content_imgs, target_style_imgs):
        # stack style images on top of each other along the channel dim
        squeezed_target_style_imgs = target_style_imgs.view(
            (target_style_imgs.shape[0], -1, *target_style_imgs.shape[-2:])
        )
        squeezed_content_imgs = content_imgs.view(
            (content_imgs.shape[0], -1, *content_imgs.shape[-2:])
        )
        input = torch.cat(
            [img, squeezed_content_imgs, squeezed_target_style_imgs],
            dim=1,
        )
        out = self.model(input)
        return out


class CXLoss(nn.Module):
    def __init__(self, sigma=0.1, b=1.0, similarity="consine"):
        super().__init__()
        self.similarity = similarity
        self.sigma = sigma
        self.b = b

    def center_by_T(self, featureI, featureT):
        # Calculate mean channel vector for feature map.
        meanT = (
            featureT.mean(0, keepdim=True).mean(2, keepdim=True).mean(3, keepdim=True)
        )
        return featureI - meanT, featureT - meanT

    def l2_normalize_channelwise(self, features):
        # Normalize on channel dimension (axis=1)
        norms = features.norm(p=2, dim=1, keepdim=True)
        features = features.div(norms)
        return features

    def patch_decomposition(self, features):
        N, C, H, W = features.shape
        assert N == 1
        P = H * W
        # NCHW --> 1x1xCXHW --> HWxCx1x1
        patches = features.view(1, 1, C, P).permute((3, 2, 0, 1))
        return patches

    def calc_relative_distances(self, raw_dist, axis=1):
        epsilon = 1e-5
        # [0] means get the value, torch min will return the index as well
        div = torch.min(raw_dist, dim=axis, keepdim=True)[0]
        relative_dist = raw_dist / (div + epsilon)
        return relative_dist

    def calc_CX(self, dist, axis=1):
        W = torch.exp((self.b - dist) / self.sigma)
        W_sum = W.sum(dim=axis, keepdim=True)
        return W.div(W_sum)

    def forward(self, featureT, featureI):
        """
        :param featureT: target
        :param featureI: inference
        :return:
        """

        featureI, featureT = self.center_by_T(featureI, featureT)

        featureI = self.l2_normalize_channelwise(featureI)
        featureT = self.l2_normalize_channelwise(featureT)

        dist = []
        N = featureT.size()[0]
        for i in range(N):
            # NCHW
            featureT_i = featureT[i, :, :, :].unsqueeze(0)
            # NCHW
            featureI_i = featureI[i, :, :, :].unsqueeze(0)
            featureT_patch = self.patch_decomposition(featureT_i)
            # Calculate cosine similarity
            dist_i = F.conv2d(featureI_i, featureT_patch)
            dist.append(dist_i)

        # NCHW
        dist = torch.cat(dist, dim=0)

        raw_dist = (1.0 - dist) / 2.0

        relative_dist = self.calc_relative_distances(raw_dist)

        CX = self.calc_CX(relative_dist)

        CX = CX.max(dim=3)[0].max(dim=2)[0]
        CX = CX.mean(1)
        CX = -torch.log(CX)
        CX = torch.mean(CX)
        return CX
