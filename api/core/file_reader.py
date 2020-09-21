
import glob
import re

montgomery_data_path = "C:/Users/ms-lu/Desktop/Lucca/IC/DQ/dorothy-image-service/api/core/MontgomerySet/ClinicalReadings/*.txt"
chinese_data_path = ''

montgomery_files = glob.glob(montgomery_data_path)
chinese_files = glob.glob(chinese_data_path)

class XRayImageMetadata:
    def __init__(self, **kwargs):
        self.age = kwargs.get('age', None)
        self.gender = kwargs.get('gender', None)
        self.filename = kwargs.get('filename', None)
        self.report = kwargs.get('report', None)
    def __str__(self):
        return f"<{self.filename}>:{self.gender}-{self.age} years -{self.report}"

class XRayMetadataReader:
    def __init__(self, folder, **kwargs):
        self.xrays = []
        self.folder = folder
        self.filenames = None

    def get_filenames(self):
        self.filenames = glob.glob(self.folder)
        return self.filenames

    def parse_files(self):
        pass

#China

class ChinaXRayMetadataReader(XRayMetadataReader):
    def clear_firstline(self, firstline):
        """
        Normally the first line is something like:
        <gender> <age>yrs

        """
        lowered_case = firstline.lower()
        gender = None
        if 'female' in firstline:
            gender = 'female'
        else:
            if 'male' in firstline:
                gender = 'male'

        try:
            age = int(re.findall('\d+', firstline)[0])
        except IndexError:
            age = None
        return gender, age


    def parse_files(self):
        for file in self.get_filenames():
            with open(file) as txtfile:
                content = txtfile.read()
                lines = content.split('\n')
                lines = [l.strip() for l in lines]
                gender, age = self.clear_firstline(lines[0])
                report = lines[1]
                xray = XRayImageMetadata(gender = gender, age=age, filename=file, report = report)
                print(xray)




china = ChinaXRayMetadataReader(chinese_data_path)

china.parse_files()



#Montgomery
class MontgomeryXRayMetadataReader(XRayMetadataReader):
    """
    Normally the first line is something like:
    <Patient's Sex: (the first letter of the gender, like F or M)>
    the second line:
    <Patient's Age: (number with 3 digits Y)>
    the third line:
    <report>

    """

    def patient_gender(self, firstline):
        gender = None
        if 'F' in firstline:
            gender = 'female'
        elif 'M' in firstline:
            gender = 'male'
        return gender

    def patient_age(self, secondline):
        try:
            age = int(re.findall('\d+', secondline)[0])

        except IndexError:
            age = None
        return age
    def read_files(self):
        DataMontgomery = []
        for file in self.get_filenames():
            with open(file) as txtfile:
                content = txtfile.read()
                lines = content.split('\n')
                lines = [l.strip() for l in lines]
                gender = self.patient_gender(lines[0])
                age = self.patient_age(lines[1])
                report = lines[2]
                xray = XRayImageMetadata(gender = gender, age = age, filename = file, report = report)
                DataMontgomery.append(xray)
        return DataMontgomery



Montgomery = MontgomeryXRayMetadataReader(montgomery_data_path)



DataMontgomery = Montgomery.read_files()



montgomery_general_data_list=[]
for file in DataMontgomery:
    montgomery_general_data_list.append(file)
