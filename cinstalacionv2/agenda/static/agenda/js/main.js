const DIAS_MOSTRADOS = 6;
const HORAS_MOSTRADAS = 24;

const FECHAS = new Array()

const TECNICOS = new Array()
const INSTALACIONES = new Array()

var tecnico_activo;
var instalacion_pendiente_activa;

const inp_instalaciones_datos = document.querySelector('#datos')

window.onload = function () {
    get_fechas()
    get_hours()
    Tecnico.get_tecnicos()
    .finally(function() {
        TECNICOS[0].select_tecnico()
        act_contador()
        Instalacion.get_instalaciones()
        .finally(function() {
            INSTALACIONES.forEach(instalacion =>{
                if (instalacion.status == 0) {
                    instalacion.set_pendiente()
                } else if (instalacion.status == 1){
                    instalacion.set_asign()
                } 
            })
            document.querySelector('.btn-save').classList.remove('save-active')
            document.querySelector('.btn-save').disabled = true
        })
    })
}

class Instalacion {
    constructor(nro_contrato, nombre_cliente, direccion, numero_telefono1, numero_telefono2, plan, prioridad, tiempo_estimado, observaciones, status, tecnico, fecha, hora) {
        this.nro_contrato = nro_contrato
        this.nombre_cliente = nombre_cliente
        this.direccion = direccion
        this.numero_telefono1 = numero_telefono1
        this.numero_telefono2 = numero_telefono2
        this.plan = plan
        this.prioridad = prioridad
        this.tiempo_estimado = tiempo_estimado
        this.observaciones = observaciones
        this.status = status
        this.tecnico = tecnico
        this.fecha = fecha
        this.hora = hora

        this.contenedor = document.createElement('div')
    }

    set_pendiente() {
        const instalacion = this
        
        const insts_pend = document.querySelector('.insts-pend')
        this.contenedor.innerHTML = `
        <p><a href="../instalaciones/update_instalacion/${this.nro_contrato}"><b>${this.nro_contrato}</b></a></p>
        <p>${this.nombre_cliente}</p>
        <p>${this.direccion}</p>
        <p><b>Tiempo estimado:</b> ${this.tiempo_estimado / 2} hora/s</p>
        <button class='btn-asignar-inst'>+</button>`

        this.status = 0
        this.tecnico = null
        this.fecha = null
        this.hora = null

        this.contenedor.querySelector('.btn-asignar-inst').addEventListener('click', function(){
            INSTALACIONES.forEach(instalacion => instalacion.contenedor.classList.remove('active')) 
            instalacion.contenedor.classList.add('active')
            active_selector(instalacion)
        })
        this.contenedor.classList = 'instalacion-pend'
        insts_pend.appendChild(this.contenedor)
        act_contador()
        act_datos()
    }

