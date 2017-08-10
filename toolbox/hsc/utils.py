import os
HSC_DIR = os.getenv('HSC_DIR')

def get_skymap(data_dir=HSC_DIR):
    import lsst.daf.persistence
    butler = lsst.daf.persistence.Butler(data_dir)
    skymap = butler.get('deepCoadd_skyMap', immediate=True)
    return butler, skymap 
