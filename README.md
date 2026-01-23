# QA Project - Urban Routes - Sprint 9

Descripción del proyecto

-Este proyecto consiste en la automatización de pruebas para la aplicación Urban Routes, una plataforma para solicitar taxis y pedir extras durante el viaje, como manta, pañuelos y helados.  
Cada prueba se genera de manera independiente siguiendo la estructura POM, asegurando que no interfieran con las demás.  

En las pruebas se verifican validaciones y funcionalidades en:
- Configuración de direcciones de origen y destino.
- Selección de tarifa Comfort.
- Registro y confirmación del número de teléfono.
- Agregado y verificación de tarjeta de pago.
- Envío de mensajes al conductor.
- Selección de extras (manta, pañuelos y helados).
- Apertura del modal de búsqueda de taxi.

Fuente de documentación

-La información utilizada para este proyecto se tomó de la aplicación web de Urban Routes, incluyendo los elementos interactivos y flujos principales de pedido de taxi. También se utilizó la función `retrieve_phone_code()` para capturar los códigos de confirmación del teléfono necesarios durante la automatización.

Tecnologías y herramientas utilizadas
- Python 3  
- Selenium WebDriver  
- Pytest  
- Git  
- GitHub  

Como ejecutar las pruebas:

-Comprobar tener instalado Python 3
-Clonar el repositorio y entrar a la carpeta del proyecto
-Instalar: pip install pytest requests
-Ejecutar las pruebas con el comando "Pytest"



 