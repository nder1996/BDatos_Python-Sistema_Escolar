from sqlalchemy import Column, String, ForeignKey , engine 
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import relationship , sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine 
import os 



# B A S E  D E  D A T O S
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
engine = create_engine('sqlite:///BD_Colegio.db', echo=True)
#'sqlite:///:memory:'

Datos_Curso    = [] ; Datos_Profesor = []

Session  = sessionmaker(bind=engine) 
session  = Session()
Base = declarative_base()

class Tabla_Estudiantes(Base):
    __tablename__ = 'ESTUDIANTES'
    id            = Column(String(20), primary_key=True)
    Nombre_M      = Column(String(20),ForeignKey('CURSOS.id')) 
    Nombre        = Column(String(40))
    Apellido      = Column(String(40))
    Un_Curso      = relationship("Tabla_Curso")

class Tabla_Curso(Base):
    __tablename__      = 'CURSOS'
    id                 = Column(String(20), primary_key=True)
    Nombre_M           = Column(String(40))
    Muchos_Profesores  = relationship("Tabla_Profesor")
    Un_Horario         = relationship("Tabla_Horario",back_populates="Un_Curso")

class Tabla_Profesor(Base):
    __tablename__   = 'PROFESOR'
    id              = Column(String(20), primary_key=True)
    Nombre_M        = Column(String(20) , ForeignKey('CURSOS.id'))
    Nombre          = Column(String(50))    
    Apellido        = Column(String(50))
    Un_Horario      = relationship("Tabla_Horario",back_populates="Un_Profesor")

class Tabla_Horario(Base):
    __tablename__ = 'HORARIO'
    id            = Column(String(20), primary_key=True )
    Profesor_id   = Column(String(20) , ForeignKey('PROFESOR.id'))
    Nombre_M      = Column(String(20) , ForeignKey('CURSOS.id'))
    Dia           = Column(String(20))
    Hora_Inicio   = Column(String(20)) 
    Hora_Final    = Column(String(20))
    Un_Profesor   = relationship("Tabla_Profesor",back_populates="Un_Horario")
    Un_Curso      = relationship("Tabla_Curso",   back_populates="Un_Horario")

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class Menu_Principal():
    def Inicio(self):
        print("\n")
        print("\n\n\t\t\t|***|  S Y S T E M  S C H O O L  |***|")

    def Registrar_Datos(self,Datos):
        print("\n\n\t\t\t     | REGISTRAR  DATOS {} |".format(Datos))
        print("\n\n")
    
    def Mensaje_Datos(self):
        print("\t\t PARA REGISTRAR LOS DATOS DEL ESTUDIANTES O EL HORARIO\n\t      SE DEBE INGRESAR PRIMERO LOS DATOS DEL CURSO Y DEL PROFESOR  ")
        print("\n\n")

    def Mensaje_Profesor(self):
        print("\t\t PARA REGISTRAR LOS DATOS DEL ESTUDIANTES O EL HORARIO\n\t      SE DEBE INGRESAR PRIMERO LOS DATOS DEL CURSO Y DEL PROFESOR  ")

    def Opcion_1(self):
        print ("\t\t\t\tSELECCIONE UNA OPCION \n\n")
        print ("\t\t\t\t1 -> REGISTRAR DATOS")
        print ("\t\t\t\t2 -> MOSTRAR   DATOS")
        print ("\t\t\t\t3 -> Salir")
        Opcion = input("\n\t\tIngrese La Opcion Correspondiente Para Continuar : ")
        return Opcion


