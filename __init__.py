###########################################################
#
#                   INICIO
#
###########################################################

# Información del Add-on registrada en Blender (metadatos principales)
bl_info = {
    "name": "INDI RIGGING SYSTEM",
    "author": "cesar andre chavez herrera",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "Properties > Data (Armature)",
    "description": "Creacion de un rigging simple para animaciones low poly con soporte para captura de movimiento con ipi mocap.",
    "category": "Rigging",
}


import bpy
from mathutils import Vector
import math
# LISTA DE PREFIJOS 

PREFIJO_HUESOS_DEFORMACION = "DF."
PREFIJO_HUESOS_FK          = "FK."
PREFIJO_HUESOS_IK          = "IK."
PREFIJO_HUESOS_API         = "IPI."

PREFIJO_HUESOS_FIJADOR     = "PIN."
PREFIJO_HUESOS_ACCESORIOS  = "PROP."
PREFIJO_HUESOS_CABELLO     = "HAIR."
PREFIJO_HUESOS_ROPA        = "ROPA."

PREFIJO_HUESO_IK_CONTROL   = "IK.CONTROL." 
# NOMECLATURA DE HUESOS 

ZONA_CABEZA   = "CABEZA."
ZONA_CEJA     = "CEJAS."
ZONA_OJOS     = "OJOS."
ZONA_BOCA     = "BOCA."

ZONA_ESPALDA  = "ESPALDA."

ZONA_BRAZO_L  = "BRAZO_L."
ZONA_MANO_L   = "MANO_L."
ZONA_PIERNA_L = "PIERNA_L."
ZONA_PIE_L    = "PIE_L."

ZONA_BRAZO_R  = "BRAZO_R."
ZONA_MANO_R   = "MANO_R."
ZONA_PIERNA_R = "PIERNA_R."
ZONA_PIE_R    = "PIE_R."

# propiedades 

PROP_MOSTRAR    = "mostrar_"
PROP_INFLUENCIA = "influencia_"

# LISTADO DE MAPEO DE NOMBRE DE HUESOS SIN PREFIJO CON LAS PROPIEDADES

MAPEO_NOMBRE_HUESOS_PROPIEDAD_MOSTRAR = {
    
    ZONA_CABEZA : PROP_MOSTRAR + ZONA_CABEZA[:-1].lower(),
    ZONA_CEJA   : PROP_MOSTRAR + ZONA_CEJA  [:-1].lower(),
    ZONA_OJOS   : PROP_MOSTRAR + ZONA_OJOS  [:-1].lower(),
    ZONA_BOCA   : PROP_MOSTRAR + ZONA_BOCA  [:-1].lower(),
    
    ZONA_ESPALDA : PROP_MOSTRAR + ZONA_ESPALDA [:-1].lower(),
    
    ZONA_BRAZO_L  : PROP_MOSTRAR + ZONA_BRAZO_L  [:-1].lower(),
    ZONA_MANO_L   : PROP_MOSTRAR + ZONA_MANO_L   [:-1].lower(),
    ZONA_PIERNA_L : PROP_MOSTRAR + ZONA_PIERNA_L [:-1].lower(),
    ZONA_PIE_L    : PROP_MOSTRAR + ZONA_PIE_L    [:-1].lower(),
        
    ZONA_BRAZO_R  : PROP_MOSTRAR + ZONA_BRAZO_R  [:-1].lower(),
    ZONA_MANO_R   : PROP_MOSTRAR + ZONA_MANO_R   [:-1].lower(),
    ZONA_PIERNA_R : PROP_MOSTRAR + ZONA_PIERNA_R [:-1].lower(),
    ZONA_PIE_R    : PROP_MOSTRAR + ZONA_PIE_R    [:-1].lower()

} 

# LISTADO DE MAPEO DE NOMBRE DE HUESOS SIN PREFIJO CON LAS PROPIEDADES

MAPEO_NOMBRE_HUESOS_PROPIEDAD_INFLUENCIA = {
    
    ZONA_CABEZA : PROP_INFLUENCIA + ZONA_CABEZA[:-1].lower(),
    ZONA_CEJA   : PROP_INFLUENCIA + ZONA_CEJA  [:-1].lower(),
    ZONA_OJOS   : PROP_INFLUENCIA + ZONA_OJOS  [:-1].lower(),
    ZONA_BOCA   : PROP_INFLUENCIA + ZONA_BOCA  [:-1].lower(),
    
    ZONA_ESPALDA : PROP_INFLUENCIA + ZONA_ESPALDA [:-1].lower(),
    
    ZONA_BRAZO_L  : PROP_INFLUENCIA + ZONA_BRAZO_L  [:-1].lower(),
    ZONA_MANO_L   : PROP_INFLUENCIA + ZONA_MANO_L   [:-1].lower(),
    ZONA_PIERNA_L : PROP_INFLUENCIA + ZONA_PIERNA_L [:-1].lower(),
    ZONA_PIE_L    : PROP_INFLUENCIA + ZONA_PIE_L    [:-1].lower(),
        
    ZONA_BRAZO_R  : PROP_INFLUENCIA + ZONA_BRAZO_R  [:-1].lower(),
    ZONA_MANO_R   : PROP_INFLUENCIA + ZONA_MANO_R   [:-1].lower(),
    ZONA_PIERNA_R : PROP_INFLUENCIA + ZONA_PIERNA_R [:-1].lower(),
    ZONA_PIE_R    : PROP_INFLUENCIA + ZONA_PIE_R    [:-1].lower()

}

###########################################################
#
#     PROPIEDADES A EXPONER
#
###########################################################

# Entradas de creacion de sistema 

# Función aux. para instanciar propiedades numéricas tipo slider (porcentaje de 0.0 a 1.0)
def crear_propiedad_sliders(Nombre, descripcion="",update =None):
    return bpy.props.FloatProperty(
        name=Nombre,
        description=descripcion,
        default=1.0, min=0.0, max=1.0, step=0.01,
        subtype='PERCENTAGE',
        update=update
    )
    pass

# Función aux. para instanciar propiedades booleanas (interruptores On/Off)
def crear_propiedad_switch(Nombre, descripcion = "",default = True,update = None):
    return bpy.props.BoolProperty(
        name=Nombre,
        description=descripcion,
        default=default,
        update=update
    )
    pass
######################################################
#           Funciones asociada al cambio de propiedades 
####################################################

# Callback que sincroniza la visibilidad de todas las partes al cambiar el interruptor principal FK
def Actualizar_mostrar(self,context):
    estado = self.mostrar
    self.mostrar_cabeza  = estado
    self.mostrar_cejas   = estado
    self.mostrar_ojos    = estado
    self.mostrar_boca    = estado
    self.mostrar_espalda = estado
    
    self.mostrar_brazo_l = estado
    self.mostrar_mano_l  = estado
    self.mostrar_brazo_r = estado
    self.mostrar_mano_r  = estado
    
    self.mostrar_pierna_l= estado
    self.mostrar_pie_l   = estado
    self.mostrar_pierna_r= estado
    self.mostrar_pie_r   = estado 
    pass

# Callback que propaga el nivel de influencia maestro a todos los sub-grupos de huesos FK
def Actualizar_influencia(self,context):
    
    influencia = self.influencia_maestra
    
    self.influencia_cabeza   = influencia
    self.influencia_cejas    = influencia
    self.influencia_ojos     = influencia
    self.influencia_boca     = influencia
    self.influencia_espalda  = influencia
    
    self.influencia_brazo_l  = influencia
    self.influencia_mano_l   = influencia
    self.influencia_pierna_l = influencia
    self.influencia_pie_l    = influencia
    
    self.influencia_brazo_r  = influencia
    self.influencia_mano_r   = influencia
    self.influencia_pierna_r = influencia
    self.influencia_pie_r    = influencia
    pass



######################################################
#           De claracion de propiedades 
####################################################

# propiedades generales: Opciones globales para combinar sistemas generados con la armadura base
class ARMATURE_GENERAL_PROPIEDADES(bpy.types.PropertyGroup):
    
    # propiedad ACTIVAR COMBINAR el esqueleto FK con el esqueleto base
    combinar_FK: crear_propiedad_switch(
        "Combinar IK",
        "Habilita que despues de crear el sistema IK lo combine con el esqueleto base"
        )
    
    # propiedad ACTIVAR COMBINAR el esqueleto IK con el esqueleto base
    combinar_IK : crear_propiedad_switch(
        "Combinar IK",
        "Habilita que despues de crear el sistema IK lo combine con el esqueleto base"
        )
    
    # propiedad ACTIVAR COMBINAR el esqueleto IPI con el esqueleto base
    combinar_IPI : crear_propiedad_switch(
        "Combinar IPI",
        "Habilita que despues de crear el sistema Mocap ipi software lo combine con el esqueleto base"
        )
    pass


