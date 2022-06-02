from collections import OrderedDict
from flask import render_template
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from functools import reduce
import numpy as np
np.set_printoptions(suppress=True, precision=3) # to avoid 1e-17 expressions in rotation matrix
def DH(conf):
    '''
    Calculates the Denavit-Hartenberg Matrix
    where
    d: offset along previous z to the common normal
    θ: angle about previous z, from old x to new x
    r: length of the common normal (aka a, but if using this notation, do not confuse with α). Assuming a revolute joint, this is the radius about previous z.
    α: angle about common normal, from old z axis to new z axis
    '''
    if len(conf) != 4:
        raise Exception('Need exactly 4 Denavit-Hartenberg parameters, you provided %i.' % len(conf))
        
    #    Z  |   X    
    Theta, d, r, alpha = conf
    
    T = np.eye(4, dtype=np.float32)

    cTheta = np.cos(Theta/180.0*np.pi)
    sTheta = np.sin(Theta/180.0*np.pi)
    calpha = np.cos(alpha/180.0*np.pi)
    salpha = np.sin(alpha/180.0*np.pi)
    
    T[np.ix_([0],[0])] = cTheta
    T[np.ix_([0],[1])] = -sTheta * calpha
    T[np.ix_([0],[2])] = sTheta * salpha
    T[np.ix_([0],[3])] = r * cTheta
    
    T[np.ix_([1],[0])] = sTheta
    T[np.ix_([1],[1])] = cTheta * calpha
    T[np.ix_([1],[2])] = -cTheta * salpha
    T[np.ix_([1],[3])] = r * sTheta

    T[np.ix_([2],[1])] = salpha
    T[np.ix_([2],[2])] = calpha
    T[np.ix_([2],[3])] = d

    return T
if __name__ == "__main__":
    T = DH([0.0, 0.0, 3.0, 0.0])
    TCP = [0.0, 0.0, 0.0, 1.0] # starting from middle of rear axis of the vehicle

    verschub_X = 4.297   # m Abstand Hinterachse zu Verschubrahmen
    verschub_Z = 0.546   # m Höhe des Verschubrahmens über Boden
    roll = 0.0        # Grad Rollwinkel

    verschub_Y = 0.0  # m [-0.612, 0.612]
    dreharm_Z = 0.833    # m Länge Verschubrahmen zu Drehpunkt Hauptarm

    hauptarm_R = 0.0  # Grad
    hauptarm_L = 1.443  # m Länge Hauptarm

    nebenarm_R = 0.0     # Grad
    nebenarm_L = 0.954   # m

    schnellwech_R = 90.0  # Grad
    schnellwech_L = 0.145# m
    #                                          Z    |     X
    #                                        Th,   d,    r,    al
    konfiguration = dict([
                    ('Fahrzeug', [0.0, 0.0, 0.0, roll]),
                    ('Verschubrahmen', [0.0, verschub_Z, verschub_X, 0.0]), # Verschubrahmen von Mitte Hinterachse
                    ('Verschubschlitten', [0.0, 0.0, 0.0, 90.0]),
                    ('Dreharm', [90.0, -verschub_Y-0.08, dreharm_Z, 90.0]), # jetzt z nach vorn, x nach oben
                    ('Hauptarm', [hauptarm_R+180.0-53.0, 0.0, hauptarm_L, 0.0]),
                    ('Nebenarm', [nebenarm_R, 0.0, nebenarm_L, 0.0]),
                    ('Schnellwechselsystem', [schnellwech_R, 0.0, schnellwech_L, 0.0])
                    ])
    T = dict()
    for name, conf in konfiguration.items():
        #print('Integriere %s...' % name)
        T[name] = DH(conf)
    M = reduce(np.dot, T.values()) # Matrix mutliplication
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    oldp = TCP
    for i in range(len(T)):
        M = reduce(np.dot, list(T.values())[:i+1]) # Matrix mutliplication

        p = np.dot(M,TCP)
        
        x = float(p[0])
        y = float(p[1])
        z = float(p[2])
        
        ax.plot([oldp[0], x], [oldp[1], y], [oldp[2], z], c='k', alpha=.5)
        ax.scatter(x, y, z, s=50)
        
        oldp = p
        
    #plt.legend(bbox_to_anchor=(0, 0))
    plt.xlabel('X')
    plt.ylabel('Y')
    #plt.axis('equal')
    #ax.view_init(0, -135)
    ax.plot(x, y, z, label='Manipulator')
    plt.savefig('3D-Konfiguration.png', dpi=300)
    ax.view_init(0, 0)
    ax.plot(x, y, z, label='Manipulator')
    plt.savefig('3D-Konfiguration1.png', dpi=300)
    ax.view_init(0, -135)
    ax.plot(x, y, z, label='Manipulator')
    plt.savefig('3D-Konfiguration2.png', dpi=300)
    ax.view_init(0, 90)
    ax.plot(x, y, z, label='Manipulator')
    plt.savefig('3D-Konfiguration3.png', dpi=300)

    import flask

    app = flask.Flask(__name__)

    @app.route('/', methods=['GET'])

    @app.route('/index')
    def index():
    #   return flask.render_template('index.html')
        #flask.send_from_directory(app.root_path, '3D-Konfiguration.png', mimetype='image/png')
        return flask.send_from_directory(app.root_path, '3D-Konfiguration.png', mimetype='image/png')
    @app.route('/zero')
    def zero():
    #   return flask.render_template('index.html')
        #flask.send_from_directory(app.root_path, '3D-Konfiguration.png', mimetype='image/png')
        return flask.send_from_directory(app.root_path, '3D-Konfiguration1.png', mimetype='image/png')
    @app.route('/minus')
    def minus():
    #   return flask.render_template('index.html')
        #flask.send_from_directory(app.root_path, '3D-Konfiguration.png', mimetype='image/png')
        return flask.send_from_directory(app.root_path, '3D-Konfiguration2.png', mimetype='image/png')
    @app.route('/direct')
    def direct():
    #   return flask.render_template('index.html')
        #flask.send_from_directory(app.root_path, '3D-Konfiguration.png', mimetype='image/png')
        return flask.send_from_directory(app.root_path, '3D-Konfiguration3.png', mimetype='image/png')
    
    app.run(host='0.0.0.0', port=8000, debug=True)
