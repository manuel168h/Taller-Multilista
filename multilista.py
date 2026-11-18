import csv

class MunicipioNode:
    def __init__(self, codigo, nombre, latitud, longitud):
        self.codigo = codigo
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.siguiente = None

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "latitud": self.latitud,
            "longitud": self.longitud
        }

class DepartamentoNode:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
        self.head_municipio = None
        self.siguiente = None

    def agregar_municipio(self, codigo, nombre, latitud, longitud):
        nuevo_mun = MunicipioNode(codigo, nombre, latitud, longitud)
        if not self.head_municipio:
            self.head_municipio = nuevo_mun
        else:
            actual = self.head_municipio
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_mun

    def to_dict(self):
        municipios = []
        actual = self.head_municipio
        while actual:
            municipios.append(actual.to_dict())
            actual = actual.siguiente
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "municipios": municipios
        }

class MultilistaPais:
    def __init__(self, nombre_pais):
        self.nombre_pais = nombre_pais
        self.head_departamento = None

    def agregar_departamento(self, cod_dpto, nom_dpto, cod_mun, nom_mun, lat, lon):
        dpto_actual = self.head_departamento
        dpto_encontrado = None
        
        while dpto_actual:
            if dpto_actual.codigo == cod_dpto:
                dpto_encontrado = dpto_actual
                break
            dpto_actual = dpto_actual.siguiente
            
        if not dpto_encontrado:
            dpto_encontrado = DepartamentoNode(cod_dpto, nom_dpto)
            if not self.head_departamento:
                self.head_departamento = dpto_encontrado
            else:
                actual = self.head_departamento
                while actual.siguiente:
                    actual = actual.siguiente
                actual.siguiente = dpto_encontrado
                
        dpto_encontrado.agregar_municipio(cod_mun, nom_mun, lat, lon)

    def to_dict(self):
        departamentos = []
        actual = self.head_departamento
        while actual:
            departamentos.append(actual.to_dict())
            actual = actual.siguiente
        return {
            "pais": self.nombre_pais,
            "departamentos": departamentos
        }

def cargar_divipola_desde_csv(ruta_csv):
    pais = MultilistaPais("Colombia")
    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            cod_dpto = fila['Código Departamento'].strip()
            nom_dpto = fila['Nombre Departamento'].strip()
            cod_mun = fila['Código Municipio'].strip()
            nom_mun = fila['Nombre Municipio'].strip()
            
            try:
                lat = float(fila['Latitud'].replace(',', '.'))
                lon = float(fila['longitud'].replace(',', '.'))
            except ValueError:
                lat = 0.0
                lon = 0.0
                
            pais.agregar_departamento(cod_dpto, nom_dpto, cod_mun, nom_mun, lat, lon)
            
    return pais