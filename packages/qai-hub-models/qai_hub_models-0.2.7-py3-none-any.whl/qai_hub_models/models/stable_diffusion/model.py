from __future__ import annotations

from typing import Any, Optional

from diffusers import StableDiffusionPipeline

from qai_hub_models.utils.asset_loaders import SourceAsRoot
from qai_hub_models.utils.base_model import BaseModel, CollectionModel
from qai_hub_models.utils.input_spec import InputSpec

SD_SOURCE_REPO = "https://github.com/apple/ml-stable-diffusion.git"
SD_SOURCE_REPO_COMMIT = "b392a0aca09a8321c8955ee84b48e9e9fdb49c93"
MODEL_ID = __name__.split(".")[-2]
MODEL_ASSET_VERSION = 1
DEFAULT_VERSION = "CompVis/stable-diffusion-v1-4"


class SDTextEncoder(BaseModel):
    """
    Model that encodes the text prompt into a latent tensor.
    """

    def __init__(self, pipe):
        super().__init__()
        self.text_encoder_sequence_length = pipe.tokenizer.model_max_length
        self.vocab_size = pipe.tokenizer.vocab_size
        self.text_encoder = pipe.text_encoder

    def get_input_spec(self) -> InputSpec:
        # Get the input specification ordered (name -> (shape, type)) pairs for
        # this model.
        #
        # This can be used with the qai_hub python API to declare
        # the model input specification upon submitting a profile job.

        return {"input_ids": ((1, self.text_encoder_sequence_length), "int32")}

    def forward(self, input_ids):
        return self.text_encoder(input_ids, return_dict=False)

    @classmethod
    def from_pretrained(cls):
        return SDModel.from_pretrained().text_encoder


class SDVAEEncoder(BaseModel):
    """
    Model that encodes the image into the low-resolution latent space (the
    domain of the UNet denoiser). This is not needed for the basic demo which
    generates only guided by a text prompt.
    """

    def __init__(self, pipe):
        super().__init__()
        self.quant_conv = pipe.vae.quant_conv
        self.encoder = pipe.vae.encoder
        self.vae_scale = 8
        self.height = pipe.unet.config.sample_size * self.vae_scale
        self.width = pipe.unet.config.sample_size * self.vae_scale

    def get_input_spec(self) -> InputSpec:
        # Get the input specification ordered (name -> (shape, type)) pairs for
        # this model.
        #
        # This can be used with the qai_hub python API to declare
        # the model input specification upon submitting a profile job.

        return {"image": ((1, 3, self.height, self.width), "float32")}

    def forward(self, z):
        return self.quant_conv(self.encoder(z))

    @classmethod
    def from_pretrained(cls):
        return SDModel.from_pretrained().vae_encoder


class SDVAEDecoder(BaseModel):
    """
    Model that decodes the image from the low-resolution latent space (the
    domain of the UNet denoiser).
    """

    def __init__(self, pipe):
        super().__init__()
        self.post_quant_conv = pipe.vae.post_quant_conv
        self.decoder = pipe.vae.decoder
        self.latent_channels = pipe.vae.config.latent_channels
        self.height = pipe.unet.config.sample_size
        self.width = pipe.unet.config.sample_size

    def get_input_spec(self) -> InputSpec:
        # Get the input specification ordered (name -> (shape, type)) pairs for
        # this model.
        #
        # This can be used with the qai_hub python API to declare
        # the model input specification upon submitting a profile job.

        return {"z": ((1, self.latent_channels, self.height, self.width), "float32")}

    def forward(self, z):
        return self.decoder(self.post_quant_conv(z))

    @classmethod
    def from_pretrained(cls):
        return SDModel.from_pretrained().vae_decoder


class SDUNet(BaseModel):
    """
    UNet is the core of the Stable Diffusion denoiser. It is a U-Net-style
    denoiser that operates on a lower-resolution embedded space. It is the only
    model that runs repeatedly during the generation of an image, so
    performance of this model is the most critical.

    Unlike the other models, this model does not use the HuggingFace model
    directly and instead uses a version developed by Apple from
    https://github.com/apple/ml-stable-diffusion.
    """

    def __init__(self, pipe, do_classifier_free_guidance: bool = True):
        super().__init__()

        # Load unet package
        unet = _load_apple_sd_package()

        # Construct UNet and load state dictionary
        self.unet = unet.UNet2DConditionModel(**pipe.unet.config)
        self.unet.load_state_dict(pipe.unet.state_dict())

        # Configuration variables
        self.batch_size = 2 if do_classifier_free_guidance else 1
        self.in_channels = pipe.unet.config.in_channels
        self.height = pipe.unet.config.sample_size
        self.width = pipe.unet.config.sample_size

        # Input shapes
        self.sample_shape = (
            self.batch_size,
            self.in_channels,
            self.height,
            self.width,
        )
        self.timestep_shape = (self.batch_size,)
        self.encoder_hidden_states_shape = (
            self.batch_size,
            pipe.text_encoder.config.hidden_size,
            1,
            pipe.text_encoder.config.max_position_embeddings,
        )

    def get_input_spec(self) -> InputSpec:
        # Get the input specification ordered (name -> (shape, type)) pairs for
        # this model.
        #
        # This can be used with the qai_hub python API to declare
        # the model input specification upon submitting a profile job.

        return {
            "sample": (self.sample_shape, "float32"),
            "timestep": (self.timestep_shape, "float32"),
            "encoder_hidden_states": (self.encoder_hidden_states_shape, "float32"),
        }

    def forward(self, *args):
        return self.unet(*args)

    @classmethod
    def from_pretrained(cls):
        return SDModel.from_pretrained().unet


def _load_apple_sd_package() -> Any:
    """
    Imports and returns the Apple the Stable Diffusion package.

    Returns:
        unet: The package where the UNet model is defined.
    """
    with SourceAsRoot(
        SD_SOURCE_REPO, SD_SOURCE_REPO_COMMIT, MODEL_ID, MODEL_ASSET_VERSION
    ):
        # import required modules and utilities
        from python_coreml_stable_diffusion import unet

        return unet


class SDModel(CollectionModel):
    """Wrapper class containing all the components to run stable diffusion."""

    def __init__(
        self,
        text_encoder: SDTextEncoder,
        vae_decoder: SDVAEDecoder,
        unet: SDUNet,
        vae_encoder: Optional[SDVAEEncoder] = None,
    ):
        self.text_encoder = text_encoder
        self.vae_decoder = vae_decoder
        self.unet = unet
        self.vae_encoder = vae_encoder

    @classmethod
    def from_pretrained(cls, model_version: str = DEFAULT_VERSION):
        pipe = StableDiffusionPipeline.from_pretrained(
            model_version, use_auth_token=True
        )
        return cls(
            text_encoder=SDTextEncoder(pipe).eval(),
            vae_decoder=SDVAEDecoder(pipe).eval(),
            unet=SDUNet(pipe).eval(),
            vae_encoder=SDVAEEncoder(pipe).eval(),
        )
