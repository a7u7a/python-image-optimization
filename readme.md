# Image optimizer for web photos

- Python script to batch optimize images for static web assets. Outputs `.webp` files.
- Similar to [handbrake-batcher](https://github.com/a7u7a/handbrake-batcher) but for images.
- Point to a directory with a structure such as this:

````tree
├── folder1
│   └── selection
│       ├── _MG_4346-Pano.tif
│       ├── _MG_4362-Pano.tif
│       └── _MG_4404-Pano.tif
├── folder2
│   └── selection
│       ├── hei.tif
│       ├── hello.tif
│       └── bai.tif
...
````

## Features

- Preserves ICC profiles
- Tested on `.jpeg` and `.tiff` images. Should work with a large variety of formats.
- Tested on macOS.
- Name files according to parent folder name.
- See `process_images.sh` for an example of how to run the script.
- Update file permissions: `chmod +x process_images.sh`