# propiedades FK: Grupo de propiedades para visibilidad e influencia de cada zona anatómica
class ARMATURE_SISTEMA_FK_PROPIEDADES(bpy.types.PropertyGroup):
    
    # muestra todas el esqueleto del sistema FK
    mostrar             : crear_propiedad_switch("Mostrar FK",
                            update= Actualizar_mostrar)
    influencia_maestra  : crear_propiedad_sliders("Influencia FK",
                            update= Actualizar_influencia)
    
    # cabeza 
    mostrar_cabeza       : crear_propiedad_switch("Mostrar cabeza FK")
    influencia_cabeza    : crear_propiedad_sliders("Influencia cabeza FK")
    
    mostrar_cejas        : crear_propiedad_switch("Mostrar cejas FK")
    influencia_cejas     : crear_propiedad_sliders("Influencia cejas FK")
    
    mostrar_ojos        : crear_propiedad_switch("Mostrar ojos FK")
    influencia_ojos     : crear_propiedad_sliders("Influencia ojos FK")
    
    mostrar_boca        : crear_propiedad_switch("Mostrar boca FK")
    influencia_boca     : crear_propiedad_sliders("Influencia boca FK")
    
    #espalda
    mostrar_espalda      : crear_propiedad_switch("Mostrar Espalda FK")
    influencia_espalda   : crear_propiedad_sliders( "Influencia Espalda FK")
    
    #brazo L
    mostrar_brazo_l     : crear_propiedad_switch("Mostrar Brazo L FK")
    influencia_brazo_l   : crear_propiedad_sliders( "Influencia Brazo L FK")
    
    #Mano L
    mostrar_mano_l       : crear_propiedad_switch("Mostrar Mano L FK")
    influencia_mano_l    : crear_propiedad_sliders( "Influencia Mano L FK")
    
    #brazo R
    mostrar_brazo_r      : crear_propiedad_switch("Mostrar Brazo R FK")
    influencia_brazo_r   : crear_propiedad_sliders( "Influencia Brazo R FK")
    
    #Mano R
    mostrar_mano_r       : crear_propiedad_switch("Mostrar Mano R FK")
    influencia_mano_r    : crear_propiedad_sliders( "Influencia Mano R FK")
    
    #Pierna L
    mostrar_pierna_l      : crear_propiedad_switch("Mostrar pierna L FK")
    influencia_pierna_l   : crear_propiedad_sliders( "Influencia Brazo L FK")
    
    #Pierna L
    mostrar_pie_l      : crear_propiedad_switch("Mostrar Pie L FK")
    influencia_pie_l   : crear_propiedad_sliders( "Influencia Pie L FK")
    
    #Pierna r
    mostrar_pierna_r      : crear_propiedad_switch("Mostrar pierna R FK")
    influencia_pierna_r   : crear_propiedad_sliders( "Influencia Brazo R FK")
    
    #Pierna r
    mostrar_pie_r      : crear_propiedad_switch("Mostrar Pie R FK")
    influencia_pie_r   : crear_propiedad_sliders( "Influencia Pie R FK")
    pass
    
# propiedades FK: Grupo de propiedades para visibilidad e influencia de cada zona anatómica
class ARMATURE_SISTEMA_IK_PROPIEDADES(bpy.types.PropertyGroup):
    
    mostrar_controles   : crear_propiedad_switch("Mostrar Controles")
    mostrar             : crear_propiedad_switch("Mostrar Huesos IK",
                            update= Actualizar_mostrar)
                            
    influencia_maestra  : crear_propiedad_sliders("Influencia IK",
                            update= Actualizar_influencia)
    
    # cabeza 
    mostrar_cabeza       : crear_propiedad_switch("Mostrar cabeza IK")
    influencia_cabeza    : crear_propiedad_sliders("Influencia cabeza IK")
    
    mostrar_cejas        : crear_propiedad_switch("Mostrar cejas IK")
    influencia_cejas     : crear_propiedad_sliders("Influencia cejas IK")
    
    mostrar_ojos        : crear_propiedad_switch("Mostrar ojos IK")
    influencia_ojos     : crear_propiedad_sliders("Influencia ojos IK")
    
    mostrar_boca        : crear_propiedad_switch("Mostrar boca IK")
    influencia_boca     : crear_propiedad_sliders("Influencia boca IK")
    
    #espalda
    mostrar_espalda      : crear_propiedad_switch("Mostrar Espalda IK")
    influencia_espalda   : crear_propiedad_sliders( "Influencia Espalda IK")
    
    #brazo L
    mostrar_brazo_l     : crear_propiedad_switch("Mostrar Brazo L IK")
    influencia_brazo_l   : crear_propiedad_sliders( "Influencia Brazo L IK")
    
    #Mano L
    mostrar_mano_l       : crear_propiedad_switch("Mostrar Mano L IK")
    influencia_mano_l    : crear_propiedad_sliders( "Influencia Mano L IK")
    
    #brazo R
    mostrar_brazo_r      : crear_propiedad_switch("Mostrar Brazo R IK")
    influencia_brazo_r   : crear_propiedad_sliders( "Influencia Brazo R IK")
    
    #Mano R
    mostrar_mano_r       : crear_propiedad_switch("Mostrar Mano R IK")
    influencia_mano_r    : crear_propiedad_sliders( "Influencia Mano R IK")
    
    #Pierna L
    mostrar_pierna_l      : crear_propiedad_switch("Mostrar pierna L IK")
    influencia_pierna_l   : crear_propiedad_sliders( "Influencia Brazo L IK")
    
    #Pierna L
    mostrar_pie_l      : crear_propiedad_switch("Mostrar Pie L IK")
    influencia_pie_l   : crear_propiedad_sliders( "Influencia Pie L IK")
    
    #Pierna r
    mostrar_pierna_r      : crear_propiedad_switch("Mostrar pierna R IK")
    influencia_pierna_r   : crear_propiedad_sliders( "Influencia Brazo R IK")
    
    #Pierna r
    mostrar_pie_r      : crear_propiedad_switch("Mostrar Pie R IK")
    influencia_pie_r   : crear_propiedad_sliders( "Influencia Pie R IK")

    pass

# propiedades FK: Grupo de propiedades para visibilidad e influencia de cada zona anatómica
class ARMATURE_SISTEMA_IPI_PROPIEDADES(bpy.types.PropertyGroup):
    

    mostrar             : crear_propiedad_switch("Mostrar IPI",
                            update= Actualizar_mostrar)
                            
    influencia_maestra  : crear_propiedad_sliders("Influencia IPI",
                            update= Actualizar_influencia)
    
    # cabeza 
    mostrar_cabeza       : crear_propiedad_switch("Mostrar cabeza IPI")
    influencia_cabeza    : crear_propiedad_sliders("Influencia cabeza IPI")
    
    mostrar_cejas        : crear_propiedad_switch("Mostrar cejas IPI")
    influencia_cejas     : crear_propiedad_sliders("Influencia cejas IPI")
    
    mostrar_ojos        : crear_propiedad_switch("Mostrar ojos IPI")
    influencia_ojos     : crear_propiedad_sliders("Influencia ojos IPI")
    
    mostrar_boca        : crear_propiedad_switch("Mostrar boca IPI")
    influencia_boca     : crear_propiedad_sliders("Influencia boca IPI")
    
    #espalda
    mostrar_espalda      : crear_propiedad_switch("Mostrar Espalda IPI")
    influencia_espalda   : crear_propiedad_sliders( "Influencia Espalda IPI")
    
    #brazo L
    mostrar_brazo_l     : crear_propiedad_switch("Mostrar Brazo L IPI")
    influencia_brazo_l   : crear_propiedad_sliders( "Influencia Brazo L IPI")
    
    #Mano L
    mostrar_mano_l       : crear_propiedad_switch("Mostrar Mano L IPI")
    influencia_mano_l    : crear_propiedad_sliders( "Influencia Mano L IPI")
    
    #brazo R
    mostrar_brazo_r      : crear_propiedad_switch("Mostrar Brazo R IPI")
    influencia_brazo_r   : crear_propiedad_sliders( "Influencia Brazo R IPI")
    
    #Mano R
    mostrar_mano_r       : crear_propiedad_switch("Mostrar Mano R IPI")
    influencia_mano_r    : crear_propiedad_sliders( "Influencia Mano R IPI")
    
    #Pierna L
    mostrar_pierna_l      : crear_propiedad_switch("Mostrar pierna L IPI")
    influencia_pierna_l   : crear_propiedad_sliders( "Influencia Brazo L IPI")
    
    #Pierna L
    mostrar_pie_l      : crear_propiedad_switch("Mostrar Pie L IPI")
    influencia_pie_l   : crear_propiedad_sliders( "Influencia Pie L IPI")
    
    #Pierna r
    mostrar_pierna_r      : crear_propiedad_switch("Mostrar pierna R IPI")
    influencia_pierna_r   : crear_propiedad_sliders( "Influencia Brazo R IPI")
    
    #Pierna r
    mostrar_pie_r      : crear_propiedad_switch("Mostrar Pie R IPI")
    influencia_pie_r   : crear_propiedad_sliders( "Influencia Pie R IPI")

    pass
