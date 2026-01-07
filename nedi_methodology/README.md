# Metodología NEDI - Documentación y Guía de Uso

## ¿Qué es este Addon?
El módulo `nedi_methodology` es una herramienta diseñada para gestionar proyectos de implementación de Odoo bajo la metodología "NEDI 2026". Su objetivo es estandarizar y automatizar los pasos necesarios para llevar un proyecto desde la venta hasta el cierre.

### Funcionalidades Principales Actuales:
1.  **Proyectos de Metodología**: Un contenedor principal para cada cliente/implementación.
2.  **Fases**: El proyecto avanza por fases:
    *   **Fase 0 - Familiarización**: Tareas iniciales, kick-off, setup básico.
    *   **Fase 1 - Descubrimiento**: Cuestionarios y levantamiento de requerimientos.
    *   **Fase 2 - Implementación MVP**: Configuración y desarrollo.
    *   **Fase 3 - Optimización**: Mejoras y capacitación.
    *   **Fase 4 - Cierre**: Entrega final.
3.  **Cuestionarios**: Formularios predefinidos para recolectar información del cliente. Se pueden filtrar por industria (ej. Construcción).
4.  **Generación Automática**: Al crear un proyecto, el sistema intenta crear tareas y asignar cuestionarios automáticamente.

---

## Tu Plan de Trabajo (Cómo iniciar)

Como eres nuevo en esto, sigue este flujo paso a paso para probar y utilizar el addon:

### Paso 1: Configuración Inicial
1.  Asegúrate de que el módulo esté instalado.
2.  Ve a **Metodología > Configuración > Plantillas de Tareas**. Revisa que existan plantillas para la "Fase 0". Si no hay, crea algunas (ej. "Reunión de Kick-off", "Creación de Base de Datos").
3.  Ve a **Metodología > Configuración > Plantillas de Cuestionarios**. Asegúrate de que existan plantillas y que algunas tengan el campo "Industrias" configurado (ej. una para "Construcción").

### Paso 2: Crear un Nuevo Proyecto (El Flujo Ideal)
1.  Ve al menú **Metodología > Proyectos**.
2.  Haz clic en **Nuevo**.
3.  Llena los datos:
    *   **Nombre**: Ej. "Implementación Constructora X".
    *   **Cliente**: Selecciona un cliente.
    *   **Paquete de Horas**: Selecciona uno (ej. H80).
    *   **Industria**: Selecciona "Construcción" (esto es clave para los cuestionarios).
    *   **Proyecto Odoo**: **[MEJORA]** Dejar esto vacío. El sistema ahora creará uno automáticamente por ti.
4.  Haz clic en **Guardar**.

### Paso 3: Verificar la Automatización
Una vez guardado, revisa los "smart buttons" (los botones arriba a la derecha de la ficha del proyecto):
1.  **Tareas**: Deberías ver un número (ej. "3 Tareas"). Haz clic y verifica que son las tareas de la Fase 0.
2.  **Cuestionarios**: Deberías ver un número. Haz clic y verifica que se crearon los cuestionarios específicos para Construcción.

### Paso 4: Trabajar los Cuestionarios
1.  Entra a un cuestionario desde el proyecto.
2.  Haz clic en **Iniciar** (cambia estado a "En Progreso").
3.  **[MEJORA]** En la pestaña "Respuestas", ahora podrás escribir directamente en las líneas sin abrir ventanas.
4.  Llena la información como si fueras el consultor entrevistando al cliente.
5.  Haz clic en **Completar** cuando termines.

---

## Resumen de Cambios Técnicos Recientes
Para cumplir con tus requerimientos, he realizado las siguientes modificaciones al código:

1.  **Automatización de Proyecto Odoo**:
    *   *Antes*: Si no elegías un proyecto existente, no se creaban tareas.
    *   *Ahora*: Si no eliges uno, el sistema crea un `project.project` nuevo automáticamente y lo enlaza. Esto dispara la creación inmediata de las tareas de familiarización.

2.  **Mejora en Cuestionarios**:
    *   *Antes*: Para escribir una respuesta de texto, tenías que abrir un popup.
    *   *Ahora*: La lista de preguntas es editable (`editable="bottom"`). Puedes escribir respuestas texto, seleccionar opciones o marcar casillas directamente en la tabla.

## Estado Actual de tu Tarea
*   [x] Análisis de código realizado.
*   [x] Plan de trabajo redactado (este documento).
*   [x] Mejoras de código implementadas (ver archivos modificados).
*   [ ] Pruebas finales (te toca realizar el Paso 2 en tu Odoo local).
