from django.db import models

# Create your models here.
PLANES = [
    ['BP', 'BÁSICO PLUS'],
    ['BA', 'BÁSICO'],
    ['BR', 'BRONCE'],
    ['PL', 'PLATA'],
    ['OR', 'ORO'],
    ['EMP', 'EMPRENDEDOR'],
    ['PRD', 'PRODUCTIVO'],
    ['PRDP', 'PRODUCTIVO PRO'],
    ['VISP', 'VISIONARIO PRO']
]

HORAS_ESTIMADAS = [
    [1, "00:30"],
    [2, "01:00"],
    [3, "01:30"],
    [4, "02:00"],
    [5, "02:30"],
    [6, "03:00"],
    [7, "03:30"],
    [8, "04:00"],
    [9, "04:30"],
    [10, "05:00"],
    [11, "05:30"],
    [12, "06:00"],
]

STATUS = [
    [0, "Por Asignar"],
    [1, "Asignada"],
    [2, "Completada"]
]

HORA_ASIGNADA = [
    [0, "08:00"],
    [1, "08:30"],
    [2, "09:00"],
    [3, "09:30"],
    [4, "10:00"],
    [5, "10:30"],
    [6, "11:00"],
    [7, "11:30"],
    [8, "12:00"],
    [9, "12:30"],
    [10, "13:00"],
    [11, "13:30"],
    [12, "14:00"],
    [13, "14:30"],
    [14, "15:00"],
    [15, "15:30"],
    [16, "16:00"],
    [17, "16:30"],
    [18, "17:00"],
    [19, "17:30"],
    [20, "18:00"],
    [21, "18:30"],
    [22, "19:00"],
    [23, "19:30"],
]

PRIORIDAD = [
    [1, 'Baja'],
    [2, 'Media'],
    [3, 'Alta'],
]

class Tecnico(models.Model):
    """ Técnicos a los que se les vana asignar instalaciones... """
    nombre = models.CharField(max_length=20, verbose_name="Nombre")
    apellido = models.CharField(max_length=20, verbose_name="Apellido")

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)

class Instalacion(models.Model):
    """ Cada una de las instalaciones para el sistema; por agendar, agendadas y completadas """
    # Datos principales
    nro_contrato = models.IntegerField(primary_key=True, verbose_name="Número de Contrato")
    nombre_cliente = models.CharField(max_length=120, verbose_name="Nombre del Cliente", blank=True, null=True)
    direccion = models.TextField(max_length=400, verbose_name="Dirección", blank=True, null=True)
    numero_telefono1 = models.CharField(max_length=13, verbose_name="Número de Teléfono 1", blank=True, null=True)
    numero_telefono2 = models.CharField(max_length=13, verbose_name="Número de Teléfono 2", blank=True, null=True)
    plan = models.CharField(max_length=12, verbose_name="Plan", choices=PLANES, default=0) #Choice
    
    # Datos para la instalación
    prioridad = models.IntegerField(verbose_name="Prioridad", choices=PRIORIDAD, default=1)
    tiempo_estimado = models.IntegerField(verbose_name="Tiempo estimado (en horas)", choices=HORAS_ESTIMADAS, default=3)
    observaciones = models.TextField(verbose_name="Observaciones", blank=True, null=True) 

    # Status diferencial para la instalación: Por agendar, Agendada y Completada
    status = models.IntegerField(verbose_name="Status", choices=STATUS, default=0)
    
    # Si está agendada o completada
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, verbose_name="Técnico", blank=True, null=True)
    fecha = models.DateField(verbose_name="Fecha", blank=True, null=True)
    hora = models.IntegerField(verbose_name="Hora", choices=HORA_ASIGNADA, blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(self.nro_contrato, self.nombre_cliente)
    
    