######################################################
#          Enlazamiento de propiedades con objeto 
####################################################


# clase en cargada de guardar todas las propiedades dentro de bpy.types.Armature.control_rig 
class ARMATURE_CONTROLADOR_PROPIEDADES(bpy.types.PropertyGroup):
    
    crear_prop  : bpy.props.PointerProperty(type = ARMATURE_GENERAL_PROPIEDADES)
    fk_prop     : bpy.props.PointerProperty(type = ARMATURE_SISTEMA_FK_PROPIEDADES)
    ik_prop     : bpy.props.PointerProperty(type = ARMATURE_SISTEMA_IK_PROPIEDADES)
    ipi_prop     : bpy.props.PointerProperty(type = ARMATURE_SISTEMA_IPI_PROPIEDADES)
    pass

######################################################
#           ACTUALIZACION en animacion
####################################################


###########################################################################################
#            Registro de propiedades 
##########################################################################################

# vinculas las propiedades: Inyecta la estructura de datos dentro de las armaduras en Blender
def registrar_propiedades():
    
    bpy.types.Armature.control_rig = bpy.props.PointerProperty(type = ARMATURE_CONTROLADOR_PROPIEDADES )
    pass

# desvincular la propiedades: Remueve la propiedad control_rig al desactivar el complemento
def unregister_properties():
    
    if hasattr(bpy.types.Armature, "control_rig"):
        del bpy.types.Armature.control_rig
    pass
        
###########################################################
#
#     BOTONES
#
###########################################################

# Crea y configura una variable dentro del driver especificado
def crear_var_driver(driver,
                    nombre,
                    data_path,
                    id_target,
                    id_type = "ARMATURE"):
    
    var = driver.variables.new()
    var.name = nombre
    var.type = 'SINGLE_PROP'
    var.targets[0].id_type = id_type
    var.targets[0].id = id_target
    var.targets[0].data_path = f"{data_path+nombre}"
    return var

# reutilizar variable: Conecta la propiedad de la UI con la propiedad de un hueso/constraint usando drivers
def vincular_driver(
                prop_nombre, # nombre de la variable expuerta
                bone,        # hueso a conectar la propiedad
                data_path,   # ruta_variable expuerta
                armature,    # objeto que tiene la variable 
                prop_maestra = "mostrar", #nombre de la variable expuerta
                contectar_prop = "hide",  #nombre de la propiedad a conectar
                ajuste_expresion = "not"    
                    ):
    
    driver = bone.driver_add(contectar_prop).driver
    driver.type = "SCRIPTED"
    
    if prop_nombre != "":
        crear_var_driver(driver,prop_maestra,data_path,armature) # crea la variable maestra
        crear_var_driver(driver,prop_nombre,data_path,armature)    # crea la variable especifica
        
        driver.expression = ajuste_expresion+f"({prop_maestra}*{prop_nombre})"
    else:
        crear_var_driver(driver,prop_maestra,data_path,armature) 
        driver.expression = ajuste_expresion+f"({prop_maestra})"               
    pass



# eliminacion de constraints
def eliminar_constraint(
                        nombre_constraint, # nombre del contraints a borrar
                        esqueleto,         # esqueleto a borrar las cosas 
                        prefijo = "DF."    # prefijo del esqueleto a borrar 
                        ):
        
    # Remueve la restricción de rotación FK de los huesos deformadores
    for bone in esqueleto.pose.bones:   
           
        if bone.name.startswith(prefijo):
           for constraint in list(bone.constraints):
                if constraint.name.startswith(nombre_constraint):
                    bone.constraints.remove(constraint)
            #if nombre_constraint in bone.constraints:
                
                #constraint_a_borrar = bone.constraints[nombre_constraint]
                #bone.constraints.remove(constraint_a_borrar)
                
            
    pass


# elimna todos los contraints
def eliminar_todo_constraints( self,
                            esqueleto,
                            prefijo="DF."
                            ):
    
    #for bone in esqueleto.pose.bones:      
        #if bone.name.startswith(prefijo):
        #bone.constraints.clear()
        #for contraint in list(bone.constraints):
            #bone.constraints.remove(contraint)
            
    bpy.ops.pose.select_all(action='DESELECT')  
    for bone in esqueleto.pose.bones:    
        for constraint in list(bone.constraints):
            #self.report({"INFO"},f"{constraint.name}"
            #constraint_a_borrar = bone.constraints[contraint]
            bone.constraints.remove(constraint)
                           
    pass


# elimina todos los drivers suelto de un esqueleto
def eliminar_drivers_rotos_esqueleto(
                                    esqueleto
                                    ):
    #if not (esqueleto and esqueleto.animation_data and esqueleto.animation_data.drivers):
    #    return
    
    # actualiza los drivers 
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    
    anim_data = esqueleto.animation_data    
    
    # evalua los drivers de los huesos   
    for fcurve in list(anim_data.drivers):
        
        # driver invalido o error eliminado
        if not fcurve.driver.is_valid:
            
            anim_data.drivers.remove(fcurve)
        else:
            
            # eliminacion de drivers que fueron desvinculado al hueso matris
            eliminar = False
            driver = fcurve.driver
            
            # si su propiedad prop esta vacia entonces se guarda y se borra despues 
            for variable in driver.variables:
                for target in variable.targets:
                    if target.id is None:
                        eliminar = True            
                pass
            if eliminar:
                anim_data.drivers.remove(fcurve)
                   #self.report({"INFO"},f"driver eliminado del hueso {bone}")
    
    bpy.context.view_layer.update()
    pass


#borra hueso segun un prefijo
def borrar_huesos_prefijo(
                esqueleto,
                prefijo,
                distinto = False
                ):
    for bone in esqueleto.data.edit_bones:
        
        if bone.name.startswith(prefijo) == (not distinto):
            esqueleto.data.edit_bones.remove(bone)
            pass
    
    pass                                        
                        
def selecionar_huesos(
                    esqueleto,
                    prefijo = "DF.",
                    selecionar = True):
                        
    bpy.ops.armature.select_all(action='DESELECT')
     
    for bone in esqueleto.data.edit_bones:
        if bone.name.startswith(prefijo):
            bone.select = selecionar
            bone.select_head = selecionar
            bone.select_tail = selecionar
                               
    pass

def renombrar_prefijo_huesos(
                    esqueleto,
                    prefijo_actual = "DF.",
                    prefijo_nuevo  = "FK.",
                    deform_bone    = False
                    ):
                        
    bpy.ops.armature.select_all(action='DESELECT')
     
    for bone in esqueleto.data.edit_bones:
        if bone.name.startswith(prefijo_actual):
            bone.name = prefijo_nuevo + bone.name[3:]
            bone.use_deform = deform_bone
                               
    pass

#cambia el color de los huesos 
def cambiar_color_huesos(
                        esqueleto,
                        prefijo,
                        color_normal,
                        color_select,
                        color_activo,
                        ):
    bpy.ops.armature.select_all(action='DESELECT')
     
    for bone in esqueleto.data.edit_bones:
        if bone.name.startswith(prefijo):
                bone.color.palette = "CUSTOM"
                bone.color.custom.normal = color_normal
                bone.color.custom.select = color_select
                bone.color.custom.active = color_activo
                               
    pass
