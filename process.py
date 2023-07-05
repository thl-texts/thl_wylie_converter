from converter import Converter
import logging
from time import time
from os import listdir


if __name__ == "__main__":
    st_time = time()
    fmt = "%(asctime)s: %(message)s"
    logging.basicConfig(format=fmt, level=logging.INFO, datefmt="%H:%M:%S")
    files = [f for f in listdir('../in') if f.endswith('.xml')]
    files.sort()
    total = len(files)
    for i, f in enumerate(files):
        vol_num = i + 1
        print(f"\rDoing volume {vol_num} of {total}", end='')
        outfile_name = f'../out/ngb-vol-{vol_num}.xml'
        conv = Converter(f"../in/{f}")
        conv.process_lines()
        conv.write_xml(outfile_name)
        # if vol_num == 2:
        #     break
    end_time = time()
    elapsed = round(end_time - st_time, 2)
    print(f"\nDone in {elapsed} seconds!")

