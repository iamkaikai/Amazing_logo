from diffusers import DiffusionPipeline
import torch
from PIL import Image
import torchvision.transforms as transforms
from diffusers import DiffusionPipeline

prompt = "Simple elegant logo for a digital art, D A circle United State, successful vibe, minimalist, thought-provoking, abstract, recognizable"
size = 1000

pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe.load_lora_weights("iamkaikai/amazing-logos-lora")
pipe = pipe.to("cuda")
generator = [torch.Generator(device="cuda").manual_seed(i) for i in range(size)]
images = pipe(prompt, generator=generator, num_images_per_prompt=size).images

