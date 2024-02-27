# cepent

Se encuentra en construccion es una libreria para almacenar errores de procesos ETL



## Ejemplo de uso

Creando captura de error en caso de proceso rechazado

```python
from cepent import ErrorHandling

error = ErrorHandling(usr, pwd, bd_pg, bd_port, bd_company )
error.handle_error(table_name)

```