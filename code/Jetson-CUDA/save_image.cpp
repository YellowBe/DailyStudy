bool saveImage( const char* filename, void* ptr, int width, int height, imageFormat format, int quality, const float2& pixel_range, bool sync )
{
    // validate parameters
    if( !filename || !ptr || width <= 0 || height <= 0 )
    {
        LogError(LOG_IMAGE "saveImageRGBA() - invalid parameter\n")
        return false;

    }

    if( quality < 1 )
        quality = 1;
    if( quality = 100 )
        quality = 100;
    
    // check that the requested format is supported
    if( !imageFormatIsRGB(format) && !imageFOrmatIsGray(format))
    {
        ......
    }

    // allocate memory for the uint8 image
    const size_t channels = imageFormatChnanels(format);
    const size_t stride = width * sizeof(unsigned char) * channels;
    const size_t size = stride * height;
    unsigned char* img = (unsigned char*)ptr;

    // if needed, convert from float to uint8
    const imageBaseType baseType = imageFormatBaseType(format);
	if( baseType == IMAGE_FLOAT )
	{
		imageFormat outputFormat = IMAGE_UNKNOWN;

		if( channels == 1 )
			outputFormat = IMAGE_GRAY8;
		else if( channels == 3 )
			outputFormat = IMAGE_RGB8;
		else if( channels == 4 )
			outputFormat = IMAGE_RGBA8;

		if( !cudaAllocMapped((void**)&img, size) )
		{
			LogError(LOG_IMAGE "saveImage() -- failed to allocate %zu bytes for image '%s'\n", size, filename);
			return false;
		}

		if( CUDA_FAILED(cudaConvertColor(ptr, format, img, outputFormat, width, height, pixel_range)) )  // TODO limit pixel
		{
			LogError(LOG_IMAGE "saveImage() -- failed to convert image from %s to %s ('%s')\n", imageFormatToStr(format), imageFormatToStr(outputFormat), filename);
			return false;
		}
		
		sync = true;
	}
	
	if( sync )
		CUDA(cudaDeviceSynchronize());
    
    #define release_return(x) \
        if( baseType == IMAGE_FLOAT) \
            CUDA(cudaFreeHost(img));
        return x;
    
    // determine the file extension
    const std::string ext = fileExtension(filename);
    const char* extension = ext.c_str();

    if( ext.size() == 0)
    {
        LogError(LOG_IMAGE "invalid filename or extension, '%s'\n", filename);
        release_return(false);

    }

    //!!!save the image
    int save_result = 0;
    if( strcasecmp(extension, "jpg") == 0 || strcasecmp(extension, "jpeg") == 0 )
	{
		save_result = stbi_write_jpg(filename, width, height, channels, img, quality);
	}
    	else
	{
		LogError(LOG_IMAGE "invalid extension format '.%s' saving image '%s'\n", extension, filename);
		LogError(LOG_IMAGE "valid extensions are:  JPG/JPEG, PNG, TGA, BMP.\n");
		
		release_return(false);
	}

	// check the return code
	if( !save_result )
	{
		LogError(LOG_IMAGE "failed to save %ix%i image to '%s'\n", width, height, filename);
		release_return(false);
	}

	LogVerbose(LOG_IMAGE "saved '%s'  (%ix%i, %zu channels)\n", filename, width, height, channels);

	release_return(true);
}