<div align="center">

<img src="https://img.shields.io/badge/UIS-Universidad%20Industrial%20de%20Santander-1B5E20?style=for-the-badge" alt="UIS"/>

# 📡 CommII_A1_A1E


### Comunicaciones II — 27145
**Escuela de Ingenierías Eléctrica, Electrónica y de Telecomunicaciones**
*Facultad de Ingenierías Físico Mecánicas*

<img src="https://img.shields.io/badge/Rama-main-2ea44f?style=flat-square" />
<img src="https://img.shields.io/badge/GNU%20Radio-SDR-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Linux-Ubuntu-orange?style=flat-square&logo=linux&logoColor=white" />
<img src="https://img.shields.io/badge/Lenguaje-Python-yellow?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/status-en%20desarrollo-brightgreen?style=flat-square" />

*"Construimos Futuro"*

</div>

## 👥 Integrantes

| Nombre completo | Rol |
|---|---|
| Jarol Nicolás Molano López | Estudiante |
| William Camilo Motta Chacón | Estudiante |
| Juan Andrés Rojas Rueda | Estudiante |


> 💡 **Nota:** este README corresponde únicamente a la rama **`main`**. Cada rama de práctica (`Practica_1`, `Practica_2`, etc.) cuenta con su propio README donde se detalla el desarrollo específico de esa entrega.

---

## 📑 Tabla de contenido

