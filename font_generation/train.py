# based on https://raw.githubusercontent.com/hologerry/Attr2Font/master/main.py

import datetime
import os
from pathlib import Path
import time
from tqdm import tqdm
import torch
from torchvision.utils import save_image
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from font_generation.model.model import Discriminator, Generator
from font_generation.data.FontStylesDataset import FontStylesDataset
from font_generation.fontutils.load_all_fonts import load_all_fonts


def train(
    device: torch.device,
    generator: Generator,
    discriminator: Discriminator,
    experiment_dir: Path = Path("experiments"),
    total_samples: int = 10000,
    size_px=64,
    epochs=5,
    batch_size=1,
    lr=0.001,
    b1=0.5,
    b2=0.999,
    val_portion=0.01,
    num_workers=2,
    init_epoch=0,
    lambda_l1=50.0,
    lambda_GAN=5.0,
    checkpoint_freq=10,
    log_freq=500,
    val_freq=500,
):
    # Dirs
    checkpoint_dir = experiment_dir / "checkpoints"
    samples_dir = experiment_dir / "samples"
    logs_dir = experiment_dir / "logs"

    writer = SummaryWriter(comment=f"LR_{lr}_BS_{batch_size}_N_{total_samples}")

    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    samples_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Loss criterion
    criterion_GAN = torch.nn.MSELoss().to(device)
    criterion_pixel = torch.nn.L1Loss().to(device)

    n_val = int(total_samples * val_portion)
    n_train = total_samples - n_val

    # # CX Loss
    # if lambda_cx > 0:
    #     criterion_cx = CXLoss(sigma=0.5).to(device)
    #     vgg19 = VGG19_CX().to(device)
    #     vgg19.load_model("vgg19-dcbb9e9d.pth")
    #     vgg19.eval()
    #     vgg_layers = ["conv3_3", "conv4_2"]

    fonts = load_all_fonts()

    train_dataloader = DataLoader(
        FontStylesDataset(fonts, n_train, size_px=size_px, static=False),
        batch_size=batch_size,
        num_workers=num_workers,
    )
    test_dataloader = DataLoader(
        FontStylesDataset(fonts, n_val, size_px=size_px, static=True),
        batch_size=batch_size,
        num_workers=num_workers,
    )

    # Model
    generator = generator.to(device)
    discriminator = discriminator.to(device)

    # Discriminator output patch shape
    patch = (1, size_px // 2 ** 4, size_px // 2 ** 4)

    # optimizers
    optimizer_G = torch.optim.Adam(
        generator.parameters(),
        lr=lr,
        betas=(b1, b2),
    )
    optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=lr, betas=(b1, b2))

    # Resume training
    if init_epoch > 0:
        gen_file = checkpoint_dir / f"G_{init_epoch}.pth"
        dis_file = checkpoint_dir / f"D_{init_epoch}.pth"

        generator.load_state_dict(torch.load(gen_file))
        discriminator.load_state_dict(torch.load(dis_file))

    prev_time = time.time()
    logfile = open(experiment_dir / "loss_log.txt", "w")
    val_logfile = open(experiment_dir / "val_loss_log.txt", "w")

    global_step = 0
    for epoch in range(init_epoch, epochs):
        with tqdm(
            total=n_train, desc=f"Epoch {epoch + 1}/{epochs}", unit="img"
        ) as pbar:
            for batch_idx, batch in enumerate(train_dataloader):
                pbar.update(batch_size)
                content_img = batch["content"].to(device)
                style_imgs = batch["styles"].to(device)

                target_img = batch["target"].to(device)

                valid = torch.ones((content_img.size(0), *patch)).to(device)
                fake = torch.zeros((content_img.size(0), *patch)).to(device)

                # Forward G and D
                fake_img = generator(content_img, style_imgs)
                pred_fake = discriminator(fake_img, style_imgs)

                # if lambda_cx > 0:
                #     vgg_fake_B = vgg19(fake_B)
                #     vgg_img_B = vgg19(img_B)

                # Calculate losses
                loss_GAN = lambda_GAN * criterion_GAN(pred_fake, valid)
                loss_pixel = lambda_l1 * criterion_pixel(fake_img, target_img)

                # loss_char_A = criterion_ce(
                #     content_logits_A, charclass_A.view(charclass_A.size(0))
                # )  # +
                # loss_char_A = lambda_char * loss_char_A

                # # CX loss
                # loss_CX = torch.zeros(1).to(device)
                # if lambda_cx > 0:
                #     for l in vgg_layers:
                #         cx = criterion_cx(vgg_img_B[l], vgg_fake_B[l])
                #         loss_CX += cx * lambda_cx

                loss_G = loss_GAN + loss_pixel  # + loss_char_A + loss_CX

                optimizer_G.zero_grad()
                loss_G.backward(retain_graph=True)
                optimizer_G.step()

                # Forward D
                pred_real = discriminator(target_img, style_imgs)
                loss_real = criterion_GAN(pred_real, valid)

                pred_fake = discriminator(fake_img.detach(), style_imgs)  # noqa
                loss_fake = criterion_GAN(pred_fake, fake)

                loss_D = loss_real + loss_fake

                optimizer_D.zero_grad()
                loss_D.backward(retain_graph=True)
                optimizer_D.step()

                batches_done = (epoch - init_epoch) * len(train_dataloader) + batch_idx
                batches_left = (epochs - init_epoch) * len(
                    train_dataloader
                ) - batches_done
                time_left = datetime.timedelta(
                    seconds=batches_left * (time.time() - prev_time)
                )
                prev_time = time.time()

                message = (
                    f"Epoch: {epoch}/{epochs}, Batch: {batch_idx}/{len(train_dataloader)}, ETA: {time_left}, "
                    f"D loss: {loss_D.item():.6f}, G loss: {loss_G.item():.6f}, "
                    f"loss_pixel: {loss_pixel.item():.6f}, "
                    f"loss_adv: {loss_GAN.item():.6f}, "
                )

                pbar.set_postfix(**{"G loss": loss_G.item(), "D loss": loss_D.item()})
                writer.add_scalar("GLoss/train", loss_G.item(), global_step)
                writer.add_scalar("DLoss/train", loss_D.item(), global_step)
                global_step += 1

                logfile.write(message + "\n")
                logfile.flush()

                if batches_done % log_freq == 0:
                    img_sample = torch.cat(
                        (
                            fake_img.data,
                            target_img.data,
                            content_img.data,
                            style_imgs.data.view(
                                (
                                    style_imgs.shape[0],
                                    style_imgs.shape[-3],
                                    -1,  # stack vertically
                                    style_imgs.shape[-1],
                                )
                            ),
                        ),
                        -2,
                    )
                    save_file = os.path.join(
                        logs_dir, f"epoch_{epoch}_batch_{batches_done}.png"
                    )
                    save_image(img_sample, save_file, nrow=11, normalize=True)
                    writer.add_scalar(
                        "learning_rate_G",
                        optimizer_G.param_groups[0]["lr"],
                        global_step,
                    )
                    writer.add_scalar(
                        "learning_rate_D",
                        optimizer_D.param_groups[0]["lr"],
                        global_step,
                    )

                if batches_done % val_freq == 0:
                    with torch.no_grad():
                        val_l1_loss = torch.zeros(1).to(device)
                        total_val_batches = 0
                        for val_idx, val_batch in enumerate(test_dataloader):
                            total_val_batches += 1
                            val_content = val_batch["content"].to(device)
                            val_styles = val_batch["styles"].to(device)

                            val_target = val_batch["target"].to(device)

                            val_fake = generator(val_content, val_styles)

                            val_l1_loss += criterion_pixel(val_fake, val_target)

                            img_sample = torch.cat(
                                (
                                    val_fake.data,
                                    val_target.data,
                                    val_content.data,
                                    val_styles.data.view(
                                        (
                                            val_styles.shape[0],
                                            val_styles.shape[-3],
                                            -1,  # stack vertically
                                            val_styles.shape[-1],
                                        )
                                    ),
                                ),
                                -2,
                            )
                            save_file = os.path.join(
                                samples_dir, f"epoch_{epoch}_idx_{val_idx}.png"
                            )
                            save_image(img_sample, save_file, nrow=11, normalize=True)
                            writer.add_images("images", img_sample, global_step)

                        val_l1_loss = val_l1_loss / total_val_batches
                        writer.add_scalar("val_l1_loss", val_l1_loss, global_step)
                        val_msg = (
                            f"Epoch: {epoch}/{epochs}, Batch: {batch_idx}/{len(train_dataloader)}, "
                            f"L1: {val_l1_loss.item(): .6f}"
                        )
                        print(val_msg)
                        val_logfile.write(val_msg + "\n")
                        val_logfile.flush()
            if epoch % checkpoint_freq == 0:
                gen_file_file = os.path.join(checkpoint_dir, f"G_{epoch}.pth")
                dis_file_file = os.path.join(checkpoint_dir, f"D_{epoch}.pth")

                torch.save(generator.state_dict(), gen_file_file)
                torch.save(discriminator.state_dict(), dis_file_file)
