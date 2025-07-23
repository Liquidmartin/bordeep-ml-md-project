#!/bin/bash



LOGFILE_MISSING="missing_files.txt"
LOGFILE_TIMING="timing_log.txt"

> "$LOGFILE_MISSING"  # Borra contenido anterior de los logs
> "$LOGFILE_TIMING"

for i in 1 #{1..2}
do
    DATAFILE="./data_in/data_POSCAR_${i}.lammps"
    #DATAFILE="./data_lammps_h2_w110_random/data_POSCAR_1_variant_${i}.lammps"

    if [[ -f "${DATAFILE}" ]]; then
        START_TIME=$(date +%s)  # Guarda el tiempo de inicio en segundos
        VEL=$(awk "BEGIN {print -53.5918146579035 + 0.0 * ${i}}")
        #VEL=$(awk "BEGIN {print -21.8787667169453 + 0.0 * ${i}}")
        lmp -var i ${i} -var DATAFILE ${DATAFILE} -var VEL ${VEL} -in in.simulation
        END_TIME=$(date +%s)  # Guarda el tiempo de finalización
        ELAPSED_TIME=$((END_TIME - START_TIME))  # Calcula la duración

        echo "Trayectoria $i: ${ELAPSED_TIME} segundos" | tee -a "$LOGFILE_TIMING"
    else
        echo "${DATAFILE}" >> "$LOGFILE_MISSING"  # Guardar los archivos faltantes
    fi
done
echo "Registro de tiempos completado en: $LOGFILE_TIMING"

#salida="./salida_dinamica_energia_23_t_menor/"
salida="./salida_prueba/"
mv log.lammps ${salida}
mv timing_log.txt ${salida}
mv missing_files.txt ${salida}
cp in.simulation ${salida}
#
#-53.5918146579035 E=300meV
#-43.7575334338906 E=200meV
#-34.5933676105158 E=125meV
#-21.8787667169453 E=50meV
#
