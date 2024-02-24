"""
Description:
The RasterConverter module provides a set of functions for efficient data conversion and manipulation of raster datasets.
"""

import numpy as np
import rasterio

def raster_list(file_path):
    """
    Read raster data from a file, convert NoData values to None, and convert the data into a Python list.

    Args:
        file_path (str): Path to the raster file.

    Returns:
        list: Raster data as a Python list with NoData values converted to None.
    """
    # Open the raster file
    dataset = rasterio.open(file_path)

    # Check if the dataset was opened successfully
    if dataset is None:
        raise Exception("Failed to open the raster file.")

    # Get the raster band
    band = dataset.read(1)

    # Get the NoData value
    nodata_value = dataset.nodata

    # 获取栅格数据的行数和列数
    rows, cols = band.shape

    # 将栅格数据转换为矩阵
    raster_matrix = band.reshape(rows, cols)

    # 将数据类型转换为 object 类型，以支持存储 None
    raster_matrix = raster_matrix.astype(object)

    # Convert NoData values to None
    raster_matrix[raster_matrix == nodata_value] = None

    # Convert NumPy array to a Python list
    raster_list = [[raster_matrix[row][col] for col in range(cols)] for row in range(rows)]

    return raster_list


def process_raster_data(input_raster_path, output_raster_path, new_data):
    """
    Create a raster template based on the input raster, process the raster data by replacing pixel values with the new data.

    Args:
        input_raster_path (str): Path to the original raster file.
        output_raster_path (str): Path to save the output raster file.
        new_data (List): New data in the form of a 2D list.

    Returns:
        None
    """
    # Open the original raster dataset
    input_raster = rasterio.open(input_raster_path)

    # Create a new raster from the original raster dataset
    output_raster = rasterio.open(output_raster_path, "w", driver="GTiff",
                                  height=input_raster.height, width=input_raster.width, count=1,
                                  dtype="int16", crs=input_raster.crs, transform=input_raster.transform,
                                  nodata=0)

    # Replace pixel values with new data，and set the NoData value to 0
    masked_array = new_data == 0
    output_raster.write(np.array(new_data), 1, masked=masked_array)

    print(f"Processed raster data saved to {output_raster_path}.")

    # 关闭数据集
    input_raster.close()
    output_raster.close()
