🇪🇸 **Gestor de Gastos en Telegram - Bot**

¡Bienvenido a la documentación para el Bot de Gestión de Gastos en Telegram, una poderosa herramienta diseñada para ayudar a los usuarios a gestionar eficientemente sus gastos personales, categorizar transacciones y obtener información a través de visualizaciones. Este documento te proporcionará una descripción general de las funcionalidades del proyecto, el proceso de inicialización, la arquitectura del proyecto y cómo utilizar el bot de manera efectiva.

📚 Índice

- Introducción
- Comenzando
- Arquitectura del Proyecto y Relaciones de Clases
- Modo de Uso
- Contribuciones

🎉 **Introducción**

El Bot de Gestión de Gastos en Telegram ofrece las siguientes funcionalidades principales:

- Seguimiento de Gastos: Los usuarios pueden agregar y categorizar sus gastos personales a través de interacciones con el bot.
- Visualización de Datos: El bot genera gráficos e tablas informativas para que los usuarios visualicen sus gastos y patrones de gasto.
- Soporte Multiusuario: El bot gestiona eficientemente interacciones con múltiples usuarios simultáneamente, cada uno identificado por su chatID único.

🚀 **Comenzando**

Para inicializar el proyecto, sigue estos pasos:

1. Clona el repositorio en tu máquina local.

```
git clone https://github.com/cmd69/teleBot.git
```

2. Instala las dependencias necesarias usando pip install -r requirements.txt.

3. Configura la API del Bot de Telegram: Obtén un token de la API del Bot de Telegram creando un nuevo bot con el BotFather. Asegúrate de habilitar los permisos necesarios para el bot.

4. Renombra el archivo .env.example a .env en el directorio raíz.

5. Abre el archivo .env y agrega tu token del Bot de Telegram y otros detalles de configuración.

6. Inicia el bot con python3 telebot.py.

📝 **Modo de Uso**

1. Inicia un chat con el Bot de Gestión de Gastos en Telegram con el comando /start.
2. Sigue el menú para agregar tus gastos, categorizarlos y proporcionar detalles relevantes.
3. Interactúa con los menús y comandos del bot para ver gráficos y tablas que muestran tus hábitos de gasto.

🏗️ **Arquitectura del Proyecto y Relaciones de Clases**

El proyecto está organizado en varios módulos clave:

- Managers: Responsables de gestionar diversos aspectos de la aplicación, incluida la gestión de usuarios, operaciones de base de datos y manipulación de datos.
- Generators: Responsables de generar componentes interactivos como teclados y gráficos para la interfaz de usuario.
- Handlers: Gestionan las interacciones de los usuarios e implementan varias funcionalidades del bot.
- telebot.py: El punto de entrada principal que configura el bot, inicializa managers y generators, y comienza a recibir actualizaciones.
- streamlit_app.py: Ejecuta la aplicación Streamlit para la visualización de datos utilizando la clase ChartsGenerator.
- bot_setup.py: Maneja la carga de configuraciones e inicializa el bot, el despachador, los managers y los generators.

🤝 **Contribuciones**

¡Damos la bienvenida a contribuciones de la comunidad! Si estás interesado en mejorar el bot, siéntete libre de enviar pull requests o abrir problemas.

Gracias por utilizar el Bot de Gestión de Gastos en Telegram. Si encuentras algún problema o tienes preguntas, no dudes en contactarnos o abrir un issue en el repositorio. 🙌

---

🇺🇸 **Telegram Expense Manager Bot**

Welcome to the documentation for the Telegram Expense Manager Bot, a powerful tool designed to help users efficiently manage personal expenses, categorize transactions, and gain insights through visualizations. This document will provide you with an overview of the project's functionality, initialization process, project architecture, and how to use the bot effectively.

📚 **Table of Contents**

- Introduction
- Getting Started
- Project Architecture and Class Relationships
- Usage Guide
- Contributions

🎉 **Introduction**

The Telegram Expense Manager Bot offers the following core functionalities:

- Expense Tracking: Users can add and categorize their personal expenses through interactions with the bot.
- Data Visualization: The bot generates insightful charts and tables for users to visualize their expenses and spending patterns.
- Multi-User Support: The bot efficiently manages interactions with multiple users simultaneously, each identified by their unique chatID.

🚀 **Getting Started**

To initialize the project, follow these steps:

1. Clone the repository to your local machine.

```
git clone https://github.com/cmd69/teleBot.git
```

2. Install the required dependencies using pip install -r requirements.txt.

3. Set Up Telegram Bot API: Obtain a Telegram Bot API token by creating a new bot using the BotFather. Make sure to enable the necessary permissions for the bot.

4. Rename the .env.example file to .env in the root directory.

5. Open the .env file and add your Telegram Bot token and other configuration details.

6. Start the bot with python3 telebot.py.

📝 **Usage Guide**

1. Start a chat with the Telegram Expense Manager Bot with the command /start.
2. Follow the menu to add your expenses, categorize them, and provide relevant details.
3. Interact with the bot's menus and commands to view charts and tables showcasing your spending habits.

🏗️ **Project Architecture and Class Relationships**

The project is organized into several key modules:

- Managers: Responsible for managing various aspects of the application, including user management, database operations, and data handling.
- Generators: Responsible for generating interactive components like keyboards and charts for the user interface.
- Handlers: Manage user interactions and implement various functionalities of the bot.
- telebot.py: The main entry point that sets up the bot, initializes managers and generators, and starts polling for updates.
- streamlit_app.py: Runs the Streamlit application for data visualization using the ChartsGenerator class.
- bot_setup.py: Handles loading settings and initializing the bot, dispatcher, managers, and generators.

🤝 **Contributions**

We welcome contributions from the community! If you're interested in improving the bot, feel free to submit pull requests or open issues.

Thank you for using the Telegram Expense Manager Bot. If you encounter any issues or have questions, please don't hesitate to contact us or open an issue in the repository. 🙌
