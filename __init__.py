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
def Actualizar_mostrar_fk(self,context):
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
def Actualizar_influencia_fk(self,context):
    
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
                            update= Actualizar_mostrar_fk)
    influencia_maestra  : crear_propiedad_sliders("Influencia FK",
                            update= Actualizar_influencia_fk )
    
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
    influencia_pierna_l   : crear_propiedad_sliders( "Influencia Brazo R FK")
    
    #Pierna L
    mostrar_pie_l      : crear_propiedad_switch("Mostrar Pie L FK")
    influencia_pie_l   : crear_propiedad_sliders( "Influencia Pie R FK")
    
    #Pierna r
    mostrar_pierna_r      : crear_propiedad_switch("Mostrar pierna L FK")
    influencia_pierna_r   : crear_propiedad_sliders( "Influencia Brazo R FK")
    
    #Pierna r
    mostrar_pie_r      : crear_propiedad_switch("Mostrar Pie L FK")
    influencia_pie_r   : crear_propiedad_sliders( "Influencia Pie R FK")
    pass
    


######################################################
#          Enlazamiento de propiedades con objeto 
####################################################


# clase en cargada de guardar todas las propiedades dentro de bpy.types.Armature.control_rig 
class ARMATURE_CONTROLADOR_PROPIEDADES(bpy.types.PropertyGroup):
    
    crear_prop  : bpy.props.PointerProperty(type = ARMATURE_GENERAL_PROPIEDADES)
    fk_prop     : bpy.props.PointerProperty(type = ARMATURE_SISTEMA_FK_PROPIEDADES)
    
    
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
    var.targets[0].data_path = data_path+nombre
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
    
    crear_var_driver(driver,prop_maestra,data_path,armature) # crea la variable maestra
    crear_var_driver(driver,prop_nombre,data_path,armature)    # crea la variable especifica
    
    driver.expression = ajuste_expresion+f"({prop_maestra}*{prop_nombre})"                 
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
            
            if nombre_constraint in bone.constraints:
                
                constraint_a_borrar = bone.constraints[nombre_constraint]
                bone.constraints.remove(constraint_a_borrar)
    
    pass


# elimna todos los contraints
def eliminar_todo_constraints(
                            esqueleto,
                            prefijo="DF."
                            ):
    
    for bone in esqueleto.pose.bones:      
        if bone.name.startswith(prefijo):
            bone.constraints.clear()
                                  
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
                prefijo
                ):
    for bone in esqueleto.edit_bones:
        
        if bone.name.startswith(prefijo):
            esqueleto.edit_bones.remove(bone)
            pass
    
    pass                                        
                        