class Opcion_Menu():

    Base.metadata.drop_all(engine) 
    Base.metadata.create_all(engine)

    def Registrar_Alumno(self):
        ID       = input("\nIngrese Su Codigo             :  ")
        if ID!="":
            N_CURSO  = input("\nIngrese El Nombre Del Curso   :  ")
            if N_CURSO!="" and  Datos_Curso.count(N_CURSO)!=0:
                Nombre   = input("\nIngrese Su Nombre             :  ")
                Aux = Nombre.replace(" ","")
                if Aux.isalpha()==True:
                    Apellido = input("\nIngrese Su Apellido           :  ") ; print("\n")
                    Aux = Apellido.replace(" ","")
                    if Aux.isalpha()==True:
                        Alumno   = Tabla_Estudiantes(id=ID,Nombre_M=N_CURSO,Nombre=Nombre,Apellido=Apellido)
                        session.add(Alumno) ; session.commit()
                        return True
        wait = input("\n\n\n\t\tE R R O R  , I N G R E S E  D A T O S  C O R R E C T O S")
        return False

    def Registrar_Profesor(self):
        ID       = input("\nIngrese Su Codigo            : ")
        if ID!="":
            N_CURSO  = input("\nIngrese El Codigo Del Curso  : ")
            if N_CURSO!="" and Datos_Curso.count(N_CURSO)!=0:
                    Nombre   = input("\nIngrese Su Nombre            : ")
                    Aux = Nombre.replace(" ","")
                    if Aux.isalpha()==True:
                        Apellido = input("\nIngrese Su Apellido          : ") ; print("\n")
                        Aux = Apellido.replace(" ","")
                        if Aux .isalpha()==True:
                            Docente  = Tabla_Profesor(id=ID,Nombre_M=N_CURSO,Nombre=Nombre,Apellido=Apellido)
                            session.add(Docente) ; session.commit()
                            Datos_Profesor.append(ID) ; Datos_Profesor.append(Nombre)
                            return True
        wait = input("\n\n\n\t\tE R R O R  , I N G R E S E  D A T O S  C O R R E C T O S")
        return False

    def Registrar_Curso(self):
        ID       = input("\nIngrese El Codigo Del Curso : ")
        if ID != "":
            Nombre   = input("\nIngrese El Nombre Del Curso : ")
            if Nombre!="":
                Curso    = Tabla_Profesor(id=ID,Nombre_M=Nombre)
                Datos_Curso.append(ID) ; Datos_Curso.append(Nombre)
                session.add(Curso) ; session.commit()
                return True
        wait = input("\n\n\n\t\tE R R O R  , I N G R E S E  D A T O S  C O R R E C T O S")
        return False

    def Registrar_Horario(self):
        ID_Horario  = input("\nIngrese El Codigo Del Horario                       : ")
        if ID_Horario != "":
            Profesor_id = input("\nIngrese El Codigo Del Profesor                      : ")
            if Profesor_id != "":
                N_CURSO    = input("\nIngrese El Codigo Del Curso                         : ")
                if N_CURSO != "" and Datos_Curso.count(N_CURSO)!=0:
                    DIA         = input("\nIngrese El Dia Que Se Impartira La Materia          : ")
                    if DIA.isalpha()==True:
                        Hora_Inicio = input("\nIngrese La Hora Inicial Que Se Impartira La Materia : ")
                        if Hora_Inicio!="":    
                            Hora_Final  = input("\nIngrese La Hora Final Que Se Impartira La Materia   : ")
                            if Hora_Final!="":  
                                Horario     = Tabla_Horario(id=ID_Horario,Profesor_id=Profesor_id,Nombre_M=N_CURSO,DIA=DIA,Hora_Inicio=Hora_Inicio,Hora_Final=Hora_Final)
                                session.add(Horario) ; session.commit()
                                return True
        wait = input("\n\n\n\t\tE R R O R  , I N G R E S E  D A T O S  C O R R E C T O S")
        return False

    def Ingresar_Curso(self):
        os.system ("cls") ; Menu_Principal().Inicio() ; Menu_Principal().Registrar_Datos("CURSOS") ; Menu_Principal().Mensaje_Datos() ; return Opcion_Menu().Registrar_Curso()

    def Ingresar_Profesor(self):
        os.system ("cls") 
        Menu_Principal().Inicio() ; Menu_Principal().Registrar_Datos("PROFESOR") ; Menu_Principal().Mensaje_Datos()
        for i in range(len(Datos_Curso)-1):
            print("\t CODIGO  : ",Datos_Curso[i],"   *|||*    NOMBRE DEL CURSO  : ",Datos_Curso[i+1],"\n")
        return Opcion_Menu().Registrar_Profesor()

    def Ingresar_Horario(self):
        os.system ("cls") 
        Menu_Principal().Inicio() ; Menu_Principal().Registrar_Datos("HORARIO") 
        for i in range(len(Datos_Curso)-1):
            print("\t CODIGO  : ",Datos_Curso[i],"   *|||*    NOMBRE DEL CURSO  : ",Datos_Curso[i+1],"\n")
        for i in range(len(Datos_Profesor)-1):
            print("\t CODIGO  : ",Datos_Profesor[i],"   *|||*    NOMBRE DEL PROFESOR  : ",Datos_Profesor[i+1],"\n")
        return Opcion_Menu().Registrar_Horario()
    
    def Ingresar_Alumno(self):
        os.system ("cls") 
        Menu_Principal().Inicio() ; Menu_Principal().Registrar_Datos("ALUMNO")
        for i in range(len(Datos_Curso)-1):
            print("\t CODIGO  : ",Datos_Curso[i],"   *|||*    NOMBRE DEL CURSO  : ",Datos_Curso[i+1],"\n")
            pass
        return Opcion_Menu().Registrar_Alumno()
        

""""
PRIMERO SE HACE EL CURSO Y DESPUES EL PROFESOR , LUEGO SE HACE EL ALUMNO Y POR ULTIMO EL HORARIO

"""
if __name__ == "__main__":
    
    os.system ("cls")
    Opcion = "0"
    while Opcion!="1":
        while Opcion_Menu().Ingresar_Curso()!=True:    wait = input(" D A T O S  G U A R D A D O S ") ; os.system ("cls")
        while Opcion_Menu().Ingresar_Profesor()!=True: wait = input(" D A T O S  G U A R D A D O S ") ; os.system ("cls")
        while Opcion_Menu().Ingresar_Alumno()!=True :  wait = input(" D A T O S  G U A R D A D O S ") ; os.system ("cls")
        while Opcion_Menu().Ingresar_Horario()!=True : wait = input(" D A T O S  G U A R D A D O S ") 
        Opcion = input("\n\n\t\tSI DESEA FINALIZAR INGRESAR EL EL NUMERO 1 ,  DE LO CONTRARIO INGRESE CUALQUIER TECLA")





















