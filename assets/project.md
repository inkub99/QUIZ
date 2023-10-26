# PyConnect2023 Construyendo soluciones de GenAI para transformación digital

Este repositorio contiene el contenido relacionado con la charla:

`Construyendo soluciones con Generative AI para la transformación digital`

Por: Kevin Knights

**Contenido**

1. [Resumen](#resumen)
2. [Comenzando](#comenzando)
3. [Contribuyendo](#contribuyendo)

---

![image](https://github.com/kevinknights29/PyConnect2023_GenAI_Digital_Transformation/assets/74464814/505dbbbb-fda8-4e52-a1a2-ac9b724cd72f)

## Resumen

Quería mostrar el verdadero valor de las aplicaciones GenAI.
y la mejor manera fue crear una aplicación de chatbot para toda la conferencia.

### Idea

Cree una aplicación para apoyar a los participantes/asistentes del evento.

### Objetivo de negocio

Incrementar la satisfacción de los participantes/asistentes (CSAT = satisfacción del cliente).

### Requisitos

- GUI (interfaz gráfica).
- Base de conocimientos de conferencia.
- Personalización (experiencia única para cada usuario).

### Objetivo de GenAI (ML)

Maximice la experiencia de los participantes/asistentes.

### Tecnologías

- LangChain
- Streamlit
- Weaviate
- OpenAI

![image](https://github.com/kevinknights29/PyConnect2023_GenAI_Digital_Transformation/assets/74464814/9eb34254-1686-4925-89e8-083376807e6c)

### Recopilación de datos

Se recopiló toda la información de texto para cada sesión en el calendario.

#### Contenido de la agenda

![image](https://github.com/kevinknights29/PyConnect2023_GenAI_Digital_Transformation/assets/74464814/6bd6dc82-3498-496e-9967-20b133a8a3d7)

#### Ejemplo del contenido de una sesión

![image](https://github.com/kevinknights29/PyConnect2023_GenAI_Digital_Transformation/assets/74464814/d51c8777-155d-4049-baae-26e3179ca84e)

#### Almacenamiento de datos

Con respecto a las tiendas de vectores, seleccioné weaviate porque son de código abierto y ofrecen un excelente nivel gratuito.

Para crear una cuenta visita: [Weaviate - Homepage](https://weaviate.io/)

![image](https://github.com/kevinknights29/PyConnect2023_GenAI_Digital_Transformation/assets/74464814/95412eb5-f4f3-4c0b-a94f-46f7a82701d8)

### Selección de modelo

Seleccioné OpenAI como proveedor de servicios LLM porque ofrecen una muy buena relación calidad/precio.

- gpt-3.5-turbo
- incrustación de texto-ada-002

Como referencia, alrededor de 750 palabras predichas por `gpt-3.5-turbo` cuestan 0,002 USD.

## Empezando

### Configuración

Crea el entorno virtual con:

```bash
python -m venv .venv
```

Luego actívalo con:

```bash
source .venv/bin/activate
```

Finalmente, instale dependencias con:

```bash
pip install -r requirements.txt
```

### Uso local

Para ejecutar la aplicación Streamlit localmente, utilice:

```bash
streamlit run app.py
```

Esto abrirá automáticamente una ventana en su navegador web predeterminado.

#### ¡Diviértete!

![image](https://github.com/kevinknights29/PyConnect2023_GenAI_Digital_Transformation/assets/74464814/04385ebb-2d07-4a41-8823-2c156dfa1a15)

## Contribuyendo

### Instalación de pre-commit

La libreria de pre-commit ya forma parte de las dependencias de este proyecto.
Si desea instalarlo de forma independiente, ejecute:

```bash
pip install pre-commit
```

Para activar la pre-commit, ejecute los siguientes comandos:

- Instalar ganchos de Git:

```bash
pre-commit install
```

- Actualizar ganchos actuales:

```bash
pre-commit autoupdate
```

Para probar su instalación de pre-commit utiliza:

```bash
pre-commit run --all-files
```
