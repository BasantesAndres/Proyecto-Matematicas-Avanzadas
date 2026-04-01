# Comparative Numerical Study of Euler, RK4, and RKF45

> Proyecto académico de **Matemáticas Avanzadas** orientado al análisis, implementación y comparación de métodos numéricos para resolver problemas de valor inicial en ecuaciones diferenciales ordinarias (EDO).

---

## Resumen

En este proyecto se implementaron **desde cero** tres métodos clásicos para resolver ecuaciones diferenciales ordinarias:

- **Euler explícito**
- **Runge–Kutta clásico de orden 4 (RK4)**
- **Runge–Kutta–Fehlberg 4(5) (RKF45)** con paso adaptativo

El objetivo principal fue comparar su comportamiento en términos de:

- **precisión numérica**
- **orden de convergencia**
- **eficiencia computacional**
- **adaptación del tamaño de paso**
- **desempeño en problemas sintéticos y modelos aplicados a computación**

Además del desarrollo del código, el proyecto incluyó:

- generación automática de **gráficas** y **archivos CSV**
- organización modular del código
- construcción de un **reporte formal en LaTeX/Overleaf**
- preparación de material de apoyo para la **defensa oral**

---

## Objetivos del proyecto

- Implementar métodos numéricos para PVI en EDO, tanto para problemas **escalares** como para **sistemas**.
- Medir y comparar el error usando distintas métricas.
- Estudiar el comportamiento de los métodos al refinar la malla temporal.
- Analizar la relación entre **error** y **número de evaluaciones de la función**.
- Aplicar los métodos a modelos con interpretación real en computación.

---

## Métodos implementados

### 1. Euler explícito
Método de paso fijo, simple y económico por iteración.

**Ventajas**
- Fácil de implementar.
- Bajo costo por paso.
- Útil como referencia base.

**Desventajas**
- Orden global 1.
- Mayor acumulación de error.
- Menor estabilidad cuando el problema cambia rápido.

### 2. RK4
Método clásico de cuarto orden que usa cuatro pendientes intermedias por paso.

**Ventajas**
- Alta precisión con paso fijo.
- Muy buen balance entre costo y exactitud.
- Excelente comportamiento en problemas suaves.

**Desventajas**
- Requiere más evaluaciones de la función por paso.

### 3. RKF45
Método adaptativo que estima el error local y ajusta automáticamente el tamaño de paso.

**Ventajas**
- Alta precisión.
- Ajuste automático del paso.
- Muy útil cuando la solución cambia bruscamente o tiene regiones con distinta dificultad.

**Desventajas**
- Implementación más compleja.
- Requiere lógica adicional de aceptación/rechazo de pasos.

---

## Problemas estudiados

### Problemas sintéticos

#### Problema 2

y'(t) = k / (1 + (k(t-1))²), con k = 100.

- Se usó para estudiar transición brusca alrededor de **t = 1**.
- Fue clave para el experimento de **estabilidad** y para mostrar la ventaja del paso adaptativo.

#### Problema 3

Oscilador armónico amortiguado:

- x'(t) = y(t)
- y'(t) = -x(t) - 0.2y(t)

- Se usó para validar el código en **sistemas de EDO**.
- Permitió comparar error de fase y amplitud en una dinámica oscilatoria.

---

### Modelos aplicados a computación

#### Problema 4 — Propagación de malware

I'(t) = βI(1 - I) - γI

Se analizaron tres configuraciones:

- β = 1.5, γ = 0.5
- β = 1.0, γ = 0.5
- β = 0.8, γ = 0.6

Este modelo representa la competencia entre:

- propagación de infección
- recuperación o limpieza de equipos

#### Problema 5 — Balanceo de carga entre dos servidores

Sistema:

- x'(t) = -ax(t) + by(t) + f(t)
- y'(t) = cx(t) - dy(t)

Casos estudiados:

- **Entrada senoidal**: f(t) = sin(t)
- **Entrada tipo pulso**: f(t) = 2 para 0 ≤ t ≤ 5, y 0 para t > 5

Este modelo representa la evolución de carga en dos servidores acoplados.

---

## Experimentos realizados

### Comparación de soluciones
Se comparó la solución exacta o de referencia con las aproximaciones numéricas.

### Error puntual
Se evaluó cómo evoluciona el error a lo largo del tiempo.

### Convergencia
Para Euler y RK4 se usaron:

- N = 50, 100, 200, 400, 800

con el fin de estimar experimentalmente el orden de convergencia.

### Eficiencia
Se construyeron diagramas de:

- error vs número de evaluaciones de la función

para comparar el costo real de cada método.

### Pasos adaptativos
En RKF45 se analizó cómo el método modifica el tamaño de paso según la dinámica del problema.

### Plano fase
Para el problema de balanceo de carga se generó la trayectoria en el plano:

- (x(t), y(t))

---

## Resultados principales

- **Euler** fue el método menos preciso en todos los casos.
- **RK4** mostró un comportamiento muy sólido y consistente con su orden teórico.
- **RKF45** fue el método más flexible gracias al control adaptativo del paso.
- En problemas con cambios bruscos, como el Problema 2, el enfoque adaptativo fue especialmente útil.
- En los modelos aplicados, las soluciones numéricas mostraron excelente acuerdo con las soluciones de referencia.

---

## Arquitectura del proyecto

