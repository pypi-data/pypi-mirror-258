from src.jacpy.io import ioUtils
from src.jacpy.geometry import geoUtils

items = ioUtils.dirItems('C:/Users/alber/Desktop/BACKUP ABRIL 2022', ioUtils.DirItemPolicy.AllAlphabetic, ioUtils.DirItemOutputForm.Name, "*.txt", 0, 2)

print(items)



partitions = geoUtils.partition1DGeometry(50, 50, 0.5, 1.5)
print(partitions)


partitions = geoUtils.partition2DGeometry(100, 51, 50, 50, 0.5, 1.5)
print(partitions)