# sistema Fk: Operador encargado de duplicar la armadura base y estructurar los huesos FK
class OBJECT_OT_Generar_sistema_FK(bpy.types.Operator): 
    """Crea al esqueleto selecionado su sistema de control FK"""
    
    bl_idname = "object.generar_fk" 
    bl_label = "Generar FK" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        armature  = context.object.data
        fk        = armature.control_rig
        combinar  = fk.crear_prop.combinar_FK 
        
        
         
        bpy.ops.object.mode_set(mode='OBJECT')
        DF_ESQUELETO = bpy.context.active_object
        bpy.ops.object.select_all(action='DESELECT')
        
        #selecionamos el esqueleto base 
        DF_SELECTION  = bpy.data.objects.get(DF_ESQUELETO.name)
        bpy.context.view_layer.objects.active = DF_SELECTION
        DF_SELECTION.select_set(True)
        
        bpy.ops.object.duplicate(linked=False)
        
        FK_esqueleto = bpy.context.active_object
        #FK_esqueleto.location.x += 1
        FK_esqueleto.name = "FK"
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        # borra todo los huesos que no sean deformacion                     
        borrar_huesos_prefijo(FK_esqueleto,PREFIJO_HUESOS_DEFORMACION,True) 

        renombrar_prefijo_huesos(FK_esqueleto,PREFIJO_HUESOS_DEFORMACION,PREFIJO_HUESOS_FK)
                                
        cambiar_color_huesos(FK_esqueleto,PREFIJO_HUESOS_FK,
                            (0,0.4,0.0), # verde oscuro
                            (1.0,0.0,0.0), # rojo
                            (0.0,1.0,0.0)  # verde
                            )
        
        #limpieza 
        bpy.ops.object.mode_set(mode='POSE')
        eliminar_todo_constraints(self,FK_esqueleto,PREFIJO_HUESOS_IK)
        eliminar_drivers_rotos_esqueleto(FK_esqueleto)
        
        borrar_ik = False
        
        if not len(FK_esqueleto.data.bones) == 0 :
            data_path = "control_rig.fk_prop."
            
            for bone in FK_esqueleto.pose.bones:
                for prefijo, propiedad in MAPEO_NOMBRE_HUESOS_PROPIEDAD_MOSTRAR.items():
                    
                    if bone.name.startswith(PREFIJO_HUESOS_FK+prefijo):
                        vincular_driver(propiedad,bone,data_path,armature)
                        
                        
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = DF_ESQUELETO
            bpy.ops.object.mode_set(mode='POSE')
            
            for bone in DF_ESQUELETO.pose.bones:
                for prefijo, propiedad in MAPEO_NOMBRE_HUESOS_PROPIEDAD_INFLUENCIA.items():
                    df_prefijo = PREFIJO_HUESOS_DEFORMACION+prefijo
                    
                    if bone.name.startswith(df_prefijo):
                        constraint_hueso = bone.constraints.new(type = "COPY_ROTATION")
                        constraint_hueso.name = "FK_ROTATION"
                        constraint_hueso.target = FK_esqueleto
                        constraint_hueso.subtarget = PREFIJO_HUESOS_FK + bone.name[3:]
                        
                        vincular_driver(propiedad,
                                            constraint_hueso,
                                            data_path,armature,
                                            "influencia_maestra",
                                            "influence","")
                        
                        pass
                    
                pass
                context.object.update_tag(refresh={'DATA'})
        else:
            # Si no hay huesos generados, elimina la copia vacía y vuelve a seleccionar el original

            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.objects.active = FK_esqueleto
            FK_esqueleto.select_set(True)
            bpy.ops.object.delete(use_global=False)
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = DF_ESQUELETO
            DF_ESQUELETO.select_set(True)
            borrar_ik = True
        
        
        if combinar:
            if not borrar_ik:
                bpy.ops.object.mode_set(mode='OBJECT')
                
                fk_join = bpy.data.objects.get(FK_esqueleto.name)
                df_join = bpy.data.objects.get(DF_ESQUELETO.name)
                
                df_join.select_set(True)
                fk_join.select_set(True)
                
                bpy.context.view_layer.objects.active = df_join
                bpy.ops.object.join()
            else:
                self.report({"INFO"},"Sistema IK No creado")
        
        else:
            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = DF_ESQUELETO
            DF_ESQUELETO.select_set(True)
            
            self.report({"INFO"},"Se combino el esqueleto IK con el esqueleto DF")
            pass
    
        return {'FINISHED'}






