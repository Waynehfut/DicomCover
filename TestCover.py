#-*-coding:utf-8-*-
import dicom
import os
import pylab

# 传入文件名显示图片
def show_image_file(fileName):
    ds = dicom.read_file(fileName)
    pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
    pylab.show()

# 解析dicom文件
def parse_dicomdir(dicomDir):
    dsdir = dicom.read_dicomdir(dicomDir)
    pixel_data = list()
    dicom_array = list()
    for record in dsdir.DirectoryRecordSequence:
        if record.DirectoryRecordType == "IMAGE":
            # 遍历路径获取得到Dicom存在的文件路径
            path = os.path.join(*record.ReferencedFileID)
            dcm = dicom.read_file(path)
            # Dicom文件传入数组
            dicom_array.append(dcm)
    return dicom_array

# 保存Dicom文件
def save_dicom_image(dicomDataset):
    if not os.path.exists(dicomDataset.filename.split('\\')[0] + '_export'):
        os.mkdir(dicomDataset.filename.split('\\')[0] + '_export')
    pylab.imshow(dicomDataset.pixel_array,cmap=pylab.cm.bone)
    os.chdir(dicomDataset.filename.split('\\')[0]+'_export')
    pylab.savefig(dicomDataset.filename.replace('\\','.')+'.jpg',bbox_inches='tight')
    os.chdir('..')

# 遍历Dicomdir中的文件并保存
for singleRecord in parse_dicomdir("DICOMDIR"):
    save_dicom_image(singleRecord)