def selecionar_huesos(
                    Esqueleto,
                    Prefijo = "DF."):
                        
    bpy.ops.armature.select_all(action='DESELECT')
     
    for bone in esqueleto.edit_bones:
        if bone.ame.startswith(prefijo):
            bone.select = True
            bone.select_head = True
            bone.select_tail = True
                               
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
        modo      = context.mode
        combinar  = fk.crear_prop.combinar_FK
        
        if modo == "OBJECT":
            
            bpy.ops.object.mode_set(mode='OBJECT')

            deformador_esqueleto = bpy.context.active_object
            
            # Clona la armadura base para generar el esqueleto de control FK
            bpy.ops.object.duplicate(linked=False)
            
            fk_esqueleto = bpy.context.active_object
            fk_esqueleto.location.x += 5
            fk_esqueleto.name = "FK"
            
            bpy.ops.object.mode_set(mode='EDIT')
            
            #borra los huesos que no tengan el prefijo DF.
            huesos_a_borrar = []
            for bone in fk_esqueleto.data.edit_bones:
                if not bone.name.startswith("DF."):
                    #huesos_a_borrar.append(bone)
                    fk_esqueleto.data.edit_bones.remove(bone)
                    
            # 2. Eliminar los huesos encontrados
            #for bone in huesos_a_borrar:
            #    fk_esqueleto.data.edit_bones.remove(bone)
            

            # 3. Ajustar los huesos restantes (los DF.): Renombra a FK. y asigna colores en el viewport
            for bone in fk_esqueleto.data.edit_bones:
                bone.use_deform = False
                bone.name = "FK." + bone.name[3:]
                
                bone.color.palette = "CUSTOM"
                bone.color.custom.normal = (0.0,1.0,0.0)
                bone.color.custom.select = (1.0, 0.0, 0.0)
                bone.color.custom.active = (1.0,1.0, 1.0)
                
            bpy.ops.object.mode_set(mode='OBJECT')    
            
            
            # si el esqueleto FK NO esta vacio 
            vacio = len(fk_esqueleto.data.bones) == 0             
            if not len(fk_esqueleto.data.bones) == 0:
                
                bpy.ops.object.mode_set(mode='POSE')
                
                ############################################
                # encargado de conectar la propiedad mostrar con su propiedad hide
                ###########################################
                data_path = "control_rig.fk_prop."
                MAPEO_NOMBRE_BONE_PROPIEDADES_MOSTRAR = {
                    "FK.CABEZA."   : "mostrar_cabeza",
                    "FK.ESPALDA."  : "mostrar_espalda",
                    
                    "FK.BRAZO_R."  : "mostrar_brazo_r",
                    "FK.MANO_R."   : "mostrar_mano_r",
                    "FK.PIERNA_R." : "mostrar_pierna_r",
                    "FK.PIE_R."    : "mostrar_pie_r",
                    
                    "FK.BRAZO_L."  : "mostrar_brazo_l",
                    "FK.MANO_L."   : "mostrar_mano_l",
                    "FK.PIERNA_L." : "mostrar_pierna_l",
                    "FK.PIE_L."    : "mostrar_pie_l",
                }
                # Aplica drivers para ocultar/mostrar huesos FK según las propiedades
                for bone in fk_esqueleto.pose.bones:
                    for prefijo, propiedad in MAPEO_NOMBRE_BONE_PROPIEDADES_MOSTRAR.items():
                        
                        if bone.name.startswith(prefijo):
                            vincular_driver(propiedad,bone,data_path,armature)
                
                ############################################
                # encargado de conectar la propiedad mostrar con su propiedad hide
                ###########################################
                data_path = "control_rig.fk_prop."
                MAPEO_NOMBRE_BONE_PROPIEDADES_INFLUENCIA = {
                    "DF.CABEZA."   : "influencia_cabeza",
                    "DF.ESPALDA."  : "influencia_espalda",
                    
                    "DF.BRAZO_R."  : "influencia_brazo_r",
                    "DF.MANO_R."   : "influencia_mano_r",
                    "DF.PIERNA_R." : "influencia_pierna_r",
                    "DF.PIE_R."    : "influencia_pie_r",
                    
                    "DF.BRAZO_L."  : "influencia_brazo_l",
                    "DF.MANO_L."   : "influencia_mano_l",
                    "DF.PIERNA_L." : "influencia_pierna_l",
                    "DF.PIE_L."    : "influencia_pie_l",
                }
                # entra al esqueleto original 
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = deformador_esqueleto            
                bpy.ops.object.mode_set(mode='POSE')
                
                # Asigna restricciones Copy Rotation a la armadura base controladas por el esqueleto FK
                for bone in deformador_esqueleto.pose.bones:
                    for prefijo, propiedad in MAPEO_NOMBRE_BONE_PROPIEDADES_INFLUENCIA.items():
                        if bone.name.startswith(prefijo):
                            
                            constraint_hueso = bone.constraints.new(type='COPY_ROTATION')
                            constraint_hueso.name = "FK_ROTATION"
                            constraint_hueso.target = fk_esqueleto
                            constraint_hueso.subtarget = "FK."+bone.name[3:]
                            
                            vincular_driver(propiedad,
                                            constraint_hueso,
                                            data_path,armature,
                                            "influencia_maestra",
                                            "influence","")
                            
                            
                    pass
                    
                    
                context.object.update_tag(refresh={'DATA'})
            
            else:
                # Si no hay huesos generados, elimina la copia vacía y vuelve a seleccionar el original
                bpy.ops.object.delete(use_global=False)
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = deformador_esqueleto
                deformador_esqueleto.select_set(True)
                

            # Fusiona las armaduras si la opción 'combinar' está activa
            if combinar:
                # cambia a modo objeto 
                bpy.ops.object.mode_set(mode='OBJECT')
                
                #seleciona ambos objeto
                fk_esqueleto_join         = bpy.data.objects.get(fk_esqueleto.name)
                deformador_esqueleto_join = bpy.data.objects.get(deformador_esqueleto.name)
                fk_esqueleto_join.select_set(True)
                deformador_esqueleto_join.select_set(True)
                
                # combierte el esqueleto deformador primero
                bpy.context.view_layer.objects.active = deformador_esqueleto_join
                bpy.ops.object.join()
                
                pass
            else:
                bpy.ops.object.mode_set(mode='OBJECT')
                #Selecionar el esqueleto original 
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = deformador_esqueleto
                deformador_esqueleto.select_set(True)
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
        self.report({'INFO'}, "HOLA MUNDO") 
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
        self.report({'INFO'}, "HOLA MUNDO") 
        return {'FINISHED'} 
    
    
