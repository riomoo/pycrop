# create thumbnails of all images in a directory concurrently
from os import listdir
from os import makedirs
from os.path import splitext
from os.path import join
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
from PIL import Image
 
# load an image and save a thumbnail version
def save_thumbnail(inpath, outpath):
    # load the image
    max_width = 150  # Define your desired thumbnail width
    max_height = 150  # Define your desired thumbnail height
    with Image.open(inpath) as image:
        # create a thumbnail image
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        # save the thumbnail image in PNG format
        image.save(outpath, 'WEBP')
 
# return the output path for a thumbnail image
def get_output_path(save_path, filename, extension):
    # separate the filename into name and extension
    name, _ = splitext(filename)
    # construct a new filename
    out_filename = f'{name}.{extension}'
    # construct the output path
    outpath = join(save_path, out_filename)
    return outpath
 
# perform the task of creating a thumbnail of an image
def task(image_path, save_path, filename):
    # construct the input path
    inpath = join(image_path, filename)
    # construct the output path
    outpath = get_output_path(save_path, filename, 'webp')
    # create the thumbnail
    save_thumbnail(inpath, outpath)
    # return the file that was saved so we can report progress
    return outpath
 
# entry point
def main():
    # location for loading images
    image_path = 'workon'
    # location for saving image thumbnails
    save_path = 'tmp'
    # create the output directory
    makedirs(save_path, exist_ok=True)
    # create the process pool
    with ProcessPoolExecutor() as exe:
        # submit tasks
        futures = [exe.submit(task, image_path, save_path, f) for f in listdir(image_path)]
        # report progress
        for future in as_completed(futures):
            # get the output path that was saved
            outpath = future.result()
            # report progress
            print(f'.saved {outpath}')
 
if __name__ == '__main__':
    main()
