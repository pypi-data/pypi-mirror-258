# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['limoe']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'swarms-torch', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'limoe',
    'version': '0.0.4',
    'description': 'LiMoE - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# LiMoE\nImplementation of the "the first large-scale multimodal mixture of experts models." from the paper: "Multimodal Contrastive Learning with LIMoE: the Language-Image Mixture of Experts". [CLICK HERE FOR THE PAPER LINK:](https://arxiv.org/abs/2206.02770)\n\n\n## install\n`pip install limoe`\n\n## usage\n```python\n\nimport torch\nfrom limoe.main import LiMoE\n\n# Text tokens (batch, sequence length)\ntext = torch.randint(0, 100, (1, 64))\n\n# image (batch, channels, height, width)\nimage = torch.randn(1, 3, 224, 224)\n\n# Create an instance of LiMoE with the specified parameters\nmodel = LiMoE(\n    dim=64,  # Dimension of the input and output tensors\n    depth=3,  # Number of layers in the encoder\n    heads=8,  # Number of attention heads\n    num_tokens=100,  # Number of tokens in the vocabulary\n    seq_length=64,  # Length of the input sequence\n    num_experts=4,  # Number of experts in the mixture-of-experts layer\n    dim_head=64,  # Dimension of each attention head\n    dropout=0.1,  # Dropout rate\n    ff_mult=4,  # Multiplier for the dimension of the feed-forward layer\n    patch_size=16,  # Patch size\n    image_size=224,  # Image size\n    channels=3,  # Number of image channels\n    dense_encoder_depth=5\n)\n\n# Pass the input tensor through the model and print the output\nout = model(text, image)\n\n# Print\nprint(out)\n```\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/LIMoE',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
