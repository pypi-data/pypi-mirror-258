import argparse

import numpy as np
from diffusers import StableDiffusionPipeline
from PIL import Image

from qai_hub_models.models.stable_diffusion.app import StableDiffusionApp
from qai_hub_models.models.stable_diffusion.model import (
    DEFAULT_VERSION,
    SDTextEncoder,
    SDUNet,
    SDVAEDecoder,
)
from qai_hub_models.utils.args import add_output_dir_arg
from qai_hub_models.utils.display import display_or_save_image

DEFAULT_DEMO_PROMPT = "a high-quality photo of a surfing dog"


# Run Stable Diffuison end-to-end on a given prompt. The demo will output an
# AI-generated image based on the description in the prompt.
def main(is_test: bool = False):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompt",
        default=DEFAULT_DEMO_PROMPT,
        help="Prompt to generate image from.",
    )
    parser.add_argument(
        "--model-version",
        default=DEFAULT_VERSION,
        help="Pre-trained checkpoint and configuration. For available checkpoints: https://huggingface.co/models?search=stable-diffusion.",
    )
    parser.add_argument(
        "--num-steps",
        default=50,
        type=int,
        help="The number of diffusion iteration steps (higher means better quality).",
    )
    parser.add_argument(
        "--seed",
        default=0,
        type=int,
        help="Random seed.",
    )
    add_output_dir_arg(parser)
    parser.add_argument(
        "--guidance-scale",
        type=float,
        default=7.5,
        help="Strength of guidance (higher means more influence from prompt).",
    )
    args = parser.parse_args([] if is_test else None)

    # Load components

    # Load model with weights from HuggingFace
    pipe = StableDiffusionPipeline.from_pretrained(
        args.model_version, use_auth_token=True
    )

    # Construct all the networks
    text_encoder = SDTextEncoder(pipe).eval()
    vae_decoder = SDVAEDecoder(pipe).eval()
    unet = SDUNet(pipe).eval()

    # Save the tokenizer and scheduler
    tokenizer = pipe.tokenizer
    scheduler = pipe.scheduler

    # Load Application
    app = StableDiffusionApp(
        text_encoder=text_encoder,
        vae_decoder=vae_decoder,
        unet=unet,
        tokenizer=tokenizer,
        scheduler=scheduler,
    )

    if not is_test:
        print()
        print("** Performing image generation with Stable Diffusion **")
        print()
        print("Prompt:", args.prompt)
        print("Model:", args.model_version)
        print("Number of steps:", args.num_steps)
        print("Guidance scale:", args.guidance_scale)
        print("Seed:", args.seed)
        print()
        print(
            "Note: This reference demo uses significant amounts of memory and may take a few minutes to run."
        )
        print()

    # Generate image
    image = app.generate_image(
        args.prompt,
        num_steps=args.num_steps,
        seed=args.seed,
        guidance_scale=args.guidance_scale,
    )

    pil_img = Image.fromarray(np.round(image.detach().numpy() * 255).astype(np.uint8))

    if not is_test:
        display_or_save_image(pil_img, args.output_dir)


if __name__ == "__main__":
    main()
