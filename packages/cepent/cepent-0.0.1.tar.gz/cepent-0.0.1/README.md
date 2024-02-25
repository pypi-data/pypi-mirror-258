# cepent

Se encuentra en construccion es una libreria para almacenar errores de procesos ETL



## Ejemplo de como usarlo

Creando captura de error en caso de proceso rechazado

```python
from cepent import StreamingServer

error = ErrorHandling(usr, pwd, bd_pg, bd_port,bd_procesos, bd_company, table_name)
error.handle_error()

```