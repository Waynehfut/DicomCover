# -*-coding:utf-8-*-
import dicom
import os
import pylab
import glob


# 传入文件名显示图片
def show_image_file(fileName):
    ds = dicom.read_file(fileName)
    pylab.imshow(ds.pixel_array, cmap=pylab.cm.bone)
    pylab.show()


# 解析dicom文件
def parse_dicomdir(dicomDir):
    dsdir = dicom.read_dicomdir(dicomDir)
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
    folder_name = dicomDataset.filename.split('\\')[0] + '_export'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    pylab.imshow(dicomDataset.pixel_array, cmap=pylab.cm.bone)
    os.chdir(folder_name)
    picture_name = dicomDataset.filename.replace('\\', '.') + '.jpg'
    pylab.savefig(picture_name, bbox_inches='tight')
    print (dicomDataset.filename.replace('\\', '.') + '.jpg'
           + ' saved to ' + folder_name)
    os.chdir('..')


def traversalDir_FirstDir(path):
    list = []
    if (os.path.exists(path)):
        # 获取该目录下的所有文件或文件夹目录路径
        files = glob.glob(path + '\\*')
        for file in files:
            # 判断该路径下是否是文件夹
            if (os.path.isdir(file)):
                list.append(file)
        return list


# 遍历Dicomdir中的文件并保存
root_path = os.getcwd()
print traversalDir_FirstDir(root_path)
for fileDir in traversalDir_FirstDir(root_path):
    os.chdir(fileDir)
    for singleRecord in parse_dicomdir("DICOMDIR"):
        save_dicom_image(singleRecord)
