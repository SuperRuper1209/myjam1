def convertDimensions(val, dim, originalDimensions=(1536, 864)):
    return val[0] / originalDimensions[0] * dim[0], val[1] / originalDimensions[1] * dim[1]