# sistema IK: Operador reservado para la generación del sistema Cinemática Inversa
class OBJECT_OT_Generar_sistema_IK(bpy.types.Operator): 
    """Crea al esqueleto selecionado su sistema de control FK"""
    
    bl_idname = "object.generar_ik" 
    bl_label = "Generar IK" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context):
        
        # esqueleto principal
        armature  = context.object.data
        ik        = armature.control_rig
        combinar  = ik.crear_prop.combinar_IK  
        
        bpy.ops.object.mode_set(mode='OBJECT')
        DF_ESQUELETO = bpy.context.active_object
        
        bpy.ops.object.select_all(action='DESELECT')
        
        DF_SELECTION  = bpy.data.objects.get(DF_ESQUELETO.name)
        
        bpy.context.view_layer.objects.active = DF_SELECTION
        DF_SELECTION.select_set(True)
        
        bpy.ops.object.duplicate(linked=False)
        
        IK_esqueleto = bpy.context.active_object
        #IK_esqueleto.location.x -= 1
        IK_esqueleto.name = "IK"
        
        bpy.ops.object.mode_set(mode='EDIT')
        borrar_huesos_prefijo(IK_esqueleto,PREFIJO_HUESOS_DEFORMACION,True)
        renombrar_prefijo_huesos(IK_esqueleto,PREFIJO_HUESOS_DEFORMACION, PREFIJO_HUESOS_IK)
        cambiar_color_huesos(IK_esqueleto,PREFIJO_HUESOS_IK,
                            (1.0,0.9,0.6), # naranja
                            (1.0,0.0,0.0), # rojo
                            (0.0,1.0,0.0)  # verde
                            )
        # limpieza                  
        bpy.ops.object.mode_set(mode='POSE')
        eliminar_todo_constraints(self,IK_esqueleto,PREFIJO_HUESOS_IK)
        eliminar_drivers_rotos_esqueleto(IK_esqueleto)
        
        borrar_ik = False
        
        if not len(IK_esqueleto.data.bones) == 0 :
            data_path = "control_rig.ik_prop."
            
            for bone in IK_esqueleto.pose.bones:
                for prefijo, propiedad in MAPEO_NOMBRE_HUESOS_PROPIEDAD_MOSTRAR.items():
                    
                    if bone.name.startswith(PREFIJO_HUESOS_IK+prefijo):
                        vincular_driver(propiedad,bone,data_path,armature)
                
                pass
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = DF_ESQUELETO
            bpy.ops.object.mode_set(mode='POSE')
            
            for bone in DF_ESQUELETO.pose.bones:
                for prefijo, propiedad in MAPEO_NOMBRE_HUESOS_PROPIEDAD_INFLUENCIA.items():
                    df_prefijo = PREFIJO_HUESOS_DEFORMACION+prefijo
                    
                    if bone.name.startswith(df_prefijo):
                        constraint_hueso = bone.constraints.new(type = "COPY_ROTATION")
                        constraint_hueso.name = "IK_ROTATION"
                        constraint_hueso.target = IK_esqueleto
                        constraint_hueso.subtarget = PREFIJO_HUESOS_IK + bone.name[3:]
                        
                        vincular_driver(propiedad,
                                            constraint_hueso,
                                            data_path,
                                            armature,
                                            "influencia_maestra",
                                            "influence","")
                        
                        pass
                
                pass
            
            ########################################################
            #creacion de sistema IK 
            
            # paleta de colores
            color_normal = (0.7,0.0,0.0)
            color_select = (0.0,1.0,1.0)
            color_activo = (0.0,1.0,0.0)
            
            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            
            # volvemos a selecionar el esqueleto de IK
            bpy.context.view_layer.objects.active = IK_esqueleto
            
            
            #######################################################################
            # Cabezaaa
            bpy.ops.object.mode_set(mode='EDIT')
            
            hueso_cabeza_name = "IK.CABEZA.cabeza"                              # nombre del hueso de la cabeza
            selecionar_huesos(IK_esqueleto,PREFIJO_HUESOS_IK,False)             # des seleciona todos los huesos en modo edition
            hueso_cabeza = IK_esqueleto.data.edit_bones.get(hueso_cabeza_name) # busca el hueso de la cabeza
            
            if not hueso_cabeza == None: # si encuentra el hueso 
                
                # duplica la cabeza 
                control_cabeza = IK_esqueleto.data.edit_bones.new(PREFIJO_HUESO_IK_CONTROL+"cabeza")

                mover_hueso         = Vector((0.0,-0.5,0.0))          # define cuanto se desplazara
                control_cabeza.head = hueso_cabeza.head + mover_hueso # mueve la cabeza del hueso
                control_cabeza.tail = hueso_cabeza.tail + mover_hueso # mueve la cola del hueso
                
                # configuracion del hueso 
                control_cabeza.use_connect  = False
                control_cabeza.use_deform   = False
                control_cabeza.parent       = None
                #control_cabeza.display_type = "BBONE"
                
                
                # antes de pasar a modo pose obtenemos nombre del hueso duplicado
                nombre_hueso = control_cabeza.name
                bpy.ops.object.mode_set(mode='POSE')
                
                # se obtiene los hueso de control y el uso que lo aplicara 
                control_cabeza_pose = IK_esqueleto.pose.bones.get(nombre_hueso)
                cabeza_pose         = IK_esqueleto.pose.bones.get(hueso_cabeza_name)
                
                # conecta el control con el boton mostrar 
                vincular_driver(
                                "",
                                control_cabeza_pose,
                                data_path,
                                armature,
                                "mostrar_controles",
                                "hide","not")
                
                # añade un contraitns                
                constraint_hueso = cabeza_pose.constraints.new(type = "TRACK_TO")
                constraint_hueso.name       = "control cabeza"
                constraint_hueso.target     = IK_esqueleto
                constraint_hueso.subtarget  = control_cabeza_pose.name
                constraint_hueso.track_axis = "TRACK_Z"
                
                
                
            else:
                self.report({"INFO"},"Hueso de la cabeza no encontrado") 
                
            
            
            
            
            ##############################################################
            # brazo
            
            bpy.ops.object.mode_set(mode='EDIT')
            
            hueso_mano_r_name = "IK.MANO_R.mano.R"                              # nombre del hueso de la cabeza
            selecionar_huesos(IK_esqueleto,PREFIJO_HUESOS_IK,False)             # des seleciona todos los huesos en modo edition
            hueso_mano_r = IK_esqueleto.data.edit_bones.get(hueso_mano_r_name)        # busca el hueso de la mano
            
            if not hueso_mano_r == None:
                
                ik_mano = IK_esqueleto.data.edit_bones.new(PREFIJO_HUESO_IK_CONTROL+"mano_R")
                
                mover_hueso         = Vector((0.0,0.0,0.0))                # define cuanto se desplazara
                ik_mano.head = hueso_mano_r.head + mover_hueso             # mueve la cabeza del hueso
                ik_mano.tail = hueso_mano_r.tail + mover_hueso             # mueve la cola del hueso
                
                # configuracion del hueso 
                ik_mano.use_connect  = False
                ik_mano.use_deform   = False
                ik_mano.parent       = None
                #ik_mano.display_type = "BBONE"
                
                 # antes de pasar a modo pose obtenemos nombre del hueso duplicado
                
                
                # creacion del polea 
                codo_name = "IK.BRAZO_R.antebrazo.R"
                selecionar_huesos(IK_esqueleto,PREFIJO_HUESOS_IK,False) 
                hueso_codo = IK_esqueleto.data.edit_bones.get(codo_name)
                
                if not hueso_codo == None:
                    
                    pole = IK_esqueleto.data.edit_bones.new(PREFIJO_HUESO_IK_CONTROL+"pole_R")
                    mover_pole  = Vector((0.0,0.5,0.0))                # define cuanto se desplazara
                    pole.head = hueso_codo.head + mover_pole             # mueve la cabeza del hueso
                    pole.tail = hueso_codo.tail + mover_pole             # mueve la cola del hueso
                
                                  # configuracion del hueso 
                    pole.use_connect  = False
                    pole.use_deform   = False
                    pole.parent       = ik_mano
                    #pole.display_type = "BBONE"
                    
                    nombre_pole = pole.name
                    nombre_hueso = ik_mano.name
                    # logica del constraints y drivers 
                    bpy.ops.object.mode_set(mode='POSE')
                    
                    
                    
                    # se obtiene los hueso de control y el uso que lo aplicara 
                    hueso_pose          = IK_esqueleto.pose.bones.get(codo_name)
                    IK                  = IK_esqueleto.pose.bones.get(nombre_hueso)
                    pole_pose           = IK_esqueleto.pose.bones.get(nombre_pole)
                    hueso_mano_r_pose   = IK_esqueleto.pose.bones.get(hueso_mano_r_name)
                    
                    # conecta el control con el boton mostrar 
                    
                    vincular_driver("",IK,data_path,armature,"mostrar_controles")
                    vincular_driver("",pole_pose,data_path,armature,"mostrar_controles")
                    
                    # añade un contraitns                
                    constraint_hueso = hueso_pose.constraints.new(type = "IK")
                    constraint_hueso.name            = "control IK"
                    constraint_hueso.target          = IK_esqueleto
                    constraint_hueso.subtarget       = IK.name
                    constraint_hueso.chain_count     = 2
                    constraint_hueso.pole_target     = IK_esqueleto
                    constraint_hueso.pole_subtarget  = pole_pose.name
                    constraint_hueso.pole_angle      = math.radians(-90)
                    #constraint_hueso.track_axis = "TRACK_Z"
                    
                    
                    pass
                else:
                    self.report({"INFO"},"Hueso del codo R no encontrado")
                    pass
                
                
                pass
            else:
                self.report({"INFO"},"Hueso del brazo R no encontrado")
                
                
                
                
                
            #cambiamos de color todos los huesos 
            bpy.ops.object.mode_set(mode='EDIT')
            cambiar_color_huesos(IK_esqueleto,
                                PREFIJO_HUESO_IK_CONTROL,
                                color_normal,
                                color_select,
                                color_activo)
            context.object.update_tag(refresh={'DATA'})
                
        else:
            # Si no hay huesos generados, elimina la copia vacía y vuelve a seleccionar el original

            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.objects.active = IK_esqueleto
            IK_esqueleto.select_set(True)
            bpy.ops.object.delete(use_global=False)
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = DF_ESQUELETO
            DF_ESQUELETO.select_set(True)
            borrar_ik = True
        
        
        if combinar:
            if not borrar_ik:
                bpy.ops.object.mode_set(mode='OBJECT')
                
                ik_join = bpy.data.objects.get(IK_esqueleto.name)
                df_join = bpy.data.objects.get(DF_ESQUELETO.name)
                
                df_join.select_set(True)
                ik_join.select_set(True)
                
                bpy.context.view_layer.objects.active = df_join
                bpy.ops.object.join()
            else:
                self.report({"INFO"},"Sistema IK No creado")
        
        else:
            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = DF_ESQUELETO
            DF_ESQUELETO.select_set(True)
            
            self.report({"INFO"},"Se combino el esqueleto IK con el esqueleto DF")
            pass
        
        return {'FINISHED'}
    
    
# sistema IPI: Operador reservado para la generación del sistema retargeting de iPi Mocap
class OBJECT_OT_Generar_sistema_IPI(bpy.types.Operator): 
    """Crea al esqueleto selecionado su sistema de control FK"""
    
    bl_idname = "object.generar_ipi" 
    bl_label = "Generar IPI" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        self.report({'INFO'}, "HOLA MUNDO") 
        return {'FINISHED'}  


##############################################################
#                 LIMPIEZA Y CORRECCIONES 
#################################################################



# selecionar FK: Operador para seleccionar rápidamente el conjunto de controles FK
class OBJECT_OT_SELECIONAR_FK(bpy.types.Operator): 
    """Crea al esqueleto selecionado su sistema de control FK"""
    
    bl_idname = "object.selecionar_fk" 
    bl_label = "Seleciona sistema FK" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        esqueleto = bpy.context.object
        selecionar_huesos(esqueleto,PREFIJO_HUESOS_FK)
        return {'FINISHED'} 
    
    
