import numpy as np

class ModeloColesterol:
    def __init__(self):
        # Parámetros por defecto
        self.Cn = 200      # Nivel normal de colesterol
        self.C0 = 150      # Nivel inicial
        self.k1 = 0.1      # Tasa de producción natural
        self.E = 400       # Ingesta diaria de colesterol
        self.alpha = 0.7   # Tasa de absorción
        self.k2 = 0.1      # Tasa de uso/metabolismo
        self.dias = 30     # Período de simulación

    def modelo(self, t, C, H=1, X=1, E_extra=0):
        """Ecuación diferencial del modelo de colesterol"""
        dCdt = self.k1*(self.Cn - C) + self.alpha*H*(self.E + E_extra) - self.k2*X*C
        return dCdt

    def runge_kutta_4(self, t0, y0, dt, f, *args):
        """Implementación del método Runge-Kutta de 4to orden"""
        f1 = f(t0, y0, *args)
        f2 = f(t0 + dt/2, y0 + dt/2 * f1, *args)
        f3 = f(t0 + dt/2, y0 + dt/2 * f2, *args)
        f4 = f(t0 + dt, y0 + dt * f3, *args)
        return y0 + dt/6 * (f1 + 2*f2 + 2*f3 + f4)

    def simular(self, H=1, X=1, E_extra=0, ejercicio=False, medicamento=False):
        """Ejecuta la simulación con los parámetros dados"""
        dt = 0.1  # Paso de tiempo más pequeño para mayor precisión
        tiempos = np.arange(0, self.dias + dt, dt)
        C = np.zeros_like(tiempos)
        C[0] = self.C0

        # Ajustar parámetros según opciones
        local_k2 = self.k2 * 1.5 if ejercicio else self.k2
        local_X = 0.7 if medicamento else 1.0

        for i in range(1, len(tiempos)):
            C[i] = self.runge_kutta_4(tiempos[i-1], C[i-1], dt,
                                     self.modelo, H, local_X, E_extra)

        # Muestreo diario para visualización
        dias_visual = np.arange(0, self.dias + 1)
        C_visual = C[::int(1/dt)]

        return dias_visual, C_visual