    set_asign() {
        const instalacion = this

        const num_fecha = get_num_fecha(this.fecha)
        if (num_fecha < 6) {
            const contenedor = this.contenedor

            const celda = this.tecnico.agenda[this.hora][num_fecha]

            for (let i = 0; i < instalacion.tiempo_estimado; i++) {
                try {
                    this.tecnico.agenda[this.hora + i][num_fecha].classList.add('ocp')
                } catch (error) {}
            }

            this.contenedor.innerHTML = `
            <p><a href="../instalaciones/update_instalacion/${this.nro_contrato}"><b>${this.nro_contrato}</b></a></p>
            <p class="p-completada">COMPLETADA</p>
            <p>${this.nombre_cliente}</p>
            <p>${this.direccion}</p>
            <div class="btns">
                <button class='btn-complete'>Completar</button>
                <button class='btn-remove'>X</button>
                <button class='btn-cancel'>Cancelar</button>
            </div>`

            contenedor.querySelector('.btn-remove').addEventListener('click', function() {
                INSTALACIONES.forEach(instalacion => instalacion.contenedor.classList.remove('active')) 
                document.querySelectorAll('.btn-asignar').forEach(btn => btn.remove())
                for (let i = 0; i < instalacion.tiempo_estimado; i++) {
                    instalacion.tecnico.agenda[instalacion.hora + i][num_fecha].classList.remove('ocp')
                }
                instalacion.set_pendiente()
            })

            contenedor.querySelector('.btn-complete').addEventListener('click', function() {
                instalacion.status = 2
                contenedor.classList.add('completed')
                act_datos()
            })

            contenedor.querySelector('.btn-cancel').addEventListener('click', function() {
                instalacion.status = 1
                contenedor.classList.remove('completed')
                act_datos()
            })


            this.contenedor.classList = `instalacion-asign te-${this.tiempo_estimado}`
            celda.appendChild(this.contenedor)  
        } else {
            const insts_other = document.querySelector('.insts-asign-or')
            const contenedor = this.contenedor;

            contenedor.innerHTML = `
            <p class="nro-contrato"><a href="../instalaciones/update_instalacion/${this.nro_contrato}"><b>${this.nro_contrato}</b></a><p class="divisor"> | </p><p class="p-completada">COMPLETADA</p></p>
            <p>${this.direccion.slice(0, 40)}...</p>
            <hr>
            <p><b>Técnico asignado:</b> ${this.tecnico.nombre} ${this.tecnico.apellido}</p>
            <p><b>Fecha:</b> ${this.fecha.getUTCDate()}-${this.fecha.getUTCMonth() + 1}-${this.fecha.getUTCFullYear()}</p>
            <div class="btns">
            <button class='btn-remove'>X</button>
            <button class='btn-complete'>Completar</button>
            <button class='btn-cancel'>Cancelar</button>
            </div>`

            contenedor.classList = `instalacion-or`

            contenedor.querySelector('.btn-remove').addEventListener('click', function() {
                instalacion.set_pendiente()
            })
            contenedor.querySelector('.btn-complete').addEventListener('click', function() {
                instalacion.status = 2
                contenedor.classList.add('completed')
                act_datos()
            })
            contenedor.querySelector('.btn-cancel').addEventListener('click', function() {
                instalacion.status = 1
                contenedor.classList.remove('completed')
                act_datos()
            })

            insts_other.appendChild(this.contenedor)
        }
        act_contador()
        act_datos()
    }

    static get_instalaciones() {
        const instalaciones = fetch('../instalaciones/json')
        .then(response => response.json())
        .then(data => {
            data.forEach(instalacion => {
                if (instalacion.fields.tecnico != null) {
                    INSTALACIONES.push(new Instalacion(
                        instalacion.pk, 
                        instalacion.fields.nombre_cliente, instalacion.fields.direccion, 
                        instalacion.fields.numero_telefono1, 
                        instalacion.fields.numero_telefono2, 
                        instalacion.fields.plan, 
                        instalacion.fields.prioridad, 
                        instalacion.fields.tiempo_estimado, 
                        instalacion.fields.observaciones, 
                        instalacion.fields.status,
                        Tecnico.get_tecnico(instalacion.fields.tecnico), 
                        new Date(instalacion.fields.fecha), 
                        instalacion.fields.hora 
                        ))

                } else {
                    INSTALACIONES.push(new Instalacion(
                        instalacion.pk, 
                        instalacion.fields.nombre_cliente, instalacion.fields.direccion, 
                        instalacion.fields.numero_telefono1, 
                        instalacion.fields.numero_telefono2, 
                        instalacion.fields.plan, 
                        instalacion.fields.prioridad, 
                        instalacion.fields.tiempo_estimado, 
                        instalacion.fields.observaciones, 
                        instalacion.fields.status
                        ))
                }
            });
        })
        return instalaciones
    }
}

class Tecnico {
    constructor(id, nombre, apellido) {
        this.id = id;
        this.nombre = nombre;
        this.apellido = apellido;

        this.contenedor = this.create_contenedor()
        this.agenda = this.create_agenda()
        this.num_instalaciones = 0
    }

    create_agenda() {
        const tabla_insts = document.querySelector('.agenda')
        const agenda = new Array()
        for (let i = 0; i < HORAS_MOSTRADAS; i++) {
            const fila = new Array()
            for (let j = 0; j < DIAS_MOSTRADOS; j++) {
                const celda = document.createElement('div');
                celda.classList = `celda tecnico-${this.id} fecha-${j} hora-${i}`
                fila.push(celda)
                tabla_insts.appendChild(celda)
            }
            agenda.push(fila)
        }
        return agenda
    }

