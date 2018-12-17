# -*- coding: utf-8 -*-

from base import *

class AipFace(AipBase):
    """
        Aip Face
    """

    __detectUrl = 'https://aip.baidubce.com/rest/2.0/face/v1/detect'

    __matchUrl = 'https://aip.baidubce.com/rest/2.0/faceverify/v1/match'

    def detect(self, image, options=None):
        """
            face attributes detect
        """

        options = options or {}
        data = {}
        data['image'] = base64.b64encode(image)
        data['max_face_num'] = options.get('max_face_num', '1')
        data['face_fields'] = options.get('face_fields', '')

        return self._request(self.__detectUrl, data)

    def __getEncodeImages(self, images):
        """
            encode image array
        """

        result = []
        
        for image in images:
            result.append(base64.b64encode(image))        

        return ','.join(result)

    def match(self, images):
        """
            match
        """

        data = {}
        data['images'] = self.__getEncodeImages(images)

        return self._request(self.__matchUrl, data)
