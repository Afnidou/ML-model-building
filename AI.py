import operator    
import OCC.GProp
import OCC.BRepGProp
import ifcopenshell
import ifcopenshell.geom
import numpy

# Couleurs RGBA pour la visualisation des éléments
RED, GRAY = (1,0,0,1), (0.6, 0.6, 0.6, 0.1)
ifc_file = ifcopenshell.open("Duplex_A_20110907_optimized.ifc")   #IFC FILLE FORMAT"FORMAT DE DESCRIPTION DES DONNEES 
# paramètre pour spécifier l’usage of pyOCC

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)
# quelque fonctions aide pour maper la liste des murs
def create_shape(elem):
 return ifcopenshell.geom.create_shape(settings, elem)
def calc_volume(s):
 props = OCC.GProp.GProp_GProps()
 OCC.BRepGProp.brepgprop_VolumeProperties(s.geometry, props)
 return props.Mass()

def calc_area(s):
 props = OCC.GProp.GProp_GProps()
 OCC.BRepGProp.brepgprop_SurfaceProperties(s.geometry, props)
 return props.Mass()

def normalize(li):
 mean, std = numpy.mean(li), numpy.std(li)
 return map(lambda v: abs(v-mean) / std, li)
# obtenir une liste des murs depuis le modèle
walls = ifc_file.by_type("IfcWall")
# créer une géométrie pour les mures
shapes = list(map(create_shape, walls))
# Calculer leur volume
volumes = map(calc_volume, shapes)
# calculer leur surface 
areas = map(calc_area, shapes)
# Composer une fonctionnalité d’après les deaux mesures
feature = normalize(map(operator.div, areas, volumes))
# Initialiser le viseur
pyocc_viewer = ifcopenshell.geom.utils.initialize_display()
# boucler les pairs de fonctionnalité
# valeur et géométrie correspondante
for d, s in sorted(zip(feature, shapes)):
 c = RED if d > 1. else GRAY
 ifcopenshell.geom.utils.display_shape(s, clr=c)

# adapter le model a la vue
pyocc_viewer.FitAll()
# permettre l’interaction avec l’utilisateur
ifcopenshell.geom.utils.main_loop()
