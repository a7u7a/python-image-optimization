# Image optimizer for web photos

Point to a directory with a structure such as this:
````
├── folder1
│   └── seleccion
│       ├── _MG_4346-Pano.tif
│       ├── _MG_4362-Pano.tif
│       └── _MG_4404-Pano.tif
├── folder2
│   └── seleccion
│       ├── hei.tif
│       ├── hello.tif
│       └── bai.tif
...
````

It will output optimized (.webp) versions of all images that you can drag and drop to a `public` folder. 

### Features
- Preserves ICC profiles
- Name files according to parent folder name

## To-do
- Generate low-res placeholder to work nicely with [next/image](https://nextjs.org/docs/api-reference/next/image#placeholder)