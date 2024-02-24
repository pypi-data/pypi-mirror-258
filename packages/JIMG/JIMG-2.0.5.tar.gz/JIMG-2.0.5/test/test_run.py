# from JIMG.functions import jimg as jg

from JIMG.app import start_app

from functions import jimg as jg


tiff_file = load_tiff(path_to_tiff = 'channel_ch1.tiff')

path_to_inx = 'Images/Index.idx.xml'


    
    

resized_tiff = resize_tiff(image = tiff_file, metadata = None, height = None, width = None, resize_factor = 2)


resized_tiff_meta, meta = resize_tiff(image = tiff_file, metadata = metadata, height = None, width = None, resize_factor = 2)

save_tiff(tiff_image = resized_tiff_meta, path_to_save = 'res.tiff', metadata = None)

z, y, x, = read_tiff_meta(file_path = 'res.tiff')

save_tiff(tiff_image = resized_tiff_meta, path_to_save = 'res2.tiff', metadata = meta)

z, y, x, = read_tiff_meta(file_path = 'res2.tiff')



projection = z_projection(tiff_object = tiff_file, projection_type = 'median')



display_preview(projection)
 

eq_pro = equalizeHist_16bit(projection)


display_preview(eq_pro)


clahe_pro = clahe_16bit(eq_pro, kernal = (100, 100))


display_preview(clahe_pro)



adj_image = adjust_img_16bit(clahe_pro, color = 'blue', max_intensity = 65535, min_intenisty = 0, brightness = 100, contrast = 3, gamma = 1)

display_preview(adj_image)


resized = resize_projection(adj_image, metadata = None, height = None, width = None, resize_factor = 2)


display_preview(resized)


split_channels(path_to_images = 'Images', path_to_save = '')





jg.manual_outlires(xml_file:pd.DataFrame, list_of_out:list = [], dispaly_plot = False)


jg.repair_image(xml_file:pd.DataFrame, dispaly_plot = True)


jg.image_sequences(opera_coordinates:pd.DataFrame)


jg.image_concatenate(path_to_images:str, path_to_save:str, imgs:pd.DataFrame, metadata, img_length:int, img_width:int, overlap:int, channels:list, resize:int = 2, n_proc:int = 4, par_type = 'processes')




jg.merge_images(image_list:list, intensity_factors:list = [])









