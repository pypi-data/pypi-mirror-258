import numpy as np
import matplotlib.pyplot as plt


def controle_IM(q0, Q0, qd0, QD0, q1, Q1, qd1, QD1, q2, Q2, qd2, QD2, Kp0, Kp1, Kp2, Kv0, Kv1, Kv2):
    t0 = Kp0 * (q0 - Q0) + Kv0 * (qd0 - QD0)
    t1 = Kp1 * (q1 - Q1) + Kv1 * (qd1 - QD1)
    t2 = Kp2 * (q2 - Q2) + Kv2 * (qd2 - QD2)
    return t0, t1, t2

def CorpoRigido(q, qd, qdd):

  #comprimento dos links
    l1 = 0.15
    l2 = 0.255
    l3 = 0.199

  #massa dos links
    m1 = 0.200
    m2 = 0.07576
    m3 = 0.07192

    g = 9.8  #gravidade, obviamente

    #ângulos = q
    theta1, theta2, theta3 = q
    v1, v2, v3 = qd #velocidades = q dot
    a1, a2, a3 = qdd #acelerações = q double dot

    #Cálculo da inércia
    m11 = (1/2)*(m1*l1**2) + (1/3)*(m2*l2**2*np.cos(theta2)**2) + (1/3)*(m3*l3**2*np.cos(theta2+theta3)**2) + (m3*l2**2*np.cos(theta2)**2) + (m3*l2*l3*np.cos(theta2+theta3)*np.cos(theta2))
    m12 = 0
    m13 = 0
    m21 = 0
    m22 = (1/3)*(m2*l2**2) + (1/3)*(m3*l3**2) + (m3*l2**2) + (m3*l2*l3*np.cos(theta3))
    m23 = (1/3)*(m3*l3**2) + (m3*l2**2) + (1/3)*(m3*l2*l3*np.cos(theta3))
    m31 = 0
    m32 = (1/3)*(m3*l3**2) + (m3*l2**2) + (1/3)*(m3*l2*l3*np.cos(theta3))
    m33 = (1/3)*(m3*l3**2)

    #Matriz M
    M11 = m11*a1 + m12*a2 + m13*a3
    M21 = m21*a1 + m22*a2 + m23*a3
    M31 = m31*a1 + m32*a2 + m33*a3

    #Matriz G
    G11 = 0
    G21 = (1/2)*(m2*g*l2*np.cos(theta2)) + (1/2)*(m3*g*l3*np.cos(theta2+theta3)) + (m3*g*l2*np.cos(theta2))
    G31 = (1/2)*(m3*g*l3*np.cos(theta2+theta3))

    #Matriz da força inercial de Coriolis --> relação angular
    C11 = ((-4/3)*(m2*l2**2*np.sin(2*theta2)) - (1/3)*(m3*l3**2*np.sin(2*theta2 + 2*theta3)) - (m3*l2*l3*np.sin(2*theta2+theta3)))*v2*v1 + ((-1/3)*(m3*l3**2*np.sin(2*theta2+2*theta3)) - (m3*l2*l3*np.cos(theta2)*np.sin(theta2+theta3)))*v3*v1
    C21 = (-m3*l2*l3*np.sin(theta3))*v2*v3 + ((-1/2)*(m3*l2*l3*np.sin(theta3)))*v3**2 + ((1/6)*(m2*l2**2*np.sin(2*theta2)) + (1/6)*(m3*l3**2*np.sin(2*theta2+2*theta3)) + (1/2)*(m3*l2**2*np.sin(2*theta2)) + (1/2)*(m3*l2*l3*np.sin(2*theta2 + theta3)))*v1**2
    C31 = ((1/2)*(m3*l2*l3*np.sin(theta3)))*v2**2 + ((1/6)*(m3*l3**2*np.sin(2*theta2+2*theta3)) + (1/2)*(m3*l2*l3*np.cos(theta2)*np.sin(theta2+theta3)))*v1**2

    #Torques
    tau11 = M11 + C11 + G11
    tau12 = M21 + C21 + G21
    tau31 = M31 + C31 + G31

    return [tau11, tau12, tau31]