    create_contenedor() {
        const tecnico = this
        const contenedor = document.createElement('div')
        contenedor.classList = 'tecnico'
        contenedor.innerHTML = `<div class="d-flex"><div><p>${this.nombre}</p><p>${this.apellido}</p></div><p class="num-insts"></p></di>`
        document.querySelector('.tecnicos').appendChild(contenedor)
        contenedor.addEventListener('click', function() {
            tecnico.select_tecnico()
        })
        return contenedor
    }

    select_tecnico() {
        tecnico_activo = this
        document.querySelectorAll('.celda').forEach(celda => celda.classList.add('d-none'))
        this.agenda.forEach(fila => {
            fila.forEach(celda => {
                celda.classList.remove('d-none')
            });
        });
        TECNICOS.forEach(tecnico => { tecnico.contenedor.classList.remove('active') });
        this.contenedor.classList.add('active')
        document.querySelector('.name-tecnico').innerHTML = `${this.nombre} ${this.apellido}`
    }

    static get_tecnico(id) {
        let tecnico;
        TECNICOS.forEach(aux_tecnico => {
            if (id == aux_tecnico.id) {tecnico = aux_tecnico}
        });
        return tecnico
    }

    static get_tecnicos() {
        const tecnicos = fetch('../tecnicos/json')
        .then(response => response.json())
        .then(data => {
            data.forEach(tecnico => {
                TECNICOS.push(new Tecnico(tecnico.pk, tecnico.fields.nombre, tecnico.fields.apellido))
            });
        })
        return tecnicos
    }
}

function act_contador() {
    TECNICOS.forEach(tecnico => tecnico.num_instalaciones = 0)

    INSTALACIONES.forEach(instalacion => {
        try {
            const num_fecha = get_num_fecha(instalacion.fecha)
            if (instalacion.status == 1) {
                if (num_fecha < 6) {
                    instalacion.tecnico.num_instalaciones++
                }    
            }
        }
        catch (error) {}
    })
    TECNICOS.forEach(tecnico => {
        tecnico.contenedor.querySelector('.num-insts').innerHTML = `(${tecnico.num_instalaciones})`
    })
}

function act_datos() {
    document.querySelector('.btn-save').classList.add('save-active')
    document.querySelector('.btn-save').disabled = false

    let text = ""
    for (let i = 0; i < INSTALACIONES.length; i++) {
        const instalacion = INSTALACIONES[i];
        if (i!=0) {text += ';'}
        if (instalacion.tecnico) {
            text += `${instalacion.nro_contrato}|${instalacion.tecnico.id}|${instalacion.fecha.getUTCDate()}-${instalacion.fecha.getUTCMonth()+1}-${instalacion.fecha.getUTCFullYear()}|${instalacion.hora}|${instalacion.status}`
        } else {
            text += `${instalacion.nro_contrato}|None|None|None|0`
        }
    }
    inp_instalaciones_datos.value = text
}

function search() {

    INSTALACIONES.forEach(instalacion => instalacion.contenedor.classList.remove('active')) 
    document.querySelectorAll('.btn-asignar').forEach(btn => btn.remove())

    const search_value = document.querySelector('#inp-search').value
    INSTALACIONES.forEach(instalacion => {
        if (instalacion.status == 0) {
            if (instalacion.nro_contrato.toString().includes(search_value) || instalacion.nombre_cliente.includes(search_value)) {
                instalacion.contenedor.classList.remove('d-none')
            } else {
                instalacion.contenedor.classList.add('d-none')
            }
        }
    })
}