# selecionar IK: Operador para seleccionar el conjunto de controles IK
class OBJECT_OT_SELECIONAR_IK(bpy.types.Operator): 
    """Crea al esqueleto selecionado su sistema de control FK"""
    
    bl_idname = "object.selecionar_ik" 
    bl_label = "Seleciona sistema IK" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        self.report({'INFO'}, "HOLA MUNDO") 
        return {'FINISHED'}  
    
# selecionar ipi: Operador para seleccionar los elementos del sistema IPI Mocap
class OBJECT_OT_SELECIONAR_IPI(bpy.types.Operator): 
    """Crea al esqueleto selecionado su sistema de control FK"""
    
    bl_idname = "object.selecionar_ipi" 
    bl_label = "Seleciona sistema IPI" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    # Código Python que se ejecuta al presionar el botton
    def execute(self, context): 
        self.report({'INFO'}, "HOLA MUNDO") 
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
        esqueleto = obj.data
        
        borrar_huesos_prefijo(esqueleto,"FK.")
      
        #borrado de constraints         
        bpy.ops.object.mode_set(mode='POSE') 
        
        NOMBRE_CONSTRAINT = "FK_ROTATION"
        esqueleto = context.object
        eliminar_constraint(NOMBRE_CONSTRAINT,esqueleto,"DF.")
        
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
        esqueleto = obj.data
        
        borrar_huesos_prefijo(esqueleto,"IK.")
      
        #borrado de constraints         
        bpy.ops.object.mode_set(mode='POSE') 
        
        NOMBRE_CONSTRAINT = "IK_ROTATION"
        esqueleto = context.object
        eliminar_constraint(NOMBRE_CONSTRAINT,esqueleto,"DF.")
        
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
        esqueleto = obj.data
        borrar_huesos_prefijo(esqueleto,"IPI.")
      
        #borrado de constraints         
        bpy.ops.object.mode_set(mode='POSE') 
        
        NOMBRE_CONSTRAINT = "IPI_ROTATION"
        esqueleto = context.object
        eliminar_constraint(NOMBRE_CONSTRAINT,esqueleto,"DF.")
        
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
    DATA_PT_UI_Control_FK,
    DATA_PT_UI_SELECIONAR_SISTEMA,
    
    
    OBJECT_OT_Generar_sistema_FK,
    OBJECT_OT_Generar_sistema_IK,
    OBJECT_OT_Generar_sistema_IPI,
    
    OBJECT_OT_SELECIONAR_FK,
    OBJECT_OT_SELECIONAR_IPI,
    OBJECT_OT_SELECIONAR_IK,
    
    OBJECT_OT_ELIMINAR_FK,
    OBJECT_OT_ELIMINAR_IK,
    OBJECT_OT_ELIMINAR_IPI,
    
    ARMATURE_GENERAL_PROPIEDADES,
    ARMATURE_SISTEMA_FK_PROPIEDADES,
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