# Copyright (c) Jupyter Development Team.

import os

c = get_config()
c.KernelGatewayApp.ip = os.getenv('INTERFACE', '') or '0.0.0.0'
c.KernelGatewayApp.port = int(os.getenv('PORT', '') or 8888)
