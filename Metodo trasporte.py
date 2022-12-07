import numpy as np
from IPython.display import Latex, display_latex
def latex(matriz):
  cad=r"\left[\begin{matrix}"
  for i in matriz:
    for j in i:
      cad+=str(j)+r"&"
    cad=cad[:-1]+r"\"
  cad=cad[:-2]
  return cad+r"\end{matrix}\right]"
def mostrar(matriz):
  display_latex(Latex(latex(matriz)))

class ModeloTransporte:
  def asignar(Ma,oferta,demanda, i,j):
    if oferta[i]==0 and demanda[i]==0:
      return None
    #Se encarga de asignar la oferta, revisa si se puede colocar la oferta disponible o si no coloca la demanda disponible
    if oferta[i]<=demanda[j]: 
      Ma[i][j]=oferta[i]
    else:
    #Elimina la demanda columna oferta de sus vectores
      Ma[i][j]=demanda[j]
    #resta la oferta
    oferta[i]-=Ma[i][j]
    demanda[j]-=Ma[i][j]

  def eliminar(K,oferta,demanda):
    #se encarga de remplazar por un número muy alto los valores que ya no se puedan tomar de la matriz
    for i in range(len(oferta)):
      if(oferta[i]==0):
        #Asigna 'M' a toda la columna
        K[i,:]=np.ones(len(K[i,:]))*1e5
    for i in range(len(demanda)):
      if(demanda[i]==0):
        #Asigna 'M' a toda la fila
        K[:,i]=np.ones(len(K[:,i]))*1e5

  def calcular(C,M):
    #La suma de la diagonal de la matriz de resultados columna la matriz de costos es igual a calcular el costo
    S=np.array(C).T@np.array(M)
    sol=sum([S[i][i] for i in range(len(S))])
    return sol
def norOeste(C,oferta,demanda):
    #Construye la matriz de resultados
    M=[[0 for i in C[0]] for i in C]
    #Recorre todos los valores de la matriz, y hace la asignación
    for i in range(len(C)):
      for j in range(len(C[0])):
        ModeloTransporte.asignar(M,oferta,demanda,i,j)
    return M,ModeloTransporte.calcular(C,M)
    
  def minimoCosto(C,oferta,demanda,M=None,K=None):
    #Hace una copia de la matriz de costos
    if M==None:
      K=np.array(C)
      M=[[0 for i in C[0]] for i in K]
    #Selecciona los mínimos de cada fila
    minimos=[np.min(i) for i in K]
    #Toma el argumento minimo del vector de minimos
    fila=np.argmin(minimos)
    #toma el minimo elemento que concuerde con la columna de minimos
    columna=[np.argmin(i) for i in K][fila]

    #Asigna y elimina los valores de la matriz
    ModeloTransporte.asignar(M,oferta,demanda,fila,columna)
    ModeloTransporte.eliminar(K,oferta,demanda)

    #Si la suma de demanda y oferta es cero, entonces se terminó el algoritmo
    if sum(demanda)+sum(oferta)!=0:
      #Cuando la suma no es igual a cero se velve a llamar al método
      ModeloTransporte.minimoCosto(C,oferta,demanda,M,K)
    
    return M,ModeloTransporte.calcular(C,M)
    