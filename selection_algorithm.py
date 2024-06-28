#The function inputs must been the location (altitude, longitud) and output the 10 clients selected
#Each client must have their computed score.
#Clients with little behavior data should have priority
#The 10 clients selected must have the best score and the highest priority
#the score is defined by
###########################################################
#                                                         #
#   age : 10%                                             #
#   distance to office : 10%                              #
#   Numbre of accepted offers: 30%                        #
#   Numbre of cancelled offers: 30%                       #
#   reply time: 20%                                       #
#                                                         #
###########################################################
#Instrucciones-----------------------------------------------------------------------------------------------#
#Ejecutar el programa usando el comando "py selection_algorithm.py"
#Se solicitan el par de coordenadas de la oficina (latitud, longitud) en ese orden.
#Se ingresan las coordenadas y se generara el json "selectedClients.json" con los 10 clientes seleccionados
#------------------------------------------------------------------------------------------------------------#
import json
import math


#La información para probar el programa se obtiene de 'taxpayers.json'
with open('taxpayers.json') as clientsdata:
    client= json.load(clientsdata)

#Se piden las coordenadas de la oficina
    officelatitude=float(input("Ingrese latitud:"));
    officelongitud=float(input("Ingrese longitud:"));

#Función para calcular distancia entre oficina y ubicación del cliente
    def distanceOffice(x1, y1, x2, y2):
        return math.sqrt((x2-x1)**2+(y2-y1)**2)
    
#Se define el mayor valor de cada rubro, ya que se utilizará para obtener lo que representa el 100% de su puntuación
#En algunos el 100% será en relación al mayor valor (ofertas aceptadas) o menor valor (distancia)
    MajorAge=0;
    mediaBehaviorAO=0;
    mediaBehaviorCO=0;
    mediaBehaviorART=0;
    majorDistance=0;
    majorART=0;
    majorAO=0;
    majorRO=0;
    percentages=[];
    clients_number=len(client);
    for i in range(clients_number):
        #Calcular cual es el mayor valor en cuanto a edad
        if(client[i]['age']>MajorAge):
            MajorAge=client[i]['age'];
        #Calcular cual es el mayor valor en cuanto a distancia
        currentdistance=distanceOffice(officelatitude, officelongitud, 
                             float(client[i]['location']['latitude']),
                             float(client[i]['location']['longitude']))              
        if(currentdistance>majorDistance):
            majorDistance=currentdistance;
        #Calcular cual es el mayor valor en cuanto a ofertas aceptadas
        if(client[i]['accepted_offers']>majorAO):
            majorAO=client[i]['accepted_offers']
        #Determinar cual es el mayor valor en cuanto a ofertas rechazadas
        if(client[i]['canceled_offers']>majorRO):
            majorRO=client[i]['canceled_offers']
        #Determinar cual es el mayor valor del valor promedio de respuesta
        if(client[i]['average_reply_time']>majorART):
            majorART=client[i]['average_reply_time']
        #Se obtiene el total de datos de comportamiento por sección
        mediaBehaviorAO=mediaBehaviorAO+client[i]['accepted_offers'];
        mediaBehaviorCO=mediaBehaviorCO+client[i]['canceled_offers'];
        mediaBehaviorART=mediaBehaviorART+client[i]['average_reply_time'];
    
    #Se obtiene la media de datos de comportamiento por sección
    mediaBehaviorAO/=10;
    mediaBehaviorCO/=10;
    mediaBehaviorART/=10;

    
    #Se determina el menor porcentaje de distancia, canceled_calls y average_reply_time. Ya que representarán el 100% de su rubro
    minorDistance2=10000;
    minorRO=10000;
    minorART=10000;
    for i in range(clients_number):
        minorDistancePercent=distanceOffice(officelatitude, officelongitud, 
                             float(client[i]['location']['latitude']),
                             float(client[i]['location']['longitude']))*100/majorDistance;
        if(minorDistancePercent<minorDistance2):
            minorDistance2=minorDistancePercent;
        #Determinar el menor porcentaje de Cancelled_offers
        minorROPercent=(client[i]['canceled_offers'])*100/majorRO;
        if(minorROPercent<minorRO):
            minorRO=minorROPercent;
        #Determinar el menor porcentaje de average_reply_time
        minorARTPercent=(client[i]['average_reply_time'])*100/majorART;
        if(minorARTPercent<minorART):
            minorART=minorARTPercent;
    
    
#Se define el porcentaje obtenido en cada rubro y la calificación final por cliente
    for i in range(clients_number):
        agep=client[i]['age']*100/MajorAge;
        distancep=distanceOffice(officelatitude, officelongitud, 
                             float(client[i]['location']['latitude']),
                             float(client[i]['location']['longitude']))*100/majorDistance;
        distancep=100-(distancep-minorDistance2);
        offers_acceptedP=(client[i]['accepted_offers']*100/majorAO)*3;
        minorROP=client[i]['canceled_offers']*100/majorRO;
        minorROP=(100-(minorROP-minorRO))*3;
        minorARTP=client[i]['average_reply_time']*100/majorART;
        minorARTP=(100-(minorARTP-minorART))*2;
        qualification=(agep+distancep+offers_acceptedP+minorROP+minorARTP)/100;
        #Se determina la prioridad de cada usuario dependiendo la cantidad de sus datos de comportamiento (0,1,2,3)
        flag=0;
        if(client[i]['accepted_offers']>mediaBehaviorAO):
            flag+=1;
        if(client[i]['canceled_offers']>mediaBehaviorCO):
            flag+=1;
        if(client[i]['average_reply_time']>mediaBehaviorART):
            flag+=1;
        percentage={
            "id": client[i]['id'],
            "name": client[i]['name'],
            "AgePercent": agep/100,
            "locationPercent": distancep/100,
            "offers_accepted_percent":offers_acceptedP/100, 
            "offers_canceled_percent":minorROP/100,
            "average_reply_time":minorARTP/100,
            "qualification": qualification,
            "priority" : flag
        }
        percentages.append(percentage);
    #Se ordenan los clientes de forma ascendente dependiendo sus calificaciones
    percentagesOrdered=sorted(percentages, key=lambda x: x['qualification'], reverse=True)
    
    #Se llena un objeto de 10 clientes; con la calificación más alta y con la más alta prioridad=0 (definida por pocos datos de comportamiento)
    j=0;
    k=0;
    selectedClients=[];
    while k<10:
        if(percentagesOrdered[j]['priority']==0):
            selectedClients.append(percentagesOrdered[j])
            k+=1;
        j+=1;

    #Escribiendo en SelectedClients.json
with open("SelectedClients.json", "w") as outfile:
    outfile.write(json.dumps(selectedClients))