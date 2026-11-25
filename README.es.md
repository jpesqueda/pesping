# pesping

**Escáner ICMP IPv4 concurrente y monitor de disponibilidad para upgrades** · Versión 1.1.0

[English](README.md) · [Guía de publicación](PUBLISHING.md)

pesping permite comprobar una dirección IP, un hostname, un archivo de hosts, una red IPv4 en formato CIDR o un rango de direcciones. También ofrece monitoreo continuo para detectar caídas y recuperaciones durante mantenimientos de red.

## Requisitos
Python 3.10 o superior, Windows/Linux/macOS y el comando `ping` del sistema. En Windows se instala automáticamente la dependencia `colorama` para colores.

## Instalación
Una vez publicado en PyPI:
```powershell
py -m pip install pesping
pesping --help
```
Antes de publicarlo en PyPI:
```powershell
git clone https://github.com/jpesqueda/pesping.git
cd pesping
py -m pip install -e .
pesping --help
```

## Parámetros de destino
Se debe indicar **exactamente una** opción de destino.

| Opción | Función | Ejemplo |
| --- | --- | --- |
| `-ho`, `--host` | Una IP o hostname | `-ho 192.0.2.10` |
| `-hf`, `--host_file` | Archivo de dispositivos | `-hf hosts.txt` |
| `-r`, `--range` | Rango completo o abreviado, inclusivo | `-r 192.0.2.100-200` |
| `-s`, `--subnet` | Red IPv4 CIDR | `-s 198.51.100.0/26` |

Los rangos `192.0.2.100-192.0.2.200` y `192.0.2.100-200` generan las mismas 101 direcciones. Para cruzar al siguiente octeto se utiliza una dirección final completa. En subnets tradicionales se excluyen red y broadcast; las máscaras /31 y /32 siguen el comportamiento de `ipaddress.hosts()`.

## Ejemplos de uso
```powershell
pesping -ho 192.0.2.10
pesping -hf hosts.txt --show down
pesping -r 192.0.2.100-200 --show up
pesping -r 192.0.2.100-192.0.2.200
pesping -s 198.51.100.0/26 --workers 20
pesping -s 192.0.2.0/24 --monitor --only-changes
pesping -hf hosts.txt --monitor --interval 2 --fail-threshold 3 --recovery-threshold 2 --log upgrade.log --csv upgrade.csv
pesping -hf hosts.txt --stop-when-all-up --only-changes
```

## Formato de hosts.txt
```text
# nombre,IPv4 (todos los datos son ficticios)
switch01.example.test,192.0.2.10
switch02.example.test,192.0.2.11
192.0.2.12
```
Ignora líneas en blanco y comentarios iniciados con `#`, además de evitar direcciones duplicadas.

## Monitoreo de upgrades
Para considerar un equipo DOWN, debe acumular `--fail-threshold` fallos consecutivos (valor predeterminado: 3). Para considerarlo UP, debe acumular `--recovery-threshold` respuestas consecutivas (valor predeterminado: 2). `--only-changes` muestra sólo eventos y omite los contadores periódicos. `--wait-for-up` termina cuando todos los equipos estén UP. `--stop-when-all-up` termina después de haber registrado un evento DOWN y de que todos se recuperen. Ctrl+C detiene el proceso y genera el resumen.

`--show all|up|down` sólo filtra los resultados del **escaneo único**, no los eventos del monitor. `--workers` configura la concurrencia (50 por defecto), `--timeout` el tiempo de respuesta (1 segundo), `--interval` la frecuencia de monitoreo (2 segundos) y `--max-hosts` el máximo de direcciones (4096 por defecto). Usa `pesping --help` para consultar todos los parámetros.

## Reportes
- Escaneo único: direcciones alcanzables/no alcanzables y resumen.
- Monitor: transiciones UP/DOWN, interrupciones, downtime acumulado y resumen final.
- `--log ARCHIVO`: eventos con fecha y hora; `--csv ARCHIVO`: registros tabulares exportables.

## Limitaciones y seguridad
Una IP que no responde ICMP **no necesariamente está apagada**: puede bloquearse el ping. Una IP que responde **no garantiza** que las aplicaciones estén saludables. El downtime es una estimación basada en el muestreo del monitor.

Todas las IP de esta documentación pertenecen a bloques reservados para ejemplos (RFC 5737) y los hostnames son ficticios (`.test`). Escanea únicamente redes autorizadas. Los logs reales pueden contener información sensible de tus dispositivos, por lo que deben protegerse.

## Desarrollo y validación
```powershell
py -m pip install -e . pytest build twine
py -m pytest -q
py -m build
py -m twine check dist/*
```

Licencia MIT. Mantenedor: [jpesqueda](https://github.com/jpesqueda).
