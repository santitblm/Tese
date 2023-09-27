def LP_valid(img):
    if img.shape[0] > img.shape[1] or img.shape[0] < 20 or img.shape[0] * img.shape[1] < 1000:
        return False
    return True