# selecionar IK: Operador para seleccionar el conjunto de controles IK
class OBJECT_OT_SELECIONAR_IK(bpy.types.Operator): 
    """Crea al esqueleto selecionado su sistema de control FK"""
    
    bl_idname = "object.selecionar_ik" 
    bl_label = "Seleciona sistema IK" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        esqueleto = bpy.context.object
        selecionar_huesos(esqueleto,PREFIJO_HUESOS_IK)
        return {'FINISHED'}  
    
# selecionar ipi: Operador para seleccionar los elementos del sistema IPI Mocap
class OBJECT_OT_SELECIONAR_IPI(bpy.types.Operator): 
    """Crea al esqueleto selecionado su sistema de control FK"""
    
    bl_idname = "object.selecionar_ipi" 
    bl_label = "Seleciona sistema IPI" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        esqueleto = bpy.context.object
        selecionar_huesos(esqueleto,PREFIJO_HUESOS_IPI)
        return {'FINISHED'}  
 
 
 
# selecionar fijadores de malla.
class OBJECT_OT_SELECIONAR_FIJADORES(bpy.types.Operator): 
    """seleciona todos los huesos fijadores de malla"""
    
    bl_idname = "object.selecionar_pin" 
    bl_label = "Seleciona Huesos Fijadores" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        esqueleto = bpy.context.object
        selecionar_huesos(esqueleto,PREFIJO_HUESOS_FIJADOR)
        return {'FINISHED'}     

# selecionar deformadores de maya .
class OBJECT_OT_SELECIONAR_DEFORMADORES(bpy.types.Operator): 
    """seleciona todos los huesos deformadores de malla"""
    
    bl_idname = "object.selecionar_df" 
    bl_label = "Seleciona Huesos deformadores" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        esqueleto = bpy.context.object
        selecionar_huesos(esqueleto,PREFIJO_HUESOS_DEFORMACION)
        return {'FINISHED'} 
    
# selecionar huesos relacionado para accesorio .
class OBJECT_OT_SELECIONAR_ACCESORIO(bpy.types.Operator): 
    """seleciona todos los huesos destinado a controlar accesorios y utileria"""
    
    bl_idname = "object.selecionar_prop" 
    bl_label = "Seleciona Huesos Accesorios" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        esqueleto = bpy.context.object
        selecionar_huesos(esqueleto,PREFIJO_HUESOS_ACCESORIOS)
        return {'FINISHED'} 
    
    
# selecionar huesos relacionado con el cabello .
class OBJECT_OT_SELECIONAR_CABELLO(bpy.types.Operator): 
    """seleciona todos los huesos destinado a controlar el cabello"""
    
    bl_idname = "object.selecionar_hair" 
    bl_label = "Seleciona Huesos Cabellos" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        esqueleto = bpy.context.object
        selecionar_huesos(esqueleto,PREFIJO_HUESOS_CABELLO)
        return {'FINISHED'}  

#################################################################################
#                 Control de eliminacion de drivers 
#################################################################################



#################################################################################
#                            Borra sistema FK
# elimina sistema FK: Elimina los huesos FK, retira constraints de los huesos base y limpia drivers huérfanos
class OBJECT_OT_ELIMINAR_FK(bpy.types.Operator): 
    """Borra la vinculacion con el sistema FK"""
    
    bl_idname = "object.eliminar_fk"
    bl_label = "ELIMINA EL SISTEMA FK" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        
        obj = context.object
        
        # eliminar huesos que no se necesita
        bpy.ops.armature.select_all(action='DESELECT')
        esqueleto = obj
        
        borrar_huesos_prefijo(esqueleto,PREFIJO_HUESOS_FK)
      
        #borrado de constraints         
        bpy.ops.object.mode_set(mode='POSE') 
        
        NOMBRE_CONSTRAINT = "FK_ROTATION"
        esqueleto = context.object
        eliminar_constraint(NOMBRE_CONSTRAINT,esqueleto,PREFIJO_HUESOS_DEFORMACION)
        
        #borra drivers sueltos
        bpy.ops.object.mode_set(mode='POSE')
        esqueleto = bpy.context.object
        eliminar_drivers_rotos_esqueleto(esqueleto)
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}  




####################################################
#                   Eliminar IK
class OBJECT_OT_ELIMINAR_IK(bpy.types.Operator): 
    """Borra la vinculacion con el sistema IK"""
    
    bl_idname = "object.eliminar_ik"
    bl_label = "ELIMINA EL SISTEMA IK" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        
        obj = context.object
        
        # eliminar huesos que no se necesita
        bpy.ops.armature.select_all(action='DESELECT')
        esqueleto = obj
        
        borrar_huesos_prefijo(esqueleto,PREFIJO_HUESOS_IK)
      
        #borrado de constraints         
        bpy.ops.object.mode_set(mode='POSE') 
        
        NOMBRE_CONSTRAINT = "IK_ROTATION"
        esqueleto = context.object
        eliminar_constraint(NOMBRE_CONSTRAINT,esqueleto,PREFIJO_HUESOS_DEFORMACION)
        
        #borra drivers sueltos
        bpy.ops.object.mode_set(mode='POSE')
        esqueleto = bpy.context.object
        eliminar_drivers_rotos_esqueleto(esqueleto)
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}
    
#################################################################################
#                            Borra sistema IPI
class OBJECT_OT_ELIMINAR_IPI(bpy.types.Operator): 
    """Borra la vinculacion con el sistema IPI"""
    
    bl_idname = "object.eliminar_ipi"
    bl_label = "ELIMINA EL SISTEMA IPI" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        
        obj = context.object
        
        # eliminar huesos que no se necesita
        bpy.ops.armature.select_all(action='DESELECT')
        esqueleto = obj
        borrar_huesos_prefijo(esqueleto,PREFIJO_HUESOS_API)
      
        #borrado de constraints         
        bpy.ops.object.mode_set(mode='POSE') 
        
        NOMBRE_CONSTRAINT = "IPI_ROTATION"
        esqueleto = context.object
        eliminar_constraint(NOMBRE_CONSTRAINT,esqueleto,PREFIJO_HUESOS_DEFORMACION)
        
        #borra drivers sueltos
        bpy.ops.object.mode_set(mode='POSE')
        esqueleto = bpy.context.object
        eliminar_drivers_rotos_esqueleto(esqueleto)
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}  
        
     
###########################################################
#
#     Vistas UI
#
###########################################################
   
    
# MENU de generalidades: Panel UI para la generación inicial de armaduras en Modo Objeto
class DATA_PT_UI_CREATE_ARMATURE(bpy.types.Panel):
    
    bl_label = "Creacion de Controles de Armature "
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"  # Apunta a la pestaña Data
    
    @classmethod
    def poll(cls,context):
        obj = context.object
        return obj and obj.type == 'ARMATURE' and context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        armature = context.object.data
        general_prop = armature.control_rig.crear_prop
        
        box_crear = layout.box()
        box_crear.label(text= "Generar sistemas de control",icon="ARMATURE_DATA") 
        
        
        fila_1 = box_crear.row(align=True)
        fila_1.prop(general_prop, "combinar_FK", toggle=True)
        fila_1.operator("object.generar_fk",icon="BONE_DATA")
        
        fila_2 = box_crear.row(align=True)
        fila_2.prop(general_prop, "combinar_IK", toggle=True)
        fila_2.operator("object.generar_ik",icon="BONE_DATA")
        
        
        fila_3 = box_crear.row(align=True)
        fila_3.prop(general_prop, "combinar_IPI", toggle=True)
        fila_3.operator("object.generar_ipi",icon="BONE_DATA")
        pass
    pass


    
