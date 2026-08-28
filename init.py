# ============================================================
# ☢️ OTP NUKLIR v4.0 - SOURCE PACKAGE
# Author: Novxzzz
# Engine: Sonic 1.2
# ============================================================

"""
OTP NUKLIR - Source Package
============================

Package ini berisi semua modul inti untuk OTP Bomber.

Modul:
    - bomber.py: Core engine OTP Bomber
    - utils.py: Fungsi utilitas (headers, payload, dll)
"""

__version__ = "4.0"
__author__ = "Profesor Iraq"
__engine__ = "Sonic 1.2"
__protocol__ = "NEXA_BYPAS_OMEGA"

# ============================================================
# EXPOSE PUBLIC FUNCTIONS
# ============================================================

# Impor dari sub modul
from .bomber import OTPBomber, send_otp, generate_payload
from .utils import (
    generate_device_id,
    generate_imei,
    get_random_user_agent,
    get_random_headers,
    load_proxies,
    save_log,
    clear_screen
)

# ============================================================
# PACKAGE INFO
# ============================================================

__all__ = [
    # Classes
    "OTPBomber",
    
    # Functions
    "send_otp",
    "generate_payload",
    "generate_device_id",
    "generate_imei",
    "get_random_user_agent",
    "get_random_headers",
    "load_proxies",
    "save_log",
    "clear_screen",
    
    # Metadata
    "__version__",
    "__author__",
    "__engine__",
    "__protocol__"
]

# ============================================================
# LOGGING
# ============================================================

import logging

# Setup logging untuk package
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def setup_logging(level=logging.INFO):
    """Setup logging untuk package"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.setLevel(level)
    return logger

# ============================================================
# VERSION CHECK
# ============================================================

import sys

def check_python_version():
    """Cek versi Python minimal"""
    if sys.version_info < (3, 8):
        raise RuntimeError(
            f"Python 3.8+ required. Current: {sys.version}"
        )
    return True

check_python_version()

# ============================================================
# INIT MESSAGE
# ============================================================

print(f"""
╔═══════════════════════════════════════════════════════╗
║  ☢️ OTP NUKLIR v{__version__}                               ║
║  Author: {__author__}                           ║
║  Engine: {__engine__}                                 ║
║  Protocol: {__protocol__}                          ║
╚═══════════════════════════════════════════════════════╝
""")
