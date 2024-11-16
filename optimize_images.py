from PIL import Image, ImageCms
import os
import io


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


def resize_images(in_path, out_path, folder_name, max_size, max_low_res_size):
    images = os.listdir(in_path)
    counter = 0
    for filename in images:
        if filename == '.DS_Store':
            continue
        print("Processing:", filename)
        image = Image.open(in_path + filename)
        icc = get_icc_profile(image)

        # Resize high-res version
        if image.size[0] > image.size[1]:
            ratio = find_ratio(max_size, image.size[0], image.size[1])
            small_size = int(image.size[1]*ratio)
            image = image.resize((max_size, small_size))
        else:
            ratio = find_ratio(max_size, image.size[1], image.size[0])
            small_size = int(image.size[0]*ratio)
            image = image.resize((small_size, max_size))

        # Create and resize low-res version
        low_res_image = image.copy()
        if low_res_image.size[0] > low_res_image.size[1]:
            ratio = find_ratio(max_low_res_size, low_res_image.size[0], low_res_image.size[1])
            small_size = int(low_res_image.size[1]*ratio)
            low_res_image = low_res_image.resize((max_low_res_size, small_size))
        else:
            ratio = find_ratio(max_low_res_size, low_res_image.size[1], low_res_image.size[0])
            small_size = int(low_res_image.size[0]*ratio)
            low_res_image = low_res_image.resize((small_size, max_low_res_size))

        # Save both versions
        high_res_path = out_path + folder_name + '_' + str(counter) + '.webp'
        low_res_path = out_path + 'low-res/' + folder_name + '_' + str(counter) + '.webp'

        image.save(high_res_path, 'webp', optimize=True, quality=75, icc_profile=icc)
        low_res_image.save(low_res_path, 'webp', optimize=True, quality=90, icc_profile=icc)
        counter += 1

def process_all(main_path, out_path):
    folders = os.listdir(main_path)
    os.makedirs(out_path, exist_ok=True)
    
    for folder in folders:
        if folder == '.DS_Store':
            continue
            
        in_path = os.path.join(main_path, folder, "selection/")
        sub_out_path = os.path.join(out_path, folder)
        low_res_path = os.path.join(sub_out_path, 'low-res')
        
        if not os.path.exists(in_path):
            print(f"Error: Input directory '{in_path}' does not exist!")
            continue
        
        os.makedirs(sub_out_path, exist_ok=True)
        os.makedirs(low_res_path, exist_ok=True)
        
        resize_images(in_path, sub_out_path + '/', folder, 2000, 50)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Optimize images for web use')
    parser.add_argument('input_path', help='Path to input directory')
    parser.add_argument('output_path', help='Path to output directory')
    
    args = parser.parse_args()
    process_all(args.input_path, args.output_path)