def KF_1D_Link1(KalmanState, KalmanUncertainty, RateMeasurement, AngleMeasurement, Ts, q, r):
    if KalmanState is None:
        KalmanState = 0
        KalmanUncertainty = 4

    KalmanState += Ts * RateMeasurement
    KalmanUncertainty += (Ts**2) * (q**2)
    KalmanGain = KalmanUncertainty * 1 / (1 * KalmanUncertainty + r**2)
    KalmanState += KalmanGain * (AngleMeasurement - KalmanState)
    KalmanUncertainty = (1 - KalmanGain) * KalmanUncertainty

    return KalmanState, KalmanUncertainty

def traj(p0, pf0, pf1, pf2):
    t = np.arange(0, 10, 0.01)
    T = t[-1]

    S0 = np.array([[pf0], [0], [0]])
    S1 = np.array([[pf1], [0], [0]])
    S2 = np.array([[pf2], [0], [0]])

    M = np.array([[T**5, T**4, T**3],
                  [5*T**4, 4*T**3, 3*T**2],
                  [20*T**3, 12*T**2, 6*T]])

    X0 = np.linalg.solve(M, S0).ravel()
    X1 = np.linalg.solve(M, S1).ravel()
    X2 = np.linalg.solve(M, S2).ravel()

    A0, B0, C0 = X0
    A1, B1, C1 = X1
    A2, B2, C2 = X2

    t0 = np.ones_like(t)
    t2 = t * t
    t3 = t2 * t
    t4 = t3 * t
    t5 = t4 * t

    tempo = np.vstack([t5, t4, t3, t2, t, t0])

    F = p0
    E = 0
    D = 0

    q0 = np.vstack([t, np.dot([A0, B0, C0, D, E, F], tempo)])
    q1 = np.vstack([t, np.dot([A1, B1, C1, D, E, F], tempo)])
    q2 = np.vstack([t, np.dot([A2, B2, C2, D, E, F], tempo)])
    qd0 = np.vstack([t, np.dot([5*A0, 4*B0, 3*C0, 2*D, E], tempo[1:])])
    qd1 = np.vstack([t, np.dot([5*A1, 4*B1, 3*C1, 2*D, E], tempo[1:])])
    qd2 = np.vstack([t, np.dot([5*A2, 4*B2, 3*C2, 2*D, E], tempo[1:])])
    qdd0 = np.vstack([t, np.dot([20*A0, 12*B0, 6*C0, 2*D], tempo[2:])])
    qdd1 = np.vstack([t, np.dot([20*A1, 12*B1, 6*C1, 2*D], tempo[2:])])
    qdd2 = np.vstack([t, np.dot([20*A2, 12*B2, 6*C2, 2*D], tempo[2:])])

    return q0, q1, q2, qd0, qd1, qd2, qdd0, qdd1, qdd2

#Definindo os ganhos dos integradores no modelo do FK
G1 = 1
G2 = 0.9

#Parâmetros do controlador
Kp0 = 30/3
Kp1 = 30/3
Kp2 = 30/3

Kv0 = 25/10
Kv1 = 25/10
Kv2 = 25/10

# Dados da simulação
# Definição de dados de exemplo
t = np.linspace(0, 10, 100)
P0 = np.sin(t)
p0 = np.cos(t)
P1 = np.sin(2*t)
p1 = np.cos(2*t)
P2 = np.sin(3*t)
p2 = np.cos(3*t)


#Visualização dos resultados
lineStyles = ['-', '--', '-.', ':']

plt.figure()
for i in range(4):
    plt.plot(t, P0, color='b', linestyle=lineStyles[i], linewidth=2)
    plt.plot(t, P1, color='k', linestyle=lineStyles[i], linewidth=2)
    plt.plot(t, P2, color='r', linestyle=lineStyles[i], linewidth=2)
for i in range(4):
    plt.plot(t, p0, color='b', linestyle=lineStyles[i], linewidth=3)
    plt.plot(t, p1, color='k', linestyle=lineStyles[i], linewidth=3)
    plt.plot(t, p2, color='r', linestyle=lineStyles[i], linewidth=3)

plt.grid(True)
plt.title('Joint Position')
plt.xlabel('Time (s)')
plt.ylabel('degree')
plt.legend(['rho*', 'theta_1*', 'theta_2*', 'rho', 'theta_1', 'theta_2'])

#Definindo a fonte para os eixos x e y
plt.xlabel('Time (s)', fontsize=12, fontname='Arial')
plt.ylabel('degree', fontsize=12, fontname='Arial')

plt.gca().set_facecolor('w')  #Define a cor de fundo para branco
plt.show()