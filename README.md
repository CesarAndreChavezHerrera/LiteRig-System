# LiteRig System

Este add-on para Blender est? dise?ado para la creaci?n de rigging personalizado en modelos de cuerpo **Low Poly y Medium Poly**. Genera un sistema de controles FK e IK simple, adem?s de incluir una base de controles faciales pensada principalmente para trabajar con **shape keys.**

Asimismo, se est? trabajando en la integraci?n de sistemas de control para animaciones provenientes de captura de movimiento **(mocap)**.


## Compatibilidad con sistemas de captura de movimiento

| Sistema de Mocap                  | Progreso | Estado |
| :--- | :---: | :---: |
| **iPi Motion Capture**            | 70%   | En desarrollo |
| **Mixamo**                        | 0%    | Pr?ximamente |
| **FreeMoCap**                     | 0%    | Pr?ximamente |
| **Rokoko**                        | 0%    | Por evaluar |
| **Plask.ai**                      | 0%    | Por evaluar |
| **DeepMotion**                    | 0%    | Por evaluar |
| **Xsens Animate**                 | 0%    | Por evaluar |
| **Seguimiento Inercial Gen?rico** | 0%    | Por evaluar |

---
<br><br><br>
# Nomenclatura

Siempre se comenzara escribiendo el prefijo que define que tipo de hueso es el que se esta usando luego la zona de control que controlara ese hueso y por ultimo el nombre que recibe el hueso


| Prefijo   | Zona de control   | nombre del hueso |
| :---      | :---              |:--- |
| DF.       | CABEZA.           |cabeza             |  

## 1.Prefijos de Funci?n y Tipo de Control

| Prefijo | Descripci?n / Uso |
| :--- | :--- |
| `PIN.`        | Huesos de fijaci?n o anclaje (*Pins*) |
| `PROP.`       | Huesos para utiler?a y accesorios (*Props*) |
| `HAIR.`       | Huesos para el cabello |
| `ROPA.`       | Huesos para vestimenta y telas |
| `DF.`         | Huesos que deforman la malla |
| `FK.`         | Controles de **Forward Kinematics** |
| `IK.`         | Controles y estructuras de **Inverse Kinematics** |
| `IK.CONTROL.` | Controles principales para el sistema IK |
| `IPI.`        | Huesos/Objetivos para integraci?n con iPi MoCap |



## 2. Prefijos de Zonas del Cuerpo y Rostro

| Zona / Lado | Prefijo | Descripci?n |
| :--- | :--- | :--- |
| **Cabeza** | `CABEZA.` | Define la estructura craneal principal; bajo el control maestro de la cabeza. |
| **Rostro** | `CEJAS.` | Controles y huesos de las cejas; subordinados al control principal de la cabeza o rostro. |
| | `OJOS.` | Controles y huesos de los ojos; subordinados al control principal de la cabeza o seguimiento (*Look-At*). |
| | `BOCA.` | Controles y huesos de la boca/labios; subordinados al control de la cabeza o mand?bula. |
| **Torso** | `ESPALDA.` | Columna y torso; bajo el control del torso/cadera (*Root/Spine*). |
| **Extremidades Izquierdas** | `BRAZO_L.` | Brazo izquierdo; subordinado a los controles de hombro y brazo. |
| | `MANO_L.` | Mano y dedos izquierdos; subordinados al control de mu?eca/mano. |
| | `PIERNA_L.` | Pierna izquierda; subordinada a los controles de cadera y pierna. |
| | `PIE_L.` | Pie izquierdo; subordinado al control de tobillo/pie. |
| **Extremidades Derechas** | `BRAZO_R.` | Brazo derecho; subordinado a los controles de hombro y brazo. |
| | `MANO_R.` | Mano y dedos derechos; subordinados al control de mu?eca/mano. |
| | `PIERNA_R.` | Pierna derecha; subordinada a los controles de cadera y pierna. |
| | `PIE_R.` | Pie derecho; subordinado al control de tobillo/pie. |