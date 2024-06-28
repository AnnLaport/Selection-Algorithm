# Selection-Algorithm
Algoritmo de selección para agendar entrevistas con clientes.

Instrucciones:
  - Ejecutar el programa usando el comando "py selection_algorithm.py"
  - Se solicitan el par de coordenadas de la oficina (latitud, longitud) en ese orden.
  - Se ingresan las coordenadas y se generara el json "selectedClients.json" con los 10 clientes seleccionados
  - Nota: "generate_data.py", se utiliza para generar los datos de prueba (taxpayers.json)

Explicación: 

Una empresa tiene una lista de clientes con información sobre su ubicación y comportamiento.
La persona encargada de agendar citas para atender a estos clientes pierde mucho tiempo tratando de contactarlos sin éxito.

  1. Este algoritmo pide la ubicación en coordenadas de la oficina de la empresa como parámetro de entrada: latitud y longitud
  2. Evalúa la información de los usuarios, considerando los siguientes porcentajes para cada rubro:
     
     + 10% Ubicación
     + 10% Edad del cliente
     
     Datos de comportamiento:
     
     + 30% Ofertas aceptadas para salir de la lista de espera
     + 30% Ofertas rechazadas para salir de la lista de espera
     + 20% Tiempo promedio de respuesta de la llamada (en segundos)
     
  4. Se le asigna una calificación a cada cliente por cada rubro. Guardándose estas calificaciones en un arreglo de objetos.
  5. La calificación se asigna tomando como referencia el valor más indicado de los clientes como el 100%. Por ejemplo. La ubicación del cliente que vive más cerca
     de las coordenadas de la oficina que se ingresaron, representa el 100% de la calificación (Ubicación: 10%). A partir de aquí se le asigna una calificación al
     resto de clientes en este rubro.
  6. Se obtiene la media de cada uno de los rubros de los datos de comportamiento. Los clientes que tengan pocos datos de comportamiento (menores a la media) tendrán
     asignada una mayor prioridad para ser elegidos. La prioridad es de 0 a 3, aumentando en relación al número de rubros donde los datos de comportamiento del cliente
     son mayores a la media, por lo tanto, la prioridad más alta para ser seleccionado es 0.
  7. Se suman las calificaciones de todos los rubros por cliente, asignandoles una calificación general. También se les asigna su prioridad dependiendo la media de los
     datos calculada anteriormente.
  8. Se ordenan los clientes de forma descendente tomando en cuenta su calificación general. Se toman los 10 primeros con la calificación más alta y prioridad 0 y se
     se genera el archivo "SelectedClients.json" con la lista de los clientes seleccionados
