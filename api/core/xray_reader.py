import glob
import re


arquivos = "C:/Users/ms-lu/Desktop/Lucca/IC/DQ/dorothy-image-service/api/core/MontgomerySet/ClinicalReadings/*.txt"

files = glob.glob(arquivos)




class XRayImageMetadata:
    def __init__(self, **kwargs):
        self.data = self
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
        DataMontgomery_list = []
        for file in self.get_filenames():
            with open(file) as txtfile:
                content = txtfile.read()
                lines = content.split('\n')
                lines = [l.strip() for l in lines]
                gender = self.patient_gender(lines[0])
                age = self.patient_age(lines[1])
                report = lines[2]
                xray = XRayImageMetadata(gender = gender, age = age, filename = file, report = report)
                DataMontgomery_list.append(xray)
        return DataMontgomery_list





Montgomery = MontgomeryXRayMetadataReader(arquivos)



DataMontgomery = Montgomery.read_files()

lista_dados = []
for file in DataMontgomery:
    lista_dados.append(file)

lista_filename = []
for file in DataMontgomery:
    for i in range(len(lista_dados)):
        lista_filename.append(str(lista_dados[i].filename))