- [Descripción del repositorio](#-descripción-del-repositorio)
- [Integrantes](#-integrantes)
- [Estructura de ramas](#-estructura-de-ramas)
- [Estructura de directorios](#-estructura-de-directorios)
- [Tecnologías y herramientas](#-tecnologías-y-herramientas)
- [Cómo clonar el repositorio](#-cómo-clonar-el-repositorio)
- [Flujo de trabajo (workflow) en Git](#-flujo-de-trabajo-workflow-en-git)
- [Buenas prácticas](#-buenas-prácticas)
- [Créditos](#-créditos)

---

## 📖 Descripción del repositorio

Este repositorio contiene el desarrollo práctico del curso **Comunicaciones II (27145)** de la **Universidad Industrial de Santander**, correspondiente al grupo **A1_A1E**. Aquí se documentan y almacenan los laboratorios, algoritmos y aplicaciones desarrolladas a lo largo del semestre, incluyendo:

- 🔧 Configuración inicial de Git/GitHub y gestión de la información (Laboratorio 1).
- 📻 Programación de bloques personalizados en **GNU Radio** para radio definida por software — *SDR* (Laboratorio 2 en adelante).
- 📊 Implementación de bloques de estadística, acumulador y diferenciador aplicados a señales reales.

Cada práctica realizada en el laboratorio se organiza en una rama independiente, y dentro de esa rama cada integrante desarrolla su propio trabajo en una subrama personal, tal como se describe más adelante.



## 🌳 Estructura de ramas

El repositorio sigue un modelo de ramas organizado por **práctica** y por **integrante**, de forma que el trabajo de cada persona sea trazable de manera independiente antes de integrarse a la rama principal de cada práctica.

```
main
 ├── Practica_1                 → Rama de "preproducción" del Laboratorio 2 (Práctica 1)
 │     ├── P1_Jarol             → Desarrollo individual de Jarol para la Práctica 1
 │     ├── P1_Juan              → Desarrollo individual de Juan para la Práctica 1
 │     └── P1_william           → Desarrollo individual de William para la Práctica 1
 │
 └── Practica_2                 → Rama de "preproducción" del Laboratorio 3 (Práctica 2)
       ├── P2_Jarol             → Desarrollo individual de Jarol para la Práctica 2
       ├── P2_Juan              → Desarrollo individual de Juan para la Práctica 2
       └── P2_Willi             → Desarrollo individual de William para la Práctica 2
```

### 🔎 ¿Qué contiene cada tipo de rama?

| Rama | Descripción |
|---|---|
| **`main`** | Rama principal y estable del repositorio. Contiene este README y sirve como base histórica del proyecto. |
| **`Practica_1` / `Practica_2`** | Ramas de integración por práctica. Son la **vista de preproducción** que revisa el docente: aquí cada integrante hace *merge* de su rama personal una vez su parte está lista. Contienen los directorios `GNURadio` e `Informe` con el desarrollo consolidado del grupo para esa práctica. |
| **`P{N}_Nombre`** | Ramas personales de trabajo (ej. `P1_Jarol`, `P2_Willi`). Contienen los **archivos temporales y de desarrollo individual** de cada integrante: flowgraphs de GNU Radio (`.grc`), bloques de Python en construcción, pruebas y avances propios antes de integrarlos a la rama de la práctica correspondiente. |



---

## 📁 Estructura de directorios

```
CommII_A1_A1E/
├── README.md
├── Practica_1/
│   ├── GNURadio/        → Flowgraphs (.grc) y bloques de Python
│   └── Informe/         → Informe en formato LaTeX
└── Practica_2/
    ├── GNURadio/
    └── Informe/
```

---

## 🛠 Tecnologías y herramientas

| Herramienta | Uso |
|---|---|
| ![Linux](https://img.shields.io/badge/-Linux%20Ubuntu-orange?logo=linux&logoColor=white) | Sistema operativo de trabajo |
| ![Git](https://img.shields.io/badge/-Git-F05032?logo=git&logoColor=white) | Control de versiones |
| ![GitHub](https://img.shields.io/badge/-GitHub-181717?logo=github&logoColor=white) | Alojamiento y gestión del repositorio |
| ![GNU Radio](https://img.shields.io/badge/-GNU%20Radio-5A5A5A) | Radio definida por software (SDR) |
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Bloques personalizados en GNU Radio |
| ![LaTeX](https://img.shields.io/badge/-LaTeX-008080?logo=latex&logoColor=white) | Redacción de informes |

---

## ⬇️ Cómo clonar el repositorio

### 1. Requisitos previos
- Tener `git` instalado en la terminal de Linux.
- Contar con un **Personal Access Token (classic)** de GitHub (necesario para autenticarse al hacer `push`).

### 2. Clonar usando HTTPS

```bash
git clone https://github.com/<usuario>/CommII_A1_A1E.git
```

### 3. Ingresar al directorio del proyecto

```bash
cd CommII_A1_A1E
```

### 4. Ver las ramas disponibles

```bash
git branch -a
```

### 5. Cambiar a la rama de la práctica que necesitas revisar

```bash
git checkout Practica_1
# o, para ver el trabajo individual de un integrante:
git checkout P1_Jarol
```

### 6. Mantener tu copia local actualizada

```bash
git pull
```

> 🔑 Al ejecutar `git push` por primera vez, Git pedirá usuario y contraseña: el **usuario** es tu usuario de GitHub y la **contraseña** es el *token* generado (no la contraseña de tu cuenta).

---

## 🔄 Flujo de trabajo (workflow) en Git

1. Cada práctica nueva parte de `main` y crea su rama `Practica_N`.
2. Dentro de `Practica_N`, cada integrante crea su propia subrama `PN_Nombre`.
3. Cada integrante trabaja y hace *commits* en **su propia subrama**:
   ```bash
   git add .
   git commit -m "Descripción del cambio"
   git push
   ```
4. Cuando su parte está lista, se hace **merge** de la subrama personal hacia la rama de la práctica correspondiente (`Practica_N`), que funciona como la versión de "preproducción" revisada por el docente.
5. Al finalizar el semestre, la rama `main` se mantiene como la rama estable de referencia del repositorio.

---

## ✅ Buenas prácticas

- Realizar *commits* pequeños y con mensajes descriptivos.
- No trabajar directamente sobre `main` ni sobre las ramas `Practica_N`; usar siempre la subrama personal.
- Actualizar (`git pull`) antes de empezar a trabajar cada sesión.
- Verificar con `git status` los cambios antes de cada `commit`.
- Mantener los archivos de cada práctica dentro de su directorio correspondiente (`GNURadio` / `Informe`).

---

## 🏫 Créditos

Proyecto desarrollado como parte del curso **Comunicaciones II (27145)** — Escuela de Ingenierías Eléctrica, Electrónica y de Telecomunicaciones, **Universidad Industrial de Santander (UIS)**.

<div align="center">

*Construimos Futuro* 🇨🇴

</div>
