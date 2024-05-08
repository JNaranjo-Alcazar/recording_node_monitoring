#!/bin/bash

 

archivo_original="/home/jgrau/snd_20230203_093922.wav"  # Nombre del archivo original
numero_copias=100000  # Número de copias que deseas hacer

 

# Bucle para copiar el archivo y renombrarlo
for ((i=1455; i<$numero_copias; i++))
do
 echo $i 
 nombre_copia="/media/jgrau/50F2-245C/snd_20230203_093922_$i.wav"  # Nombre de la copia con el número correspondiente
  cp "$archivo_original" "$nombre_copia"  # Copiar el archivo original con el nuevo nombre
done
