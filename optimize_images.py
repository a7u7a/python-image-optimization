import PIL
from PIL import Image, ImageCms
import os
import io

main_path = "/Users/userfriendly/Dropbox/Proyectos/esrs-2023/content/"
out_path = "/Users/userfriendly/Dropbox/Proyectos/esrs-2023/content-optimized/"

# save images to low-res folder


def get_base_filename(path):
    path_list = path.split('/')
    name_index = len(path_list)-3
    base_filename = path_list[name_index]
    print("Base filename is: ", base_filename)
    return base_filename


def find_ratio(max_size, large_size, small_size):
    ratio = abs(((large_size - max_size)/large_size)-1)
    return ratio


def get_icc_profile(image):
    # get icc profile to be used with saved image
    try:
        icc = image.info.get('icc_profile')
        icc = io.BytesIO(icc)
        icc = ImageCms.ImageCmsProfile(icc)
        icc = icc.tobytes()
        return icc
    except:
        print("Error getting profile")
        return None


def resize_images(in_path, out_path, thumb_path,folder_name, max_size, max_low_res_size):
    images = os.listdir(in_path)
    counter = 0
    for filename in images:
        if filename == '.DS_Store':
            continue
        print("processing:", filename)
        image = Image.open(in_path + filename)
        icc = get_icc_profile(image)

        # if width is larger than height
        if image.size[0] > image.size[1]:
            ratio = find_ratio(max_size, image.size[0], image.size[1])
            small_size = int(image.size[1]*ratio)
            image = image.resize((max_size, small_size))
            
            low_res_ratio = find_ratio(max_low_res_size, image.size[0], image.size[1])
            low_res_small_size = int(image.size[1]*low_res_ratio)
            low_res_image = image.resize((low_res_small_size, max_low_res_size))
        else:
            ratio = find_ratio(max_size, image.size[1], image.size[0])
            small_size = int(image.size[0]*ratio)
            image = image.resize((small_size, max_size))

            low_res_ratio = find_ratio(max_low_res_size, image.size[1], image.size[0])
            low_res_small_size = int(image.size[0]*low_res_ratio)
            low_res_image = image.resize((low_res_small_size, max_low_res_size))

        final_out_path = thumb_path + 'thumb.webp'
        low_res_path = out_path + '/low-res/' + \
            folder_name + '_' + str(counter) + '.webp'

        # print("processing file:",filename,"resolution pre:",size_pre ,"resolution post:",image.size, "saving as:",final_out_path )
        
        image.save(final_out_path, 'webp', optimize=True,
                   quality=75, icc_profile=icc)
        #   Save low-res version

        # low_res_image.save(low_res_path, 'webp', optimize=True,
        #                    quality=90, icc_profile=icc)
        counter += 1


def process_all(main_path, out_path):
    folders = os.listdir(main_path)
    # create main output dir
    os.mkdir(out_path)
    for folder in folders:
        print("Project:", folder)
        if folder == '.DS_Store':
            continue
        # get image from "seleccion"
        in_path = main_path + folder + "/thumb/"
        sub_out_path = out_path + folder + '/'
        sub_thumb_path = sub_out_path
        low_res_path = sub_out_path + '/low-res/'
        os.mkdir(sub_out_path)
        # os.mkdir(sub_thumb_path)
        # os.mkdir(low_res_path)
        resize_images(in_path, sub_out_path,sub_thumb_path, folder, 2000, 50)


if __name__ == "__main__":
    process_all(main_path, out_path)
