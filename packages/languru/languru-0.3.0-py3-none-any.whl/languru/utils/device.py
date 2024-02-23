from typing import Optional, Text

from languru.config import logger


def validate_device(device: Optional[Text] = None) -> Text:
    if device is not None and device.strip().lower() == "cpu":
        return "cpu"
    try:
        import torch
    except ImportError:
        logger.warning("Torch is not installed. The device will be CPU.")
        return "cpu"
    # Try to find the device
    if device is None:
        if torch.cuda.is_available():
            logger.debug("Device found: CUDA")
            return "cuda"
        elif torch.backends.mps.is_available():
            logger.debug("Device found: MPS")
            return "mps"
        else:
            logger.debug("Device found: CPU")
            return "cpu"
    # Validate cuda device
    if device.strip().startswith("cuda"):
        if not torch.cuda.is_available():
            logger.warning("CUDA is not available. The device will be CPU.")
            return "cpu"
        return device
    # Validate mps device
    if device.strip().startswith("mps"):
        if not torch.backends.mps.is_available():
            logger.warning("MPS is not available. The device will be CPU.")
            return "cpu"
        return device
    # Validate cpu device
    if device.strip() == "cpu":
        return device
    # Validate unknown device
    logger.warning(f"Unknown device: {device}. The device will be CPU.")
    return "cpu"