# menu en propiedades sistema FK: Panel para controlar visibilidad e influencia FK durante la animación en Pose Mode
class DATA_PT_UI_Control_FK(bpy.types.Panel):
    
    bl_label = "Sistema de control Fk"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"  # Apunta a la pestaña Data
    
    @classmethod
    def poll(cls,context):
        return context.object is not None and context.object.type == "ARMATURE" and context.mode == 'POSE'
    pass
    
    def draw(self, context):
        layout = self.layout
        armature = context.active_object.data.control_rig.fk_prop
        
        # control general
        box_general = layout.box()
        box_general.label(text="Sistema de control FK")
        box_general.prop(armature,"mostrar",toggle=True)
        box_general.prop(armature,"influencia_maestra",slider=True)
        layout.separator()
        
        #control Cabeza
        cabeza = layout.box()
        cabeza.label(text="cabeza")
        cabeza_botones = cabeza.row()
        cabeza_botones.prop(armature,"mostrar_cabeza",toggle=True)
        cabeza_botones.prop(armature,"influencia_cabeza",slider=True)
        
        cejas = cabeza.box()
        cejas.label(text ="CEJAS")
        cejas_botones = cejas.row()
        cejas_botones.prop(armature,"mostrar_cejas", toggle=True)
        cejas_botones.prop(armature,"influencia_cejas", toggle=True)
        
        ojos = cabeza.box()
        ojos.label(text ="OJOS")
        ojos_botones = ojos.row()
        ojos_botones.prop(armature,"mostrar_ojos", toggle=True)
        ojos_botones.prop(armature,"influencia_ojos", toggle=True)
        
        boca = cabeza.box()
        boca.label(text ="BOCA")
        boca_botones = boca.row()
        boca_botones.prop(armature,"mostrar_boca", toggle=True)
        boca_botones.prop(armature,"influencia_boca", toggle=True)

        
        layout.separator()
        
        
        
        # espalda
        espalda = layout.box()
        espalda.label(text="ESPALDA")
        espalda_botones = espalda.row()
        espalda_botones.prop(armature,"mostrar_espalda",toggle=True)
        espalda_botones.prop(armature,"influencia_espalda",slider=True)
        layout.separator()
        
        
        # brazo L
        brazo_L = layout.box()
        brazo_L.label(text="BRAZO L")
        brazo_botones_L = brazo_L.row()
        brazo_botones_L.prop(armature,"mostrar_brazo_l",toggle=True)
        brazo_botones_L.prop(armature,"influencia_brazo_l",slider=True)
        #mano
        mano_L = brazo_L.box()
        mano_L.label(text="MANO L")
        mano_botones_L = mano_L.row()
        mano_botones_L.prop(armature,"mostrar_mano_l",toggle=True)
        mano_botones_L.prop(armature,"influencia_mano_l",slider=True)
        layout.separator()
        
        
        # brazo R
        brazo_R = layout.box()
        brazo_R.label(text="BRAZO R")
        brazo_botones_R = brazo_R.row()
        brazo_botones_R.prop(armature,"mostrar_brazo_r",toggle=True)
        brazo_botones_R.prop(armature,"influencia_brazo_r",slider=True)
        #mano
        mano_R = brazo_R.box()
        mano_R.label(text="MANO R")
        mano_botones_R = mano_R.row()
        mano_botones_R.prop(armature,"mostrar_mano_r",toggle=True)
        mano_botones_R.prop(armature,"influencia_mano_r",slider=True)
        layout.separator()
        
        
        # pierna L
        pierna_L = layout.box()
        pierna_L.label(text="PIERNA L")
        pierna_botones_L = pierna_L.row()
        pierna_botones_L.prop(armature,"mostrar_pierna_l",toggle=True)
        pierna_botones_L.prop(armature,"influencia_pierna_l",slider=True)
        #pie L
        pie_L = pierna_L.box()
        pie_L.label(text="PIE L")
        pie_botones_L = pie_L.row()
        pie_botones_L.prop(armature,"mostrar_pie_l",toggle=True)
        pie_botones_L.prop(armature,"influencia_pie_l",slider=True)
        layout.separator()
        
        # pierna R
        pierna_R = layout.box()
        pierna_R.label(text="PIERNA R")
        pierna_botones_R = pierna_R.row()
        pierna_botones_R.prop(armature,"mostrar_pierna_r",toggle=True)
        pierna_botones_R.prop(armature,"influencia_pierna_r",slider=True)
        #pie R
        pie_R = pierna_R.box()
        pie_R.label(text="PIE R")
        pie_botones_R = pie_R.row()
        pie_botones_R.prop(armature,"mostrar_pie_r",toggle=True)
        pie_botones_R.prop(armature,"influencia_pie_r",slider=True)
        layout.separator()
        pass
    pass

# menu de control ik
class DATA_PT_UI_Control_IK(bpy.types.Panel):
    
    bl_label = "Sistema de control IK"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"  # Apunta a la pestaña Data
    
    @classmethod
    def poll(cls,context):
        return context.object is not None and context.object.type == "ARMATURE" and context.mode == 'POSE'
    pass


    def draw(self, context):
        layout = self.layout
        armature = context.active_object.data.control_rig.ik_prop
        
        # control general
        box_general = layout.box()
        box_general.label(text="Sistema de control IK")
        box_general.prop(armature,"mostrar",toggle=True)
        box_general.prop(armature,"mostrar_controles",toggle=True)
        box_general.prop(armature,"influencia_maestra",slider=True)
        layout.separator()
        
        #control Cabeza
        cabeza = layout.box()
        cabeza.label(text="cabeza")
        cabeza_botones = cabeza.row()
        cabeza_botones.prop(armature,"mostrar_cabeza",toggle=True)
        cabeza_botones.prop(armature,"influencia_cabeza",slider=True)
        
        cejas = cabeza.box()
        cejas.label(text ="CEJAS")
        cejas_botones = cejas.row()
        cejas_botones.prop(armature,"mostrar_cejas", toggle=True)
        cejas_botones.prop(armature,"influencia_cejas", toggle=True)
        
        ojos = cabeza.box()
        ojos.label(text ="OJOS")
        ojos_botones = ojos.row()
        ojos_botones.prop(armature,"mostrar_ojos", toggle=True)
        ojos_botones.prop(armature,"influencia_ojos", toggle=True)
        
        boca = cabeza.box()
        boca.label(text ="BOCA")
        boca_botones = boca.row()
        boca_botones.prop(armature,"mostrar_boca", toggle=True)
        boca_botones.prop(armature,"influencia_boca", toggle=True)

        
        layout.separator()
        
        
        
        # espalda
        espalda = layout.box()
        espalda.label(text="ESPALDA")
        espalda_botones = espalda.row()
        espalda_botones.prop(armature,"mostrar_espalda",toggle=True)
        espalda_botones.prop(armature,"influencia_espalda",slider=True)
        layout.separator()
        
        
        # brazo L
        brazo_L = layout.box()
        brazo_L.label(text="BRAZO L")
        brazo_botones_L = brazo_L.row()
        brazo_botones_L.prop(armature,"mostrar_brazo_l",toggle=True)
        brazo_botones_L.prop(armature,"influencia_brazo_l",slider=True)
        #mano
        mano_L = brazo_L.box()
        mano_L.label(text="MANO L")
        mano_botones_L = mano_L.row()
        mano_botones_L.prop(armature,"mostrar_mano_l",toggle=True)
        mano_botones_L.prop(armature,"influencia_mano_l",slider=True)
        layout.separator()
        
        
        # brazo R
        brazo_R = layout.box()
        brazo_R.label(text="BRAZO R")
        brazo_botones_R = brazo_R.row()
        brazo_botones_R.prop(armature,"mostrar_brazo_r",toggle=True)
        brazo_botones_R.prop(armature,"influencia_brazo_r",slider=True)
        #mano
        mano_R = brazo_R.box()
        mano_R.label(text="MANO R")
        mano_botones_R = mano_R.row()
        mano_botones_R.prop(armature,"mostrar_mano_r",toggle=True)
        mano_botones_R.prop(armature,"influencia_mano_r",slider=True)
        layout.separator()
        
        
        # pierna L
        pierna_L = layout.box()
        pierna_L.label(text="PIERNA L")
        pierna_botones_L = pierna_L.row()
        pierna_botones_L.prop(armature,"mostrar_pierna_l",toggle=True)
        pierna_botones_L.prop(armature,"influencia_pierna_l",slider=True)
        #pie L
        pie_L = pierna_L.box()
        pie_L.label(text="PIE L")
        pie_botones_L = pie_L.row()
        pie_botones_L.prop(armature,"mostrar_pie_l",toggle=True)
        pie_botones_L.prop(armature,"influencia_pie_l",slider=True)
        layout.separator()
        
        # pierna R
        pierna_R = layout.box()
        pierna_R.label(text="PIERNA R")
        pierna_botones_R = pierna_R.row()
        pierna_botones_R.prop(armature,"mostrar_pierna_r",toggle=True)
        pierna_botones_R.prop(armature,"influencia_pierna_r",slider=True)
        #pie R
        pie_R = pierna_R.box()
        pie_R.label(text="PIE R")
        pie_botones_R = pie_R.row()
        pie_botones_R.prop(armature,"mostrar_pie_r",toggle=True)
        pie_botones_R.prop(armature,"influencia_pie_r",slider=True)
        layout.separator()
        pass
    pass

