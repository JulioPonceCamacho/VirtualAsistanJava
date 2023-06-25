import sys
import Interfaz as IN

if __name__ == '__main__':
    aplicacion = IN.QApplication(sys.argv)
    ventana = IN.ventanaPrincipal()
    ventana.show()
    

    sys.exit(aplicacion.exec_())