# Aug 5, 2022

# This program fits two unets and displays results. Used for local testing.

# Imports
from pathlib import Path
import hydra
from omegaconf import DictConfig
import numpy as np
import matplotlib.pyplot as plt
from unet_compare.real_unet import real_main
from unet_compare.comp_unet import comp_main
from unet_compare.functions import get_brains, mask_gen, get_test
import logging

# Import settings with hydra
@hydra.main(
    version_base=None,
    config_path="../UofC2022/inputs/configs",
    config_name="settings_1",
)
def main(cfg: DictConfig):

    logging.info("Settings version: " + str(cfg["params"]["UNIT_CONFIRM"]))

    ADDR = Path.cwd()  # /Users/duncan.boyd/Documents/WorkCode/workvenv/UofC2022

    # Creates masks
    mask_gen(ADDR, cfg)

    # Loads data
    (
        mask,
        stats,
        dec_train,
        rec_train,
        dec_val,
        rec_val,
    ) = get_brains(cfg, ADDR)

    print(dec_train[0].dtype)
    print(rec_train[1].dtype)
    print(dec_val[0].dtype)
    print(rec_val[1].dtype)

    (
        dec_test,
        rec_test,
    ) = get_test(cfg, ADDR)

    # Calls both models
    comp_model = comp_main(
        cfg,
        ADDR,
        mask,
        stats,
        rec_train,
        dec_val,
        rec_val,
    )
    comp_model.summary()

    real_model = real_main(
        cfg,
        ADDR,
        mask,
        stats,
        rec_train,
        dec_val,
        rec_val,
    )
    real_model.summary()

    # Makes predictions
    logging.info("Evaluating UNet")
    comp_pred = comp_model.predict(dec_test)

    # Makes predictions
    logging.info("Evaluating UNet")
    real_pred = real_model.predict(dec_test)

    comp_pred = comp_pred / np.max(np.abs(comp_pred[:, :, :, 0] + 1j * comp_pred[:, :, :, 1]))
    real_pred = real_pred / np.max(np.abs(real_pred[:, :, :, 0] + 1j * real_pred[:, :, :, 1]))

    print(comp_pred[0].dtype)
    print(real_pred[1].dtype)

    # Displays predictions (Not necessary for ARC)
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 4, 1)
    plt.imshow((255.0 - rec_test[0, :, :, 0]), cmap="Greys")
    plt.subplot(1, 4, 2)
    plt.imshow((255.0 - comp_pred[0, :, :, 0]), cmap="Greys")
    plt.subplot(1, 4, 3)
    plt.imshow((255.0 - real_pred[0, :, :, 0]), cmap="Greys")
    plt.subplot(1, 4, 4)
    plt.imshow((255.0 - dec_test[0, :, :, 0]), cmap="Greys")
    plt.show()

    return


# Name guard
if __name__ == "__main__":

    # Runs the main program above
    main()