function active_selector(instalacion) {
    document.querySelectorAll('.btn-asignar').forEach(btn => btn.remove())
    TECNICOS.forEach(tecnico => {
        for (let i = 0; i < tecnico.agenda.length; i++) {
            const fila = tecnico.agenda[i];
            for (let j = 0; j < fila.length; j++) {
                const celda = fila[j];
                if (!celda.classList.contains('ocp')) {
                    let puede_haber = true;
                    for (let h = 0; h < instalacion.tiempo_estimado; h++) {
                        try {
                            const aux_celda = tecnico.agenda[i+h][j];
                            if (aux_celda.querySelector('.instalacion-asign')!=null) {puede_haber = false}
                        } catch (error) {
                            puede_haber = false
                        }
                    }
                    if (puede_haber) {
                        const btn_asignar = document.createElement('button')
                        btn_asignar.classList = `btn-asignar te-${instalacion.tiempo_estimado}`
                        btn_asignar.innerHTML = "Asignar"
                        btn_asignar.addEventListener('click', function() {
                            document.querySelector('#inp-search').value = ""
                            search()
                            document.querySelectorAll('.btn-asignar').forEach(btn => btn.remove())
                            instalacion.status = 1
                            instalacion.tecnico = tecnico
                            instalacion.fecha = FECHAS[j]
                            instalacion.hora = i
                            instalacion.set_asign()
                        })
                        celda.appendChild(btn_asignar)     
                    }

                      
                }
               
            }
        }
    })
}

function get_hours() {
    const contenedor_horas = document.querySelector('.horas')
    let hour = 8
    for (let i = 0; i < HORAS_MOSTRADAS; i++) {
        const contenedor_hora = document.createElement('div')
        if (i % 2 == 0){
            contenedor_hora.innerHTML = `${hour}:00`
        } else {
            contenedor_hora.innerHTML = `${hour}:30`
            hour++
        }
        contenedor_hora.classList = "hora"
        contenedor_horas.appendChild(contenedor_hora)
    }
}

function get_num_fecha(fecha) {
    for (let i = 0; i < FECHAS.length; i++) {
        const aux_fecha = FECHAS[i];
        if (
            fecha.getUTCDate() == aux_fecha.getUTCDate() &&
            fecha.getUTCMonth() == aux_fecha.getUTCMonth() &&
            fecha.getUTCFullYear() == aux_fecha.getUTCFullYear()
            ) {
            return i
        }
    }
    return 6;
}

function get_fechas() {
    const contenedor_fechas = document.querySelector('.fechas')
    const first_date = document.querySelector('#input_date').value
    for (let i = 0; i < DIAS_MOSTRADOS; i++) {
        const fecha = new Date(first_date)
        fecha.setUTCDate(fecha.getUTCDate() + i)
        const contenedor_dia = document.createElement('div')
        contenedor_dia.classList = 'fecha'
        contenedor_dia.innerHTML = `${fecha.getUTCDate()}/${fecha.getUTCMonth() + 1}/${fecha.getUTCFullYear()}`
        contenedor_fechas.appendChild(contenedor_dia)

        contenedor_dia.addEventListener('click', () => {
            let instalaciones_fecha = []
            INSTALACIONES.forEach(instalacion => {
                if (instalacion.tecnico == tecnico_activo) {
                    if (instalacion.fecha.getUTCDate() == fecha.getUTCDate() &&
                        instalacion.fecha.getUTCMonth() == fecha.getUTCMonth() &&
                        instalacion.fecha.getUTCFullYear() == fecha.getUTCFullYear()
                    ) {
                        let hora_mostrada

                        if (instalacion.hora % 2 == 0) {
                            hora_mostrada = `${instalacion.hora / 2 + 8}:00`
                        } else {
                            hora_mostrada = `${Math.trunc(instalacion.hora / 2) + 8}:30`
                        }

                        instalaciones_fecha[instalacion.hora] = 
                        `${hora_mostrada} - C${instalacion.nro_contrato}, ${instalacion.nombre_cliente}, ${instalacion.direccion.slice(0, 80)}...

`
                    }
                }
            })
            texto = `Agenda ${tecnico_activo.nombre} ${tecnico_activo.apellido} ${fecha.getUTCDate()}-${fecha.getUTCMonth() + 1}-${fecha.getFullYear()}

`

            instalaciones_fecha.forEach(data => {
                texto += data
            })


            navigator.clipboard.writeText(texto)
            .finally(() => {
                alert("Se ha copiado la agenda al portapapeles")
            })
        })

        FECHAS.push(fecha)
    }
}