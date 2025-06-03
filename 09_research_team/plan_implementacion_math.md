# Plan de Implementación: Ciclo Evolutivo Multi-Agente para math_debug_team.py

## Objetivo
Diseñar e implementar un ciclo evolutivo en el equipo `math_debug_team.py` para mejorar la calidad de las soluciones matemáticas a través de rondas de generación, evaluación, selección y mejora de propuestas, inspirados en los enfoques Darwin/Gödel Machine y AlphaEvolve.

---

## Fases del Ciclo Evolutivo

### 1. Generación
- Cada agente genera una propuesta o solución independiente al problema matemático planteado.

### 2. Evaluación y Selección
- Un agente moderador o auditor evalúa todas las propuestas.
- Se seleccionan las mejores propuestas según criterios definidos (rigor, claridad, originalidad, utilidad, etc).

### 3. Mutación y Combinación
- Las propuestas seleccionadas pueden ser mejoradas, modificadas o combinadas por los agentes, generando nuevas variantes.
- Se pueden mezclar ideas de diferentes agentes para crear soluciones híbridas.

### 4. Iteración
- El ciclo se repite un número fijo de veces (por ejemplo, 2-3 rondas) o hasta alcanzar un criterio de calidad.
- Al final, el moderador sintetiza la mejor solución o informe final.

---

## Implementación Inicial

1. **Configurar el equipo para trabajar en rondas (generaciones evolutivas).**
2. **En cada ronda:**
   - Todos los agentes generan una respuesta a la misma pregunta.
   - El moderador evalúa y selecciona 1-2 propuestas destacadas.
   - Los agentes reciben las propuestas seleccionadas y pueden mejorarlas, combinarlas o mutarlas.
   - Repetir el ciclo 2-3 veces.
3. **Síntesis final:** El moderador presenta la mejor solución y explica el proceso evolutivo seguido.

---

## Consideraciones Técnicas
- Utilizar la memoria persistente para guardar propuestas y evaluaciones de cada ronda.
- Instrucciones dinámicas: Los agentes deben saber cuándo están en una ronda inicial (generar propuesta) o de mejora (mejorar/combinarlas).
- Mostrar al usuario el proceso evolutivo y las mejoras ronda a ronda.
- Dejar el sistema abierto para futuras mejoras: automatización de selección, mutación más sofisticada, métricas cuantitativas, etc.

---

## Siguientes Pasos
1. Implementar la lógica de rondas en `math_debug_team.py`.
2. Adaptar las instrucciones de los agentes para el ciclo evolutivo.
3. Probar el sistema con ejemplos concretos.
4. Documentar el proceso y resultados en este archivo.

---

**Última actualización:** 2025-06-03
