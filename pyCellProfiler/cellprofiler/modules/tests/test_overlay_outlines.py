'''test_overlay_outlines.py Test the OverlayOutlines module
CellProfiler is distributed under the GNU General Public License.
See the accompanying file LICENSE for details.

Developed by the Broad Institute
Copyright 2003-2010

Please see the AUTHORS file for credits.

Website: http://www.cellprofiler.org
'''
__version__="$Revision$"

import base64
import numpy as np
from StringIO import StringIO
import unittest
import zlib

import cellprofiler.pipeline as cpp
import cellprofiler.cpmodule as cpm
import cellprofiler.cpimage as cpi
import cellprofiler.measurements as cpmeas
import cellprofiler.objects as cpo
import cellprofiler.workspace as cpw

import cellprofiler.modules.overlay_outlines as O

INPUT_IMAGE_NAME = 'inputimage'
OUTPUT_IMAGE_NAME = 'outputimage'
OUTLINE_NAME = 'outlineimage'

class TestOverlayOutlines(unittest.TestCase):
    def make_workspace(self, image, outline):
        '''Make a workspace for testing ApplyThreshold'''
        module = O.OverlayOutlines()
        module.blank_image.value = False
        module.image_name.value = INPUT_IMAGE_NAME
        module.output_image_name.value = OUTPUT_IMAGE_NAME
        module.outlines[0].outline_name.value = OUTLINE_NAME
        pipeline = cpp.Pipeline()
        object_set = cpo.ObjectSet()
        image_set_list = cpi.ImageSetList()
        image_set = image_set_list.get_image_set(0)
        workspace = cpw.Workspace(pipeline,
                                  module,
                                  image_set,
                                  object_set,
                                  cpmeas.Measurements(),
                                  image_set_list)
        image_set.add(OUTLINE_NAME, cpi.Image(outline))
        image_set.add(INPUT_IMAGE_NAME, cpi.Image(image))
        return workspace, module
    
    def test_01_01_load_matlab(self):
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUX'
                'AuSk0sSU1RyM+zUvDNz1PwKs1TMLBQMDS1MjayMjJTMDIwsFQgGTAw'
                'evryMzAwbGNiYKiY8zbCMf+ygUjZpWVaOVrJzJ3O/JZFEsqiMhabMj'
                'mUNi5Luqyiopf3SqxZOrwzeOsfqTo29zqpwtlL+m5KXed9zRexac3z'
                'Pd9/7j1/Xt8viqHhpjCD1MkbPrs4p531SnV+EbPPpedhgkjkAr55Sz'
                '/vn1zH68zzmyXWWWgxxxPd2eXNintn+X9yFy8REL7SmhxomXm34o57'
                '4hNe48NfCvnPC+w8Yi+gsc3nrfCsRxyXFbb6f3x6syb21JLSaM/63d'
                'sfHZxQsUL1r8eM+BfNU+v+st3jY/nbvCV+oWT1xzy22rR+xc/7i+aY'
                'q1r4crafjutwT+e8qvVtWsr5p8ZMze8zZfw6a/cmxLM/X24bnnq3bY'
                've9N0b/QXCHq9Xvbm9qFo/jYW9hrv8aPxxy7q3DFstvqlW68UfmOnb'
                'biZ3+KLS0tACOS+LGLvlZQ4zZd1fHgy4eT6KcTmbnbrLq2MPfQM9Ht'
                'y56yqTxnicJXbV9PORcm9m/V/1U/vwzckFO95s1Nh2X/hWu8rxlbfW'
                'G9X1MPUxWll/cr6n/nxH8IfkyxZxmrdO/nw5x2Ju7JPjzEBn5x0IEE'
                'g0E/9z8hi/akW/qo3e44SG5RUCzpvWtE5sCN9av+ury/H+yzMuPmHt'
                'r+W1f7LH8mZTf2ndiwe9Thb9NR4TGjbn7v0d/l77avGCV+15dSvuJZ'
                'f85Ig75PUtMVrO6Hfn1n9yutcac1/fWpTR4yTlv+r4Sbe5u9x+359w'
                'XqyhLOjxhZRmi/xd6RdTlz2Re1VXv+ZRzK7S2/vMVfasSa1YlqDeH/'
                'qzNP7x5aM/5c/fPVJ8//imqiKOrj2FkTb/kxwFC2cfe1savu7/rtJP'
                'yq3M4TtWrDzyOeTQw03WDoyHD1fqH0n+2Lfo0XVlzv7TL8sz/jnpnl'
                'afyW88ka9/zdp9/max52+Z//9VH5gW7l+6b8veb+e/Fd2NT9hcW7/P'
                'zT67fOl/9tZZsgEA6Ux4DA==')
        #
        # Blank input image
        # Outlines = "NucleiOutlines"
        # max of image
        # output image = OverlayImage
        # Blue color
        #
        pipeline = cpp.Pipeline()
        pipeline.load(StringIO(zlib.decompress(base64.b64decode(data))))
        self.assertEqual(len(pipeline.modules()),3)
        module = pipeline.modules()[2]
        self.assertTrue(isinstance(module, O.OverlayOutlines))
        self.assertTrue(module.blank_image.value)
        self.assertEqual(module.wants_color.value, O.WANTS_COLOR)
        self.assertEqual(len(module.outlines),1)
        self.assertEqual(module.outlines[0].outline_name.value, "NucleiOutlines")
        self.assertEqual(module.outlines[0].color.value, "Blue")
        self.assertEqual(module.max_type.value, O.MAX_IMAGE)

    def test_01_02_load_v1(self):
        data = ('eJztWl1v0zAUdbtubAyNMR5A2osfAW1ROlY09kK7DUbR+iFWDfEEXu'
                'p2Rq5dJc5o+WU88sjP4ScQt0mbmrTpWtamkEhRdx0fn+vjazu5cyFX'
                'OcsdwYymw0KuslsjFMMyRaLGzcYhZGIHHpsYCVyFnB3CAmfwnc2gfg'
                'DTLw71/cP0HtzT9ZdgsiuRL2w4Pz+fArDi/K46d9J9tOzaCd8t7XMs'
                'BGF1axmkwGO3/IdzXyCToEuKLxC1sdWn8MrzrMYr7WbvUYFXbYqLqO'
                'Gv7FxFu3GJTatU84Du4zJpYXpOvmGlC1619/iaWIQzF++2r5b2eLlQ'
                'eKUO8GFfh4Siw5Jzb/vKZf23oF8/FaDbA1/9TdcmrEquSdVGFJIGqv'
                'e8kO0dhLS3qrQn7ZJJ6keO5BKvh+CTA/gkKPIubzYEt6nwyruCW2L3'
                'dQsZAjaQMK7G8X9FaUfaRdugmMym/4kBfAI8H1P3ZYVX2ml9Z18H4+'
                'l3T8FLu3SNTYraeRkDYMx27irtSPuEQ8YFtC13Yoyjw9JAO0vgoxOF'
                'k+pwzCk3x+QdFn+3FbdBuhdQC/Jad+55eoXN40dKO9I+wTVkUwE7Aw'
                'hPiIkNwc32VPqH9WdD8UPa3flTsgUlTC4mk8wDDYyn57rCL+2SsGx4'
                'SvklosDTc5I4OjUxZuB240jtdzqAb0XBeZeHW3N/b9NPNT70nfSt+p'
                'ka4EuBk1w5PwlO1/T0NH5Ou/5nQ/BrCl7aeSYws4hoD9FrFjovmt9F'
                'ziZ630jr0fRTXRcyAXxR8HPYvvE3/LwJLhvi5yT71Cz8XhR9Yz/n66'
                'ezj0VyXo37/hV1fRclDqLqp7qvapn5jHs2xM+geK185dCgyLLczMc8'
                '/A773gvK23zApH4l03DXMuHEDOxrL2q6B+UJ3nAT101us+r0/M2tm+'
                'XJZtnPzoe97Ghzev5Zxhe//IIN0XEcElbFzX9AhzC/g/KKfb+7Msx7'
                '/Y1x0+OyYHQcBOXpePdLoRfBi9TfGPd/4rJgdJzH612Mi3HReQ/bAo'
                'PzUdr+fcf/IrZI/Y5xMS4K+11Uv0tiXIyLcYuHayX6ODXvpOZvZf3P'
                'Pp6g9ekZGFyfpG1gSpsml+fwTK3ROSxmaZSjave0lnbm/Jn3Hdzq5M'
                'NCeLIKT3YYD6liJkit3TQdNlvwBhLE0PJuadkpzXmlkvcqhDej8GaG'
                '8fLuYaRP7suPpbmnk/r/rvtj3NYC+Pz6Jx3r/vadkeOtjnN//H+9mo'
                'QvuZTo8PnPEayH4FI+n4Dbz+/gZnH2ZER9r4+zqv8b5il/ZA==')
        pipeline = cpp.Pipeline()
        pipeline.load(StringIO(zlib.decompress(base64.b64decode(data))))
        self.assertEqual(len(pipeline.modules()),3)
        module = pipeline.modules()[2]
        self.assertTrue(isinstance(module, O.OverlayOutlines))
        self.assertFalse(module.blank_image.value)
        self.assertEqual(module.image_name.value, "OrigBlue")
        self.assertEqual(module.wants_color.value, O.WANTS_COLOR)
        self.assertEqual(len(module.outlines),1)
        self.assertEqual(module.outlines[0].outline_name.value, "NucleiOutlines")
        self.assertEqual(module.outlines[0].color.value, "Green")
        self.assertEqual(module.max_type.value, O.MAX_IMAGE)

    def test_02_01_gray_to_color_outlines(self):
        np.random.seed(0)
        image = np.random.uniform(size=(50,50))
        outline = np.zeros((50,50),bool)
        outline[20:31,20:31] = 1
        outline[21:30,21:30] = 0
        expected = np.dstack((image,image,image))
        expected[:,:,0][outline.astype(bool)] = 1
        expected[:,:,1][outline.astype(bool)] = 0
        expected[:,:,2][outline.astype(bool)] = 0
        workspace, module = self.make_workspace(image, outline)
        module.wants_color.value = O.WANTS_COLOR
        module.outlines[0].color.value = "Red"
        module.run(workspace)
        output_image = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(np.all(output_image.pixel_data == expected))

    def test_02_02_color_to_color_outlines(self):
        np.random.seed(0)
        image = np.random.uniform(size=(50,50,3))
        outline = np.zeros((50,50),bool)
        outline[20:31,20:31] = 1
        outline[21:30,21:30] = 0
        expected = image.copy()
        expected[:,:,0][outline.astype(bool)] = 1
        expected[:,:,1][outline.astype(bool)] = 0
        expected[:,:,2][outline.astype(bool)] = 0
        workspace, module = self.make_workspace(image, outline)
        module.wants_color.value = O.WANTS_COLOR
        module.outlines[0].color.value = "Red"
        module.run(workspace)
        output_image = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(np.all(output_image.pixel_data == expected))
    
    def test_02_03_blank_to_color_outlines(self):
        np.random.seed(0)
        image = np.random.uniform(size=(50,50,3))
        outline = np.zeros((50,50),bool)
        outline[20:31,20:31] = 1
        outline[21:30,21:30] = 0
        expected = np.zeros((50,50,3))
        expected[:,:,0][outline.astype(bool)] = 1
        expected[:,:,1][outline.astype(bool)] = 0
        expected[:,:,2][outline.astype(bool)] = 0
        workspace, module = self.make_workspace(image, outline)
        module.blank_image.value = True
        module.wants_color.value = O.WANTS_COLOR
        module.outlines[0].color.value = "Red"
        module.run(workspace)
        output_image = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(np.all(output_image.pixel_data == expected))
    
    def test_03_01_blank_to_gray(self):
        np.random.seed(0)
        image = np.random.uniform(size=(50,50))
        outline = np.zeros((50,50),bool)
        outline[20:31,20:31] = 1
        outline[21:30,21:30] = 0
        expected = np.zeros_like(image)
        expected[outline.astype(bool)] = 1
        workspace, module = self.make_workspace(image, outline)
        module.blank_image.value = True
        module.wants_color.value = O.WANTS_GRAYSCALE
        module.run(workspace)
        output_image = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(np.all(output_image.pixel_data == expected))
    
    def test_03_02_gray_max_image(self):
        np.random.seed(0)
        image = np.random.uniform(size=(50,50)) * .5
        outline = np.zeros((50,50),bool)
        outline[20:31,20:31] = 1
        outline[21:30,21:30] = 0
        expected = image.copy()
        expected[outline.astype(bool)] = np.max(image)
        workspace, module = self.make_workspace(image, outline)
        module.blank_image.value = False
        module.wants_color.value = O.WANTS_GRAYSCALE
        module.max_type.value = O.MAX_IMAGE
        module.run(workspace)
        output_image = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(np.all(output_image.pixel_data == expected))

    def test_03_02_gray_max_possible(self):
        np.random.seed(0)
        image = np.random.uniform(size=(50,50)) * .5
        outline = np.zeros((50,50),bool)
        outline[20:31,20:31] = 1
        outline[21:30,21:30] = 0
        expected = image.copy()
        expected[outline.astype(bool)] = 1
        workspace, module = self.make_workspace(image, outline)
        module.blank_image.value = False
        module.wants_color.value = O.WANTS_GRAYSCALE
        module.max_type.value = O.MAX_POSSIBLE
        module.run(workspace)
        output_image = workspace.image_set.get_image(OUTPUT_IMAGE_NAME)
        self.assertTrue(np.all(output_image.pixel_data == expected))
