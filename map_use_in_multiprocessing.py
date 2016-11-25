from multiprocessing import Pool
from PIL import Image
import os,time

SIZE = (75,75)
SAVE_DIRECTORY = 'thumbs'

def get_image_paths(folder):
    return (os.path.join(folder,f) for f in os.listdir(folder) if 'jp' in f or 'JP' in f)

def create_thumbnail(filename):
    im = Image.open(filename)
    im.thumbnail(SIZE,Image.ANTIALIAS)
    base,fname = os.path.split(filename)
    save_path = os.path.join(base,SAVE_DIRECTORY,'s_%s' % fname)
    im.save(save_path)

if __name__ == '__main__':
    t = time.time()
    folder = os.path.abspath('D:\wan')
    os.mkdir(os.path.join(folder,SAVE_DIRECTORY))
    images = get_image_paths(folder)
    pool = Pool(2)
    pool.map(create_thumbnail,images)
    pool.close()
    pool.join()
    print(time.time()-t)