El proyecto fue organizado de forma modular para facilitar:

- mantenimiento
- reutilización del código
- claridad en la defensa del trabajo
- generación automática de resultados

### Estructura general

```text
Proyecto M,Avanzadas/
│
├── euler.py
├── rk4.py
├── rkf45.py
├── problems.py
├── reference_solutions.py
├── metrics.py
├── plots.py
├── experiments.py
├── main.py
├── test_problem1.py
├── Reporte final Matematicas Avanzadas Basantes Andres.pdf
│
└── outputs/
    ├── problem2/
    ├── problem3/
    ├── problem4_beta_1.5_gamma_0.5/
    ├── problem4_beta_1.0_gamma_0.5/
    ├── problem4_beta_0.8_gamma_0.6/
    ├── problem5_sin/
    └── problem5_pulse/
```

---

## Descripción de archivos

<details>
<summary><strong>euler.py</strong></summary>

Implementa el método de Euler de paso fijo para problemas escalares y sistemas.

</details>

<details>
<summary><strong>rk4.py</strong></summary>

Implementa el método clásico de Runge–Kutta de orden 4.

</details>

<details>
<summary><strong>rkf45.py</strong></summary>

Implementa el método adaptativo RKF45 con historial de pasos, conteo de evaluaciones y control de error.

</details>

<details>
<summary><strong>problems.py</strong></summary>

Define los problemas numéricos y modelos aplicados usados en el proyecto.

</details>

<details>
<summary><strong>reference_solutions.py</strong></summary>

Construye soluciones exactas o de referencia de alta precisión para comparar los métodos.

</details>

<details>
<summary><strong>metrics.py</strong></summary>

Calcula error puntual, norma infinito, norma discreta L2 y estimación de órdenes de convergencia.

</details>

<details>
<summary><strong>plots.py</strong></summary>

Genera todas las figuras del proyecto:

- soluciones
- error puntual
- convergencia
- eficiencia
- pasos adaptativos
- plano fase

</details>

<details>
<summary><strong>experiments.py</strong></summary>

Coordina los experimentos numéricos y guarda automáticamente las gráficas y tablas.

</details>

<details>
<summary><strong>main.py</strong></summary>

Punto de entrada principal del proyecto. Ejecuta todos los experimentos y llena la carpeta `outputs/`.

</details>

---

## Carpeta `outputs/`

La carpeta `outputs/` contiene todos los resultados generados automáticamente:

- imágenes `.png`
- tablas `.csv`

Cada subcarpeta corresponde a un problema específico.

### Ejemplos de archivos generados

- `problem2_solution_euler.png`
- `problem2_solution_rk4.png`
- `problem2_solution_rkf45.png`
- `problem2_pointwise_error_euler.png`
- `problem3_convergence.png`
- `problem3_efficiency.png`
- `problem5_sin_phase_plane.png`
- `problem4_beta_1.5_gamma_0.5_adaptive_steps.csv`

Esto permitió integrar el código con el informe de forma limpia y reproducible.

---

## Cómo ejecutar el proyecto

### 1. Clonar o descargar el repositorio
```bash
git clone <repo-url>
cd Proyecto-Matematicas-Avanzadas
```

### 2. Instalar dependencias
```bash
pip install numpy matplotlib
```

### 3. Ejecutar el archivo principal
```bash
python main.py
```

### 4. Revisar resultados
Todos los resultados aparecerán automáticamente dentro de la carpeta:

```text
outputs/
```

---

## Flujo de trabajo del proyecto

```text
Definir problema
   ↓
Resolver con Euler / RK4 / RKF45
   ↓
Construir solución exacta o de referencia
   ↓
Calcular errores
   ↓
Generar gráficas
   ↓
Exportar CSV y PNG
   ↓
Integrar en el informe final
```

---

## Tecnologías utilizadas

- **Python**
- **NumPy**
- **Matplotlib**
- **LaTeX / Overleaf**
- **GitHub**

---

## Entregables generados

- Código fuente completo del proyecto
- Carpeta `outputs/` con gráficas y tablas
- Informe final en PDF
- Resumen para defensa oral
- README profesional para documentación del repositorio

---

## Aportes del proyecto

Este trabajo no solo consistió en programar métodos numéricos, sino también en:

- comprender su fundamento teórico
- verificar experimentalmente su orden de convergencia
- comparar su eficiencia real
- aplicarlos en modelos con interpretación en computación
- documentar todo el proceso de forma académica y profesional

---

## Conclusión

Este proyecto demuestra que la elección del método numérico depende del equilibrio entre:

- simplicidad
- precisión
- costo computacional
- adaptabilidad

**Euler** funciona como línea base y referencia pedagógica.  
**RK4** ofrece un excelente compromiso entre costo y precisión.  
**RKF45** resulta especialmente valioso cuando la solución presenta comportamientos locales complejos y se necesita un control más inteligente del tamaño de paso.

---

## Autor

**Andres Basantes**  
Proyecto de Matemáticas Avanzadas  
Yachay Tech University

---

## Vista rápida del proyecto

<details>
<summary><strong>¿Qué hace especial a este repositorio?</strong></summary>

- Implementación desde cero de tres métodos clásicos
- Comparación teórica y experimental
- Aplicación en problemas reales inspirados en computación
- Resultados automatizados y organizados
- Documentación lista para defensa, informe y portafolio

</details>