# menu de control ipi
class DATA_PT_UI_Control_IPI(bpy.types.Panel):
    
    bl_label = "Sistema de control IPI"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"  # Apunta a la pestaña Data
    
    @classmethod
    def poll(cls,context):
        return context.object is not None and context.object.type == "ARMATURE" and context.mode == 'POSE'
    pass


    def draw(self, context):
        layout = self.layout
        armature = context.active_object.data.control_rig.ipi_prop
        
        # control general
        box_general = layout.box()
        box_general.label(text="Sistema de control IPI")
        box_general.prop(armature,"mostrar",toggle=True)
        box_general.prop(armature,"influencia_maestra",slider=True)
        layout.separator()
        
        #control Cabeza
        cabeza = layout.box()
        cabeza.label(text="cabeza")
        cabeza_botones = cabeza.row()
        cabeza_botones.prop(armature,"mostrar_cabeza",toggle=True)
        cabeza_botones.prop(armature,"influencia_cabeza",slider=True)

        layout.separator()
        
        
        
        # espalda
        espalda = layout.box()
        espalda.label(text="ESPALDA")
        espalda_botones = espalda.row()
        espalda_botones.prop(armature,"mostrar_espalda",toggle=True)
        espalda_botones.prop(armature,"influencia_espalda",slider=True)
        layout.separator()
        
        
        # brazo L
        brazo_L = layout.box()
        brazo_L.label(text="BRAZO L")
        brazo_botones_L = brazo_L.row()
        brazo_botones_L.prop(armature,"mostrar_brazo_l",toggle=True)
        brazo_botones_L.prop(armature,"influencia_brazo_l",slider=True)
        #mano
        mano_L = brazo_L.box()
        mano_L.label(text="MANO L")
        mano_botones_L = mano_L.row()
        mano_botones_L.prop(armature,"mostrar_mano_l",toggle=True)
        mano_botones_L.prop(armature,"influencia_mano_l",slider=True)
        layout.separator()
        
        
        # brazo R
        brazo_R = layout.box()
        brazo_R.label(text="BRAZO R")
        brazo_botones_R = brazo_R.row()
        brazo_botones_R.prop(armature,"mostrar_brazo_r",toggle=True)
        brazo_botones_R.prop(armature,"influencia_brazo_r",slider=True)
        #mano
        mano_R = brazo_R.box()
        mano_R.label(text="MANO R")
        mano_botones_R = mano_R.row()
        mano_botones_R.prop(armature,"mostrar_mano_r",toggle=True)
        mano_botones_R.prop(armature,"influencia_mano_r",slider=True)
        layout.separator()
        
        
        # pierna L
        pierna_L = layout.box()
        pierna_L.label(text="PIERNA L")
        pierna_botones_L = pierna_L.row()
        pierna_botones_L.prop(armature,"mostrar_pierna_l",toggle=True)
        pierna_botones_L.prop(armature,"influencia_pierna_l",slider=True)
        #pie L
        pie_L = pierna_L.box()
        pie_L.label(text="PIE L")
        pie_botones_L = pie_L.row()
        pie_botones_L.prop(armature,"mostrar_pie_l",toggle=True)
        pie_botones_L.prop(armature,"influencia_pie_l",slider=True)
        layout.separator()
        
        # pierna R
        pierna_R = layout.box()
        pierna_R.label(text="PIERNA R")
        pierna_botones_R = pierna_R.row()
        pierna_botones_R.prop(armature,"mostrar_pierna_r",toggle=True)
        pierna_botones_R.prop(armature,"influencia_pierna_r",slider=True)
        #pie R
        pie_R = pierna_R.box()
        pie_R.label(text="PIE R")
        pie_botones_R = pie_R.row()
        pie_botones_R.prop(armature,"mostrar_pie_r",toggle=True)
        pie_botones_R.prop(armature,"influencia_pie_r",slider=True)
        layout.separator()
        pass
    pass

# menu de control global 
class DATA_PT_UI_Control_SISTEMAS(bpy.types.Panel):
    
    bl_label = "CONTROL GLOBAL SISTEMAS"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"  # Apunta a la pestaña Data
    
    @classmethod
    def poll(cls,context):
        return context.object is not None and context.object.type == "ARMATURE" and context.mode == 'POSE'
    pass


    def draw(self, context):
        layout = self.layout
        
        FK = context.active_object.data.control_rig.fk_prop
        IK = context.active_object.data.control_rig.ik_prop
        IPI = context.active_object.data.control_rig.ipi_prop
        
        
        box_general = layout.box()
        box_general.prop(FK,"mostrar",toggle=True)
        
        row = box_general.row()
        row.prop(IK,"mostrar",toggle=True)
        row.prop(IK,"mostrar_controles",toggle=True)
        box_general.prop(IPI,"mostrar",toggle=True) 
               
        
 # permite selecionar los diferente esqueletos: Panel de herramientas de selección y borrado de subsistemas
class DATA_PT_UI_SELECIONAR_SISTEMA(bpy.types.Panel):
    
    bl_label = "Selecionar sistema"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"  # Apunta a la pestaña Data

    
    @classmethod
    def poll(cls,context):
        obj = context.object
        return obj and obj.type == 'ARMATURE' and context.mode != "OBJECT" and context.mode != "POSE" 
    
    def draw(self, context):
        layout = self.layout
        armature = context.object.data
        
        herramientas = layout.box()
        herramientas.label(text = "Selecionar huesos")
        
        herramientas.operator("object.selecionar_df")
        herramientas.operator("object.selecionar_pin")
        herramientas.operator("object.selecionar_prop")
        herramientas.operator("object.selecionar_hair")
        
        Selecionar = layout.box()
        Selecionar.label(text="Selecionar sistma")
        Selecionar.operator("object.selecionar_fk")
        Selecionar.operator("object.selecionar_ik")
        Selecionar.operator("object.selecionar_ipi")
        Selecionar.separator()
        
        Eliminar_sistema = layout.box()
        Eliminar_sistema.label(text = "Eliminar sistema")
        Eliminar_sistema.operator("object.eliminar_fk")
        Eliminar_sistema.operator("object.eliminar_ik")
        Eliminar_sistema.operator("object.eliminar_ipi")
       

###########################################################
#
#     LIMPIEZA
#
###########################################################

# listado de clases a registrar/desregistrar en Blender
classes = [
    DATA_PT_UI_CREATE_ARMATURE,
    DATA_PT_UI_Control_SISTEMAS,
    DATA_PT_UI_Control_FK,
    DATA_PT_UI_Control_IK,
    DATA_PT_UI_Control_IPI,
    DATA_PT_UI_SELECIONAR_SISTEMA,
    
    
    OBJECT_OT_Generar_sistema_FK,
    OBJECT_OT_Generar_sistema_IK,
    OBJECT_OT_Generar_sistema_IPI,
    
    OBJECT_OT_SELECIONAR_FK,
    OBJECT_OT_SELECIONAR_IPI,
    OBJECT_OT_SELECIONAR_IK,
    
    OBJECT_OT_SELECIONAR_FIJADORES,
    OBJECT_OT_SELECIONAR_DEFORMADORES,
    OBJECT_OT_SELECIONAR_ACCESORIO,
    OBJECT_OT_SELECIONAR_CABELLO,
    
    OBJECT_OT_ELIMINAR_FK,
    OBJECT_OT_ELIMINAR_IK,
    OBJECT_OT_ELIMINAR_IPI,
    
    ARMATURE_GENERAL_PROPIEDADES,
    ARMATURE_SISTEMA_FK_PROPIEDADES,
    ARMATURE_SISTEMA_IK_PROPIEDADES,
    ARMATURE_SISTEMA_IPI_PROPIEDADES,
    ARMATURE_CONTROLADOR_PROPIEDADES,
    
]







# Punto de entrada para habilitar el complemento en Blender
def register():
    
    
    for cls in classes: 
        bpy.utils.register_class(cls)
        
    registrar_propiedades()
    
# Punto de entrada para deshabilitar el complemento en Blender
def unregister(): 
    for cls in reversed(classes): 
        bpy.utils.unregister_class(cls)
        
    unregister_properties()
        
if __name__ == "__main__": register()