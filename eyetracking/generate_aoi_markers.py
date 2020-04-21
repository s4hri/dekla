import numpy as np
from tobiiglasses.aoi.aruco.model import AOI_Aruco_Model

cameraMatrix = np.array([[1.13683020e+03, 0.00000000e+00, 9.48918123e+02],
                            [0.00000000e+00, 1.13349542e+03, 5.32682856e+02],
                            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]] )
distCoeffs = np.array( [0.06136298, -0.19235713,  0.00088979,  0.00089367,  0.12656455] )

ar_model = AOI_Aruco_Model(cameraMatrix, distCoeffs)
ar_model.createArucoAOI('stage', markerLength=0.05, markerSeparation=0.15)
ar_model.createArucoAOI('score')
ar_model.createArucoAOI('timer')
ar_model.exportArucoAOIs()
